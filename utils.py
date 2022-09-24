#!/usr/bin/env python3

def selectPoint(ax, xmin, x, ymin, y):
    ax.vlines(x=x, ymin=ymin, ymax=y, colors = 'blue', linestyles='dashed')
    ax.hlines(y=y, xmin=xmin, xmax=x, colors = 'blue', linestyles='dashed')
    ax.text(x*0.99, y*0.9, "({:.3f},{:.3f})".format(x,y))