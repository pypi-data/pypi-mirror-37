import combine_swarp
import combine_numpy

def COMBINE():
    location = input("-> Enter path to data directory: ")
    method = input("\n-> Choose combination method-- numpy (default) or swarp: ")
    if method == "swarp":
        combine_swarp.swarp(location)
    elif method == "numpy" or method == "":
        combine_numpy.combine_median(location)
    else:
        print("-> Error: unknown method entered")

if __name__ == '__main__':
    location = input("-> Enter path to data directory: ")
    method = input("\n-> Choose combination method-- numpy (default) or swarp: ")
    if method == "swarp":
        combine_swarp.swarp(location)
    elif method == "numpy" or method == "":
        combine_numpy.combine_median(location)

    else:
        print("-> Error: unknown method entered")
