import numpy as np
import math
from sklearn.utils.extmath import softmax as softmax_
from . import hyperopt

def softmax (x):
    return softmax_ ([x])[0].tolist ()

def sigmoid (x):   
    return [1 / (1 + np.exp(-e)) for e in x]

def confusion_matrix (labels, predictions, num_labels):
  rows = []
  for i in range (num_labels):
    row = np.bincount (predictions[labels == i], minlength=num_labels)
    rows.append (row)
  return np.vstack (rows)

def render_trial (space, trial, stringfy = False):
    if trial.get ("misc"):
        trial = dict ([(k, v [0]) for k, v in trial ["misc"]["vals"].items ()])
    params = hyperopt.space_eval(space, trial)
    if stringfy:
        return ", ".join (["{}: {}".format (k, v) for k, v in params.items ()])
    return params
  