'''
Calculate the 2-norms of vectors

File format:
vecs: 3 numbers/line, as the concatenation of vectors
'''

import argparse
from pathlib import Path
import numpy

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("vecs", type=Path, help="vectors file")
    parser.add_argument("dim", type=int, help="dimension of a vector")
    parser.add_argument("-o","--output", type=Path, default=Path('norms.txt'), help="norms output (default = norms.txt)")
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

if __name__ == "__main__":
    args = parse_args()
    cated_vecs = read_vector(args.vecs)
    NVecs = int(cated_vecs.shape[0] / args.dim)
    vecs = cated_vecs.reshape((NVecs, args.dim))
    with open(args.output, 'w') as f:
        for i in range(NVecs):
            print(numpy.linalg.norm(vecs[i,:]), file=f)
