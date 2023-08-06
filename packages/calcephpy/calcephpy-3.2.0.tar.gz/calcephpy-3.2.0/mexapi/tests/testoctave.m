addpath('../src/')
mkoctfile --mex -I../../src/ ../src/interfacemex.c -L../../src/.libs/ -lcalceph
%quiet normal or verbose
mode="verbose";
success =test("tgetversionstr",mode);
success &=test("topen1",mode);
success &=test("topen2",mode);
success &=test("topen3",mode);
success &=test("topenfail",mode);
success &=test("ttimescale",mode);
success &=test("ttimespan",mode);
success &=test("mcomputeunitfail",mode);
success &=test("mgetconstant",mode);
success &=test("mgetconstantvd",mode);
success &=test("mgetconstantvs",mode);
success &=test("mgetconstantindex",mode);
success &=test("morientunitfail",mode);
success &=test("mcheck",mode);
success &=test("mcomputeorder01",mode);
success &=test("mcomputeorder23",mode);
success &=test("mcomputeunit",mode);
success &=test("mcomputeunitnaifid",mode);
success &=test("getorientrecordindex",mode);
success &=test("getpositionrecordindex",mode);
success &=test("rotangmomorder0",mode);
success &=test("rotangmomorder0",mode);
success &=test("rotangmomunit",mode);
success &=test("mcomputearray",mode);
success &=test("mcomputeunitarray",mode);
success &=test("mcomputeorderarray",mode);
success &=test("morientunitarray",mode);
success &=test("morientorderarray",mode);
success &=test("mrotangmomunitarray",mode);
success &=test("mrotangmomorder0array",mode);
success &=test("terror", mode);
resultat=success
if (success)
disp('all tests are OK')
%    exit(0)
else
disp('some tests are BAD')
%    exit(1)
end
        
