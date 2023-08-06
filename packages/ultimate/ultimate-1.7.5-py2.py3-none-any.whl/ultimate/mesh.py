# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals, absolute_import

import os, sys
import ctypes, platform
import numpy

_basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_basedir)
import conlib
sys.path.pop()

class Mesh(object):
    __version__ = 5

    FLAG_V = 1
    FLAG_DV = 2
    FLAG_EX = 4
    
    def __init__(self, mi=0, dtype="float64"):        
        self.init(mi, dtype=dtype)
        
    def init(self, mi, dtype):
        self._mi = mi
        self.tensors = {}
        self.filters = {}

        if dtype == numpy.float64 or dtype in ["float64", "double"]:
            self.DTYPE = numpy.float64
            self.C_FLOAT = ctypes.c_double

            if platform.system() == "Windows":
                self._libc = ctypes.cdll.LoadLibrary(os.path.join(_basedir, 'mesh.dll.2'))
            elif platform.system() == "Linux":
                self._libc = ctypes.cdll.LoadLibrary(os.path.join(_basedir, 'mesh.so.2'))
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()
            
        self._libc.mesh_cal_loss.restype = self.C_FLOAT
        self._libc.mesh_random.restype = self.C_FLOAT

        if isinstance(Mesh.__version__, int):
            Mesh.__version__ = self.info("version") + '.' + str(Mesh.__version__)
            print(self.info("appname"), Mesh.__version__)
            sys.stdout.flush()
            
    def save_para(self, filepath="para.bin"):
        ret = self._libc.mesh_save_para(self._mi, filepath.encode())
        if ret <= 0: raise ValueError()

    def load_para(self, filepath="para.bin"):
        ret = self._libc.mesh_load_para(self._mi, filepath.encode())
        if ret <= 0: raise ValueError()

    def set_conf(self, con={}):
        if not isinstance(con, dict): raise NotImplementedError()
        con = conlib.dumps(con).encode()

        self._libc.mesh_set_conf(self._mi, con)

    def show_conf(self):
        self._libc.mesh_show_conf(self._mi)
    
    def show_filter(self, fi=-1):
        self._libc.mesh_show_filter(self._mi, fi)

    def show_tensor(self, ti=-1):
        self._libc.mesh_show_tensor(self._mi, ti)

    def set_tensor(self, ti, con={}):
        if not isinstance(con, dict): raise NotImplementedError()
        if ti in self.tensors:
            self.tensors[ti].update(con)
        else: self.tensors[ti] = con
        con = conlib.dumps(con).encode()

        self._libc.mesh_set_tensor(self._mi, ti, con)

    def set_filter(self, fi, con={}):
        if not isinstance(con, dict): raise NotImplementedError()
        if fi in self.filters:
            self.filters[fi].update(con)
        else: self.filters[fi] = con
        con = conlib.dumps(con).encode()

        self._libc.mesh_set_filter(self._mi, fi, con)

    def clear_tensor(self, ti=-1, flag=FLAG_V | FLAG_DV):
        self._libc.mesh_clear_tensor(self._mi, ti, flag)

    def clear_filter(self, fi=-1, flag=FLAG_DV):
        self._libc.mesh_clear_filter(self._mi, fi, flag)

    def importance(self, ti=-1):
        self._libc.mesh_importance(self._mi, ti)

    def input(self, ti, buf):
        self._libc.mesh_input(self._mi, ti, numpy.ctypeslib.as_ctypes(buf))

    def cal_loss(self, ti, buf=None):
        return self._libc.mesh_cal_loss(self._mi, ti, numpy.ctypeslib.as_ctypes(buf))

    def read_tensor(self, ti, buf, flag):
        self._libc.mesh_read_tensor(self._mi, ti, numpy.ctypeslib.as_ctypes(buf), flag)

    def run_filler(self, fi=-1):
        self._libc.mesh_run_filler(self._mi, fi)

    def forward(self):
        self._libc.mesh_forward(self._mi)

    def backward(self):
        self._libc.mesh_backward(self._mi)

    def renew(self, rate):
        self._libc.mesh_renew(self._mi, self.C_FLOAT(rate))

    def destroy(self):
        self._libc.mesh_destroy(self._mi)

    def random(self):
        return self._libc.mesh_random()

    def shuffle(self, buf):
        if buf.dtype != numpy.int32:
            raise NotImplementedError()
        self._libc.mesh_shuffle(numpy.ctypeslib.as_ctypes(buf), buf.shape[0])

    def info(self, info_type=None, buf_size=1024):
        if not isinstance(info_type, "".__class__): 
            info_type = None
        else: info_type = info_type.encode() 
            
        str_buf = ctypes.create_string_buffer(buf_size)
        self._libc.mesh_info(info_type, str_buf)

        return str_buf.value.decode()
        
if __name__ == '__main__':
    pass



