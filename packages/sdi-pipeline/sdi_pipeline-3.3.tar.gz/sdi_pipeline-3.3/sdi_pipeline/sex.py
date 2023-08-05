#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 13:04:32 2018

@author: andrew
"""

import os
import glob
import initialize

def src_filter(location):
    source_loc = location + '/sources'
    temp_source_loc = source_loc + '/temp'
    temp_source_files = glob.glob(temp_source_loc + '/*.txt')
    for file in temp_source_files:
        with open(file, 'r') as fl:
            data = fl.readlines()
            fl.close()
        data = [str(file[len(source_loc)+1:-4]) + '\n'] + data
        data.append("\n\n\n")
        with open(source_loc + '/sources.txt', 'a+') as s:
            s.writelines(data)
            s.close()
        os.remove(file)
        
    #filter source file by spread_model
    del_lin = []
#    source = glob.glob(source_loc + '/*.txt')
    with open(source_loc + '/sources.txt', 'r') as src:
        lines = src.readlines()
        src.close()
        
    for lin in lines:
        parse = lin.split()
        if parse != []:
            try:
                int(parse[0])
                if float(parse[-1]) < 0 or float(parse[-1]) > 0.1:
                    del_lin.append(lin)
            except ValueError or IndexError:
                pass
            
    lines = [a for a in lines if a not in del_lin]
    
    with open(source_loc + '/filtered_sources.txt', 'w+') as fil_src:
        fil_src.writelines(lines)
        fil_src.close()

#%%
#runs SExtractor on all residual images in a directory
def sextractor(location):
    x = 0
    sources = location + "/sources"
    residuals = location + "/residuals"
    check = os.path.exists(sources)
    check_temp = os.path.exists(sources + '/temp')
    length = len(residuals) + 1
    if check == False:
        os.system("mkdir %s" % (sources))
        os.system("mkdir %s/temp" % (sources))
    else:
        if check_temp == False:
            os.system("mkdir %s/temp" % (sources))
    images = glob.glob(residuals + "/*.fits")
    initialize.create_configs(location)
    config_loc = location + '/configs/default.sex'
    with open(config_loc, 'r') as config:
        data = config.readlines()
        config.close()
    data[9] = "PARAMETERS_NAME" + "        " + location + "/configs/default.param" + "\n"
    data[20] = "FILTER_NAME" + "        " + location + "/configs/default.conv" + "\n"
    with open(config_loc, 'w') as config:
        config.writelines(data)
        config.close()
    print("\n-> SExtracting images...")
    for i in images:
        name = i[length:-5]
        with open(config_loc, 'r') as config:
            data = config.readlines()
            config.close()
        data[104] = "PSF_NAME" + "        " + location + "/psf/" + name[:-9] + ".psf" + "\n"
        with open(config_loc, 'w') as config:
            config.writelines(data)
            config.close()
        os.system("sextractor %s[0]> %s/temp/%s.txt -c %s" % (i, sources, name, config_loc))
        x += 1
        per = float(x)/float(len(images)) * 100
        print("-> %.1f%% sextracted..." % (per))
    print("-> SExtracted %d images, catalogues placed in 'sources' directory\n" % (len(images)))
    print("-> Filtering source catalogs...\n")
    src_filter(location)
    
def sextractor_psf(location):
    x = 0
    psf_loc = location + "/psf"
    data = location + "/data"
    check = os.path.exists(psf_loc)
    length = len(data) + 1
    if check == False:
        os.system("mkdir %s" % (psf_loc))
    images = glob.glob(data + "/*.fits")
    initialize.create_configs(location)
    config_loc = location + '/configs/psf.sex'
    with open(config_loc, 'r') as config:
        data = config.readlines()
        config.close()
    data[9] = "PARAMETERS_NAME" + "        " + location + "/configs/default.psfex" + "\n"
    data[20] = "FILTER_NAME" + "        " + location + "/configs/default.conv" + "\n"
    with open(config_loc, 'w') as config:
        config.writelines(data)
        config.close()
    print("\n-> SExtracting images...")
    for i in images:
        name = i[length:-5]
        with open(config_loc, 'r') as config:
            data = config.readlines()
            config.close()
        data[6] = "CATALOG_NAME" + "        " + psf_loc + "/" + name + ".cat" + "\n"
        with open(config_loc, 'w') as config:
            config.writelines(data)
            config.close()
        os.system("sextractor %s[0] -c %s" % (i, config_loc))
        x += 1
        per = float(x)/float(len(images)) * 100
        print("-> %.1f%% sextracted..." % (per))
    print("-> SExtracted %d images, catalogues placed in 'psf' directory\n" % (len(images)))

    
