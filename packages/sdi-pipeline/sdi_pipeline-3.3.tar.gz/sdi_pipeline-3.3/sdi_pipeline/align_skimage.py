#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 14:24:51 2018

@author: andrew
"""

from skimage.feature import register_translation
from scipy.ndimage import fourier_shift
import numpy as np
from astropy.io import fits
import glob
import os

def skimage(location):
    x = 0
    ref_image = glob.glob(location + '/*_ref_A_.fits')
    images = glob.glob(location + '/*_N_.fits')
    if len(ref_image) == 1:
        ref_data = fits.getdata(ref_image[0])
#        ref_data = np.array(ref_data, dtype='float64')
        print("\n-> Aligning images with skimage...")
        for i in images:
            data = fits.getdata(i)
#            data = np.array(data, dtype='float64')
            shift, error, diffphase = register_translation(ref_data, data, 100)
            corrected_image = fourier_shift(np.fft.fftn(data), shift)
            corrected_image = np.fft.ifftn(corrected_image)
            hdu = fits.PrimaryHDU(corrected_image.real)
            hdu.writeto(i[:-8] + '_A_.fits')
            os.remove(i)
            x += 1
            print("-> %.1f%% aligned..." % (float(x)/float(len(images)) * 100))
    else:
        print("-> Alignment failed: Reference image missing")
        
def skimage_template(location):
    print(location[:-5] + '/templates/*.fits')
    x = 0
    template = glob.glob(location[:-5] + '/templates/*.fits')
    images = glob.glob(location + '/*_a_.fits')
    if len(template) == 1:
        template_data = fits.getdata(template[0])
#        template_data = np.array(ref_data, dtype='float64')
        print("\n-> Aligning images to template with skimage...")
        for i in images:
            data = fits.getdata(i)
#            data = np.array(data, dtype='float64')
            shift, error, diffphase = register_translation(template_data, data, 100)
            corrected_image = fourier_shift(np.fft.fftn(data), shift)
            corrected_image = np.fft.ifftn(corrected_image)
            hdu = fits.PrimaryHDU(corrected_image.real)
            hdu.writeto(i[:-8] + '_A_.fits')
            os.remove(i)
            x += 1
            print("-> %.1f%% aligned..." % (float(x)/float(len(images)) * 100))
    else:
        print("-> Alignment failed: Template image missing")