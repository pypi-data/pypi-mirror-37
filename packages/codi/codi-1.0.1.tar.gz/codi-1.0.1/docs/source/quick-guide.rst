===========
Quick Guide
===========

-------------
Usage example
-------------

This is a typical usage example::
    
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

--------------------------
Config class usage example
--------------------------

This is a typical usage example for the `Config` class::
    
    import codi
    
    #Config objects are dictionary objects. you can pass the constructor
    #anything you pass to a dictionary.
    config = codi.Config()
    
    #set default values
    config.set_default('b', 2)
    config.set_default('c', 3)
    
    #set config values
    config['a'] = -1
    config['b'] = -2
    
    #print config values
    #will print -1 because we set its value previously
    print(config['a'])
    
    #will print -2 because we set its value. default is ignored.
    print(config['b'])
    
    #we did not set its value. will take the default value and print 3.
    print(config['c'])
    
    #no value and no default value. will raise KeyError
    print(config['d'])

----------------
Further readings
----------------
In :doc:`reference` you will find the library reference.

