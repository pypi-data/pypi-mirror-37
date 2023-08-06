# python built-in library
import os
import argparse
import time
import csv
import uuid
# 3rd party library
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from skimage.morphology import label
from PIL import Image
from torch.multiprocessing import Pool, get_context
from functools import partial
from itertools import islice
from tqdm import tqdm
# own code
from .config import config
from .dataset import NucleiDataset, Compose
from .helper import load_ckpt, prob_to_segment, segment_to_instances, segment_to_rles, iou_metric, clahe


def main(ckpt, action=['csv'], save=False, target='test'):
    infr_batchsize = config['valid'].getint('inference_batchsize')
    save_png_preds = False
    if (len(action) == 2) and ('rle_mask' in action) and ('png_preds' in action):
        action = 'rle_mask'
        save_png_preds = True
    elif (len(action) == 1):
        action = action[0]
    else:
        raise ValueError(f'Multiple actions: {action} not supported!')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # load one or more checkpoint
    models = []
    for fn in ckpt or [None]:
        # load model
        model, _ = load_ckpt(filepath=fn)
        if not model:
            print("Aborted: checkpoint {} not found!".format(fn))
            return
        # Sets the model in evaluation mode.
        model.eval()
        # put model to GPU
        # Note: Comment out DataParallel due to
        #       (1) we won't need it in our inference scenario
        #       (2) it will change model's class name to 'dataparallel'
        # if torch.cuda.device_count() > 1:
        #     print("Let's use", torch.cuda.device_count(), "GPUs!")
        #     model = nn.DataParallel(model)
        model = model.to(device)
        # append to model list
        models.append(model)

    resize = not config['valid'].getboolean('pred_orig_size')
    compose = Compose(augment=False, resize=resize)
    # decide which dataset to pick sample
    data_dir = os.path.join('data', target)
    dataset = NucleiDataset(data_dir, policy='Once', transform=compose)
    if target == 'train':
        _, dataset = dataset.split()

    action_dict = {
        'csv': { 'filename': 'result.csv', 'header': ['ImageId', 'EncodedPixels'] },
        'iou': { 'filename': 'iou.csv', 'header': ['ImageId', 'IoU'] },
        'rle_mask': { 'filename': None, 'header': None},
        'png_mask': { 'filename': None, 'header': None },
        'png_preds': { 'filename': None, 'header': None },
    }

    # iterate dataset and inference each sample
    writer = csvfile = None
    batchjob_info = action_dict.get(action, None)
    if batchjob_info is not None: # Non-GUI, parallelized processing
        # inference dataset in batch via GPU, then post-process them in parallel via CPU
        if batchjob_info['filename'] and (writer is None):
            dir = predict_save_folder()
            fp = os.path.join(dir, batchjob_info['filename'])
            csvfile = open(fp, 'w')
            writer = csv.writer(csvfile)
            writer.writerow(batchjob_info['header'])

        ious = []
        for batch_data in split_every(infr_batchsize, dataset):
            preds = []
            for data in tqdm(batch_data, desc='Inference'):
                with torch.no_grad():
                    uid, y, y_c, y_m = inference(data, models, resize)
                    y, y_c, y_m = prob_to_segment(y, y_c, y_m)
                    x, gt, gt_s, gt_c, gt_m = unpack_data(data, compose, resize)
                    preds.append([uid, y, y_c, y_m, gt])

            desc = 'Post-processing'
            if action == 'csv': # one output file for all inferences
                for result in parallel_processing_with_progress(collect_csv_job, preds, desc):
                    for r in result:
                        writer.writerow(r)
            elif action == 'iou': # one output file for all inferences
                for result in parallel_processing_with_progress(collect_iou_job, preds, desc):
                    writer.writerow(result)
                    ious.append(result[1])
            elif action == 'rle_mask': # one output file per inference
                for _ in parallel_processing_with_progress(partial(save_rle_mask_job, save_png=save_png_preds), preds, desc): pass
            elif action == 'png_mask': # one output file per inference
                for _ in parallel_processing_with_progress(save_png_mask_job, preds, desc): pass
            elif action == 'png_preds': # 3 output file per inference
                for _ in parallel_processing_with_progress(save_png_preds_job, preds, desc): pass

        if action == 'iou':
            print('\nIoU Metrics:\n mean: {0:.4f}\t std: {1:.4f}\t max: {2:.4f}\t min: {3:.4f}\t count: {4}\n'
                .format(np.mean(ious), np.std(ious), np.max(ious), np.min(ious), len(ious)))
        if csvfile is not None:
            csvfile.close()
    else: # GUI, sequential inspection
        for data in tqdm(dataset):
            with torch.no_grad():
                uid, y, y_c, y_m = inference(data, models, resize)
                x, gt, gt_s, gt_c, gt_m = unpack_data(data, compose, resize)
            if target == 'test':
                show(uid, x, y, y_c, y_m, save)
            else: # train or valid
                show_groundtruth(uid, x, y, y_c, y_m, gt, gt_s, gt_c, gt_m, save)
