'''
Plot all kinds of 2-dimensional figures

File format:
x: 1 number/line
y: n numbers/line, each column will be plotted as a series
'''

import argparse
from pathlib import Path
import numpy
import basic.io
import basic.visualization

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-x', type=Path, help='x file')
    parser.add_argument( 'y', type=Path, help='y file')
    parser.add_argument('ZeroPoint_y', nargs='?', type=float, default=0, help='y -= ZeroPoint_y (default = 0)')
    parser.add_argument('-sy','--scale_y', type=float, default=1, help='y *= scale_y (after zero point shift) (default = 1)')
    parser.add_argument('-t','--title', type=str, default=' ', help='default = ')
    parser.add_argument('-lx','--label_x', type=str, default='x', help='default = x')
    parser.add_argument('-ly','--label_y', type=str, default='y', help='default = y')
    parser.add_argument('-c','--color', type=str, default='black', help='default = black')
    parser.add_argument('-pt','--PlotType', type=str, default='scatter', help='scatter or line (default = scatter)')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    # Read y
    y  = basic.io.read_matrix(args.y)
    y -= args.ZeroPoint_y
    y *= args.scale_y
    # Read x
    if args.x == None:
        x = numpy.array(range(y.shape[0]))
    else:
        x = basic.io.read_vector_1(args.x)
        assert x.shape[0] == y.shape[0]
    ''' Do the job '''
    basic.visualization.Plot2D(x, y.transpose(),
    args.title, args.label_x, args.label_y, args.color, args.PlotType)
