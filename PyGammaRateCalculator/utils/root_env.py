import ROOT
import os
import PyGammaRateCalculator 
from   ROOT import gROOT
class SingletonDecorator:
    def __init__(self,klass):
        self.klass = klass
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.klass(*args,**kwds)
        return self.instance
class EDStatus:
    __macro_set = set() 
    __ED_loaded = False
    def __init__(self):
        pass 

    def loadED(self):  
        if(not self.__ED_loaded):
            gROOT.ProcessLine(".L $EVNDISPSYS/lib/libVAnaSum.so")
            self.__ED_loaded = True

    def loadMacro(self,macro_name):
        pp = os.path.dirname(PyGammaRateCalculator.__file__) + '/root_macro/'    
        pp = os.path.realpath(pp+macro_name)
        if(not os.path.isfile(pp)):
            raise Exception(pp+': Does not exist!')
        if(not (pp in self.__macro_set)):
            self.__macro_set.add(pp)
            gROOT.ProcessLine(".L {}+".format(pp)) 
EDStatus = SingletonDecorator(EDStatus)         