# end of main()

def split_every(size, iterable):
    with tqdm(total=len(iterable), desc='Dataset') as pbar:
        src_iter = iter(iterable)
        items = list(islice(src_iter, size))
        while items:
            yield items
            pbar.update(len(items))
            items = list(islice(src_iter, size))

def parallel_processing_with_progress(func, data, desc):
    n_process = config['post'].getint('n_worker')
    with get_context("spawn").Pool(n_process) as p:
        with tqdm(total=len(data), desc=desc) as pbar:
            for result in p.imap(func, data):
                yield result
                pbar.update()

def collect_csv_job(pred):
    uid, y, y_c, y_m, _ = pred
    instances = []
    for rle in segment_to_rles(y, y_c, y_m):
        instances.append([uid, ' '.join([str(i) for i in rle])])
    return instances

def collect_iou_job(pred):
    uid, y, y_c, y_m, gt = pred
    return [uid, get_iou(y, y_c, y_m, gt)]

def save_rle_mask_job(pred, save_png):
    uid, y, y_c, y_m, _ = pred
    dir = os.path.join(predict_save_folder(), uid)
    if not os.path.exists(dir):
        os.makedirs(dir)
    rle_csv = os.path.join(dir, 'mask.csv')
    with open(rle_csv, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['ImageId', 'EncodedPixels'])
        for idx, rle in enumerate(segment_to_rles(y, y_c, y_m)):
            writer.writerow([f'mask_{idx+1}', ' '.join([str(i) for i in rle])])
    if save_png:
        save_png_preds_job(pred)

def save_png_mask_job(pred):
    uid, y, y_c, y_m, _ = pred
    instances, _ = segment_to_instances(y, y_c, y_m)
    idxs = np.unique(instances) # sorted, 1st is background (e.g. 0)
    dir = os.path.join(predict_save_folder(), uid, 'masks')
    if not os.path.exists(dir):
        os.makedirs(dir)
    for idx in idxs[1:]:
        mask = (y == idx).astype(np.uint8)
        mask *= 255
        img = Image.fromarray(mask, mode='L')
        img.save(os.path.join(dir, f'mask_{idx}.png'), 'PNG')

def save_png_preds_job(pred):
    uid, y, y_c, y_m, _ = pred
    dir = os.path.join(predict_save_folder(), uid, 'infr')
    if not os.path.exists(dir):
        os.makedirs(dir)
    img = Image.fromarray(y.astype(np.uint8)*255, mode='L')
    img.save(os.path.join(dir, f'segment.png'), 'PNG')
    img = Image.fromarray(y_c.astype(np.uint8)*255, mode='L')
    img.save(os.path.join(dir, f'contour.png'), 'PNG')
    img = Image.fromarray(y_m.astype(np.uint8)*255, mode='L')
    img.save(os.path.join(dir, f'marker.png'), 'PNG')

def unpack_data(data, compose, resize):
    x = data['image']
    size = data['size']
    gt_s = data['label']
    gt_c = data['label_c']
    gt_m = data['label_m']
    gt = data['label_gt']
    # convert input to numpy array
    x = compose.denorm(x)
    s = size if resize else None
    x = compose.to_numpy(x, s)
    gt = compose.to_numpy(gt, s)
    gt_s = compose.to_numpy(gt_s, s)
    gt_c = compose.to_numpy(gt_c, s)
    gt_m = compose.to_numpy(gt_m, s)
    return x, gt, gt_s, gt_c, gt_m

