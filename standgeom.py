"""
Standardize a geometry

Default file format: 
geometry: xyz
mass: 3 numbers/line
"""

''' Library '''
import argparse
from pathlib import Path
import numpy
import FortranLibrary as FL
import basic

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
    # Command line input
    args = parse_args()
    if args.format == 'Columbus7':
        NAtoms, symbol, number, r, mass = basic.read_geom_Columbus7(args.geom)
    else:
        NAtoms, symbol, r = basic.read_geom_xyz(args.geom)
        assert args.mass.exists(), 'Mass file is required for default format'
        mass = basic.read_mass(args.mass, NAtoms)
    ''' Do the job '''
    FL.StandardizeGeometry(r, mass)
    ''' Output '''
    if args.format == 'Columbus7':
        if args.output == None:
            basic.write_geom_Columbus7(Path('geom'), NAtoms, symbol, number, r, mass)
        else:
            basic.write_geom_Columbus7(args.output, NAtoms, symbol, number, r, mass)
    else:
        if args.output == None:
            basic.write_geom_xyz(Path(str(args.geom)+'.xyz'), NAtoms, symbol, r)
        else:
            basic.write_geom_xyz(args.output, NAtoms, symbol, r)