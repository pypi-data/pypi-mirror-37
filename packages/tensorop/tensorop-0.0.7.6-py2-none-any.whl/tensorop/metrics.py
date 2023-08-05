from collections import defaultdict

from scipy import spatial
import numpy as np


def numeric_score(preds,gt):
    FP = np.float(np.sum((preds==1)&(gt==0)))
    FN = np.float(np.sum((preds==0)&(gt==1)))
    TP = np.float(np.sum((preds==1)&(gt==1)))
    TN = np.float(np.sum((preds==0)&(gt==0)))
    return FP,FN,TP,TN

def iou(preds,gt):
    """
    Intersection over Union
    """
    FP,FN,TP,TN = numeric_score(preds,gt)
    if(TP+FP+FN) <= 0.0:
        return 0.0
    return TP/(TP+FP+FN)*100.0