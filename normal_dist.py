
#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import pdb
import math
from scipy.integrate import quad
import scipy.stats

def usage(desc):
    print("")
    print(desc)
    print("Usage:")
    print("{} --mean <value> --std <value> --area_range <value:value> --desc <string>".format(__file__))
    print("")

def normal_distribution_function(x, mean, std):
    values = scipy.stats.norm.pdf(x, mean, std)
    # returns: type <class 'numpy.ndarray'>
    return values

def main(argv):
   
    try:
      opts, args = getopt.getopt(argv,"hvm:s:a:d:",["help", "verbose", "mean=","std=", "area_range=", "desc="])
    except getopt.GetoptError:
      usage()
      sys.exit(2)
    
    mean, std = 0, 1
    area_range = [0, 0]
    desc = ""
    verbose = False
    for opt, arg in opts:
        try:
            if opt == '-h':
                usage()
                sys.exit()
            elif opt in ("-m", "--mean"):
                mean = float(arg)
            elif opt in ("-v", "--verbose"):
                verbose = True
            elif opt in ("-d", "--desc"):
                desc = arg
            elif opt in ("-s", "--std"):
                std = float(arg)
            elif opt in ("-a", "--area_range"):
                rng = arg.split(':', 1)
                area_range = [float(rng[0]), float(rng[1])]
        except Exception as ex:
            usage("failed to parse argv - {}".format(ex))
            sys.exit(3)

    if verbose:
        print('Argument List: {}'.format(sys.argv))
        print("mean = {}, std = {}, area_range = {}, desc = {}".format(mean, std, area_range, desc))
    
    if not desc:
        desc = "normal distribution: mean {} , std {}".format(mean, std)
    
    x_min, x_max = mean -std * 6, mean + std * 6
    x = np.linspace(x_min, x_max, 100)
    y = normal_distribution_function(x, mean, std)
    plt.plot(x, y, color='red')
    
    if area_range[0] != 0 and area_range[1] != 0:
        x1, x2 = area_range[0], area_range[1]
        ptx = np.linspace(x1, x2, 100)
        pty = normal_distribution_function(ptx, mean, std)
        plt.fill_between(ptx, pty, color='#0b559f', alpha=1.0)
        
        res, err = quad(normal_distribution_function, x1, x2, args=(mean,std,))
        desc += " - {}".format(res) 
        
        if verbose:
            print('Integration between {} and {} --> {} , with absolute error {}'.format(x1, x2, res, err))
    
    plt.title(desc)
    plt.grid()
    plt.show()
 
if __name__ == "__main__":
    main(sys.argv[1:])