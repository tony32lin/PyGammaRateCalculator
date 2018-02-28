import numpy as np 
import ROOT as r
from ROOT import gROOT
import os
import contextlib
import collections

__ED_inited__ = False

def initED():
    __file_path__ = os.path.dirname(os.path.realpath(__file__))
    gROOT.ProcessLine(".L $EVNDISPSYS/lib/libVAnaSum.so")
    gROOT.ProcessLine(".L {dirname}/root_macro/convolveEA.C+".format(dirname=__file_path__))
    global __ED_inited__
    __ED_inited__ = True

@contextlib.contextmanager
def CppPrintContext(verbose=True):
    if(not verbose):
        gROOT.ProcessLine("std::cout.setstate(std::ios_base::failbit)")
    else:
        pass
    yield
    if(not verbose):
        gROOT.ProcessLine("std::cout.clear()")    

@contextlib.contextmanager
def IRFContext(fname,dZe,Fnorm,index,E0,nsb=250):
    irf_MC =  r.VInstrumentResponseFunctionReader();
    irf_Rec = r.VInstrumentResponseFunctionReader(); 
    irf_MC.fillData(fname,dZe,0.5,16,index,nsb,"A_MC");
    irf_Rec.fillData(fname,dZe,0.5,16,index,nsb,"A_Rec");
    h_Migration_Original = irf_MC.getMigrationMatrix()
    EA_ori = irf_Rec.gEffArea_Rec
    h_FA = r.getConvolvedHist(h_Migration_Original,EA_ori,Fnorm,index,E0)
    yield h_FA
    h_Migration_Original.Delete()
    EA_ori.Delete()
    h_FA.Delete()

def calRate(energy,fname,dZe,fNorm,index,E0,nsb=250,verbose=False):
    global __ED_inited__
    if(not __ED_inited__):
        initED()
    isList = isinstance(energy,(collections.Sequence,np.ndarray))
    if(isList):
        result = []
    Eprime_max = 30.
    logEmin = np.log10(0.1);
    logEprimeMax = np.log10(Eprime_max);

    if(not os.path.isfile(fname)):
        raise Exception('{} does not exist.'.format(fname))

    with CppPrintContext(verbose=verbose):
        with IRFContext(fname,dZe,fNorm,index,E0,nsb=nsb) as h_FA:
            xAxis = h_FA.GetXaxis()
            yAxis = h_FA.GetYaxis()
            binx1 = xAxis.FindBin(logEmin);
            nBinsX = h_FA.GetNbinsX()
            logEhigh = xAxis.GetBinCenter(nBinsX)
            binx2 = xAxis.FindBin(logEhigh);
            
            biny2 = yAxis.FindBin(logEprimeMax);
            if(isList):
                for e in energy:
                    biny1 = yAxis.FindBin(np.log10(e))
                    result.append(h_FA.Integral(binx1,binx2,biny1,biny2,"width")*60)            

            else:
                biny1 = yAxis.FindBin(np.log10(energy))
                result =h_FA.Integral(binx1,binx2,biny1,biny2,"width")*60
    return result
                
 
