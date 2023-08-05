:Date: 2018-10-06
:Version: 1.0.1
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

    --------
    Tutorial
    --------
    Check out codi tutorial at http://codi.readthedocs.io/
    
