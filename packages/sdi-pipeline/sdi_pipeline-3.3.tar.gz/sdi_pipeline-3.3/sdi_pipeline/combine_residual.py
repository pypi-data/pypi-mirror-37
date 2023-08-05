import glob
from time import strftime
from time import gmtime
import numpy as np
from astropy.io import fits
import os

def combine_MR(Location):
    data = []
    residuals = glob.glob(Location + "/residuals" + "/*residual*.fits")
    log_loc = Location + "/residuals/master_residual_log.txt"
    log_list = open(log_loc, "a+")
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for i in residuals:
        hdu1 = fits.open(i)
        data1 = hdu1[0].data
        data1 = np.array(data1, dtype="float64")
        data.append(data1)
        Header = hdu1[0].header
        hdu1.close()
    comb = np.sum(data, axis=0)
    combined_name = Location + "/residuals/MR_%d.fits" % (len(residuals))
    hdu = fits.PrimaryHDU(comb, header=Header)
    hdu.writeto(combined_name)
    log_list.write("master residual updated at %s UTC | method = sum (numpy) | images = %d\n" % (str(time), len(residuals)))
    log_list.close()
    print("\nmaster residual created!\nmaster residual log updated\n")