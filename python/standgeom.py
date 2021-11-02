'''
Standardize a geometry

Default file format:
geometry: xyz
          output = input.xyz
mass: 3 numbers/line
'''

import argparse
from pathlib import Path
import numpy
import FortranLibrary as FL
import basic.io

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('format', type=str, help='File format: Columbus7 or default')
    parser.add_argument('geom', type=Path, help='geometry file')
    parser.add_argument('-m','--mass', type=Path, default='mass', help='mass file (default = mass, required for default format)')
    parser.add_argument('-r','--reference', type=Path, help='reference geometry file to define a unique standard orientation')
    parser.add_argument('-o','--output', type=Path, help='output file')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    # Read geometry and mass
    if args.format == 'Columbus7':
        NAtoms, symbol, number, r, mass = basic.io.read_geom_Columbus7(args.geom)
        if args.reference != None:
            NAtoms, symbol, number, ref, mass = basic.io.read_geom_Columbus7(args.reference)
    else:
        NAtoms, symbol, r = basic.io.read_geom_xyz(args.geom)
        assert args.mass.exists(), 'Mass file is required for default format'
        mass = basic.io.read_mass(args.mass, NAtoms)
        if args.reference != None: NAtoms, symbol, ref = basic.io.read_geom_xyz(args.reference)
    ''' Do the job '''
    if args.reference == None:
        FL.StandardizeGeometry(r, mass)
    else:
        FL.StandardizeGeometry(r, mass, ref=ref)
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