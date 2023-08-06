# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals, absolute_import

import sys
import os
import math
import numpy

_basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_basedir)
from mesh import Mesh
sys.path.pop()

# add shortcut

class MLP(Mesh):
    def __init__(self,
                 mi=0,
                 dtype='float64',
                 activation=[],
                 layer_size=[],
                 input_type='pointwise',
                 loss_type='mse',
                 output_range=[0, 1],
                 output_shrink=0.001,  # 0.1
                 importance_mul=0.001,
                 leaky=-0.001,
                 dropout=0,
                 bias_rate=[0.005], weight_rate=[],
                 regularization=1):

        self.init(mi, dtype=dtype)
        self.input_type = input_type
        self.loss_type = loss_type
        self.layer_size = layer_size

        self.rate = None
        self.loss = None

        self.set_conf({})
        for idx, size in enumerate(layer_size):
            arg = {'Shape': [1, 1, size]}
            if idx == 0:
                arg['InputType'] = input_type
                arg['ImportanceMul'] = importance_mul
            if idx == len(layer_size) - 1:
                arg['Regularization'] = regularization
                arg['LossType'] = loss_type
                arg['OutputRange'] = output_range
                arg['OutputShrink'] = output_shrink

            self.set_tensor(idx, arg)

        for idx in range(len(layer_size) - 1):
            arg = {'Tin': idx, 'Tout': idx+1, 'Op': 'fc'}
            
            kv = {
                'BiasRate': bias_rate,
                'Dropout': dropout,
                'Leaky': leaky,
                'WeightRate': weight_rate,
                'Activation': activation,
            } 

            for k in kv:
                if not isinstance(kv[k], (list, tuple)):
                    if kv[k] is not None: 
                        arg[k] = kv[k]
                elif idx < len(kv[k]) and kv[k][idx] is not None:
                    arg[k] = kv[k][idx]

            self.set_filter(idx, arg)

        self.run_filler()

    def check_arr(self, arr):
        if self.layer_size is None or self.layer_size == []:
            self.layer_size = [0] * len(self.tensors.keys())
            for key in self.tensors:
                self.layer_size[key] = self.tensors[key]['Shape'][2]  
                
        if not isinstance(arr, numpy.ndarray):
            raise NotImplementedError()
        if len(arr.shape) == 1:
            arr = arr.reshape((-1, 1))
        if arr.dtype != self.DTYPE:
            arr = arr.astype(self.DTYPE)
        if not arr.flags['C_CONTIGUOUS']:
            arr = numpy.ascontiguousarray(arr)
        if len(arr.shape) != 2:
            raise NotImplementedError()
        return arr

    def train(self, in_arr, target_arr,
              epoch_train=5, epoch_decay=1, iteration_log=100,
              rate_init=0.06, rate_decay=0.9,
              importance_out=False,
              loss_mul=0.001, verbose=1, shuffle=True):

        self.set_conf({'IsTrain':True})

        in_arr = self.check_arr(in_arr)
        target_arr = self.check_arr(target_arr)

        SIZE = len(in_arr)
        if SIZE != len(target_arr):
            raise NotImplementedError()

        pos = numpy.arange(SIZE, dtype=numpy.int32)
        self.rate = rate_init

        for epoch in range(epoch_train):
            if epoch > 0 and epoch % epoch_decay == 0:
                self.rate *= rate_decay

            if shuffle:
                self.shuffle(pos)
            for idx in range(SIZE):
                idx_ = pos[idx]
                loss_ = self.train_one(
                    in_arr[idx_], target_arr[idx_], self.rate, importance_out)
                if self.loss is None:
                    self.loss = loss_
                else:
                    self.loss += (loss_ - self.loss) * loss_mul

                if verbose > 1:
                    if (idx + 1) % iteration_log == 0:
                        print("Iteration %d/%d Epoch %d/%d\n    rate: %g loss: %g" %
                              (idx+1, SIZE, epoch, epoch_train, self.rate, self.loss))
                        sys.stdout.flush()
                        if math.isnan(self.loss):
                            raise ValueError("loss is nan")

            if verbose > 0:
                print("Epoch %d/%d\n    rate: %g loss: %g" %
                      (epoch+1, epoch_train, self.rate, self.loss))
                sys.stdout.flush()
                if math.isnan(self.loss):
                    raise ValueError("loss is nan")

        if importance_out:
            importance_buf = numpy.zeros((self.layer_size[0],), dtype=self.DTYPE)
            self.read_tensor(0, importance_buf, self.FLAG_EX)
            return importance_buf

    def predict(self, in_arr, out_arr=None, verbose=0, iteration_log=100):
        self.set_conf({'IsTrain':False})
        
        if out_arr is None:
            out_arr = numpy.zeros(
                (len(in_arr), self.layer_size[-1]), dtype=self.DTYPE)

        in_arr = self.check_arr(in_arr)
        out_arr = self.check_arr(out_arr)

        SIZE = len(in_arr)
        if SIZE != len(out_arr):
            raise NotImplementedError()

        for idx in range(SIZE):
            self.predict_one(in_arr[idx], out_arr[idx])

            if verbose > 1:
                if (idx + 1) % iteration_log == 0:
                    print("Iteration %d/%d" % (idx+1, SIZE))

        return out_arr

    def train_one(self, in_buf, target_buf, rate, importance_out):
        self.clear_tensor(-1, self.FLAG_V | self.FLAG_DV)
        self.clear_filter(-1, self.FLAG_DV)
        self.input(0, in_buf)

        self.forward()

        loss = self.cal_loss(len(self.layer_size) - 1, target_buf)

        # if loss_range[1] is not None and loss > loss_range[1]:
        #     return loss
        # if loss_range[0] is not None and loss < loss_range[0]:
        #     return loss

        self.backward()
        self.renew(rate)

        if importance_out:
            self.importance(0)

        return loss

    def predict_one(self, in_buf, out_buf):
        self.clear_tensor(-1, self.FLAG_V)
        self.input(0, in_buf)
        self.forward()

        flag = self.FLAG_V
        if self.loss_type in ["softmax", "hardmax"]:
            flag = self.FLAG_EX

        self.read_tensor(len(self.layer_size) - 1, out_buf, flag)


if __name__ == '__main__':
    m = MLP(layer_size=[2, 1])
    m = MLP(mi=1, layer_size=[2, 1])
    print("appname:", m.info("appname"))

    m.set_tensor(1,
        {'Regularization':    0.1})

    m.show_conf()
    m.show_tensor()
    m.show_filter()
    m.destroy()
