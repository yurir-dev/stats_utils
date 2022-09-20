
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

def validInterval(range_):
    return range_[0] < range_[1]

def main(argv):
   
    try:
      opts, args = getopt.getopt(argv,"hvm:s:a:d:p:s:",["help", "verbose", "mean=","std=", "samples=", "area_range=", "percentile=", "desc="])
    except getopt.GetoptError as ex:
      usage(ex)
      sys.exit(2)
    
    mean, std = 0, 1
    area_range = [0, -1]
    desc = ""
    verbose = False
    percentile = 0
    for opt, arg in opts:
        try:
            if opt in ('-h', '--help'):
                usage()
                sys.exit()
            elif opt in ('-s', '--samples'):
                rng = arg.split(',')
                arr = np.array([float(x) for x in rng])
                mean, std = np.mean(arr, axis=0), np.std(arr, axis=0)
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
            elif opt in ("-p", "--percentile"):
                percentile = float(arg)
                if percentile < 0 or percentile > 1.0:
                    raise Exception("invalid percentile {} , should be in range (0, 1)".format(percentile))
        except Exception as ex:
            usage("failed to parse argv - {}".format(ex))
            sys.exit(3)

    if verbose:
        print('Argument List: {}'.format(sys.argv))
        print("mean = {}, std = {}, area_range = {}, desc = {}".format(mean, std, area_range, desc))
    
    if not desc:
        desc = "normal distribution: mean {} , std {}".format(mean, std)
    
    fig, (axNrm, axCdf, axQuantil) = plt.subplots(3, 1)
    
    x_min, x_max = mean -std * 6, mean + std * 6
    x = np.linspace(x_min, x_max, 100)
    y = normal_distribution_function(x, mean, std)
    axNrm.grid()
    axNrm.plot(x, y, color='red')
    
    y = scipy.stats.norm.cdf(x, loc=mean, scale=std)
    axCdf.grid()
    axCdf.plot(x, y, color='red')
    axCdf.set_title('cdf', y=0.5, x=0.95, pad=-14)

    x = np.linspace(0, 1, 100)
    y = scipy.stats.norm.ppf(x, loc=mean, scale=std)
    axQuantil.plot(x, y, 'r-', lw=1, alpha=1.0)
    axQuantil.set_title('quantile', y=1.0, pad=-14)
    
    #pdb.set_trace()
    if percentile > 0 :
        x1 = (1.0 - percentile) / 2.0
        x2 = 1.0 - x1
        y1 = scipy.stats.norm.ppf(x1, loc=mean, scale=std)
        y2 = scipy.stats.norm.ppf(x2, loc=mean, scale=std)
        axQuantil.set_title('quantile {} - {:.3f}:{:.3f}'.format(percentile, y1, y2), y=1.0, pad=-14)
        
        area_range = [y1, y2]
    
    if validInterval(area_range):
        x1, x2 = area_range[0], area_range[1]
        ptx = np.linspace(x1, x2, 100)
        pty = normal_distribution_function(ptx, mean, std)
        axNrm.fill_between(ptx, pty, color='#0b559f', alpha=1.0)
        
        res, err = quad(normal_distribution_function, x1, x2, args=(mean,std,))
        desc += " - [{:.3f},{:.3f}] = {}".format(x1, x2, res) 
        
        if verbose:
            print('Integration between {} and {} --> {} , with absolute error {}'.format(x1, x2, res, err))

        #pdb.set_trace()
        #x = np.linspace(scipy.stats.norm.ppf(0.01, loc=mean, scale=std), x1, 2)
        #yLow = [scipy.stats.norm.cdf(x1, loc=mean, scale=std) for _ in x]
        #axCdf.plot(x, yLow, 'b-', lw=1.5, alpha=1.0)
        #axCdf.vlines(x=x1, ymin=0, ymax=scipy.stats.norm.cdf(x1, loc=mean, scale=std), colors = 'blue')
        
        #x = np.linspace(scipy.stats.norm.ppf(0.01, loc=mean, scale=std), x2, 2)
        #yHigh = [scipy.stats.norm.cdf(x2, loc=mean, scale=std) for _ in x]
        #axCdf.plot(x, yHigh, 'b-', lw=1, alpha=1.0)
        #axCdf.vlines(x=x2, ymin=0, ymax=scipy.stats.norm.cdf(x2, loc=mean, scale=std), colors = 'blue')
        #
        #axCdf.vlines(x=beta.ppf(0.01, a, b), ymin=beta(a, b).cdf(x1), ymax=beta(a, b).cdf(x2), colors = 'red', linestyles='dotted')

    
    axNrm.title.set_text(desc)
    
    plt.grid()
    plt.show()
 
if __name__ == "__main__":
    main(sys.argv[1:])