def inference(data, models, resize):
    threshold = config['param'].getfloat('threshold')
    threshold_edge = config['param'].getfloat('threshold_edge')
    threshold_mark = config['param'].getfloat('threshold_mark')
    tta = config['valid'].getboolean('test_time_augment')
    ensemble_policy = config['valid']['ensemble']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # sub-rountine to convert output tensor to numpy
    def convert(t):
        assert isinstance(t, (torch.FloatTensor, torch.cuda.FloatTensor))
        if len(t) == 0:
            return None
        # pixel wise ensemble output of models
        t = torch.mean(t, 0, True)
        # to numpy array
        t = t.to('cpu').numpy()[0]
        if ensemble_policy == 'vote':
            t = np.where(t >= 0.5, 1., 0.) # majority vote
        # channel first [C, H, W] -> channel last [H, W, C]
        t = np.transpose(t, (1, 2, 0))
        # Remove single-dimensional channel from the shape of an array
        t = np.squeeze(t)
        t = align_size(t, size, resize)
        return t

    # get input data
    uid = data['uid']
    size = data['size']
    inputs = data['image']
    # prepare input variables
    inputs = inputs.unsqueeze(0)
    inputs = inputs.to(device)

    if tta:
        txf_funcs = [lambda x: x,
                     lambda x: flip(x, 2), # up down flip
                     lambda x: flip(x, 3), # left right flip
                     lambda x: flip(flip(x, 3), 2),
                    ]
    else:
        txf_funcs = [lambda x: x]

    y_s = y_c = y_m = torch.FloatTensor().to(device)
    for model in models:
        model_name = type(model).__name__.lower()
        with_contour = config.getboolean(model_name, 'branch_contour')
        with_marker = config.getboolean(model_name, 'branch_marker')
        # predict model output
        for txf in txf_funcs:
            # apply test time transform
            x = inputs
            x = txf(x)
            # padding
            if not resize:
                x = pad_tensor(x, size)
            # inference model
            s = model(x)
            # handle multi-head
            c = m = torch.FloatTensor().to(device)
            if with_contour and with_marker:
                s, c, m = s
            elif with_contour:
                s, c = s
            # crop padding
            if not resize:
                w, h = size
                s = s[:, :, :h, :w]
                c = c[:, :, :h, :w] if len(c) > 0 else c
                m = m[:, :, :h, :w] if len(m) > 0 else m
            # reverse flip
            s = txf(s)
            c = txf(c)
            m = txf(m)
            # concat outputs
            if ensemble_policy == 'avg':
                y_s = torch.cat([y_s, s], 0)
                if len(c) > 0:
                    y_c = torch.cat([y_c, c], 0)
                if len(m) > 0:
                    y_m = torch.cat([y_m, m], 0)
            elif ensemble_policy == 'vote':
                y_s = torch.cat([y_s, (s > threshold).float()], 0)
                if len(c) > 0:
                    y_c = torch.cat([y_c, (c > threshold_edge).float()], 0)
                if len(m) > 0:
                    y_m = torch.cat([y_m, (m > threshold_mark).float()], 0)
            else:
                raise NotImplementedError("Ensemble policy not implemented")
    return uid, convert(y_s), convert(y_c), convert(y_m)
# end of predict()

def flip(t, dim):
    dim = t.dim() + dim if dim < 0 else dim
    inds = tuple(slice(None, None) if i != dim
            else t.new(torch.arange(t.size(i)-1, -1, -1).tolist()).long()
            for i in range(t.dim()))
    return t[inds]

def tensor_rgb2gray(rgb):
    c, h, w = rgb.shape[1:]
    if c != 3:
        return rgb
    # refer https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gray_mat = torch.tensor([0.299, 0.587, 0.114]).to(device)
    # matmul() could not handle (1x3) x (1x3x5x5) directly
    # convert to (1x3) x (1x3x25) then reshape (1x1x25) to (1x1x5x5)
    g = torch.matmul(gray_mat, rgb.view(1, 3, -1))
    g = g.view(1, 1, h, w)
    # expand(): repeat channel dimension without memory copy
    # reshape (1x1x5x5) to (1x3x5x5)
    g = g.expand(1, 3, -1, -1)
    return g

def pad_tensor(img_tensor, size, mode='reflect'):
    # get proper mini-width required for model input
    # for example, 32 for 5 layers of max_pool
    gcd = config['param'].getint('gcd_depth')
    # estimate border padding margin
    # (paddingLeft, paddingRight, paddingTop, paddingBottom)
    pad_w = pad_h = 0
    w, h = size
    if 0 != (w % gcd):
        pad_w = gcd - (w % gcd)
    if 0 != (h % gcd):
        pad_h = gcd - (h % gcd)
    pad = (0, pad_w, 0, pad_h)
    # decide padding mode
    if mode == 'replica':
        f = nn.ReplicationPad2d(pad)
    elif mode == 'constant':
        # padding color should honor each image background, default is black (0)
        bgcolor = 0 if np.median(img_tensor) < 100 else 255
        f = nn.ConstantPad2d(pad, bgcolor)
    elif mode == 'reflect':
        f = nn.ReflectionPad2d(pad)
    else:
        raise NotImplementedError()
    return f(img_tensor)

