=================
codi Tutorial
=================

This tutorial gives an introduction to how to use codi python library and its
features.

This is not a python tutorial. You are expected to have general knowledge in
python before you start this tutorial.

-----------
The problem
-----------

Imagin your program needs to read some files at start up that change its
behaviour . For example, it reads a config file that contains an array of
values. Configuration files are usually stored in user files. However, when the
program runs for the first time, the configuration files do not exist and you
need to find fallback configuration files.

------------
The solution
------------

This library solves this problem. You specify the user configuration directory
and a fallback directory.

When you ask the library to read a file for you, the library tries to open the
file from the user configuration directory. If the file (or the whole directory)
is not found, the library looks for the file in the fallback directory. That
only happens when you try to open a file for reading.

On the other hand, when you try to write to a file, the library only writes in
the user configuration directory. It never writes to the fallback directory. You
do not need to create any subdirectories since the library will create all
subdirectories you need when you try to open a file for writing.

The library also gives you a `Config` class which is useful to store
configuration values as well as set default values for your configuration.

-------
Content
-------

.. toctree::
    :maxdepth: 2

    installation
    quick-guide
    reference
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

