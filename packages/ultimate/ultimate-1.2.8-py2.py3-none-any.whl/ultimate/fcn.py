# -*- coding: utf-8 -*-

# NOT IMPLEMENTED YET

from __future__ import print_function, division, unicode_literals, absolute_import

import sys, os 

import numpy
_basedir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(_basedir)
import mesh
sys.path.pop()

class FCN(mesh.Mesh):
    def __init__(self, 
            mi=0, layers={}):
       
        self.init(mi)
      
if __name__ == '__main__':
    fcn = FCN(
        layers = [
            {'Shape':[28,28,1]},
            {'Shape':[14,14,2], 'Op':'conv'},
        ],
    )


