'''
Rotate a geometry

The rotation is defined by:
rotating alpha along axis
axis = [sin(theta)cos(phi), sin(theta)sin(phi), cos(theta)]

Default file format: 
geometry: xyz
          output = input.xyz
'''

import argparse
from pathlib import Path
import math; import numpy
import FortranLibrary as FL
import basic.io

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('format', type=str, help='File format: Columbus7 or default')
    parser.add_argument('geom', type=Path, help='geometry file')
    parser.add_argument('alpha', type=float)
    parser.add_argument('theta', type=float)
    parser.add_argument('phi'  , type=float)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    if args.format == 'Columbus7':
        NAtoms, symbol, number, r, mass = basic.io.read_geom_Columbus7(args.geom)
    else:
        NAtoms, symbol, r = basic.io.read_geom_xyz(args.geom)
    ''' Do the job '''
    q = numpy.empty(4)
    sintheta = math.sin(args.theta)
    q[0] = math.cos(args.alpha/2.0)
    q[1] = math.sin(args.alpha/2.0) * sintheta * math.cos(args.phi)
    q[2] = math.sin(args.alpha/2.0) * sintheta * math.sin(args.phi)
    q[3] = math.sin(args.alpha/2.0) * math.cos(args.theta)
    FL.Rotate(q, r)
    ''' Output '''
    if args.format == 'Columbus7':
        if args.output == None:
            basic.io.write_geom_Columbus7(Path('geom'), NAtoms, symbol, number, r, mass)
        else:
            basic.io.write_geom_Columbus7(args.output, NAtoms, symbol, number, r, mass)
    else:
        if args.output == None:
            basic.io.write_geom_xyz(Path(str(args.geom)+'.xyz'), NAtoms, symbol, r)
        else:
            basic.io.write_geom_xyz(args.output, NAtoms, symbol, r)