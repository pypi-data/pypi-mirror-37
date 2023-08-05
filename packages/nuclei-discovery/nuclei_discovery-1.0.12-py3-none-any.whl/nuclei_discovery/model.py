import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from .config import config

class DilatedConvBlock(nn.Module):
    ''' no dilation applied if dilation equals to 1 '''
    def __init__(self, in_size, out_size, kernel_size=3, dropout_rate=0.1, activation=F.relu, dilation=1):
        super().__init__()
        # to keep same width output, assign padding equal to dilation
        self.conv = nn.Conv2d(in_size, out_size, kernel_size, padding=dilation, dilation=dilation)
        self.norm = nn.BatchNorm2d(out_size)
        self.activation = activation
        if dropout_rate > 0:
            self.drop = nn.Dropout2d(p=dropout_rate)
        else:
            self.drop = self.identity # no-op

    @staticmethod
    def identity(x):
        return x

    def forward(self, x):
        # CAB: conv -> activation -> batch normal
        x = self.norm(self.activation(self.conv(x)))
        x = self.drop(x)
        return x

class ConvBlock(nn.Module):
    def __init__(self, in_size, out_size, dropout_rate=0.2, dilation=1):
        super().__init__()
        self.block1 = DilatedConvBlock(in_size, out_size, dropout_rate=0)
        self.block2 = DilatedConvBlock(out_size, out_size, dropout_rate=dropout_rate, dilation=dilation)
        self.pool = nn.MaxPool2d(kernel_size=2)

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        return self.pool(x), x


