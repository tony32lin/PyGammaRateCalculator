import ROOT as r
from  ROOT import TFile,gROOT 
import numpy as np
from PyGammaRateCalculator.utils.root_env import EDStatus
import pandas as pd
import  collections 

def GetBkgCount(tFile,runID,Ecut):
    es = EDStatus()
    es.loadED()
    hname = 'run_{:d}/stereo/energyHistograms/hLinerecCounts_off'.format(int(runID))
    hoff = tFile.Get(hname)
    xaxis = hoff.GetXaxis() 
    binHigh = xaxis.FindBin(50.)
    if(isinstance(Ecut,collections.Sequence)):
    
        result = []
    
        for ee in Ecut:
            binLow = xaxis.FindBin(ee)
            result.append(hoff.Integral(binLow,binHigh)) 
    else:
        binLow = xaxis.FindBin(Ecut)
        result = hoff.Integral(binLow,binHigh) 

    hoff.Delete()
    return result


def GetOnCount(tFile,runID,Ecut):
    es = EDStatus()
    es.loadED()
    hname = 'run_{:d}/stereo/energyHistograms/hLinerecCounts_on'.format(int(runID))
    hon =tFile.Get(hname)
    xaxis = hon.GetXaxis()
    binHigh = xaxis.FindBin(50.)
    if(isinstance(Ecut,collections.Sequence)):
     
         result = []
     
         for ee in Ecut:
             binLow = xaxis.FindBin(ee)
             result.append(hon.Integral(binLow,binHigh)) 
    else:
         binLow = xaxis.FindBin(Ecut)
         result = hon.Integral(binLow,binHigh) 
    hon.Delete()
    return result

def getElevationBkgRate(fname,Ecut):
    es = EDStatus()
    es.loadED()
    f= TFile.Open(fname)
    flux = r.VFluxCalculation(fname)
    runlist = flux.getRunList()
    ton = flux.getTOn()
    
    islist = isinstance(Ecut,collections.Sequence)
    RunID_out = []
    Ze_out    = []
    Ecut_out      = []
    GammaRate_out = []
    GammaRateErr_out  = []
    BkgRate_out       = []
    BkgRateErr_out    = []
 
    for i,rid in enumerate(runlist):
        if(rid < 0):
            continue
        duration = ton[i]
        rid = int(rid)
        alpha    = flux.getAlpha(rid)
        NOff          = flux.getNOff(rid) 
        NOn          = flux.getNOn(rid)
        NOff_L       =  GetBkgCount(f,rid,Ecut)
        NOn_L        =  GetOnCount(f,rid,Ecut)
        Ze= 90 - flux.getRunElevation(rid)
        if(islist):
            for off,on,ee in zip(NOff_L,NOn_L,Ecut):
                RunID_out.append(rid)
                Ze_out.append(Ze)
                Ecut_out.append(ee)         
                GammaRate_out.append((on-off*alpha)/duration*60.)
                GammaRateErr_out.append(np.sqrt(on+off*alpha*alpha)/duration*60.)
                BkgRate_out.append(off/duration*60.*alpha) 
                BkgRateErr_out.append(np.sqrt(off)/duration*60.*alpha) 
    df = pd.DataFrame({'RunID':RunID_out,
                       'Ze'   : Ze_out,
                       'Ecut' : Ecut_out,
                       'GammaRate':GammaRate_out,
                       'GammaErr' :GammaRateErr_out,
                       'BkgRate'  :BkgRate_out,
                       'BkgRateErr':BkgRateErr_out})
    return df
