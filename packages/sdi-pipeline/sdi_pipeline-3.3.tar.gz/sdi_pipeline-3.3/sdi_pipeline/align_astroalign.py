#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 12:59:13 2018

@author: andrew
"""

import os
from astropy.io import fits
import glob
from initialize import loc
import numpy as np
import astroalign

#%%
#align images to reference image using astroalign package
def align2(location):
    x = 1
    images = glob.glob(location + "/*_N_.fits")
    ref = glob.glob(location + "/*_ref_A_.fits")
    hdu2 = fits.open(ref[0])
    data2 = hdu2[0].data
    data2 = np.array(data2, dtype="float64")
    print("\n-> Aligning images with astroalign...")
    for i in images:
        worked = True
        hdu1 = fits.open(i)
        data1 = hdu1[0].data
        data1 = np.array(data1, dtype="float64")
#        transf, (source_list, target_list) = astroalign.find_transform(data1, data2)
#        aligned = astroalign.apply_transform(transf, data1, data2)
        try:
            aligned = astroalign.register(data1, data2)
        except:
            view_im = input("\n-> Alignment failed: View trouble image in ds9? (y/n): ")
            if view_im == 'y':
                os.system("ds9 -scale zscale %s" % (i))
            elif view_im == 'n':
                pass
            else:
                print("-> Unknown input: must be y or n")
            delete = input("\n-> Delete trouble image from data set? (Do so if image has obvious issues or artifacts) (y/n): ")
            if delete == 'y':
                os.system("mkdir -p %s/sdi/archive/failed_alignments ; mv %s %s/sdi/archive/failed_alignments" % (loc, i, loc))
                print("\n-> Moved trouble image to 'failed_alignments' in 'archive' directory")
            elif delete == 'n':
                pass
            else:
                print("\n-> Unknown input: must be y or n")
            worked = False
            x += 1
        if worked == True:
            aligned_name = i[:-8] + "_A_.fits"
            hdu = fits.PrimaryHDU(aligned, header=hdu1[0].header)
            hdu.writeto(aligned_name)
            hdu1.close()
            os.system("mv %s %s/sdi/archive/data" % (i, loc))
            percent = float(x)/float(len(images)) * 100
            print("-> %.1f%% aligned..." % (percent))
            x += 1
    hdu2.close()
    