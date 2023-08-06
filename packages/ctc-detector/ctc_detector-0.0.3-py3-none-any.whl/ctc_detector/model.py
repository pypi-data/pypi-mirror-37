import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from config import config

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

# Unet
class UNet(nn.Module):
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


# Transfer Learning ResNet as Encoder part of Unet
class Res_UNet(nn.Module):
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
        self.ce = nn.ConvTranspose2d(l[0], 1, 2, stride=2)

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
        x = self.ce(x)
        x = F.sigmoid(x)
        return x

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def build_model(model_name='unet'):
    # initialize model
    if model_name == 'unet':
        return UNet()
    elif model_name == 'res_unet':
        return Res_UNet(34)
    else:
        raise NotImplementedError()

if __name__ == '__main__':
    print('Network parameters -')
    for n in ['unet', 'res_unet']:
        net = build_model(n)
        #print(net)
        print('\t model {}: {}'.format(n, count_parameters(net)))
        del net

    print("Forward pass sanity check - ")
    for n in ['unet', 'res_unet']:
        t = time.time()
        net = build_model(n)
        x = torch.randn(1, 3, 256, 256)
        y = net(x)
        #print(x.shape, y.shape)
        del net
        print('\t model {0}: {1:.3f} seconds'.format(n, time.time() - t))