import glob
from time import strftime
from time import gmtime
import numpy as np
from astropy.io import fits
import os
from combine_residual import combine_MR
                
def MR(location):
    check = glob.glob(location + "/residuals/MR*")
    ask = input("\nCreate master residual? (y/n) : ")
    if ask == 'y':
            if check == []:
                combine_MR(location)
            elif check != []:
                replace = input("\nMaster residual already exists\nDo you want to update it? (y/n) : ")
                if replace == 'y':
                    os.system("rm %s/residuals/MR*" % (location))
                    combine_MR(location)
                elif replace == 'n':
                    pass
                else:
                    print("\nUnknown input: Need to choose y or n\n")
    elif ask == 'n':
        pass
    else:
        print("\nUnknown input: Need to choose y or n\n")