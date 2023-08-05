'''
:Date: 2018-10-06
:Version: 1.0.2
:Authors:
    * Mohammad Alghafli <thebsom@gmail.com>

Multiple configuration directories for your program.
This library is useful if you have the following situation: you have a config
directory where you store default configuration and another config directory
where you store user custom configuration. When a user runs your program for the
first time, no files exist in the user config directory and you want to read
everything from the default config directory. When you write a config file, it
must always be written in the user config directory.
This library does this for you. You specify user config directory and any more
directories you want to use for default config files. When you open a file for
reading, the library opens the file from the user config directory if it exists.
Otherwise, it searches for the file in the default config directories. When you
open a file for writing, it is always opened in the user config directory. A
typical usage example is below::
    
    from codi import *

    #assume we have 2 config directories:
    #   * default-cfg/
    #   * user-cfg/
    #
    #in other words, we have the following directory structure:
    #
    #
    #default-cfg/
    #|
    #--path/
    #  |
    #  --to/
    #    |
    #    |-file.txt
    #    |
    #    --file.bin
    #
    #
    #
    #user-cfg/


    #user config dir
    user_dir = 'user-cfg/'
    #default config dir
    default_dir = 'default-cfg/'

    #create a Codi object. you can give more than 2 dirs if you need.
    config_dirs = Codi(user_dir, default_dir)

    #read a file. args are same as builtin open
    #will first try to open `user-cfg/path/to/file.txt`. because the file does
    #not exist, will go to the next config dir and open
    #`default-cfg/path/to/file.txt`.
    f = config_dirs.open('path/to/file.txt')
    print(f.read())
    f.close()

    #write a file.
    #will always write in `user-cfg/path/to/file.txt`. any parent directories
    #that do not exist will be created
    f = config_dirs.open('path/to/file.txt', 'w')
    print('hello world', file=f)
    f.close()

    #convinience method to read data
    #text. default encoding is utf8
    #will open `user-cfg/path/to/file.txt` because it exists from our previous
    #write operation.
    print(config_dirs.read('path/to/file.txt', encoding='ascii'))
    #binary
    #will open `default-cfg/path/to/file.bin`
    print(config_dirs.read('path/to/file.bin', text=False))

    #convinience method to write data
    #text. default encoding is utf8
    #will always write in `user-cfg/path/to/file.txt`.
    config_dirs.write('path/to/file.txt', 'hello world', encoding='ascii')
    #binary
    #again, will always write in `user-cfg/path/to/file.bin`.
    config_dirs.write('path/to/file.bin', b'some binary data')
    
The library also provides `Config` class which acts as a dict for config values.
It adds the ability to set default values.
'''

import pathlib
import re

__version__ = re.search(
        ':Version: (?P<version>[0-9](\.[0-9])*)',
        __doc__
    ).group(1)

class Config(dict):
    '''
    Used to store config values. This class subclasses dict and adds the
    functionality of adding default values. Instead of raising a `KeyError` if
    the key is not in the dict, it looks for the key in an internal default
    values dict. If there is a default value for key, it adds it to itself and
    returns it. Otherwise, `KeyError` is raised.
    '''
    def __init__(self, *args, **kwargs):
        self._defaults = {}
        super().__init__(*args, **kwargs)
    
    def set_default(self, key, value):
        '''
        Sets default value of `key` to `value`.
        '''
        self._defaults[key] = value
    
    def pop_default(self, key):
        '''
        Removes and returns default value of `key`.
        '''
        return self._defaults.pop(key)
    
    def get_default(self, key):
        '''
        Returns the default value of `key`.
        '''
        return self._defaults[key]
    
    def __missing__(self, key):
        self[key] = self._defaults[key]
        return self[key]

