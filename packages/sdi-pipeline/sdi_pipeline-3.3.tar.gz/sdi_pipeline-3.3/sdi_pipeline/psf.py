#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 20:09:18 2018

@author: andrew
"""

import glob
import os
import initialize

def psfex(location):
    psf_loc = location + '/psf'
    cats = glob.glob(psf_loc + '/*.cat')
    initialize.create_configs(location)
    config_loc = location + '/configs/psfex.config'
    print("\n-> Calculating PSFs...\n")
    for cat in cats:
        with open(config_loc, 'r') as config:
            data = config.readlines()
            config.close()
        data[83] = "PSF_DIR" + "        " + location + "/psf" + "\n"
        with open(config_loc, 'w') as config:
            config.writelines(data)
            config.close()
        os.system("psfex %s > %s.psf -c %s" % (cat, cat[:-4], config_loc))