#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import pdb
import math
from scipy.integrate import quad
import scipy.stats



def main(argv):
    k = range(2, 100)
    p = [1 - (364/365)**math.comb(i, 2) for i in k]

    plt.plot(k, p, color='red')
    plt.title("two persons have the same birthday")
    plt.grid()
    plt.show()
   
if __name__ == "__main__":
    main(sys.argv[1:])