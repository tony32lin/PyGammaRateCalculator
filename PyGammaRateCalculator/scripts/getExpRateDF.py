from PyGammaRateCalculator import calRate
import numpy as np
import click
import pandas as pd
import os
import collections
import itertools 

def getExpRateDF(fname,dZe,energy,
                 pul_SI,nebula_SI,
                 pul_fNorm,nebula_fNorm,
                 E0=0.15,nsb=250):
    ''' Generate data frame for resulting expected rates
        fname: effective area file name
        dZe  : Zenith angle
        energy: thresholds for the rate to be calculated
        pul_fNorm: pulsar flux normalisation
        nebula_fNorm: nebula flux normalisation
        pul_SI: pulsar spectral index
        nebula_SI: nebula spectral index
        E0       : normalisation energy
    '''     
    if(not isinstance(energy,collections.Sequence)):
       energy = [energy]     
    if(not isinstance(pul_SI,collections.Sequence)):
       pul_SI = [pul_SI]
    if(not isinstance(nebula_SI,collections.Sequence)):
       nebula_SI = [nebula_SI]     
    nsb_l       = []
    pul_SI_l    = []
    energy_l    = []
    nebula_SI_l = []
    ze_l        = []
    E0_l        = []
    rate_pul_l  = []
    rate_nebula_l = []
    for ns in nebula_SI:
        for ps in pul_SI:
            rate_nebula = calRate(energy,fname,dZe,nebula_fNorm,ns,E0)
            rate_pul = calRate(energy,fname,dZe,pul_fNorm,ps,E0)
            energy_l.append(energy)  
            for rn,rp in zip(rate_nebula,rate_pul):
                pul_SI_l.append(ps)  
                nebula_SI_l.append(ns)  
                ze_l.append(dZe)
                E0_l.append(E0)
                rate_pul_l.append(rp)
                rate_nebula_l.append(rn)
                nsb_l.append(nsb)
    energy_l = list(itertools.chain(*energy_l))        
    out = pd.DataFrame({'Ze':ze_l,
                        'SI_P2':pul_SI_l,
                        'SI_Nebula':nebula_SI_l,
                        'E0':E0_l,
                        'P2Rate':rate_pul_l,
                        'NebulaRate':rate_nebula_l,
                        'EPrimeMin':energy_l,
                        'NSB':nsb_l})                                           
    return out