class ConvUpBlock(nn.Module):
    def __init__(self, in_size, out_size, dropout_rate=0.2, dilation=1):
        super().__init__()
        ratio = in_size // out_size
        self.up = nn.ConvTranspose2d(in_size, in_size//ratio, 2, stride=2)
        self.block1 = DilatedConvBlock(in_size//ratio + out_size, out_size, dropout_rate=0)
        self.block2 = DilatedConvBlock(out_size, out_size, dropout_rate=dropout_rate, dilation=dilation)
        self.gate = AttentionGate(out_size)

    def forward(self, x, bridge):
        x = self.up(x)
        # align concat size by adding pad
        diffY = x.shape[2] - bridge.shape[2]
        diffX = x.shape[3] - bridge.shape[3]
        bridge = F.pad(bridge, (0, diffX, 0, diffY), mode='reflect')
        bridge = self.gate(x, bridge)
        x = torch.cat([x, bridge], 1)
        # CAB: conv -> activation -> batch normal
        x = self.block1(x)
        x = self.block2(x)
        return x

# Attentional Gating papers:
# (1) Attention U-Net: Learning Where to Look for the Pancreas (2018)
# (2) Gated Convolutional Neural Network for Semantic Segmentation in High-Resolution Images (2017)
# (3) Language Modeling with Gated Convolutional Networks (2016)
class AttentionGate(nn.Module):
    def __init__(self, out_size):
        super().__init__()
        self.gating = config.getboolean('param', 'attention_gate')
        if self.gating:
            self.conv1 = nn.Conv2d(out_size, out_size, kernel_size=1, padding=0)
            self.conv2 = nn.Conv2d(out_size, out_size, kernel_size=1, padding=0)
            self.conv3 = nn.Conv2d(out_size, out_size, kernel_size=1, padding=0)

    def entropy(self, x):
        y = F.sigmoid(x)
        return F.binary_cross_entropy_with_logits(x, y, size_average=False, reduce=False)

    def forward(self, x, bridge):
        if self.gating:
            # TEST1: decoder entropy as gating (concat)
            # gate = self.entropy(x)
            # bridge = gate * bridge

            # TEST2: decoder conv & entropy as gating (concat)
            # gate = self.entropy(self.conv1(x))
            # bridge = gate * bridge

            # TEST3: encoder conv & sigmoid as gating (concat)
            # gate = F.sigmoid(self.conv1(bridge))
            # bridge = gate * self.conv2(bridge)

            # TEST4: (encoder conv + decoder conv) & conv & sigmoid as gating (concat)
            additive = self.conv1(x) + self.conv2(bridge)
            gate = F.sigmoid(self.conv3(F.relu(additive)))
            bridge = gate * bridge
        return bridge

class CoordsBlock(nn.Module):
    # refer to CoordConv https://arxiv.org/abs/1807.03247
    def __init__(self, with_r=False):
        super().__init__()
        self.with_r = with_r

    def forward(self, x):
        assert x.dim() == 4
        n, _, h, w = x.shape
        # the i coordinate channel is an h x w matrix
        # with 1st row filled with 0's, 2nd row with 1's, 3rd row with 2's, etc.
        ci = torch.ones((n, 1, h, w))
        ci *= torch.arange(h).view(-1, 1)
        # The j coordinate channel is similar, but with columns filled in with constant values instead of rows
        cj = torch.ones((n, 1, h, w))
        cj *= torch.arange(w)
        # apply a final linear scaling of both i and j coordinate values to make them fall in the range [-1,1]
        ci = 2*(ci/(h-1))-1
        cj = 2*(cj/(w-1))-1
        # move to cuda if fit
        if x.is_cuda:
            ci = ci.to('cuda')
            cj = cj.to('cuda')
        x = torch.cat([x, ci, cj], 1)
        if self.with_r:
            # a third channel for an r coordinate, where r = sqrt[(i - h/2)^2 + (j - w/2)^2]
            # note: paper's example code was incorrect to formula
            cr = torch.sqrt(ci ** 2 + cj ** 2)
            x = torch.cat([x, cr], 1)
        return x

class UNet(nn.Module):
    def __init__(self):
        super().__init__()
        # down conv
        self.c1 = ConvBlock(3, 16)
        self.c2 = ConvBlock(16, 32)
        self.c3 = ConvBlock(32, 64)
        self.c4 = ConvBlock(64, 128)
        # bottom conv tunnel
        self.cu = ConvBlock(128, 256)
        # up conv
        self.u5 = ConvUpBlock(256, 128)
        self.u6 = ConvUpBlock(128, 64)
        self.u7 = ConvUpBlock(64, 32)
        self.u8 = ConvUpBlock(32, 16)
        # final conv tunnel
        self.ce = nn.Conv2d(16, 1, 1)

    def forward(self, x):
        x, c1 = self.c1(x)
        x, c2 = self.c2(x)
        x, c3 = self.c3(x)
        x, c4 = self.c4(x)
        _, x = self.cu(x) # no maxpool for U bottom
        x = self.u5(x, c4)
        x = self.u6(x, c3)
        x = self.u7(x, c2)
        x = self.u8(x, c1)
        x = self.ce(x)
        x = F.sigmoid(x)
        return x

# Contour aware Marker Unet
class CamUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = ConvBlock(3, 16)
        self.c2 = ConvBlock(16, 32)
        self.c3 = ConvBlock(32, 64)
        self.c4 = ConvBlock(64, 128)
        # bottom conv tunnel
        self.cu = ConvBlock(128, 256)
        # segmentation up conv branch
        self.u5s = ConvUpBlock(256, 128)
        self.u6s = ConvUpBlock(128, 64)
        self.u7s = ConvUpBlock(64, 32)
        self.u8s = ConvUpBlock(32, 16)
        self.ces = nn.Conv2d(16, 1, 1)
        # contour up conv branch
        self.u5c = ConvUpBlock(256, 128)
        self.u6c = ConvUpBlock(128, 64)
        self.u7c = ConvUpBlock(64, 32)
        self.u8c = ConvUpBlock(32, 16)
        self.cec = nn.Conv2d(16, 1, 1)
        # marker up conv branch
        self.u5m = ConvUpBlock(256, 128)
        self.u6m = ConvUpBlock(128, 64)
        self.u7m = ConvUpBlock(64, 32)
        self.u8m = ConvUpBlock(32, 16)
        self.cem = nn.Conv2d(16, 1, 1)

    def forward(self, x):
        x, c1 = self.c1(x)
        x, c2 = self.c2(x)
        x, c3 = self.c3(x)
        x, c4 = self.c4(x)
        _, x = self.cu(x) # no maxpool for U bottom
        xs = self.u5s(x, c4)
        xs = self.u6s(xs, c3)
        xs = self.u7s(xs, c2)
        xs = self.u8s(xs, c1)
        xs = self.ces(xs)
        xs = F.sigmoid(xs)
        xc = self.u5c(x, c4)
        xc = self.u6c(xc, c3)
        xc = self.u7c(xc, c2)
        xc = self.u8c(xc, c1)
        xc = self.cec(xc)
        xc = F.sigmoid(xc)
        xm = self.u5m(x, c4)
        xm = self.u6m(xm, c3)
        xm = self.u7m(xm, c2)
        xm = self.u8m(xm, c1)
        xm = self.cem(xm)
        xm = F.sigmoid(xm)
        return xs, xc, xm

# Shared Contour aware Marker Unet
class SCamUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = ConvBlock(3, 16)
        self.c2 = ConvBlock(16, 32)
        self.c3 = ConvBlock(32, 64)
        self.c4 = ConvBlock(64, 128)
        # bottom conv tunnel
        self.cu = ConvBlock(128, 256)
        self.u5 = ConvUpBlock(256, 128)
        self.u6 = ConvUpBlock(128, 64)
        self.u7 = ConvUpBlock(64, 32)
        self.u8 = ConvUpBlock(32, 16)
        self.ce = nn.Conv2d(16, 3, 1)

    def forward(self, x):
        x, c1 = self.c1(x)
        x, c2 = self.c2(x)
        x, c3 = self.c3(x)
        x, c4 = self.c4(x)
        _, x = self.cu(x) # no maxpool for U bottom
        x = self.u5(x, c4)
        x = self.u6(x, c3)
        x = self.u7(x, c2)
        x = self.u8(x, c1)
        x = self.ce(x)
        x = torch.split(x, split_size=1, dim=1) # split 3 channels
        s = F.sigmoid(x[0])
        c = F.sigmoid(x[1])
        m = F.sigmoid(x[2])
        return s, c, m

# Transfer Learning ResNet as Encoder part of Contour aware Marker Unet
class Res_CamUNet(nn.Module):
    def __init__(self, layers=34, fixed_feature=True):
        super().__init__()
        # define pre-train model parameters
        if layers == 101:
            builder = models.resnet101
            l = [64, 256, 512, 1024, 2048]
        else:
            builder = models.resnet34
            l = [64, 64, 128, 256, 512]
        # load weight of pre-trained resnet
        self.resnet = builder(pretrained=True)
        if fixed_feature:
            for param in self.resnet.parameters():
                param.requires_grad = False
        # segmentation up conv branch
        self.u5s = ConvUpBlock(l[4], l[3])
        self.u6s = ConvUpBlock(l[3], l[2])
        self.u7s = ConvUpBlock(l[2], l[1])
        self.u8s = ConvUpBlock(l[1], l[0])
        self.ces = nn.ConvTranspose2d(l[0], 1, 2, stride=2)
        # contour up conv branch
        self.u5c = ConvUpBlock(l[4], l[3])
        self.u6c = ConvUpBlock(l[3], l[2])
        self.u7c = ConvUpBlock(l[2], l[1])
        self.u8c = ConvUpBlock(l[1], l[0])
        self.cec = nn.ConvTranspose2d(l[0], 1, 2, stride=2)
        # marker up conv branch
        self.u5m = ConvUpBlock(l[4], l[3])
        self.u6m = ConvUpBlock(l[3], l[2])
        self.u7m = ConvUpBlock(l[2], l[1])
        self.u8m = ConvUpBlock(l[1], l[0])
        self.cem = nn.ConvTranspose2d(l[0], 1, 2, stride=2)

    def forward(self, x):
        # refer https://github.com/pytorch/vision/blob/master/torchvision/models/resnet.py
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = c1 = self.resnet.relu(x)
        x = self.resnet.maxpool(x)
        x = c2 = self.resnet.layer1(x)
        x = c3 = self.resnet.layer2(x)
        x = c4 = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        # segmentation up conv branch
        xs = self.u5s(x, c4)
        xs = self.u6s(xs, c3)
        xs = self.u7s(xs, c2)
        xs = self.u8s(xs, c1)
        xs = self.ces(xs)
        xs = F.sigmoid(xs)
        # contour up conv branch
        xc = self.u5c(x, c4)
        xc = self.u6c(xc, c3)
        xc = self.u7c(xc, c2)
        xc = self.u8c(xc, c1)
        xc = self.cec(xc)
        xc = F.sigmoid(xc)
        # marker up conv branch
        xm = self.u5m(x, c4)
        xm = self.u6m(xm, c3)
        xm = self.u7m(xm, c2)
        xm = self.u8m(xm, c1)
        xm = self.cem(xm)
        xm = F.sigmoid(xm)
        return xs, xc, xm

# Transfer Learning ResNet as Encoder part of Contour aware Marker Unet
class Res_SamUNet(nn.Module):
    def __init__(self, layers=34, fixed_feature=True):
        super().__init__()
        # define pre-train model parameters
        if layers == 101:
            builder = models.resnet101
            l = [64, 256, 512, 1024, 2048]
        else:
            builder = models.resnet34
            l = [64, 64, 128, 256, 512]
        # load weight of pre-trained resnet
        self.resnet = builder(pretrained=True)
        if fixed_feature:
            for param in self.resnet.parameters():
                param.requires_grad = False
        # segmentation up conv branch
        self.u5 = ConvUpBlock(l[4], l[3])
        self.u6 = ConvUpBlock(l[3], l[2])
        self.u7 = ConvUpBlock(l[2], l[1])
        self.u8 = ConvUpBlock(l[1], l[0])
        # final conv tunnel
        self.ces = nn.ConvTranspose2d(l[0], 1, 2, stride=2)
        self.cec = nn.ConvTranspose2d(l[0], 1, 2, stride=2)
        self.cem = nn.ConvTranspose2d(l[0], 1, 2, stride=2)

    def forward(self, x):
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = c1 = self.resnet.relu(x)
        x = self.resnet.maxpool(x)
        x = c2 = self.resnet.layer1(x)
        x = c3 = self.resnet.layer2(x)
        x = c4 = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        x = self.u5(x, c4)
        x = self.u6(x, c3)
        x = self.u7(x, c2)
        x = self.u8(x, c1)
        xs = self.ces(x)
        xs = F.sigmoid(xs)
        xc = self.cec(x)
        xc = F.sigmoid(xc)
        xm = self.cem(x)
        xm = F.sigmoid(xm)
        return xs, xc, xm

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def build_model(model_name='unet'):
    # initialize model
    if model_name == 'unet':
        return UNet()
    elif model_name == 'camunet':
        return CamUNet()
    elif model_name == 'scamunet':
        return SCamUNet()
    elif model_name == 'res_camunet':
        return Res_CamUNet(34)
    elif model_name == 'res_samunet':
        return Res_SamUNet(34)
    else:
        raise NotImplementedError()

if __name__ == '__main__':
    print('Network parameters -')
    for n in ['unet', 'camunet', 'scamunet', 'res_camunet', 'res_samunet']:
        net = build_model(n)
        #print(net)
        print('\t model {}: {}'.format(n, count_parameters(net)))
        del net

    print("Forward pass sanity check - ")
    for n in ['camunet', 'res_camunet', 'res_samunet']:
        t = time.time()
        net = build_model(n)
        x = torch.randn(1, 3, 256, 256)
        y = net(x)
        #print(x.shape, y.shape)
        del net
        print('\t model {0}: {1:.3f} seconds'.format(n, time.time() - t))

    # x = torch.randn(10, 3, 256, 256)
    # b = ConvBlock(3, 16)
    # p, y = b(x)
    # print(p.shape, y.shape)