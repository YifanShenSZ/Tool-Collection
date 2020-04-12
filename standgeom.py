"""
Standardize a geometry

Default file format:
geometry: xyz
          output = input.xyz
mass: 3 numbers/line
"""

''' Library '''
import argparse
from pathlib import Path
import numpy
import FortranLibrary as FL
import basic.io

''' Routine '''
def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('format', type=str, help='File format: Columbus7 or default')
    parser.add_argument('geom', type=Path, help='geometry file')
    parser.add_argument('-m','--mass', type=Path, default='mass', help='mass file (default = mass, required for default format)')
    parser.add_argument('-o','--output', type=Path, help='output file')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    # Read geometry and mass
    if args.format == 'Columbus7':
        NAtoms, symbol, number, r, mass = basic.io.read_geom_Columbus7(args.geom)
    else:
        NAtoms, symbol, r = basic.io.read_geom_xyz(args.geom)
        assert args.mass.exists(), 'Mass file is required for default format'
        mass = basic.io.read_mass(args.mass, NAtoms)
    ''' Do the job '''
    FL.StandardizeGeometry(r, mass)
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