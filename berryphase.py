'''
Calculate berry phase of a 2-state conical intersection from:
    g & h vectors
    a mesh in g-h plane

File format:
g & h: 3 numbers/line
mesh_gh: 2 numbers/line (g, h)
'''

import argparse
from pathlib import Path
import numpy
import basic.io

def parse_args() -> argparse.Namespace: # Command line input
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('g', type=Path, help='g vector file')
    parser.add_argument('h', type=Path, help='h vector file')
    parser.add_argument('mesh_gh', type=Path, help='mesh grids coordinates (g, h) file')
    parser.add_argument('mesh_nac', type=Path, help='mesh grids nonadiabatic coupling file')
    parser.add_argument('-me','--mesh_energy', type=Path, help='mesh grids energy file, presence means isc is provided instead of nac')
    parser.add_argument('-s','--state', type=int, help=
    'the upper state of the conical intersection (refered only with mesh_energy, default = highest)')
    parser.add_argument('-i','--inner_loop', type=int, default=0, help=
    'use the outmost - inner_loop edges as integral contour (default = 0)')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    ''' Initialize '''
    args = parse_args()
    # Read g & h
    g_unit = basic.io.read_grad_cart(args.g); g_unit /= numpy.linalg.norm(g_unit)
    h_unit = basic.io.read_grad_cart(args.h); h_unit /= numpy.linalg.norm(h_unit)
    dim = g_unit.shape[0]
    # Read mesh_gh
    mesh_gh = basic.io.read_matrix(args.mesh_gh)
    assert mesh_gh.shape[1] == 2
    NGrids = mesh_gh.shape[0]
    # Read mesh_nac
    mesh_nac_raw = basic.io.read_grad_cart(args.mesh_nac)
    mesh_nac_raw = mesh_nac_raw.reshape((NGrids, dim))
    if args.mesh_energy != None:
        mesh_energy = basic.io.read_matrix(args.mesh_energy)
        assert mesh_energy.shape[0] == NGrids
        if args.state == None: args.state = mesh_energy.shape[1] - 1
        for i in range(NGrids): mesh_nac_raw[i,:] /= mesh_energy[i,args.state] - mesh_energy[i,args.state-1]
    # Sort mesh
    g, glist = numpy.unique(mesh_gh[:,0], return_inverse=True)
    h, hlist = numpy.unique(mesh_gh[:,1], return_inverse=True)
    assert g.shape[0] * h.shape[0] == NGrids
    mesh_nac = numpy.empty((g.shape[0], h.shape[0], dim))
    for i in range(NGrids): mesh_nac[glist[i], hlist[i], :] = mesh_nac_raw[i, :]
    ''' Do the job '''
    phase = 0.0
    z = args.inner_loop
    m = mesh_nac.shape[0] - 1 - z
    n = mesh_nac.shape[1] - 1 - z
    # Up edge
    phase += mesh_nac[z,z,:].dot(h_unit) * (h[z+1] - h[z]) / 2.0
    for i in range(z+1, n):
        phase += mesh_nac[z,i,:].dot(h_unit) * (h[i+1] - h[i-1]) / 2.0
    phase += mesh_nac[z,n,:].dot(h_unit) * (h[n] - h[n-1]) / 2.0
    # Right edge
    phase += mesh_nac[z,n,:].dot(g_unit) * (g[z+1] - g[z]) / 2.0
    for i in range(z+1, m):
        phase += mesh_nac[i,n,:].dot(g_unit) * (g[i+1] - g[i-1]) / 2.0
    phase += mesh_nac[m,n,:].dot(g_unit) * (g[m] - g[m-1]) / 2.0
    # Low edge
    phase -= mesh_nac[m,z,:].dot(h_unit) * (h[z+1] - h[z]) / 2.0
    for i in range(z+1, n):
        phase -= mesh_nac[m,i,:].dot(h_unit) * (h[i+1] - h[i-1]) / 2.0
    phase -= mesh_nac[m,n,:].dot(h_unit) * (h[n] - h[n-1]) / 2.0
    # Left edge
    phase -= mesh_nac[z,z,:].dot(g_unit) * (g[z+1] - g[z]) / 2.0
    for i in range(z+1, m):
        phase -= mesh_nac[i,z,:].dot(g_unit) * (g[i+1] - g[i-1]) / 2.0
    phase -= mesh_nac[m,z,:].dot(g_unit) * (g[m] - g[m-1]) / 2.0
    print(phase)
