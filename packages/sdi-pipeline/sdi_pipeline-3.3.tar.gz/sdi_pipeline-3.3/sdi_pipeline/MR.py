#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:58:35 2018

@author: andrew
"""

import glob
from astropy.io import fits
import numpy as np

def stack_res(location):
    check = glob.glob(location + "/residuals/*MR")
    ask = True
    if check != []:
        ask = input("\t-> Master residual exists. Replace? (y/n): ")
    elif check == [] or ask == 'y':
        pass
    
images = glob.glob("/home/andrew/sdi/targets/TEST/21:40:47.388_+00:28:35.11/B/90/residuals/*.fits")
im_list = []
for i in images:
    hdu = fits.getdata(i)
    im_list.append(hdu)
size_x = np.shape(im_list[0])[0]
size_y = np.shape(im_list[0])[1]
stack_im = np.zeros((size_x, size_y))
num_im = len(im_list)
pixels = []
per = 0
for x in range(size_x):
    for y in range(size_y):
        for n in range(num_im):
            pixels.append(im_list[n][x,y])
            if n == num_im - 1:
                sort = sorted(pixels)
                first = sort[0]
                last = sort[-1]
                std = np.std(sort)
                if first + (6*std) < last:
                    stack_im[x,y] = last
                elif first + (6*std) >= last:
                    stack_im[x,y] = np.mean(sort)
                pixels = []
                per += 1
                print("\t-> %.1f%% percent..." % (float(per)/float(size_x*size_y)))