def align_size(img_array, size, regrowth=True):
    from skimage.transform import resize
    if img_array is None:
        return img_array
    elif regrowth:
        return resize(img_array, size[::-1], mode='constant', preserve_range=True)
    else:
        w, h = size
        # crop padding
        return img_array[:h, :w]

def _make_overlay(img_array):
    img_array = img_array.astype(float)
    img_array[img_array == 0] = np.nan # workaround: matplotlib cmap mistreat vmin(1) as background(0) sometimes
    cmap = plt.get_cmap('prism') # prism for high frequence color bands
    cmap.set_bad('w', alpha=0) # map background(0) as transparent/white
    return img_array, cmap

def _save_fullsize_overlay(x_arr, y_arr, y_cmap, filepath):
    plt.imsave(fname=filepath, arr=y_arr, cmap=y_cmap)
    y = Image.open(filepath) # workaroud, save then open it
    overlay = Image.blend(Image.fromarray(x_arr).convert('RGB'),
                          y.convert('RGB'), alpha=0.3)
    overlay.save(filepath)

def show_figure():
    backend = matplotlib.get_backend()
    _x = config['valid'].getint('figure_pos_x')
    _y = config['valid'].getint('figure_pos_y')
    mgr = plt.get_current_fig_manager()
    if backend == 'TkAgg':
        mgr.window.wm_geometry("+%d+%d" % (_x, _y))
    elif backend == 'WXAgg':
        mgr.window.SetPosition((_x, _y))
    elif backend == 'Qt5Agg':
        mgr.window.move(_x, _y)
    else:
        # jupyter notebook etc.
        pass
    plt.show()

def show(uid, x, y, y_c, y_m, save=False):
    threshold = config['param'].getfloat('threshold')
    threshold_edge = config['param'].getfloat('threshold_edge')
    view_color_equalize = config['valid'].getboolean('view_color_equalize')

    if save:
        fig, ax1 = plt.subplots(1, 3, sharey=True, figsize=(20, 16))
    else:
        fig, (ax1, ax2) = plt.subplots(2, 3, sharey=True, figsize=(10, 8))
    fig.suptitle(uid, y=1)
    ax1[1].set_title('Final Pred, P > {}'.format(threshold))
    ax1[2].set_title('Overlay, P > {}'.format(threshold))
    y, y_c, y_m = prob_to_segment(y, y_c, y_m)
    y_bw = y.copy()
    if view_color_equalize:
        x = clahe(x)
    ax1[0].set_title('Image')
    ax1[0].imshow(x, aspect='auto')
    markers = np.zeros_like(x)
    y, markers = segment_to_instances(y, y_c, y_m)
    _, n_instance = label(y, return_num=True)
    y, cmap = _make_overlay(y)
    ax1[1].imshow(y, cmap=cmap, aspect='auto')
    # alpha
    ax1[2].imshow(x, aspect='auto')
    ax1[2].imshow(y, cmap=cmap, alpha=0.3, aspect='auto')

    if not save:
        ax2[0].set_title('Semantic Pred, P > {}'.format(threshold))
        ax2[0].imshow(y_bw, cmap='gray', aspect='auto')
        _, count = label(markers, return_num=True)
        ax2[1].set_title('Markers, #={}'.format(count))
        ax2[1].imshow(markers, cmap='gray', aspect='auto')
        if y_c is not None:
            ax2[2].set_title('Contour Pred, P > {}'.format(threshold_edge))
            ax2[2].imshow(y_c, cmap='gray', aspect='auto')

    plt.tight_layout()
    if save:
        # save side by side prediction figures
        dir = predict_save_folder()
        fp = os.path.join(dir, uid + '.png')
        plt.savefig(fp)
        # save fullsize overlay, filename encoded with instance count
        fp = os.path.join(dir, uid + '-' + str(n_instance) + '-fullsize.png')
        _save_fullsize_overlay(x, y, cmap, fp)
    else:
        show_figure()

