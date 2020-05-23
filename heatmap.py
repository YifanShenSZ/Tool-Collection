'''
Plot a heat map

File format:
xy: 2 numbers/line (x, y)
z:  n numbers/line, each column will be plotted as a heat map
    if xy is present: the ordering of data will be infered from xy
    else: number of lines must be a perfect square
          ordering e.g. 2 x 2 case, z[0,0], z[0,1], z[1,0], z[1,1] 
'''

import argparse
from pathlib import Path
import numpy as numpy
import matplotlib.pyplot as plt
import basic.io
import basic.visualization

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-xy', type=Path, help='xy file')
    parser.add_argument(  'z', type=Path, help= 'z file')
    parser.add_argument('ZeroPoint_z', nargs='?', type=float, default=0, help='z -= ZeroPoint_z (default = 0)')
    parser.add_argument('-sz','--scale_z', type=float, default=1, help='z *= scale_z (after zero point shift) (default = 1)')
    parser.add_argument('-t','--title', type=str, default=' ', help='default = ')
    parser.add_argument('-lx','--label_x', type=str, default='x', help='default = x')
    parser.add_argument('-ly','--label_y', type=str, default='y', help='default = y')
    parser.add_argument('-cm','--color_map', type=str, default='inferno', help='default = inferno')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    # Read z
    z_raw = basic.io.read_matrix(args.z)
    z_raw -= args.ZeroPoint_z
    z_raw *= args.scale_z
    # Read xy
    if args.xy == None:
        n = int(numpy.sqrt(z_raw.shape[0]))
        assert float(n) == numpy.sqrt(z_raw.shape[0])
        x = numpy.array(range(n))
        y = numpy.array(range(n))
        z = numpy.empty((z_raw.shape[1], n, n))
        index = 0
        for i in range(n):
            for j in range(n):
                for k in range(z_raw.shape[1]):
                    z[k, j, i] = z_raw[index, k]
                index += 1
    else:
        xy = basic.io.read_matrix(args.xy)
        assert xy.shape[1] == 2
        x, xlist = numpy.unique(xy[:,0], return_inverse=True)
        y, ylist = numpy.unique(xy[:,1], return_inverse=True)
        z = numpy.empty((z_raw.shape[1], y.shape[0], x.shape[0]))
        for i in range(z_raw.shape[0]):
            for j in range(z_raw.shape[1]):
                z[j, ylist[i], xlist[i]] = z_raw[i, j]
    for i in range(z.shape[0]):
        basic.visualization.Plot3D(x, y, z[i,:,:],
        title=args.title, xlabel=args.label_x, ylabel=args.label_y,
        PlotType='heatmap', colormap=args.color_map)
