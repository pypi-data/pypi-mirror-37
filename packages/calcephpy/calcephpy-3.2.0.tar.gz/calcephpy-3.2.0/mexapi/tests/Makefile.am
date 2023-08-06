#/*-----------------------------------------------------------------*/
#/*! 
#  \file Makefile.am
#  \brief Makefile for automake
#  \author  M. Gastineau 
#           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 
#
#   Copyright, 2018, CNRS
#   email of the author : Mickael.Gastineau@obspm.fr
#  
#*/
#/*-----------------------------------------------------------------*/
#
#/*-----------------------------------------------------------------*/
#/* License  of this file :
#  This file is "triple-licensed", you have to choose one  of the three licenses 
#  below to apply on this file.
#  
#     CeCILL-C
#     	The CeCILL-C license is close to the GNU LGPL.
#     	( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
#  
#  or CeCILL-B
#        The CeCILL-B license is close to the BSD.
#        (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
#  
#  or CeCILL v2.1
#       The CeCILL license is compatible with the GNU GPL.
#       ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
#  
# 
# This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under 
# French law and abiding by the rules of distribution of free software.  
# You can  use, modify and/ or redistribute the software under the terms 
# of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA  
# at the following URL "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its terms.
# */
# /*-----------------------------------------------------------------*/

## Makefile.am -- Process this file with automake to produce Makefile.in

if COND_MEX_OCTAVE
   MAYBE_MEXAPI = testoctave.m 
else
   MAYBE_MEXAPI = 
endif

TESTS = $(MAYBE_MEXAPI)

FILESTESTS =                   mgetconstant.m                  testmatlab.m \
              mgetconstantindex.m             \
getorientrecordindex.m          morientunitfail.m               tgetversionstr.m \
getpositionrecordindex.m        myerrorhandler.m                topen1.m \
mcheck.m                        myerrorhandlerhide.m            topen2.m \
mcomputeorder01.m                            topen3.m \
mcomputeorder23.m                                   topenfail.m \
mcomputeunit.m                  rotangmomorder0.m               ttimescale.m \
mcomputeunitfail.m              rotangmomunit.m                 ttimespan.m \
mcomputeunitnaifid.m            terror.m                        mcomputearray.m \
mcomputeunitarray.m             mcomputeorderarray.m            morientunitarray.m \
morientorderarray.m             mrotangmomunitarray.m           mrotangmomorder0array.m \
mgetconstantvd.m               mgetconstantvs.m
                 
AM_TESTS_ENVIRONMENT = DYLD_LIBRARY_PATH=:'$(abs_top_builddir)'/src/.libs:$(DYLD_LIBRARY_PATH) LD_LIBRARY_PATH=:'$(abs_top_builddir)'/src/.libs:$(LD_LIBRARY_PATH)

TEST_EXTENSIONS = .m
M_LOG_COMPILER = octave
AM_M_LOG_FLAGS =  -W

EXTRA_DIST= $(TESTS)  openfiles.m  myerrorhandler.m  myerrorhandlerhide.m \
   buildtestmatlab.sh testmatlab.m  testoctave.m $(FILESTESTS) # Makefile.mingw

testmatlab.m : testoctave.m
	./buildtestmatlab.sh

