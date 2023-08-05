#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 13:01:19 2018

@author: andrew
"""

import glob
from initialize import loc
import os
from time import strftime
from time import gmtime
import stats
from astropy.io import fits
import numpy as np

#%%
#median combine images using SWarp
def swarp(location):
    location = location[:-5]
    images = glob.glob(location + "/data/*_A_.fits")
    shapes = []
    for i in images:
        image_data = fits.getdata(i)
        shapes.append(np.shape(image_data))
#        sh = np.shape(image_data)
#        if shapes[0] != sh:
#            diff = tuple(np.subtract(shapes[0], sh))
#            
            
    if shapes[0] != all(shapes):
        print("-> Cannot use SWarp: images differ in dimension")
    else:
        config_files = glob.glob(os.path.dirname(stats.__file__) + '/config/*default.swarp')
        if config_files != []:
            config_loc = config_files[0]
            template = location + "/templates/swarp_median_" + str(len(images)) + ".fits"
            with open(config_loc, 'r') as config:
                data = config.readlines()
                config.close()
            data[4] = "IMAGEOUT_NAME" + "        " + template + "\n"
            data[33] = "IMAGE_SIZE" + "        " + "%s, %s" % shapes[0] + "\n"
            with open(config_loc, 'w') as config:
                config.writelines(data)
                config.close()
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            og_templates = glob.glob(location + "/templates/*.fits")
            log_loc = location + "/templates/log.txt"
            tlist_loc = location + "/templates/template_inputs.txt"
            log_list = open(log_loc, "a+")
            template_list = open(tlist_loc, "w+")
            for i in images:
                template_list.write(str(i) + "[0]" + "\n")
            template_list.close()
            if images == []:
                print("-> no aligned images to combine\n")
            else:
                try:
                    print("-> images being combined...\n")
                    os.system("swarp @%s -c %s" % (tlist_loc, config_loc))
                    log_list.write("template updated at %s UTC | method = median (SWarp) | images = %d\n" % (str(time), len(images)))
                    log_list.close()
                    if len(og_templates) > 0:
                        for o in og_templates:
                            os.system("mv %s %s/sdi/archive/templates" % (o, loc))
                    print("-> image combination successful!\ntemplate log updated\n")
                except:
                    print("-> image combination failed\n")
        else:
            print("\n-> no default.swarp file in config directory\n")