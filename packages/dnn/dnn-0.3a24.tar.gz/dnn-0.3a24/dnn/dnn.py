import tensorflow as tf
import numpy as np
import sys
import os, shutil
import random
from aquests.lib import pathtool
from . import overfit, optimizers, predutil, result
import sys
from functools import partial
import pickle
from sklearn.decomposition import PCA
from tensorflow.python.framework.ops import Tensor

def _standardize (x, mean, std):
    return (x - mean) / std

def _get_scaling_range (normrange):
    if isinstance (normrange, (list, tuple)):
        scale_min, scale_max = normrange
    else:
        scale_min, scale_max = -1, 1
    return scale_min, scale_max    
    
def _scaling (x, min_, gap, normrange):
    scale_min, scale_max = _get_scaling_range (normrange) 
    return np.clip (scale_min + (scale_max - scale_min) * ((x - min_) / gap), scale_min, scale_max)
    
def _normalize (x, *args):
    pca = None
    if isinstance (x, list): 
        x = np.array (x)    
    if len (args) == 8:
        # old version
        mean, std, min_, gap, pca_k, pca, normalize, standardize = args        
    else:
        mean, std, min_, gap, pca_k, eigen_vecs, pca_mean, normalize, standardize = args
        
    if standardize: # 0 mean, 1 var
        x = _standardize (x, mean, std)        
    if normalize: # -1 to 1
        x = _scaling (x, min_, gap, normalize)
        
    if pca_k: # PCA
        orig_shape = x.shape
        if len (orig_shape) == 3:
            x = x.reshape ([orig_shape [0]  * orig_shape [1], orig_shape [2]])
        if pca:
            # for old version
            x = pca.transform (x)
        else:    
            x = np.dot (x - pca_mean, eigen_vecs)
        if len (orig_shape) == 3:
            x = x.reshape ([orig_shape [0], orig_shape [1], pca_k])    

    return x
                
