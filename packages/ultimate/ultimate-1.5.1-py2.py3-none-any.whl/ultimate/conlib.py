# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals, absolute_import

import sys

def dumps(obj):
    if isinstance(obj, bool):
        if obj: return "true"
        return "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    # if isinstance(obj, str):
    if isinstance(obj, "".__class__):
        return "'" + obj.replace("'", "''") + "'"
    if obj is None:
        return "null"
    if isinstance(obj, (list, tuple)):
        s = "{"
        for i, ele in enumerate(obj):
            if i > 0: s += ","
            s += dumps(ele)
        s += "}"
        return s
    if isinstance(obj, dict):
        s = "{"
        for i, key in enumerate(obj.keys()):
            if i > 0: s += ","
            s += key + ":"
            s += dumps(obj[key])
        s += "}"
        return s
    return "null"

if __name__ == '__main__':
    print(dumps([{"x":[complex(1,2),1,True, 2,(3,4), None, [{"y":11}, 1e44]]},[1,2,3],"3'"]))