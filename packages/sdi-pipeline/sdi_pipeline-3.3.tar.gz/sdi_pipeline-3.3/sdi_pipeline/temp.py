#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:26:57 2018

@author: andrew
"""

import glob
from initialize import loc
import os
from time import strftime
from time import gmtime

def swarp_residual(location):
    images = glob.glob(location + "/residuals/*residual.fits")
    config_files = glob.glob(os.getcwd() + '/*default.swarp')
    if config_files != []:
        config_loc = config_files[0]
        template = location + "/templates/swarp_median_" + str(len(images)) + ".fits"
        with open(config_loc, 'r') as config:
            data = config.readlines()
            config.close()
        data[4] = "IMAGEOUT_NAME" + "        " + template + "\n"
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
            print("no aligned images to combine\n")
        else:
            try:
                print("images being combined...\n")
                os.system("swarp @%s -c %s" % (tlist_loc, config_loc))
                log_list.write("template updated at %s UTC | method = median (SWarp) | images = %d\n" % (str(time), len(images)))
                log_list.close()
                if len(og_templates) > 0:
                    for o in og_templates:
                        os.system("mv %s %s/sdi/archive/templates" % (o, loc))
                print("image combination successful!\ntemplate log updated\n")
            except:
                print("image combination failed\n")
    else:
        print("\nno default.swarp file in cwd\n")