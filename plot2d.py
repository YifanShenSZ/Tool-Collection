'''
Plot all kinds of 2-dimensional figures

File format:
data: default, N + 1 numbers/line = (x, y1, y2, ..., yN)
      with --no_x, N numbers/line = (y1, y2, ..., yN)
x: refered only with --no_x, 1 number/line
'''

import argparse
from pathlib import Path
import numpy
import basic.io
import basic.visualization

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    # data file reading control
    parser.add_argument('data', type=Path, help='data file')
    parser.add_argument('-t','--title', action='store_true', help='there is a title line in the data file')
    parser.add_argument('-n','--no_x', action='store_true', help='x is not stored in the data file')
    parser.add_argument('-x', type=Path, help='x file')
    # data modification
    parser.add_argument('-zp','--zero_point', type=float, default=0, help='y -= zero_point (default = 0)')
    parser.add_argument('-s','--scale', type=float, default=1, help='y *= scale (after zero point shift) (default = 1)')
    # plot style
    parser.add_argument('-xl','--xlabel', type=str, default='x', help='default = x')
    parser.add_argument('-yl','--ylabel', type=str, default='y', help='default = y')
    parser.add_argument('-pt','--PlotType', type=str, default='line', help='line or scatter (default = line)')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    ''' Do the job '''
    # Read data
    if args.no_x:
        # Read y
        y  = basic.io.read_matrix(args.data, args.title)
        # Read x
        if args.x == None:
            x = numpy.array(range(y.shape[0]))
        else:
            x = basic.io.read_vector_1(args.x)
    else:
        # Read (x,y)
        temp = basic.io.read_matrix(args.data, args.title)
        x = temp[:, 0]
        y = temp[:, 1:]
    # Modify data
    y -= args.zero_point
    y *= args.scale
    # Plot
    basic.visualization.Plot2D(x, y.transpose(),
    xlabel=args.xlabel, ylabel=args.ylabel,
    PlotType=args.PlotType)