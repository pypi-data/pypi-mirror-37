#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 20:12:31 2018

@author: andrew
"""

import glob
from image_registration import chi2_shift
from image_registration.fft_tools import shift
from astropy.io import fits
import numpy as np
import os

def chi2(location):
    x = 0
    template = glob.glob(location[:-4] + '/templates/*.fits')
    images = glob.glob(location + '/*_a_.fits')
    if len(template) == 1:
        ref_data = fits.getdata(template[0])
        ref_data = np.array(ref_data, dtype='float64')
        print("\n-> Aligning images with chi2...")
        for i in images:
            data = fits.getdata(i)
            data = np.array(data, dtype='float64')
            dx,dy,edx,edy = chi2_shift(ref_data, data, upsample_factor='auto')
            corrected_image = shift.shiftnd(data, (-dx,-dy))
            hdu = fits.PrimaryHDU(corrected_image)
            hdu.writeto(i[:-8] + '_A_.fits')
            os.remove(i)
            x += 1
            print("-> %.1f%% aligned..." % (float(x)/float(len(images)) * 100))
    else:
        print("-> Alignment failed: Template missing")
