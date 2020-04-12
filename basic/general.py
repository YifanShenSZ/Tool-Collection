'''
This is one of the basics of Tool-Collection

General basic constants and routines
'''

from pathlib import Path
from typing import List
import numpy; import numpy.linalg

AMUInAU  = 1822.888486192
AInAU    = 1.8897261339212517
cm_1InAU = 0.000004556335830019422
AUIncm_1 = 219474.60356444737
AUIneV   = 27.2114
fsInAU   = 41.341373336561354

# take in numpy.array x and tolerance tol
# return the indice list of elements with absolute value > tol
def Pick_Significant(x:numpy.ndarray, tol:float) -> List:
    indice=[]
    for i in range(x.shape[0]):
        if abs(x[i]) > tol: indice.append(i)
    return indice

# vector a & b, return a b
def vector_direct_product(a:numpy.ndarray, b:numpy.ndarray) -> numpy.ndarray:
    m = a.shape[0]; n = b.shape[0]; c = numpy.empty((m,n))
    for i in range(m):
        for j in range(n): c[i,j] = a[i] * b[j]
    return c

# 3 x NAtoms matrix geom, NAtoms dimensional numpy.array mass
# Return eigenvalues and eigenvectors of moment of inertia tensor in centre of mass frame
def MomentOfInertia(geom:numpy.ndarray, mass:numpy.ndarray) -> (numpy.ndarray, numpy.ndarray):
    # Get centre of mass
    com = numpy.zeros(3)
    totalmass = 0.0
    for i in range(mass.shape[0]):
        com += mass[i] * geom[:,i]
        totalmass += mass[i]
    com /= totalmass
    # Move to centre of mass frame, compute momentum of inertia tensor
    r = geom.copy()
    moi = numpy.zeros((3,3))
    for i in range(mass.shape[0]):
        r[:,i] -= com
        moi += mass[i]*(sum(r[:,i]*r[:,i])*numpy.identity(3)-vector_direct_product(r[:,i],r[:,i]))
    eigval, eigvec = numpy.linalg.eig(moi)
    return eigval, eigvec

if __name__ == "__main__": print(__doc__)