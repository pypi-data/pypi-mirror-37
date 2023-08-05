import align_astroalign
from ref_image import ref_image
from initialize import loc
import subtract_hotpants
import combine_swarp
import combine_numpy
import extract
import check_saturation
import get
import subtract_ais
import align_chi2

def PIPELINE():
    get_check = input("-> Get data or analyze existing data? (get/analyze): ")
    if get_check == 'get':
        get.GET()
    elif get_check == 'analyze':
        location = input("-> Enter path to data directory: ")
        sat = check_saturation.check_saturate(location)
        if sat == 0:
            ref_image(location)
            align_astroalign.align2(location)
        else:
            check = input("-> Saturated images found, continue image alignment? (y/n): ")
            if check == 'y':
                move = input("-> Move saturated images to SDI archives before continuing? (y/n): ")
                if move == 'y':
                    check_saturation.move_arch(sat)
                    ref_image(location)
                    align_astroalign.align2(location)
                else:
                    ref_image(location)
                    align_astroalign.align2(location)
        method = input("-> Choose combination method-- numpy (default) or swarp: ")
        if method == "swarp":
            combine_swarp.swarp(location)
        elif method == "numpy" or method == "":
            combine_numpy.combine_median(location)
        else:
            print("-> Error: unknown method entered")
        path = location[:-5]
        sub_method = input("\n-> Choose subtraction method-- ais (default) or hotpants: ")
        if sub_method == '' or sub_method == 'ais':
            subtract_ais.isis_sub(path)
        elif sub_method == 'hotpants':
            subtract_hotpants.hotpants(path)
        else:
            print("\n-> Error: Unknown method")
        ask = input("-> Run sextractor on residual images? (y/n): ")
        if ask == 'y':
            extract.SEXTRACTOR(path)
        elif ask != 'y' and ask != 'n':
            print("-> Error: unknown input")

if __name__ == '__main__':
    get_check = input("-> Get data or analyze existing data? (get/analyze): ")
    if get_check == 'get':
        get.GET()
    elif get_check == 'analyze':
        location = input("-> Enter path to data directory: ")
        sat = check_saturation.check_saturate(location)
        if sat == 0:
            ref_image(location)
            align_astroalign.align2(location)
        else:
            check = input("-> Saturated images found, continue image alignment? (y/n): ")
            if check == 'y':
                move = input("-> Move saturated images to SDI archives before continuing? (y/n): ")
                if move == 'y':
                    check_saturation.move_arch(sat)
                    ref_image(location)
                    align_astroalign.align2(location)
                else:
                    ref_image(location)
                    align_astroalign.align2(location)
        method = input("-> Choose combination method-- numpy (default) or swarp: ")
        if method == "swarp":
            combine_swarp.swarp(location)
        elif method == "numpy" or method == "":
            combine_numpy.combine_median(location)
        else:
            print("-> Error: unknown method entered")
        path = location[:-5]
        sub_method = input("\n-> Choose subtraction method-- ais (default) or hotpants: ")
        if sub_method == '' or sub_method == 'ais':
            subtract_ais.isis_sub(path)
        elif sub_method == 'hotpants':
            subtract_hotpants.hotpants(path)
        else:
            print("\n-> Error: Unknown method")
        ask = input("-> Run sextractor on residual images? (y/n): ")
        if ask == 'y':
            extract.SEXTRACTOR(path)
        elif ask != 'y' and ask != 'n':
            print("-> Error: unknown input")