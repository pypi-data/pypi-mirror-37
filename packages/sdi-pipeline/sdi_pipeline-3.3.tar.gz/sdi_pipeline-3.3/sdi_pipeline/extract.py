import sex
import psf
import glob

def EXTRACT():
    path = input("-> Enter path to target's exposure time directory: ")
    images = glob.glob(path + '/data/*.fits')
    psf_data = glob.glob(path + '/psf/*')
    if len(psf_data) == 3*len(images):
        sex.sextractor(path)
        sex.src_filter(path)
    else:
        sex.sextractor_psf(path)
        psf.psfex(path)
        sex.sextractor(path)
        sex.src_filter(path)

if __name__ == '__main__':
    path = input("-> Enter path to target's exposure time directory: ")
    images = glob.glob(path + '/data/*.fits')
    psf_data = glob.glob(path + '/psf/*')
    if len(psf_data) == 3*len(images):
        sex.sextractor(path)
        sex.src_filter(path)
    else:
        sex.sextractor_psf(path)
        psf.psfex(path)
        sex.sextractor(path)
        sex.src_filter(path)