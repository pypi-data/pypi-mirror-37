#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 13:07:01 2018

@author: andrew
"""

import imreg_dft
import numpy as np
from astropy.io import fits
import glob
import os

def imreg(location):
    x = 0
    ref_image = glob.glob(location + '/*_ref_A_.fits')
    images = glob.glob(location + '/*_a_.fits')
    if len(ref_image) == 1:
        ref_data = fits.getdata(ref_image[0])
#        ref_data = np.array(ref_data, dtype='float64')
        print("\n-> Aligning images with imreg...")
        for i in images:
            data = fits.getdata(i)
#            data = np.array(data, dtype='float64')
            corrected_image = imreg_dft.similarity(ref_data, data)
            hdu = fits.PrimaryHDU(corrected_image['timg'])
            hdu.writeto(i[:-8] + '_A_.fits')
            os.remove(i)
            x += 1
            print("-> %.1f%% aligned..." % (float(x)/float(len(images)) * 100))
    else:
        print("-> Alignment failed: Reference image missing")