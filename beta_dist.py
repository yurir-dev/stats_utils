
#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import pdb
import math
from scipy.integrate import quad
from scipy.stats import beta
import scipy.stats

def usage(desc = ""):
    print("")
    print(desc)
    print("Usage:")
    print("{} --alpha <value> -beta <value> --area_range <value:value> --desc <string>".format(__file__))
    print("")

def beta_distribution_function(x, a, b):
    values = beta.pdf(x, a, b)
    return values

def validArea(area_range):
    return area_range[0] < area_range[1]

def main(argv):
   
    try:
      opts, args = getopt.getopt(argv,"hva:b:r:d:",["help", "verbose", "alpha=","beta=", "area_range=", "desc="])
    except getopt.GetoptError:
      usage("Failed to parse argv")
      sys.exit(2)
    
    a, b = 2, 2
    area_range = [0, -1]
    desc = ""
    verbose = False
    for opt, arg in opts:
        try:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-v", "--verbose"):
                verbose = True
            elif opt in ("-a", "--alpha"):
                a = int(arg)
            elif opt in ("-b", "--beta"):
                b = int(arg)
            elif opt in ("-r", "--area_range"):
                rng = arg.split(':', 1)
                area_range = [float(rng[0]), float(rng[1])]
            else:
                usage("unexpected parameter: {} {}".format(opt, arg))
        except Exception as ex:
            usage("failed to parse argv - {}, opt {}, arg {}".format(ex, opt, arg))
            sys.exit(3)

    if not desc:
        desc = "Beta distribution a = {}, b = {}, range {}".format(a, b, area_range)

    if verbose:
        print('Argument List: {}'.format(sys.argv))
        print("a = {}, b = {}, area_range = {}, desc = {}".format(a, b, area_range, desc))

    x = np.linspace(beta.ppf(0.01, a, b), beta.ppf(0.99, a, b), 100)
    y = beta.pdf(x, a, b)
    
    if verbose:
        print("x : {}".format(x))
        print("y : {}".format(y))

    plt.plot(x, y, 'r-', lw=1, alpha=1.0)

    #pdb.set_trace()
    if validArea(area_range): 
        x1, x2 = area_range[0], area_range[1]
        ptx = np.linspace(x1, x2, 100)
        pty = beta.pdf(ptx, a, b)
        plt.fill_between(ptx, pty, color='#0b559f', alpha=1.0)
        
        betacdf = beta(a, b).cdf
        res = betacdf(x2) - betacdf(x1)
        desc += " - {}".format(res) 
        
        if verbose:
            print('Integration between {} and {} --> {}'.format(x1, x2, res))


    plt.title(desc)
    plt.grid()
    plt.show()
 
if __name__ == "__main__":
    main(sys.argv[1:])