class DNN:
    def __init__ (self, gpu_usage = 0, name = None, graph = None):
        self.gpu = gpu_usage
        self.name = name
        if graph is None:
            self.graph = tf.Graph ()            
        else:
            self.graph = graph
        
        self.sess = None
        self.in_service = True
        self.writers = {}
        self.overfitwatch = None
        
        self.summaries_dir = None
        self.verbose = True
        self.filter_func = None
        self.norm_factor = None
        self.train_dir = None
        self.max_acc = 0.0
        self.accuracy_threshold = 0.0
        self.is_validating = False
        self.is_improved = False
        self.batch_size = 0
        self.epoch = 0
        self.norm_file = None  
        self.monitor = 'cost'        
        self.labels = None
        self.label_file = None        
        self.auto_save = True        
        self.log_per_steps = 100   
        self.__optimzables = set ()    
                    
    def create_network (self):    
        with self.graph.as_default ():
            with tf.variable_scope ("placeholders"):
                self.make_default_place_holders ()
                self.make_place_holders ()
            self.make_variables ()    
            self.logit = self.make_logit ()
            if isinstance (self.logit, tuple):
                self.logit, self.end_points = self.logit            
            self.saver = tf.train.Saver (tf.global_variables())            
    
    def make_default_place_holders (self):    
        self.dropout_rate = tf.placeholder_with_default (tf.constant (0.0), [])
        self.is_training = tf.placeholder_with_default (tf.constant (False), [])        
        self.n_sample = tf.placeholder_with_default (tf.constant (1), [])
        self.random_dropout_rate = tf.random_uniform ([], minval=0.1, maxval=0.7, dtype=tf.float32)
        self.nullop = tf.constant (0.0)
    
    def init_session (self):
        if self.sess is not None:
            return
        
        if self.gpu:
            self.sess = tf.Session (graph = self.graph, config = tf.ConfigProto(gpu_options=tf.GPUOptions (per_process_gpu_memory_fraction = self.gpu), log_device_placement = False))
        else:
            self.sess = tf.Session(graph = self.graph)            
        self.sess.run (tf.global_variables_initializer())     

    def get_best_cost (self):
        return overfitwatch.min_cost
    
    def get_best_accuracy (self):
        return self.max_acc
    
    @property
    def is_overfit (self):
        return self.overfitwatch.is_overfit ()
    
    def eval (self, tensor):
        with self.sess.as_default ():
            return tensor.eval ()
            
    # data filtering for multi model training -----------------------------
    def set_filter (self, func):
        self.filter_func = func
    
    def filter (self, ys, *args):
        is_no_x = True
        xs = None
        if args:
            is_no_x = False        
            xs = args [0]
             
        if self.filter_func:
            ys, xs = self.filter_func (ys, xs)
        if is_no_x:
            return ys
        return ys, xs
                    
    # labels -----------------------------------------------------------
    def set_labels (self, labels):
        self.labels = labels
    
    def save_labels (self):
        with open (self.label_file, "wb") as f:
            pickle.dump (self.labels, f)
    
    def load_labels (self):
        if not os.path.isfile (self.label_file):
            return
        with open (os.path.join (self.label_file), "rb") as f:
            self.labels = pickle.load (f)
        
    def set_epoch (self, epoch):
        self.epoch = epoch
    
    def get_epoch (self):
        return self.epoch
            
    def  get_best_accuracy (self):
        return self.name, self.max_acc
    
    # normalization -----------------------------------------------------
    def get_norm_factor (self):
        return self.norm_factor
    
    def has_norm_factor (self):
        return os.path.exists (self.norm_file)
        
    def load_norm_factor (self):
        if self.norm_factor:
            return
        if not os.path.isfile (self.norm_file):
            return
        with open (self.norm_file, "rb") as f:
            self.norm_factor = pickle.load (f)
                        
    def normalize (self, x, normalize = False, standardize = False, axis = 0, pca_k = None, pca_random = False):
        if self.norm_factor:
            return _normalize (x, *self.norm_factor)
        
        if not normalize and not standardize and pca_k is None:
            if not self.norm_file:
                return x
            if os.path.isfile (self.norm_file):
                os.remove (self.norm_file)
            return x
        
        min0_ = None
        gap0 = None
            
        if isinstance (x, list): 
            x = np.array (x)
        
        mean = np.mean (x, axis, keepdims = True)
        std = np.std (x, axis, keepdims = True) + 1e-8
        if standardize: # 0 mean, 1 var            
            x = _standardize (x, mean, std)

        min_ = np.min (x, axis, keepdims = True)
        gap = (np.max (x, axis, keepdims = True) - min_) + 1e-8
        if normalize: # -1 to 1
            x = _scaling (x, min_, gap, normalize)
        
        eigen_vecs = None    
        pca_mean = None        
        if pca_k:
            if pca_k < 0:
                self.show_pca (x, pca_random)
            else:
                x, pca = self.pca (x, pca_k, pca_random)
            eigen_vecs = pca.components_.swapaxes (1, 0)    
            pca_mean = pca.mean_
            # DO NOT NORMALIZE pca transformed data
        
        self.norm_factor = (mean, std, min_, gap, pca_k, eigen_vecs, pca_mean, normalize, standardize)
        if self.norm_file and (normalize or standardize or pca_k):
            with open (self.norm_file, "wb") as f:
                pickle.dump (self.norm_factor, f)
        
        return x
    
    def show_pca (self, data, pca_random = False):
        orig_shape = data.shape
        if len (orig_shape) == 3:
            data = data.reshape ([orig_shape [0]  * orig_shape [1], orig_shape [2]])
        
        print ("* Principal component analyzing (showing eigen vector)...")
        pca = PCA (n_components = orig_shape [-1], svd_solver = pca_random and 'randomized' or "auto")
        pca.fit (data)
        for i, r in enumerate (pca.explained_variance_ratio_.cumsum ()):
            if r > 0.9 and i % 10 == 0:
                print ("n_components: {}, retained variance: {:.2f}".format (i, r))
                if "{:.2f}".format (r) == "1.00":
                    break
        print ("* Principal component analyzing, done.")    
        sys.exit (1)    
        
    def pca (self, data, n_components = None, pca_random = False):
        orig_shape = data.shape
        if len (orig_shape) == 3:
            data = data.reshape ([orig_shape [0]  * orig_shape [1], orig_shape [2]])
        pca = PCA (n_components = n_components, svd_solver = pca_random and 'randomized' or "auto")
        pca.fit (data)        
        data = pca.transform (data)
        if len (orig_shape) == 3:
            data = data.reshape ([orig_shape [0], orig_shape [1], n_components])        
        return data, pca
    
    # train dir / log dir ----------------------------------------------------
    def turn_off_verbose (self):
        self.verbose = False
    
    def reset_dir (self, target):
        if os.path.exists (target):
            shutil.rmtree (target)
        if not os.path.exists (target):
            os.makedirs (target)
    
    def set_train_dir (self, path, reset = False, auto_save = True):
        self.auto_save = auto_save
        if self.name:
            path = os.path.join (path, self.name.strip ())        
        self.train_dir = path        
        if reset and os.path.exists (self.train_dir):
            for file in os.listdir (self.train_dir):
                if file == "normfactors":
                    continue
                t = os.path.join (self.train_dir, file)
                if os.path.isdir (t):
                    shutil.rmtree (t)
                else:    
                    os.remove (t)
        else:
            pathtool.mkdir (self.train_dir)
        self.norm_file = os.path.join (self.train_dir, 'normfactors')
        self.label_file = os.path.join (self.train_dir, 'labels')
                
    def set_tensorboard_dir (self, summaries_dir, reset = True, log_per_steps = 10):
        self.summaries_dir = summaries_dir
        self.log_per_steps = log_per_steps
        if reset:
            os.system ('killall tensorboard')
            if tf.gfile.Exists(summaries_dir):
                tf.gfile.DeleteRecursively(summaries_dir)
            tf.gfile.MakeDirs(summaries_dir)            
    
    def get_writers (self, *writedirs):        
        return [tf.summary.FileWriter(os.path.join (self.summaries_dir, "%s%s" % (self.name and self.name.strip () + "-" or "", wd)), self.graph) for wd in writedirs]
        
    def make_writers (self, *writedirs):        
        for i, w in enumerate (self.get_writers (*writedirs)):
            self.writers [writedirs [i]] = w
                        
    def write_summary (self, writer, feed_dict, verbose = True):
        if writer not in self.writers:
            self.make_writers (writer)
        
        summary = tf.Summary()
        output = []
        for k, v in feed_dict.items ():
            if self.name:
                k = "{}:{}".format (self.name, k)
            if isinstance (v, (list, tuple)):
                if len (v) == 1:
                    v = v [0]
                else:
                    raise ValueError ("Required float, int or an array contains only one of them")     

            summary.value.add (tag = k , simple_value = v)
            if isinstance (v, (float, np.float64, np.float32)):
                if v > 1: fmt = "{} {:.2f}"                
                elif v > 0.01: fmt = "{} {:.3f}"
                else: fmt = "{} {:.7f}"    
                output.append (fmt.format (k, v))
            elif isinstance (v, (int, np.int64, np.int32)):
                output.append ("{} {:04d}".format (k, v))
            else:
                raise ValueError ("Required float, int type")
        
        output.sort ()    
        if self.is_overfit:
            output.append ("!Overfitted")
        if self.is_improved:
            output.append ("*Improved")
            
        self.writers [writer].add_summary (summary, self.eval (self.global_step))
        if verbose and self.verbose:
            print ("[%d:%7s] %s" % (self.epoch, writer, " | ".join (output)))
    
    def log (self, name, val, family = "net"):
        if isinstance (val, Tensor):
            #tf.summary.scalar (name, val)
            tf.summary.scalar ("net/" + name, self.add_average (val))
        else:    
            self.write_summary (family, {name: val}, False)        
    
    def logp (self, name, val):
        self.log (name, val, self.is_validating and "valid" or "recall")
    
    def add_average(self, variable):        
        tf.add_to_collection (tf.GraphKeys.UPDATE_OPS, self.ema.apply([variable]))
        average_variable = tf.identity (self.ema.average(variable), name=variable.name[:-2] + '_avg')
        return average_variable
    
    # model save -------------------------------------------------------        
    def restore (self):     
        try: self.max_acc = sorted ([float (each [4:12]) for each in os.listdir (self.train_dir) if each.startswith ('acc-')])[-1]
        except IndexError: pass
        self.load_norm_factor ()
        self.load_labels ()
        self.create_network ()
        with self.graph.as_default ():
            self.init_session ()
            self.saver.restore (self.sess, tf.train.latest_checkpoint (self.train_dir))
        
    def save (self, filename = None):
        if not filename:
            filename = "%04d-acc-%.3f+cost-%.3f" % (self.epoch, self.max_acc, self.overfitwatch.latest_cost)
        path = os.path.join (self.train_dir, filename)
        with self.graph.as_default ():
            self.saver.save (self.sess, path, global_step = self.global_step)
    
    def get_latest_model_version (self, path):
        if not os.listdir (path):
            return 0
        return max ([int (ver) for ver in os.listdir (path) if ver.isdigit () and os.path.isdir (os.path.join (path, ver))])    
    
    def to_tflite (self, path, saved_model_dir, quantized_input = None, quantized_input_stats = (128, 128), default_ranges_stats = (0, 1)):
        from . import tflite
        
        tflite.convert (path, saved_model_dir, quantized_input, quantized_input_stats, default_ranges_stats)
        interp = tflite.Interpreter (path, quantized_input is not None and quantized_input_stats or None)
        inputs, outputs = interp.get_info ()
        
        print ("* TF Lite")
        #print ("  - " + self.output_stat (os.path.join (saved_model_dir, "outputstat")))
        print ("  - Inputs")
        for k, v in inputs.items (): print ("    . {}: {}".format (k, v))
        print ("  - Outputs")
        for k, v in outputs.items (): print ("    . {}: {}".format (k, v))
    
    def to_tflite_from_graph_def (self, saved_model_dir, inputs, outputs, quantized_input = None, quantized_input_stats = (128, 128), default_ranges_stats = (0, 1)):
        from . import tflite
        
        inputs=dict ([(k, tf.saved_model.utils.build_tensor_info (v)) for k, v in inputs.items ()])
        outputs=dict ([(k, tf.saved_model.utils.build_tensor_info (v)) for k,v in outputs.items ()])
        
        tf.train.write_graph(self.sess.graph_def, saved_model_dir, 'graph-def.pb', as_text=False)
        graph_def_file = os.path.join (saved_model_dir, 'graph-def.pb')
        input_arrays = [v.name.endswith (":0") and v.name [:-2] or v for v in inputs.values ()]
        output_arrays = [v.name.endswith (":0") and v.name [:-2] or v for v in outputs.values ()]
        tflite.convert_from_graph_def (self.train_dir, graph_def_file, input_arrays, output_arrays, quantized_input, quantized_input_stats, default_ranges_stats)
            
    def to_save_model (self, path, predict_def, inputs, outputs):
        from . import saved_model
        if self.name:
            path = os.path.join (path, self.name.strip ())
        pathtool.mkdir (path)
        version = self.get_latest_model_version (path) + 1        
        inputs, outputs = saved_model.convert (
            "{}/{}/".format (path, version), 
            predict_def, inputs, outputs,
            self.sess,
            self.graph
        )        
        if os.path.isfile (self.norm_file):
            shutil.copy (self.norm_file, os.path.join (path, str (version), "normfactors"))    
        if os.path.isfile (self.label_file):
            shutil.copy (self.label_file, os.path.join (path, str (version), "labels"))    
            
        print ("* Saved Model")
        print ("  - Inputs")
        for k, v in inputs.items (): print ("    . {}: {}".format (k, v.name))
        print ("  - Outputs")
        for k, v in outputs.items (): print ("    . {}: {}".format (k, v.name))
        return version
    
    export = to_save_model
                
    def maybe_save_checkpoint (self, acc):
        if isinstance (acc, (tuple, list)):
            acc = acc [self.metric == "cost" and -1 or self.metric]
        if acc < self.accuracy_threshold:
            return
        
        save = False
        if self.metric == 'cost' and self.overfitwatch.is_renewaled ():
            save = True
            
        if acc > self.max_acc:
            self.max_acc = acc
            if self.metric != "cost":
                save = True
         
        if save:
            self.is_improved = True
            self.auto_save and self.train_dir and self.save ()    
            
    # make trainable ----------------------------------------------------------
    def network_created (self):
        pass
    
    def get_regularization_losses (self, scopes = [None]):
        if not isinstance (scopes, (tuple, list)):
            scopes = [scopes]
        losses = 0.0
        for scope in scopes:
            losses += tf.losses.get_regularization_loss (scope)
        return losses    
                
    def trainable (
            self, initial_learning_rate=0.001, decay_step=100, decay_rate=0.99, 
            overfit_threshold = 40, accuracy_threshold = 0.0, improve_metric = "cost"
        ):
        if not (improve_metric == "cost" or improve_metric.startswith ("accuracy")): 
            raise ValueError ("improve_metric should be one of cost|accuracy[:index]")
        if self.labels and self.label_file:
            self.save_labels ()
        if not self.summaries_dir:
            self.set_tensorboard_dir ("/var/tmp/tflog", True)
        self.create_network ()
        self.in_service = False
        self.overfitwatch = overfit.Overfit (overfit_threshold)
        self.accuracy_threshold = accuracy_threshold
        self.initial_learning_rate = initial_learning_rate
        self.decay_step = decay_step
        self.decay_rate = decay_rate
        self.metric = improve_metric
        if self.metric.startswith ("accuracy"):
            try: 
                self.metric = int (self.metric [9:])
            except ValueError:
                self.metric = -1
        self.network_created ()

        with self.graph.as_default ():
            self.global_step = tf.Variable (0, trainable=False)
            self.ema = tf.train.ExponentialMovingAverage(0.99, self.global_step)
            self.learning_rate = tf.train.exponential_decay (
                self.initial_learning_rate, 
                self.global_step, 
                self.decay_step, 
                self.decay_rate, 
                staircase = True
            )   
            self.log ("opt/default/learning-rate", self.learning_rate)
            cost = self.make_cost ()
            if isinstance (cost, tuple):
                cost, reg_cost, _ = cost
            else:
                reg_cost = tf.add (cost, self.get_regularization_losses())
            self.cost = reg_cost
            self.log ("opt/default/cost", cost)
            self.log ("opt/default/cost/regularized", reg_cost)
            
            self.update_ops = tf.get_collection (tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies (self.update_ops):                
                self.optimize_op = self.make_optimizer ()
                if self.__optimzables:
                    for var in tf.trainable_variables ():
                        if var not in self.__optimzables:
                            raise AssertionError ("{} will be not optimizing".format (var.name))
            
            try:
                self.accuracy = self.calculate_accuracy ()
            except TypeError:
                # custom
                self.accuracy = tf.constant (0.0)
                     
            self.summary_op = tf.summary.merge_all ()                    
            self.init_session ()
        
        if self.summaries_dir:
            self.make_writers ("net")        
    
    def count_kernels (self, scopes = []):
        if not isinstance (scopes, (tuple, list)):
            scopes = [scopes]
            
        total_parameters = 0
        with self.graph.as_default ():
            for variable in tf.trainable_variables ():
                valid = True
                if scopes:
                    valid = False                    
                    for scope in scopes:
                        if variable.name.startswith (scope):
                            valid = True
                            break                    
                #if variable.name.find ("/kernel") == -1:
                #    valid = False                
                if not valid:
                    continue            
                shape = variable.get_shape()
                print ("  - kernel shape:", variable.name, shape)                
                variable_parameters = 1                
                for dim in shape [:-1]:
                    variable_parameters *= dim.value                
                total_parameters += variable_parameters
        return total_parameters
        
    def evaluate (self, x, y, is_training, ops, *args, **kargs):
        logits = []
        costs = []
        accs = []
        opsres = []
        ops = [self.logit, self.cost, self.accuracy] + ops
                
        for i in range (0, len (x), self.batch_size):
            x_ = x [i:i + self.batch_size]
            y_ = y [i:i + self.batch_size]            
            results =  self.run (*ops, x = x_, y = y_, dropout_rate = 0.0, is_training = is_training, **kargs)
            logits.append (results [0])
            costs.append (results [1])                
            accs.append (results [2])                
            opsres.append (results [3:])
            
        r = result.Result (
            x, y, is_training,            
            np.concatenate(logits, 0),            
            np.mean (costs), 
            np.mean (accs),
            self.epoch,
            self.custom_accuracy,
            self.write_summary,
            self.train_dir,
            self.labels,
            np.concatenate(opsres, 0),
        )
        self.overfitwatch.add_cost (r.cost, self.is_validating)
        return r
        
    def fit (self, x, y, ops = None, **kargs):
        self.is_improved = False
        self.batch_size = x.shape [0]
        _ops = []
        if isinstance (self.optimize_op, (tuple, list)):
            for op in self.optimize_op:
                _ops.append (op)
        else:
            _ops.append (self.optimize_op)
        
        if self.summary_op is not None:
            _ops.append (self.summary_op)
        _ops.append (self.logit)
        _ops.append (self.cost)
        _ops.append (self.learning_rate)
        
        trailers = 0
        if ops:
            for op in ops:
                _ops.append (op)
            trailers = len (ops)    
        
        r = self.run (*tuple (_ops), x = x, y = y, is_training = True, **kargs)
        
        if trailers:
            logit, cost, lr = r [:-trailers][-3:]
        else:
            logit, cost, lr = r [-3:]
        global_step = self.eval (self.global_step)
        if self.summary_op is not None:
            self.writers ["net"].add_summary (r [-(trailers + 4)], global_step)
        
        return result.Result (
            x, y, True,            
            logit,            
            cost, 
            0.0,
            self.epoch,
            self.custom_accuracy,
            self.write_summary,
            self.train_dir,
            self.labels,
            trailers and r [-trailers:] or None
        )
            
    def recall (self, x, y, ops = [], **kargs):
        self.is_validating = False
        r = self.evaluate (x, y, True, ops, **kargs)
        return r
    train = recall
    
    def valid (self, x, y, ops = [], **kargs):
        self.is_validating = True        
        r = self.evaluate (x, y, False, ops, **kargs)
        if r.accuracy:
            self.maybe_save_checkpoint (r.accuracy)            
        return r    
    
    def trainrun (self, *ops, **kargs):
        self.is_validating = False
        return self.run (*ops, is_training = True, **kargs)
    
    def testrun (self, *ops, **kargs):
        self.is_validating = True
        return self.run (*ops, is_training = False, **kargs)
    
    def run (self, *ops, **kargs):  
        if "y" in kargs:
            if "x" in kargs:
                kargs ["y"], kargs ["x"] = self.filter (kargs ["y"], kargs ["x"])            
            kargs ["n_sample"] = kargs ["y"].shape [0]
        elif "x" in kargs:
            kargs ["n_sample"] = kargs ["x"].shape [0]
        
        if self.norm_factor and self.in_service and "x" in kargs:
            kargs ["x"] = self.normalize (kargs ["x"])
            
        feed_dict = {}
        for k, v in kargs.items ():
            feed_dict [getattr (self, k)] = v

        result = self.sess.run (ops, feed_dict = feed_dict)
        return result
        
    #---------------------------------------------------------------            
    def custom_accuracy (self, logit, y, *args, **karg):
        acc = self.calculate_accuracy (logit, self.filter (y), *args, **karg)
        if self.is_validating:
            self.maybe_save_checkpoint (acc)            
        return acc
    
    # layering -------------------------------------------------------------------
    def dropout (self, layer, dropout = True, activation = None):
        if activation is not None:
           layer = activation (layer)
        if self.in_service or not dropout:
            return layer
        dr = tf.where (tf.less (self.dropout_rate, 0.0), self.random_dropout_rate, self.dropout_rate)
        return tf.layers.dropout (inputs=layer, rate = dr, training = self.is_training)
        
    def lstm_with_dropout (self, n_input, hidden_size, lstm_layers = 1, activation = None, dynamic = True, basic = True):
        return self.lstm (n_input, hidden_size, lstm_layers, activation, dynamic, basic = basic, dropout = True)
        
    def lstm (self, n_input, hidden_size, lstm_layers = 1, activation = None, dynamic = True, dropout = False, basic = True, kreg = None):
        try:
            rnn = tf.nn.rnn_cell
            type_rnn = dynamic and tf.nn.dynamic_rnn or tf.nn.static_rnn                    
        except AttributeError:
            rnn = tf.contrib.rnn
            type_rnn = dynamic and rnn.dynamic_rnn or rnn.static_rnn
        
        cells = []
        cell_class = basic and rnn.BasicLSTMCell or tf.contrib.rnn.LSTMCell
        for i in range (lstm_layers):
            lstm = cell_class (hidden_size, activation = activation)
            if dropout:
                lstm = rnn.DropoutWrapper (lstm, output_keep_prob = 1.0 - self.dropout_rate)
            cells.append (lstm)
            
        cell = rnn.MultiRNNCell (cells)
        initial_state = cell.zero_state (self.n_sample, tf.float32)
        
        # transform time major form      
        shape = len (n_input.get_shape())
        lstm_in = tf.transpose (n_input, [1, 0] + list (range (max (2, shape - 2), shape)))
        if dynamic:            
            output, final_state = type_rnn (cell, lstm_in, time_major = True, dtype = tf.float32)
        else:
            seq_len = shape [1]
            n_channel = len (shape) >= 3 and shape [2] or 0
            if n_channel:
                lstm_in = tf.reshape (lstm_in, [-1, n_channel])
            lstm_in = tf.layers.dense (lstm_in, hidden_size)
            lstm_in = tf.split (lstm_in, seq_len, 0)
            output, final_state = type_rnn (cell, lstm_in, dtype = tf.float32, initial_state = initial_state)
                
        return output
    
    def full_connect (self, tensor):
        n_output = 1
        for d in tensor.get_shape ()[1:]:
            n_output *= int (d)
        return tf.reshape (tensor, [-1, n_output])
    
    def sequencial_connect (self, tensor, seq_len, n_output):
        # outputs is rnn outputs
        fc = self.full_connect (tensor)
        outputs = tf.layers.dense (fc, n_output, activation = None)
        return tf.reshape (outputs, [self.n_sample, seq_len, n_output])
    
    def batch_norm (self, n_input, activation = None, momentum = 0.99, center = True, scale = True):
        layer = tf.layers.batch_normalization (n_input, momentum = momentum, training = self.is_training, center = center, scale = scale)
        if activation is not None:
           return activation (layer)
        return layer
        
    def batch_norm_with_dropout (self, n_input, activation = None, momentum = 0.99, center = True, scale = True):
       layer = self.batch_norm (n_input, activation, momentum, center = center, scale = scale)
       return self.dropout (layer) 
   
    def dense (self, n_input, n_output, activation = None, kreg = None):
        return tf.layers.dense (inputs = n_input, units = n_output, activation = activation, kernel_regularizer = kreg)
    
    def merge (self, *layers):
        return tf.keras.layers.Add ()(list (layers))
        
    def zero_pad1d (self, input, padding = 1):
        return tf.keras.layers.ZeroPadding1D (padding = padding) (input)
    
    def zero_pad2d (self, input, padding = (1, 1)):
        return tf.keras.layers.ZeroPadding2D (padding = padding) (input)
    
    def zero_pad3d (self, input, padding = (1, 1, 1)):
        return tf.keras.layers.ZeroPadding3D (padding = padding) (input)
        
    def conv1d (self, n_input, filters, kernel = 2, strides = 1, activation = None,  padding = "same", kreg = None):
        return tf.layers.conv1d (inputs = n_input, filters = filters, kernel_size = kernel, strides = strides, padding = padding, activation = activation, kernel_regularizer = kreg)
    
    def separable_conv1d (self, n_input, filters, kernel = 2, strides = 1, activation = None,  padding = "same", kreg = None):
        return tf.keras.layers.SeparableConv1D (filters, kernel, strides, activation = activation,  padding = padding, kernel_regularizer = kreg) (n_input)
    
    def max_pool1d (self, n_input, pool = 2, strides = 2, padding = "same"):
        return tf.layers.max_pooling1d (inputs = n_input, pool_size = pool, strides = strides, padding = padding)
    
    def avg_pool1d (self, n_input, pool = 2, strides = 2, padding = "same"):
        return tf.layers.average_pooling1d (inputs = n_input, pool_size = pool, strides = strides, padding = padding)
        
    def upsample1d (self, input, size = 2):
        return tf.keras.layers.UpSampling1D (size = size) (input)
    
    def conv2d (self, n_input, filters, kernel = (2, 2), strides = (1,1), activation = None, padding = "same", kreg = None):
        return tf.layers.conv2d (inputs = n_input, filters = filters, kernel_size = kernel, strides = strides, padding = padding, activation = activation, kernel_regularizer = kreg)
    
    def separable_conv2d (self, n_input, filters, kernel = (2, 2), strides = (1,1), activation = None, padding = "same", kreg = None):
        return tf.keras.layers.SeparableConv2D (filters, kernel, strides, activation = activation,  padding = padding, kernel_regularizer = kreg) (n_input)
        
    def max_pool2d (self, n_input, pool = (2, 2), strides = (2, 2), padding = "same"):
        return tf.layers.max_pooling2d (inputs = n_input, pool_size = pool, strides = strides, padding = padding)
    
    def avg_pool2d (self, n_input, pool = (2, 2), strides = (2, 2), padding = "same"):
        return tf.layers.average_pooling2d (inputs = n_input, pool_size = pool, strides = strides, padding = padding)
    
    def upsample2d (self, input, size = (2, 2)):
        return tf.keras.layers.UpSampling2D (size = size) (input)
        
    def conv3d (self, n_input, filters, kernel = (2, 2, 2), strides = (1, 1, 1), activation = None, padding = "same", kreg = None):
        return tf.layers.conv3d (inputs = n_input, filters = filters, kernel_size = kernel, strides = strides, padding = padding, activation = activation, kernel_regularizer = kreg)
    
    def max_pool3d (self, n_input, pool = (2, 2, 2), strides = (2, 2, 2), padding = "same"):
        return tf.layers.max_pooling3d (inputs = n_input, pool_size = pool, strides = strides, padding = padding)
    
    def avg_pool3d (self, n_input, pool = (2, 2, 2), strides = (2, 2, 2), padding = "same"):
        return tf.layers.average_pooling3d (inputs = n_input, pool_size = pool, strides = strides, padding = padding)
    
    def upsample3d (self, input, size = (2, 2, 2)):
        return tf.keras.layers.UpSampling3D (size = size) (input)
    
    def global_avg_pool1d(self, input):
        return tf.keras.layers.GlobalAveragePooling1D ()(input)
    
    def global_avg_pool2d(self, input):
        return tf.keras.layers.GlobalAveragePooling2D ()(input)
    
    def global_avg_pool3d(self, input):
        return tf.keras.layers.GlobalAveragePooling3D ()(input)
    
    def global_max_pool1d(self, input):
        return tf.keras.layers.GlobalMaxPooling1D ()(input)
    
    def global_max_pool2d(self, input):
        return tf.keras.layers.GlobalMaxPooling2D ()(input)
    
    def global_max_pool3d(self, input):
        return tf.keras.layers.GlobalMaxPooling3D ()(input)
    
    def bernoulli_decode (self, input, n_output):
        y = self.dense (input, n_output, activation = tf.sigmoid)
        return tf.clip_by_value (y, 1e-8, 1 - 1e-8)
        
    def gaussian_encode (self, input, n_output):
        # https://github.com/hwalsuklee/tensorflow-mnist-VAE/blob/master/vae.py
        gaussian_params = self.dense (input, n_output * 2)
        mean = gaussian_params[:, :n_output]
        stddev = 1e-6 + tf.nn.softplus(gaussian_params[:, n_output:])
        y = mean + stddev * tf.random_normal (tf.shape (mean), 0, 1, dtype=tf.float32)
        return y, mean, stddev
        
    def embeddings (self, n_input, dim, expand_dim = False, kreg = None):
        W = tf.get_variable (
            "embedding",
            initailizer = tf.random_uniform (dim, -1.0, 1.0),
            regularizer = kreg
        )
        embeddings = tf.nn.embedding_lookup (W, n_input)
        if expand_dim:
            # for 2d CNN
            return tf.expand_dims (embeddings, -1)
        return embeddings

    # helpers ------------------------------------------------------------------
    def l1 (self, scale):        
        return tf.contrib.layers.l1_regularizer (scale)
    
    def l2 (self, scale):        
        return tf.contrib.layers.l2_regularizer (scale)
    
    def swish (self, a):
        return tf.nn.sigmoid (a) * a
    
    def tanh (self, a):
        # tf.nn.tanh is not working for quantizing
        return 2 * tf.nn.sigmoid (2 * a) - 1
    
    def scoped_cost (self, cost, scopes = None):
        if scopes:
            if not isinstance (scopes, (list, tuple)):
                scopes = [scopes]            
            t_vars = tf.trainable_variables ()
            collected = set ()
            for var in t_vars:                
                for name_ in scopes:
                    if name_ in var.name:
                        collected.add (var)
                        self.__optimzables.add (var)
                        break
        reg_cost = tf.add (cost, self.get_regularization_losses (scopes))
        return cost, reg_cost, list (collected)
            
    def optimizer (self, name = 'adam', cost = None, learning_rate = None, var_names = [], **karg):
        if isinstance (cost, tuple):
            cost, reg_cost, var_list = cost
            karg ["var_list"] = var_list            
        if cost is None:
            reg_cost = self.cost       
        if learning_rate is None:
            learning_rate = self.learning_rate
        return getattr (optimizers, name) (reg_cost, learning_rate, self.global_step, **karg)
        
    # override theses ----------------------------------------------------------            
    def make_place_holders (self):
        pass
    
    def make_variables (self):
        pass
    
    def make_optimizer (self):
        return self.optimizer ("adam")
    
    def make_logit (self):
        raise NotImplemented
        #return self.dense (self.x, 1)
   
    def make_cost (self):
        raise NotImplemented
        #return tf.constant (0.0)
     
    def calculate_accuracy (self):
        raise NotImplemented
    