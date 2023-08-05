#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 15:55:42 2018

@author: andrew
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

h, w = img_shape = np.shape(hdu)
n_stars = 3
pos_x = [1500,2000,1200]
pos_y = [1600,1400,2200]
array = np.array([ 0.65343465,  0.50675629,  0.84946314])
fluxes = 200000.0 + array * 300.0
img = np.zeros(img_shape)
for x, y, f in zip(pos_x, pos_y, fluxes):
    img[x, y] = f

img = gaussian_filter(img, sigma=15.0, mode='constant')

plt.imshow(img)