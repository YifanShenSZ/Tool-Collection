'''
Convert geometry from internal coordinate to Cartesian coordinate
Optionally, convert gradient as well

Unit:
Length and energy are the same to your input
Angle is assumed to be in radius

Default file format:
internal coordinate definition: Fortran-Library default format
geometry: 3 numbers/line for internal coordinate, xyz for Cartesian coordinate
          output = input.xyz
gradient: 3 numbers/line
          output = input.cartgrad
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
    parser.add_argument('init', type=Path, help='initial Cartesian guess geometry file')
    parser.add_argument('-g','--grad', type=Path, help='gradient file')
    parser.add_argument('-o','--output', type=Path, help='geometry output file')
    parser.add_argument('-go','--gradoutput', type=Path, help='gradient output file')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    if args.format == 'Columbus7':
        # Define internal coordinate
        intdim, _ = FL.DefineInternalCoordinate('Columbus7', file=args.IntCoordDef)
        # Read geometry
        q = basic.io.read_geom_int(args.geom,intdim)
        # Read initial Cartesian guess geometry
        NAtoms, symbol, number, r0, mass = basic.io.read_geom_Columbus7(args.init)
        # Read gradient
        if args.grad != None: intgrad = basic.io.read_grad_int(args.grad,intdim)
    else:
        # Define internal coordinate
        intdim, _ = FL.DefineInternalCoordinate(args.format, file=args.IntCoordDef)
        # Read geometry
        q = basic.io.read_geom_int(args.geom,intdim)
        # Read initial Cartesian guess geometry
        NAtoms, symbol, r0 = basic.io.read_geom_xyz(args.init)
        # Read gradient
        if args.grad != None: intgrad = basic.io.read_grad_int(args.grad,intdim)
    ''' Do the job '''
    cartdim = 3*NAtoms; r = numpy.empty(cartdim)
    if args.grad == None:
        FL.CartesianCoordinate(q, r, r0=r0)
    else:
        cartgrad = numpy.empty(cartdim)
        FL.Internal2Cartesian(q, intgrad, r, cartgrad, r0=r0)
    ''' Output '''
    if args.format == 'Columbus7':
        if args.output == None:
            basic.io.write_geom_Columbus7(Path('geom'), NAtoms, symbol, number, r, mass)
        else:
            basic.io.write_geom_Columbus7(args.output, NAtoms, symbol, number, r, mass)
        if args.grad != None:
            if args.gradoutput == None:
                basic.io.write_grad_cart(Path('cartgrd'), cartgrad)
            else:
                basic.io.write_grad_cart(args.gradoutput, cartgrad)
    else:
        if args.output == None:
            basic.io.write_geom_xyz(Path(str(args.geom)+'.xyz'), NAtoms, symbol, r)
        else:
            basic.io.write_geom_xyz(args.output, NAtoms, symbol, r)
        if args.grad != None:
            if args.gradoutput == None:
                basic.io.write_grad_cart(Path(str(args.grad)+'.cartgrad'), cartgrad)
            else:
                basic.io.write_grad_cart(args.gradoutput, cartgrad)