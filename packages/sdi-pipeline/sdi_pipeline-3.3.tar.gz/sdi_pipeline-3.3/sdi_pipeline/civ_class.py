#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 12:21:04 2018

@author: andrew
"""

import numpy as np
import matplotlib.pyplot as plt

data_loc = '/home/andrew/sdi/writes_and_calcs/grapher_data/'

#all wavelengths in nm

def flux_ratio(p_laser, p_star, d_array, lamb):
    f_ratio = (float(p_laser)/float(p_star))*(np.pi)*d_array**2/((lamb*10**-9)**2)
    return f_ratio

def beam_diam(L_d, lamb, d_array): #L_d in ly
    d_beam = 2*L_d*9.5*10**15*np.tan(lamb*10**-9/d_array)
    d_beam *= 6.68459*10**-12
    return d_beam #returns beam diameter in AUs

def nm_to_hz(nm):
    c = 3*10**17
    hz = c/nm
    return hz

def delta_lamb(delta_hz, lamb):
    c = 3*10**17
    delt_lamb = delta_hz*lamb**2/c
    return delt_lamb

def delta_hz(delta_lamb, lamb):
    c = 3*10**17
    delt_hz = delta_lamb*c/lamb**2
    return delt_hz

def resolving_power_hz(delta_hz, lamb):
    R = lamb/delta_lamb(delta_hz, lamb)
    return R

def resolving_power_lamb(delta_lamb, lamb):
    R = lamb/delta_lamb
    return R

def f_ratio_civ_class_plot(p_star, lamb):
    f_ratios = []
    civ_classes = []
    p_laser = []
    d_array = np.arange(0,100000)
    for i in range(len(d_array)):
        civ_classes.append(np.log10(d_array[i]))
        p_laser.append(0.7*(d_array[i]**2)*10**3)
        f_ratios.append(np.log10(flux_ratio(p_laser[i], p_star, d_array[i], lamb)))
    zips = (list(zip(civ_classes,f_ratios)))
    with open(data_loc + 'fluxratio_vs_civclass.txt', 'w+') as dat:
        dat.write('\n'.join('%s %s' % x for x in zips))
        dat.close
        
def f_ratio_bandwidth_plot(p_laser, p_star, d_array, lamb):
    f_ratio = flux_ratio(p_laser, p_star, d_array, lamb)
    res_powers = []
    fluxes = []
    del_lamb = np.arange(10**-9,.1, 10**-7)
    for i in range(len(del_lamb)):
        res_powers.append(resolving_power_lamb(del_lamb[i], lamb))
        fluxes.append(f_ratio*res_powers[i])
    for d in range(len(del_lamb)):
        del_lamb[d] = delta_hz(del_lamb[d], 1000)
    plt.plot(np.log10(del_lamb), np.log10(fluxes))
    zips = (list(zip(np.log10(del_lamb),np.log10(fluxes))))
    with open(data_loc + 'fluxratio_vs_bandwidth.txt', 'w+') as dat:
        dat.write('\n'.join('%s %s' % x for x in zips))
        dat.close

def beam_diam_plot(lamb, d_array):
    d_beam = []
    L_d = np.arange(10, 10**7,1000)
    for i in L_d:
        d_beam.append(beam_diam(i, lamb, d_array))
    plt.plot(np.log10(L_d), np.log10(d_beam))
    zips = (list(zip(np.log10(L_d),np.log10(d_beam))))
    with open(data_loc + 'beamdiameter_vs_Ldistance.txt', 'w+') as dat:
        dat.write('\n'.join('%s %s' % x for x in zips))
        dat.close
    
    