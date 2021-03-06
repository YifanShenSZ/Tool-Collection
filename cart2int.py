'''
Convert geometry from Cartesian coordinate to internal coordinate
Optionally, convert gradient as well

Unit:
Length and energy are the same to your input
Angle is in radius

Default file format: 
internal coordinate definition: Fortran-Library default format
geometry: xyz for Cartesian coordinate, 3 numbers/line for internal coordinate
          output = input.intgeom
gradient: 3 numbers/line
          output = input.intgrad
'''

import argparse
from pathlib import Path
import numpy
import FortranLibrary as FL
import basic.io

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('format', type=str, help='File format: Columbus7 or default')
    parser.add_argument('IntCoordDef', type=Path, help='internal coordinate definition file')
    parser.add_argument('geom', type=Path, help='geometry file')
    parser.add_argument('-g','--grad', type=Path, help='gradient file')
    parser.add_argument('-o','--output', type=Path, help='geometry output file')
    parser.add_argument('-go','--gradoutput', type=Path, help='gradient output file')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    # Define internal coordinate
    intdim, _ = FL.DefineInternalCoordinate(args.format, file=args.IntCoordDef)
    # Read geometry
    if args.format == 'Columbus7':
        NAtoms, symbol, number, r, mass = basic.io.read_geom_Columbus7(args.geom)
    else:
        NAtoms, symbol, r = basic.io.read_geom_xyz(args.geom)
    if args.grad != None: cartgrad = basic.io.read_grad_cart(args.grad)
    ''' Do the job '''
    cartdim=3*NAtoms; q = numpy.empty(intdim)
    if args.grad == None:
        FL.InternalCoordinate(r, q)
    else:
        intgrad = numpy.empty(intdim)
        FL.Cartesian2Internal(r, cartgrad, q, intgrad)
    ''' Output '''
    if args.format == 'Columbus7':
        if args.output == None:
            with open('intgeom','a') as f:
                for i in range(intdim): print('%14.8f'%q[i], file=f)
        else:
            with open(args.output,'a') as f:
                for i in range(intdim): print('%14.8f'%q[i], file=f)
        if args.grad != None:
            if args.gradoutput == None:
                with open('intgrd','a') as f:
                    for i in range(intdim): print('%14.8f'%intgrad[i], file=f)
            else:
                with open(args.gradoutput,'a') as f:
                    for i in range(intdim): print('%14.8f'%intgrad[i], file=f)
    else:
        if args.output == None:
            basic.io.write_geom_int(Path(str(args.geom)+'.intgeom'), q)
        else:
            basic.io.write_geom_int(args.output, q)
        if args.grad != None:
            if args.gradoutput == None:
                basic.io.write_grad_int(Path(str(args.grad)+'.intgrad'), intgrad)
            else:
                basic.io.write_grad_int(args.gradoutput, intgrad)