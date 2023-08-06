import torch
from torch import nn

class ConvBlock(nn.Module):
    def __init__(self,inp,out,kernel_size,stride,bn=True,padding=None):
        super().__init__()
        if padding is None:
            padding = kernel_size//(2*stride)
        self.conv = nn.Conv2d(inp,out,kernel_size,bn,padding=padding,bias=False)
        if bn:
            self.bn = nn.BatchNorm2d(out) 
        self.relu = nn.LeakyReLU(0.2,inplace=True)

    def forward(self,x):
        x = self.relu(self.conv(x))
        return self.bn(x) if self.bn else x
        
class DeConvBlock(nn.Module):
    def __init__(self,inp,out,kernel_size,stride,padding,bn=True):
        super().__init__()
        self.conv = nn.ConvTranspose2d(inp,out,kernel_size,stride,padding,bias=False)
        self.bn = nn.BatchNorm2d(out)
        self.relu = nn.LeakyReLU(inplace=True)

    def forward(self,x):
        x = self.relu(self.conv(x))
        return self.bn(x) if self.bn else x