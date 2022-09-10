
#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import pdb
import math
from scipy.integrate import quad
from scipy.stats import binom
import scipy.stats

def usage(desc):
    print("")
    print(desc)
    print("Usage:")
    print("{} --k_range <value:value> -n <value> -p <value:value> --area_range <value:value> --desc <string>".format(__file__))
    print("area_range should be inside k_range")
    print("")

def binomial_distribution_function(k, n, p):
    values = binom.pmf(k, n, p)
    return values

def validArea(area_range):
    return area_range[0] < area_range[1]

def main(argv):
   
    try:
      opts, args = getopt.getopt(argv,"hvk:n:p:a:d:",["help", "verbose", "k_range=","n=", "probability=", "area_range=", "desc="])
    except getopt.GetoptError:
      usage()
      sys.exit(2)
    
    n, p = 1, 0.5
    k_range = [1, 1]
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
            elif opt in ("-k", "--k_range"):
                rng = arg.split(':', 1)
                k_range = [int(rng[0]), int(rng[1])]
            elif opt in ("-d", "--desc"):
                desc = arg
            elif opt in ("-n", "--n"):
                n = float(arg)
            elif opt in ("-p", "--probability"):
                p = float(arg)
            elif opt in ("-a", "--area_range"):
                rng = arg.split(':', 1)
                area_range = [int(rng[0]), int(rng[1])]
        except Exception as ex:
            usage("failed to parse argv - {}, opt {}, arg {}".format(ex, opt, arg))
            sys.exit(3)

    if verbose:
        print('Argument List: {}'.format(sys.argv))
        print("k = {}, n = {}, p = {}, area_range = {}, desc = {}".format(k_range, n, p, area_range, desc))
    
    if not desc:
        desc = "binomial distribution: k {}, n {}, p {}".format(k_range, n, p)
    
    ks = range(k_range[0], k_range[1] + 1)
    dist = [binom.pmf(k, n, p) for k in ks ]
    
    if verbose:
        print("ks: {}".format(ks))
        print("dist: {}".format(dist))
    
    colors = []
    if validArea(area_range): 
        res = sum(dist[x - 1] for x in range(area_range[0], area_range[1] + 1)) 
        desc += " - sum({}, {}) = {}".format(area_range[0], area_range[1], res)
        
        colors = ['blue' for k in ks]
        for x in range(area_range[0], area_range[1] + 1):
            colors[x - 1] = 'red'
    
    ks_strs = [str(k) for k in ks]
    if len(colors) == len(ks_strs):
        plt.bar(ks_strs, dist, color=colors)
    else:
        plt.bar(ks_strs, dist)

    plt.title(desc)
    #plt.grid()
    plt.show()
 
if __name__ == "__main__":
    main(sys.argv[1:])