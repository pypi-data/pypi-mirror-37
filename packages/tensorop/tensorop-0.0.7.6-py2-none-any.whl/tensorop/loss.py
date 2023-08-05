from __future__ import absolute_import
import sys

import torch
from torch import nn

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")

class CrossEntropy(nn.Module):
    def __init__(self,num_classes,epsilon=0.1,use_gpu=True):
        super(CrossEntropy,self).__init__()
        self.num_classes = num_classes
        self.epsilon = epsilon
        self.use_gpu = use_gpu
        self.logsoftmax = nn.LogSoftmax(dim=1)

    def forward(self,inputs,targets):
        log_probs = self.logsoftmax(inputs)
        targets = torch.zeros(log_probs.size()).scatter_(1,targets.unsqueeze(1).data.cpu(),1)
        if self.use_gpu: 
            targets = targets.cuda()
        epsilon = 0.1
        targets = (1-epsilon)*targets+self.epsilon/self.num_classes
        loss = (-targets*log_probs).mean(0).sum()
        return loss

class TripletLoss(nn.Module):
    def __init__(self,margin=0.3):
        super(TripletLoss,self).__init__()
        self.margin = margin
        self.ranking_loss = nn.MarginRankingLoss(margin=margin)

    def forward(self,inputs,targets):
        """
        targets = ground truth with labels
        """
        n = inputs.size(0)
        #n = len(inputs)
        dist = torch.pow(inputs,2).sum(dim=1,keepdim=True).expand(n,n)
        dist = dist+dist.t()
        dist.addmm_(1,-2,inputs,inputs.t())
        dist = dist.clamp(min=1e-12).sqrt()
        mask = targets.expand(n,n).eq(targets.expand(n,n).t())
        dist_ap,dist_an = [],[]
        for i in range(n):
            dist_ap.append(dist[i][mask[i]].max().unsqueeze(0))
            dist_an.append(dist[i][mask[i]==0].min().unsqueeze(0))
        dist_ap = torch.cat(dist_ap)
        dist_an = torch.cat(dist_an)
        y = torch.ones_like(dist_an)
        loss = self.ranking_loss(dist_an,dist_ap,y)
        return loss

class ConfidentMSELoss(Module):
    def __init__(self,threshold=0.96):
        self.threshold = threshold
        super().__init__()

    def forward(self,input,targets):
        n = input.size(0)
        conf_mask = torch.gt(target,self.threshold).float()
        input_flat = input.view(n,-1)
        target_flat = target.view(n,-1)
        conf_mask_flat = conf_mask.view(n,-1)
        diff = (input_flat-target_flat)**2
        diff_conf = diff*conf_mask_flat
        loss = diff_conf.mean()
        return loss

class MaskNLLLoss(inp,target,mask):
    ntotal = mask.sum()
    cross_entropy = -torch.log(torch.gather(inp,1,target.view(-1,1)))
    loss = cross_entropy.masked_select(mask).mean()
    loss = loss.to(device)
    return loss,ntotal.item()

class FocalLoss(BCE_Loss):
    def weight(self,x,t):
        alpha,gamma=0.25,1
        p = x.sigmoid()
        pt = p*t+(1-p)*(1-t)
        w = alpha*t + (1-alpha)*(1-t)
        return w*(1-pt).pow(gamma)


def cross_ent_onehot(y_train_onehot):
    y_train_onehot = torch.from_numpy(y_train_onehot)
    ui = [np.where(r==1)[0][0] for r in y_train_onehot]
    yu = torch.FloatTensor(ui)
    yu = yu.long()
    return yu
