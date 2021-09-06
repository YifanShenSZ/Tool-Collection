'''
Normalize a vector
'''

import argparse
from pathlib import Path
from typing import List
import numpy

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('v', type=Path, help='vector file')
    parser.add_argument("-o","--output", type=Path, default=Path('unit'), help='output vector file (default = unit)')
    args = parser.parse_args()
    return args

# Read a vector from file
def read_vector(file:Path) -> numpy.ndarray:
    with open(file,'r') as f: lines = f.readlines()
<<<<<<< HEAD
    v = []
    for line in lines:
        strs = line.split()
        for string in strs:
            v.append(float(string))
    return numpy.array(v)
=======
    l = []
    for line in lines:
        strs = line.split()
        for str in strs: l.append(float(str))
    return numpy.array(l)
>>>>>>> fa523aad426a1471bb5c2c9a2c7311720c2e916c
# Write a vector to file (1 number/line)
def write_vector(file:Path, vector:List) -> numpy.ndarray:
    with open(file,'w') as f:
        for el in vector: print(el, file=f)

if __name__ == "__main__":
    args = parse_args()
    v = read_vector(args.v)
    norm = numpy.linalg.norm(v)
    print("Norm = ", norm)
    v /= norm
    write_vector(args.output, v)