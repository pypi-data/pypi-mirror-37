Library interface
*****************

A simple example program
========================
    
The following example program shows the typical usage of the |API| interface.

Other examples using the |API| interface can be found in the directory *examples* of the library sources. 

.. include:: examples/simple_program.rst

.. _calcephpy:


|menu_Headers_and_Libraries|
============================

.. ifconfig:: calcephapi in ('C')

    .. include :: calceph.interface.cusage.rst


.. ifconfig:: calcephapi in ('F2003')

    .. include :: calceph.interface.f2003usage.rst

.. ifconfig:: calcephapi in ('F90')

    .. include :: calceph.interface.f9xusage.rst

.. ifconfig:: calcephapi in ('Python')

    .. include :: calceph.interface.pythonusage.rst

.. ifconfig:: calcephapi in ('Mex')

    .. include :: calceph.interface.mexusage.rst


.. %----------------------------------------------------------------------------


.. _`NaifId`:

Types
=====


.. ifconfig:: calcephapi in ('C')

    .. c:type:: t_calcephbin

    This type contains all information to access an ephemeris file.

    .. c:type:: t_calceph_charvalue

    This type is a array of characters to store the value of the constants as a string.

.. ifconfig:: calcephapi in ('Python')

    .. py:attribute:: calcephpy.CalcephBin

    This type contains all information to access an ephemeris file.

    .. py:attribute::  calcephpy.NaifId

    This type contains the NAIF identification numbers.

    .. py:attribute::  calcephpy.Constants

    This type contains all constants defined in the library, except the NAIF identification numbers.

.. ifconfig:: calcephapi in ('Mex')

    .. mat:class:: CalcephBin

    This type contains all information to access an ephemeris file.

    .. mat:class::  NaifId

    This type contains the NAIF identification numbers.

    .. mat:class::  Constants

    This type contains all constants defined in the library, except the NAIF identification numbers.

.. %----------------------------------------------------------------------------

.. _`Constants`:

Constants
=========

.. ifconfig:: calcephapi in ('F2003')

    The following constants are defined in the module :file:`calceph.mod`.
    
.. ifconfig:: calcephapi in ('F90')

    The following constants are defined in the file :file:`f90calceph.h`.

.. ifconfig:: calcephapi in ('Python')

    The following constants are defined in the class **Constants** (or *calcephpy.Constants*).

.. ifconfig:: calcephapi in ('Mex')

    The following constants are defined in the class **Constants**.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_MAX_CONSTANTNAME

    This integer defines the maximum number of characters, including the trailing '\\0',  that the name of a constant, available from the ephemeris file, could contain.

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_MAX_CONSTANTNAME
        :type: integer

    This integer defines the maximum number of characters, including the trailing '\\0',  that the name of a constant, available from the ephemeris file, could contain.

.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_MAX_CONSTANTVALUE

    This integer defines the maximum number of characters, including the trailing '\\0',  that the value of a constant, available from the ephemeris file, could contain if the value is stored as a string of characters.

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_MAX_CONSTANTVALUE
        :type: integer

    This integer defines the maximum number of characters, including the trailing '\\0',  that the value of a constant, available from the ephemeris file, could contain if the value is stored as a string of characters.

.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_VERSION_MAJOR

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_VERSION_MAJOR
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: VERSION_MAJOR
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: VERSION_MAJOR
    
This integer constant defines the major revision of this library. It can be used to distinguish different releases of this library.

.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_VERSION_MINOR

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_VERSION_MINOR
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: VERSION_MINOR
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: VERSION_MINOR

This integer constant defines the minor revision of this library. It can be used to distinguish different releases of this library.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_VERSION_PATCH


.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_VERSION_PATCH
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: VERSION_PATCH
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: VERSION_PATCH
    
This integer constant defines the patch level revision of this library. It can be used to distinguish different releases of this library.


.. ifconfig:: calcephapi in ('C')

    ::
    
        #if   (CALCEPH_VERSION_MAJOR>=2) 
          ||  (CALCEPH_VERSION_MAJOR>=3 && CALCEPH_VERSION_MINOR>=2)
        ...
        #endif

.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_VERSION_STRING

    This C null-terminated string constant is the version of the library, which can be compared to the result of calceph_getversion to check at run time if the header file and library used match:

    ::

        char version[CALCEPH_MAX_CONSTANTNAME];
        calceph_getversion_str(version);
        if (strcmp (version, CALCEPH_VERSION_STRING)!=0)
        fprintf (stderr, "Warning: header and library do not match\n");

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_VERSION_STRING
        :type: character(len=*)

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: VERSION_STRING
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: VERSION_STRING
    
.. ifconfig:: calcephapi in ('F2003', 'F90', 'Python', 'Mex')

    This string is the version of the library, which can be compared to the result of calceph_getversion to check at run time if the header file and library used match:

Note: Obtaining different strings is not necessarily an error, as in general, a program compiled with some old CALCEPH version can be dynamically linked with a newer CALCEPH library version (if allowed by the operating system).

.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_ASTEROID

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_ASTEROID
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: ASTEROID
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: ASTEROID
    
This integer defines the offset value for the asteroids that must be used as target or center for the computation functions, such as |calceph_compute|.


The following constants specify in which units are expressed the output of the computation functions, such as |calceph_compute_unit| :  

.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_UNIT_AU

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_UNIT_AU
        :type: integer

.. ifconfig:: calcephapi in ('Python')
    
    .. py:data:: UNIT_AU
    
.. ifconfig:: calcephapi in ('Mex')
    
    .. mat:attribute:: UNIT_AU
    
This integer defines that the unit of the positions and velocities is expressed in astronomical unit.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_UNIT_KM

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_UNIT_KM
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: UNIT_KM
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: UNIT_KM
    
This integer defines that the unit of the positions and velocities is expressed in kilometer.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_UNIT_DAY

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_UNIT_DAY
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: UNIT_DAY
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: UNIT_DAY
    
This integer defines that the unit of the velocities or the quantity TT-TDB or TCG-TCB is expressed in day (one day=86400 seconds).


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_UNIT_SEC

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_UNIT_SEC
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: UNIT_SEC
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: UNIT_SEC
    
This integer defines that the unit of the velocities or the quantity TT-TDB or TCG-TCB is expressed in second.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_UNIT_RAD

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_UNIT_RAD
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: UNIT_RAD
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: UNIT_RAD
    
This integer defines that the unit of the angles is expressed in radian.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_OUTPUT_EULERANGLES

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_OUTPUT_EULERANGLES
        :type: integer

.. ifconfig:: calcephapi in ('Python')
    
    .. py:data:: OUTPUT_EULERANGLES
    
.. ifconfig:: calcephapi in ('Mex')
    
    .. mat:attribute:: OUTPUT_EULERANGLES
    
This integer defines that the output array contains the euler angles.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_OUTPUT_NUTATIONANGLES

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_OUTPUT_NUTATIONANGLES
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: OUTPUT_NUTATIONANGLES
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: OUTPUT_NUTATIONANGLES

This integer defines that the output array contains the nutation angles.


.. ifconfig:: calcephapi in ('C')

    .. c:macro:: CALCEPH_USE_NAIFID

.. ifconfig:: calcephapi in ('F2003', 'F90')

    .. f:variable:: CALCEPH_USE_NAIFID
        :type: integer

.. ifconfig:: calcephapi in ('Python')

    .. py:data:: USE_NAIFID
    
.. ifconfig:: calcephapi in ('Mex')

    .. mat:attribute:: USE_NAIFID
    
This integer defines that the NAIF identification numbers are used as target or center for the computation functions, such as |calceph_compute_unit|.

