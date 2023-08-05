import tensorflow as tf
import numpy as np
from . import predutil
        
class Result:    
    def __init__ (self, x, y, is_validating, logit, cost, acc, epoch, accfunc, summaryfunc, train_dir, labels, ops = None):
        self.x = x        
        self.is_validating = is_validating
        self.epoch = epoch
        self.logit = logit
        self.y = y
        self.cost = cost
        self.accuracy = acc
        self.accfunc = accfunc
        self.summaryfunc = summaryfunc
        self.train_dir = train_dir
        self.labels = labels        
        self.ops = ops
    
    def update (self, summary = {}, *args, **karg): 
        try:
            self.accuracy = self.accfunc (self.logit, self.y, *args, **karg)
        except NotImplementedError:
            self.accuracy = 0.0    
        self.summaryfunc (self.is_validating  and 'recall' or 'valid', self.make_summary (summary), True)    
    
    def confusion_matrix (self, num_label = 0, label_index = 0):
        if num_label <= 0:
            if not self.labels:
                raise ValueError ("num_label required")
            num_label = len (self.labels [label_index])
            
        return predutil.confusion_matrix (
             np.argmax (self.logit [:, :num_label], 1), 
             np.argmax (self.y [:, :num_label], 1),
             num_label
        )
                
    def make_summary (self, d):
        d  ["eval/cost/regularized"] = self.cost
        if isinstance (self.accuracy, (tuple, list)):
            if not self.labels:
                for i, acc in enumerate (self.accuracy [:-1]):
                    d ["eval/accuracy/{}".format (i + 1)] = acc                                        
            else:
                for i in range (len (self.accuracy) - 1):
                    label = self.labels [i]
                    d ["eval/accuracy/" + label.name] = self.accuracy [i]
            d ["eval/accuracy/average"] = self.accuracy [-1]                    
        else:
            d ["eval/accuracy"] = self.accuracy
        return d
    
    def confidence_level (self, label_index = 0):
        label = self.labels [label_index]
        stat = {}
        for idx in range (len (self.y)):
            logit = self.logit [idx][:len (label)]
            y = self.y [idx][:len (label)]
            probs = predutil.softmax (logit)
            prob = "{:.5f}".format (probs [np.argmax (probs)])
            if prob not in stat:
                stat [prob] = [0, 0]
            if np.argmax (probs) == np.argmax (y):    
                stat [prob][0] += 1
            stat [prob][1] += 1
            
        ordered = [] 
        accum = 0        
        accum_t = 0
        total = len (self.y)
        for lev, (c, t) in sorted (stat.items (), reverse = True):            
            accum += c            
            accum_t += t
            accuracy = accum / accum_t * 100
            ordered.append ((
                lev, 
                accum, accum_t, accuracy, 
                accum / total * 100 
            ))
            if len (ordered) >= 10 and accuracy < 100.:
                break
        return ordered    
                     
    def logit_range (self):
        output_range = [self.logit.min (), self.logit.max (), np.mean (self.logit), np.std (self.logit)]
        quant_range = {}
        for idx, m in enumerate (self.logit [:,:29].argsort (1)[:,-2]):
            sec = int (self.logit [idx, m])
            try: quant_range [sec] += 1
            except KeyError: quant_range [sec] = 1
        quant_range = quant_range
        if quant_range:           
            stats = sorted (quant_range.items ())
            # output range for top1: {} ~ {}, logit range: {:.3f} ~ {:.3f}, mean: {:.3f} std: {:.3f}
            return stats [0][0] - 1, stats [-1][0] + 1, output_range [0], output_range [1], output_range [2], output_range [3]                                
        