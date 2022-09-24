
#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import pdb
import math
from scipy.integrate import quad
from scipy.stats import beta
import scipy.stats

import utils

def usage(desc = ""):
    print("")
    print(desc)
    print("Usage:")
    print("{} --alpha <value> -beta <value> --area_range <value:value> --percentile <value> --desc <string>".format(__file__))
    print("")

def beta_distribution_function(x, a, b):
    values = beta.pdf(x, a, b)
    return values

def validArea(area_range):
    return area_range[0] < area_range[1]




def main(argv):
   
    try:
      opts, args = getopt.getopt(argv,"hva:b:r:p:d:",["help", "verbose", "alpha=","beta=", "area_range=", "percentile=", "desc="])
    except getopt.GetoptError:
      usage("Failed to parse argv")
      sys.exit(2)
    
    a, b = 1,1
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
            elif opt in ("-d", "--desc"):
                desc = arg
            elif opt in ("-r", "--area_range"):
                rng = arg.split(':', 1)
                area_range = [float(rng[0]), float(rng[1])]
            elif opt in ("-p", "--percentile"):
                percentile = float(arg)
                if percentile < 0 or percentile > 1.0:
                    raise Exception("invalid percentile {} , should be in range (0, 1)".format(percentile))
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

    #plt.plot(x, y, 'r-', lw=1, alpha=1.0)
    fig, (axBeta, axCdf, axQuantil) = plt.subplots(3, 1)
 
    axBeta.plot(x, y, 'r-', lw=1, alpha=1.0)
    axBeta.grid()

    y = beta(a, b).cdf(x)
    axCdf.plot(x, y, 'r-', lw=1, alpha=1.0)
    axCdf.set_title('cdf', y=0.5, x=0.95, pad=-14)
    
    x = np.linspace(0, 1, 100)
    y = beta.ppf(x, a, b)
    axQuantil.plot(x, y, 'r-', lw=1, alpha=1.0)
    axQuantil.set_title('quantile', y=1.0, pad=-14)
    
    if percentile > 0 :
        x1 = (1.0 - percentile) / 2.0
        x2 = 1.0 - x1
        y1 = beta.ppf(x1, a, b)
        y2 = beta.ppf(x2, a, b)
        axQuantil.set_title('quantile {} - {:.3f}:{:.3f}'.format(percentile, y1, y2), y=1.0, pad=-14)
        
        utils.selectPoint(axQuantil, xmin=0, x=x1, ymin=0, y=y1)
        utils.selectPoint(axQuantil, xmin=0, x=x2, ymin=0, y=y2)

        area_range = [y1, y2]

    #pdb.set_trace()
    if validArea(area_range): 
        x1, x2 = area_range[0], area_range[1]
        ptx = np.linspace(x1, x2, 100)
        pty = beta.pdf(ptx, a, b)
        axBeta.fill_between(ptx, pty, color='#0b559f', alpha=1.0)
        
        betacdf = beta(a, b).cdf
        res = betacdf(x2) - betacdf(x1)
        desc += " - [{:.3f},{:.3f}] = {}".format(x1, x2, res) 
        
        if verbose:
            print('Integration between {} and {} --> {}'.format(x1, x2, res))
        
        xmin = beta.ppf(0.01, a, b)
        utils.selectPoint(axCdf, xmin, x=x1, ymin=0, y=beta(a, b).cdf(x1))
        utils.selectPoint(axCdf, xmin, x=x2, ymin=0, y=beta(a, b).cdf(x2))

    axBeta.title.set_text(desc)
    
    #plt.title()
    plt.grid()
    plt.show()
 
if __name__ == "__main__":
    main(sys.argv[1:])