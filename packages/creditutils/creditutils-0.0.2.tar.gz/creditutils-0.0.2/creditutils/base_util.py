# -*- coding:UTF-8 -*- # 标识为


'''
Created on 2013-7-4

@author: caifenghua
'''

import os
import inspect


# 不能对'self.variable'进行解析，因为self不确定
def is_defined(var_name):
    try:
        type(eval(var_name))
    except:
        return False
    else:
        return True


def func_flag():
    pass


# 将 python 打包成可执行文件时，不能使用 __file__ 或 __line__ 来标识文件名和行号，下面提供了一种解决方案
def module_path(local_function):
    ''' returns the module path without the use of __file__.  Requires a function defined 
       locally in the module.
       from http://stackoverflow.com/questions/729583/getting-file-path-of-imported-module'''
    return os.path.abspath(inspect.getsourcefile(local_function))


global __modpath__
__modpath__ = module_path(func_flag)


# 该部分代码用于作参考，直接调用不会显示被调用的文件名和行号，应该将整体代码拷贝到相应的文件中使用
def get_file_line():
    return (__modpath__, inspect.currentframe().f_back.f_lineno)


if __name__ == '__main__':
    print(is_defined('one'))
    two = None
    print(is_defined('two'))

    from . import str_enc_dec_util as enc_dec

    enc = enc_dec.StrEncDec()
    print(is_defined('enc.one'))
    print(is_defined('enc.CHAR_COUNT'))