def show_groundtruth(uid, x, y, y_c, y_m, gt, gt_s, gt_c, gt_m, save=False):
    only_contour = config['contour'].getboolean('exclusive')
    view_color_equalize = config['valid'].getboolean('view_color_equalize')
    print_table = config['valid'].getboolean('print_table')

    fig, (ax1, ax2, ax3) = plt.subplots(3, 4, sharey=True, figsize=(12, 8))
    fig.suptitle(uid, y=1)
    y, y_c, y_m = prob_to_segment(y, y_c, y_m)
    y_s = y.copy() # to show pure semantic predict later

    if view_color_equalize:
        x = clahe(x)
    ax1[0].set_title('Image')
    ax1[0].imshow(x, aspect='auto')
    y, markers = segment_to_instances(y, y_c, y_m)
    _, count = label(y, return_num=True)
    ax1[1].set_title('Final Pred, #={}'.format(count))
    ax1[1].imshow(y, cmap='gray', aspect='auto')
    # overlay contour to semantic ground truth (another visualized view for instance ground truth, eg. gt)
    _, count = label(gt, return_num=True)
    ax1[2].set_title('Instance Lbls, #={}'.format(count))
    ax1[2].imshow(gt_s, cmap='gray', aspect='auto')
    gt_c2, cmap = _make_overlay(gt_c)
    ax1[2].imshow(gt_c2, cmap=cmap, alpha=0.7, aspect='auto')
    if only_contour: # can not tell from instances in this case
        iou = iou_metric(y, label(gt > 0), print_table)
    else:
        iou = iou_metric(y, gt, print_table)
    ax1[3].set_title('Overlay, IoU={:.3f}'.format(iou))
    ax1[3].imshow(gt_s, cmap='gray', aspect='auto')
    y, cmap = _make_overlay(y)
    ax1[3].imshow(y, cmap=cmap, alpha=0.3, aspect='auto')

    _, count = label(y_s, return_num=True)
    ax2[0].set_title('Semantic Predict, #={}'.format(count))
    ax2[0].imshow(y_s, cmap='gray', aspect='auto')
    _, count = label(gt_s, return_num=True)
    ax2[1].set_title('Semantic Lbls, #={}'.format(count))
    ax2[1].imshow(gt_s, cmap='gray', aspect='auto')

    if y_c is not None:
        _, count = label(y_c, return_num=True)
        ax2[2].set_title('Contour Predict, #={}'.format(count))
        ax2[2].imshow(y_c, cmap='gray', aspect='auto')
        _, count = label(gt_c, return_num=True)
        ax2[3].set_title('Contour Lbls, #={}'.format(count))
        ax2[3].imshow(gt_c, cmap='gray', aspect='auto')

    _, count = label(markers, return_num=True)
    ax3[0].set_title('Final Markers, #={}'.format(count))
    ax3[0].imshow(markers, cmap='gray', aspect='auto')
    if y_m is not None:
        _, count = label(y_m, return_num=True)
        ax3[1].set_title('Marker Predict, #={}'.format(count))
        ax3[1].imshow(y_m, cmap='gray', aspect='auto')
        _, count = label(gt_m, return_num=True)
        ax3[2].set_title('Marker Lbls, #={}'.format(count))
        ax3[2].imshow(gt_m, cmap='gray', aspect='auto')

    plt.tight_layout()
    if save:
        dir = predict_save_folder()
        fp = os.path.join(dir, uid + '.png')
        plt.savefig(fp)
    else:
        show_figure()

def predict_save_folder():
    dir = os.path.join('data', 'predict')
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def get_iou(y, y_c, y_m, gt):
    only_contour = config['contour'].getboolean('exclusive')
    instances, _ = segment_to_instances(y, y_c, y_m)
    if only_contour:
        iou = iou_metric(instances, label(gt > 0))
    else:
        iou = iou_metric(instances, gt)
    return iou


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', action='store', choices=['train', 'valid', 'test'], help='Specify dataset to evaluate')
    parser.add_argument('--action', action='append', choices=['csv', 'iou', 'rle_mask', 'png_mask', 'png_preds','show'], help='Specify action to do, multiple actions only for rle_mask & png_mask')
    parser.add_argument('--save', action='store_true', help='Save overlay prediction as PNG files, only valid for "show" in action')
    parser.add_argument('ckpt', nargs='*', help='filepath of checkpoint(s), otherwise lookup checkpoint/current.json')
    parser.set_defaults(save=False, dataset='test')
    args = parser.parse_args()
    if not args.action:
        args.action = ['csv']

    if 'show' in args.action:
        try:
            import matplotlib
            import matplotlib.pyplot as plt
        except ImportError as err:
            print(err)
            print("[ERROR] No GUI library for rendering, consider to save as RLE '--action csv'")
            exit(-1)

        if args.save:
            print("[INFO] Save side-by-side prediction figure in 'data/predict' folder...")

    main(args.ckpt, args.action, args.save, args.dataset)
