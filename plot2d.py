'''
Plot all kinds of 2-dimensional figures

File format:
data: default, 2 numbers/line = (x,y)
      with -m, multiple numbers/line, each column will be plotted as a series
x: refered only with -m, 1 number/line
'''

import argparse
from pathlib import Path
import numpy
import basic.io
import basic.visualization

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-m','--multiple', action='store_true', help='plot multiple series')
    parser.add_argument('-x', type=Path, help='x file')
    parser.add_argument('data', type=Path, help='data file')
    parser.add_argument('-zp','--zero_point', type=float, default=0, help='y -= zero_point (default = 0)')
    parser.add_argument('-s','--scale', type=float, default=1, help='y *= scale (after zero point shift) (default = 1)')
    parser.add_argument('-t','--title', type=str, default=' ', help='default = ')
    parser.add_argument('-xl','--xlabel', type=str, default='x', help='default = x')
    parser.add_argument('-yl','--ylabel', type=str, default='y', help='default = y')
    parser.add_argument('-pt','--PlotType', type=str, default='line', help='line or scatter (default = line)')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    ''' Do the job '''
    if args.multiple:
        # Read y
        y  = basic.io.read_matrix(args.data)
        y -= args.zero_point
        y *= args.scale
        # Read x
        if args.x == None:
            x = numpy.array(range(y.shape[0]))
        else:
            x = basic.io.read_vector_1(args.x)
        # Plot
        basic.visualization.Plot2D(x, y.transpose(),
        title=args.title, xlabel=args.xlabel, ylabel=args.ylabel,
        PlotType=args.PlotType)
    else:
        # Read (x,y)
        x, y = basic.io.read_2vectors(args.data)
        # Plot
        basic.visualization.Plot2D(x, y,
        title=args.title, xlabel=args.xlabel, ylabel=args.ylabel,
        PlotType=args.PlotType)