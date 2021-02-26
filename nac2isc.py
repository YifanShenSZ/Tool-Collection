'''
Convert nonadiabatic coupling (nac) to interstate coupling (isc)

File format:
nac & isc: 3 numbers/line
'''

import argparse
from pathlib import Path
from typing import List
import math
import numpy

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('nac', type=Path, help='nac vector file')
    parser.add_argument("e1", type=float, help="energy of lower state")
    parser.add_argument("e2", type=float, help="energy of upper state")
    parser.add_argument("-o","--output", type=Path, default=Path('isc.txt'), help='output isc vector file (default = isc.txt)')
    args = parser.parse_args()
    return args

def read_vector(file:Path) -> numpy.ndarray:
    with open(file,'r') as f: lines = f.readlines()
    n = len(lines)
    v = numpy.empty(int(3 * n))
    for i in range(n):
        temp = lines[i].split()
        v[3 * i    ] = float(temp[0].replace('D', 'e'))
        v[3 * i + 1] = float(temp[1].replace('D', 'e'))
        v[3 * i + 2] = float(temp[2].replace('D', 'e'))
    return v

def write_vector(file:Path, vector:List) -> None:
    size = len(vector)
    with open(file,'a') as f:
        n = math.ceil(int(size / 3))
        for i in range(n):
            print(('%20.14f%20.14f%20.14f')%(vector[3 * i],vector[3 * i + 1],vector[3 * i + 2]), file=f)

if __name__ == "__main__":
    args = parse_args()
    nac = read_vector(args.nac)
    nac *= args.e2 - args.e1
    write_vector(args.output, nac)
