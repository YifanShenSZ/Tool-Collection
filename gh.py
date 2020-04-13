'''
Orthogonalize g & h vectors
Optionally, produce a file with geometry + g & h vectors visualizable in Avogadro

File format:
geometry: xyz
gradient: 3 numbers/line
'''

import argparse
from pathlib import Path
import numpy
import FortranLibrary as FL
import basic.io

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('grad1', type=Path, help='state 1 energy gradient file')
    parser.add_argument('grad2', type=Path, help='state 2 energy gradient file')
    parser.add_argument('h',     type=Path, help='interstate coupling file')
    parser.add_argument('-go','--goutput', type=Path, default='g.cartgrad', help='g output file (default = g.cartgrad)')
    parser.add_argument('-ho','--houtput', type=Path, default='h.cartgrad', help='h output file (default = h.cartgrad)')
    parser.add_argument('-g','--geom', type=Path, help='geometry file')
    parser.add_argument('-o','--output', type=Path, default='mex.log', help='geometry + g & h vectors output file (default = mex.log)')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    # Read gradient
    grad1 = basic.io.read_grad_cart(args.grad1)
    grad2 = basic.io.read_grad_cart(args.grad2)
    h     = basic.io.read_grad_cart(args.h    )
    if args.geom != None: NAtoms, symbol, r = basic.io.read_geom_xyz(args.geom)
    ''' Do the job '''
    FL.ghOrthogonalization(grad1, grad2, h)
    ''' Output '''
    g = (grad2 - grad1) / 2.0
    basic.io.write_grad_cart(args.goutput, g)
    basic.io.write_grad_cart(args.houtput, h)
    if args.geom != None:
        freq = numpy.array([1000.0,2000.0])
        # Here we use infinity-norm to normalize g & h vectors to 9.99
        # since the visualization file format is %5.2f
        modeT = numpy.empty((2,g.shape[0]))
        modeT[0,:] = 9.99 * g / numpy.amax(numpy.abs(g))
        modeT[1,:] = 9.99 * h / numpy.amax(numpy.abs(h))
        FL.Avogadro_Vibration(symbol, r, freq, modeT, file=args.output)