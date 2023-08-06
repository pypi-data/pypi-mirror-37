It is designed to work with Matlab or Octave software. 

With Octave, you should load this package :

.. code-block::  matlab
   
        pkg load calcephoct
        
If you want Octave to automatically load this package, simply add to the file *octaverc* the command **pkg load calcephoct** .


With Matlab, you should add the path to the Matlab files of the dynamic library |LIBRARYSHORTNAME| :

.. code-block::  matlab
    
        addpath('<prefix>/libexec/calceph/mex/')
        
By default, this prefix is */usr/local*, so you have to enter before using calceph library.        
        
.. code-block::  matlab
    
        addpath('/usr/local/libexec/calceph/mex/')


If you want Matlab to automatically add this path at startup, simply add to this path to the environment variable *MATLABPATH*.



.. If you receive a message message similar to ``error: ... : .../libexec/calceph/mex/interfacemex.mex: failed to load: libcalceph.so.1: cannot open shared object file: No such file or directory``, the path to the library is missing in the environment variable *LD_LIBRARY_PATH* or  *DYLD_LIBRARY_PATH* and you should add to it.

Relative to C or Fortran interface, the prefixes  *calceph_*, *CALCEPH_*, *NAIFID_* are deleted for the naming convention of the functions, constants and NAIF identification numbers.  
