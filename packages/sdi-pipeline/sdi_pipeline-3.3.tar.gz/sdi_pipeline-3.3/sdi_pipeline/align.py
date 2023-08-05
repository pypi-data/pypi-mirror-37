import align_astroalign
from ref_image import ref_image
import check_saturation

def ALIGN():
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
            elif move == 'n':
                ref_image(location)
                align_astroalign.align2(location)
            else:
                print("-> Unknown input: must be y or n")
        elif check =='n':
            pass
        else:
            print("-> Unknown input: must be y or n")

if __name__ == '__main__':
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
            elif move == 'n':
                ref_image(location)
                align_astroalign.align2(location)
            else:
                print("-> Unknown input: must be y or n")
        elif check =='n':
            pass
        else:
            print("-> Unknown input: must be y or n")