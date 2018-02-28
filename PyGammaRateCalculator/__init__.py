import os
from   os.path import isfile
from PyGammaRateCalculator.calRate import calRate

keys = os.environ.keys()
if (not 'EVNDISPSYS' in keys):
    raise Exception("EVNDISPSYS not defined")

if (not isfile(os.environ['EVNDISPSYS']+"/lib/libVAnaSum.so")):
    raise Exception("libVAnaSum.so doesn't exist")

