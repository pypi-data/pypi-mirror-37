#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 17:24:29 2018

@author: andrew
"""

import glob
import os
import shutil
import initialize

def isis_sub(location):
    x = 0
    images = glob.glob(location + "/data/*_A_.fits")
    template = glob.glob(location + "/templates/*.fits")
    if images == []:
        print("-> Subtraction failure: No images to subtract")
    elif len(template) == 1:
        ais_loc = os.path.dirname(initialize.__file__) + "/AIS/package/bin/./mrj_phot"
        initialize.create_configs(location)
        ais_config_loc = location + '/configs/default_config'
        cwd = os.getcwd()
        os.mkdir(cwd + "/AIS_temp")
        os.chdir(cwd + "/AIS_temp")
        length = len(location) + 5
        print("\n-> Subtracting images...")
        for i in images:
            os.system(ais_loc + " " + template[0] + " " + i + " -c " + ais_config_loc)
            os.system("mv -f %s/AIS_temp/conv.fits %s/residuals/%sresidual_.fits" % (cwd, location, i[length:-5]))
            x += 1
            per = float(x)/float(len(images)) * 100
            print("-> %.1f%% subtracted..." % (per))
    else:
        print("-> Subtraction failure: Template missing")
    os.chdir(cwd)
    shutil.rmtree(cwd + "/AIS_temp")
    
def isis_sub_test(location):
    x = 0
    images = glob.glob(location + "/data/*_A_.fits")
    template = glob.glob(location + "/templates/*.fits")
    if images == []:
        print("-> Subtraction failure: No images to subtract")
    elif len(template) == 1:
        ais_loc = os.path.dirname(initialize.__file__) + "/AIS/package/bin/./mrj_phot"
        initialize.create_configs(location)
        ais_config_loc = location + '/configs/default_config'
        cwd = os.getcwd()
        os.mkdir(cwd + "/AIS_temp")
        os.chdir(cwd + "/AIS_temp")
        length = len(location) + 5
        print("\n-> Subtracting images...")
        for i in images:
            os.system(ais_loc + " " + i + " " + template[0] + " -c " + ais_config_loc)
            os.system("mv -f %s/AIS_temp/conv.fits %s/residuals/%sresidual_.fits" % (cwd, location, i[length:-5]))
            x += 1
            per = float(x)/float(len(images)) * 100
            print("-> %.1f%% subtracted..." % (per))
    else:
        print("-> Subtraction failure: Template missing")
    os.chdir(cwd)
    shutil.rmtree(cwd + "/AIS_temp")