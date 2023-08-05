from initialize import loc
from master_residual import MR
import subtract_hotpants
import subtract_ais

def SUBTRACT():
    path = input("\n-> Enter path to exposure time directory: ")
    method = input("\n-> Choose subtraction method: hotpants or AIS: ")
    if method == 'hotpants':
#        align_skimage.skimage_template(location)
        subtract_hotpants.hotpants(path)
#        MR(path)
    elif method == 'AIS':
#        align_chi2.chi2(location)
        subtract_ais.isis_sub(path)
#        MR(path)
    else:
        print("\n-> Error: Unknown method")

if __name__ == '__main__':
    path = input("\n-> Enter path to exposure time directory: ")
    method = input("\n-> Choose subtraction method: hotpants or ais: ")
    if method == 'hotpants':
#        align_chi2.chi2(location)
        subtract_hotpants.hotpants(path)
#        MR(path)
    elif method == 'ais':
#        align_chi2.chi2(location)
        subtract_ais.isis_sub(path)
#        MR(path)
    else:
        print("\n-> Error: Unknown method")