class Codi:
    '''
    Class to set multiple directories for configuration files. The first config
    directory is the user config directory. The other config directories added
    are used as fallbacks when a file opened for reading is not found in the
    user config directory. If a path is opened for writing, it is always opened
    in the user config directory.
    '''
    def __init__(self, *dirs):
        '''
        args:
            * dirs (list of path-like objects): list of config directories.
        '''
        self.dirs = [pathlib.Path(c).resolve() for c in dirs]
        
    def append(self, dir):
        '''
        Append a config dir.
        
        args:
            * dir (any type accepted by `pathlib.Path` constructor):
                Directory to add.
        '''
        self.dirs.append(pathlib.Path(dir))
    
    def extend(self, dirs):
        '''
        Append new config dirs from iterable.
        
        args:
            * dirs (path-like object): iterable of directories to add.
        '''
        self.dirs.extend([pathlib.Path(c).resolve() for c in dirs])
    
    def insert(self, index, dir):
        '''
        Insert a config dir.
        
        args:
            * index (int): The index in which the new directory is added.
            * dir (path-like object): Directory to add.
        '''
        self.dirs.insert(index, pathlib.Path(dir).resolve())
    
    def pop(self, index=-1):
        '''
        Remove the config directory at index.
        
        args:
            * index (int): The index of the dir to be removed.
        '''
        self.dirs.pop(index)
    
    def remove(self, value):
        '''
        Remove a config directory.
        
        args:
            * value (path-like object): The directory to remove.
        '''
        self.dirs.remove(pathlib.Path(value).resolve())
    
    def __getitem__(self, idx):
        return self.dirs[idx]
    
    def __setitem__(self, idx, value):
        self.dirs[idx] = value
    
    def path(self, path='', writable=False):
        '''
        Return an absolute path as a pathlib.Path object for `path` in one of
        the config directories added to `self`.
        
        args:
            * path (path-like object): The relative path to return.
            * writable (bool): Whether the path is requested for writing or
                reading. If `False`, the function searches the config
                directories in the order they were added for an existing path.
                If `writable` is `True`, the returned path is in the first
                config dir added to `self` whether it exists or not.
        '''
        for c in self.dirs:
            p = c / path
            p = p.resolve()
            if (writable or p.exists()) and (p == c or c in p.parents):
                return p
        else:
            raise FileNotFoundError(
                    'no file named `{}` was found.'.format(path)
                )
    
    def glob(self, pattern):
        '''
        Same as `pathlib.Path.glob` but searches all config dirs added to
        `self` for glob results. If a file is found in multiple config dirs,
        only the path of the file found in the first config dir is returned. The
        returned paths are absolute.
        
        args:
            * pattern (str): Glob pattern.
        returns:
            The glob result as a `list` of `pathlib.Path` objects.
        '''
        out = set()
        for c in self.dirs:
            out.update([f.relative_to(c) for f in c.glob(pattern)])
        
        out = [self.path(c) for c in out]
        return out
    
    def open(self, file, mode='r', *args, **kwargs):
        '''
        Opens a file. This function is used in the same way as the builtin
        `open`. If `mode` contains w, x, a or +, the file is created in the
        first config dir and all directories in the path are created if they do 
        not exist.
        
        args:
            Same as builtin `open`.
        returns:
            File object.
        '''
        writable = bool(set('wxa+') & set(mode))
        p = self.path(file, writable)
        if writable:
            p.parent.mkdir(parents=True, exist_ok=True)
        f = p.open(mode, *args, **kwargs)
        return f
    
    def read(self, path, text=True, encoding='utf-8'):
        '''
        Returns the content of the file `path`.
        
        args:
            * path (path-like object): The path to read relative to the config 
                dirs added to `self`.
            * text (bool): If `True`, the file is read in text mode and str
                object is returned . If `False`, the file is read in binary mode
                and bytes object is returned.
            * encoding: Text encoding to open the file with. Ignored if `text`
                is `False`.
        returns:
            The content of the file as str or bytes object.
        '''
        if text:
            mode = 'rt'
            with self.open(path, mode, encoding=encoding) as f:
                return f.read()
        else:
            mode = 'rb'
            with self.open(path, mode) as f:
                return f.read()
    
    def write(self, path, data, encoding='utf-8'):
        '''
        Writes data to the file `path`.
        
        args:
            * path (path-like object): The path to write into
                relative to the config dirs added to `self`.
            * data (str or bytes): Data to write. If an str object, file is
                opened in text mode. If bytes object, file is opened in binary
                mode.
            * encoding: Text encoding to open the file with. Ignored if `data`
                is a bytes object.
            
        returns:
            None
        '''
        if type(data) is str:
            mode = 'wt'
            with self.open(path, mode, encoding=encoding) as f:
                f.write(data)
        elif type(data) is bytes:
            mode = 'wb'
            with self.open(path, mode) as f:
                f.write(data)
        else:
            raise ValueError('`data` must be of type str or bytes.')

