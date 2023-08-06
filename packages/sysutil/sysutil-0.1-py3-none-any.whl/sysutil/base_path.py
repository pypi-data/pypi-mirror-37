import sys
import os
import inspect
import pathlib
def get_base_path():
    file_path = os.getcwd()
    path_arr = file_path.split('/')
    base_path = '/'
    for path in path_arr:
        if path != '':
           base_path += "{}/".format(path)
           file = pathlib.Path(base_path+"/constants.py")
           if file.exists():
              return base_path
    return 
