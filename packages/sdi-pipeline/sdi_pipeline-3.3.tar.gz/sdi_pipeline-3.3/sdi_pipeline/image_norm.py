#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 16:43:36 2018

@author: andrew
"""

import glob
from astropy.io import fits
from image_registration import chi2_shift
from image_registration.fft_tools import shift
import numpy as np

image = '/home/andrew/sdi/targets/NGC6744/19:09:46.104_-63:51:27.00/rp/20.0/data/NORM_17:53:30.954_ref_A_.fits'
data = fits.getdata(image)
data = np.array(data, dtype='float64')
#image = '/home/andrew/sdi/targets/NGC6744/19:09:46.104_-63:51:27.00/rp/20.0/data/17:34:05.966_N_.fits'
#data = fits.getdata(image)
#Min = np.min(data)
#Max = np.max(data)
#new_min = 1
#new_max = -1
#data = (data-Min)*((new_max-new_min)/(Max-Min))
#data += new_min
#data -= np.mean(data)
#hdu = fits.PrimaryHDU(data)
#hdu.writeto('/home/andrew/sdi/targets/NGC6744/19:09:46.104_-63:51:27.00/rp/20.0/data/NORM3_17:34:05.966_N_.fits')
image2 = '/home/andrew/sdi/targets/NGC6744/19:09:46.104_-63:51:27.00/rp/20.0/data/NORM3_17:34:05.966_N_.fits'
data2 = fits.getdata(image2)
data2 = np.array(data2, dtype='float64')
dx,dy,edx,edy = chi2_shift(data, data2, upsample_factor='auto')
corrected_image = shift.shiftnd(data2, (-dy,-dx))
hdu2 = fits.PrimaryHDU(corrected_image)
hdu2.writeto('/home/andrew/sdi/targets/NGC6744/19:09:46.104_-63:51:27.00/rp/20.0/data/NORM5_align.fits')