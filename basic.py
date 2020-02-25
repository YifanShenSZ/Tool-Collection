"""
General basic routines for Tool-Collection
"""

''' Library '''
from pathlib import Path
from typing import List
import math; import numpy

''' Routine '''
# Read Columbus7 geometry file, return:
#     NAtoms (number of atoms)
#     symbol (element symbol of each atom)
#     number (element number of each atom)
#     r      (Cartesian coordinate in Bohr)
#     mass   (mass of each atom in atomic mass unit)
def read_geom_Columbus7(GeomFile:Path) -> (int, numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray):
    with open(GeomFile,'r') as f: lines=f.readlines()
    NAtoms = len(lines)
    symbol = numpy.empty(NAtoms,dtype=str)
    number = numpy.empty(NAtoms)
    r      = numpy.empty(int(3*NAtoms))
    mass   = numpy.empty(NAtoms)
    for i in range(NAtoms):
        temp = lines[i].split()
        symbol[i] = temp[0].strip()
        number[i] = float(temp[1])
        r[3*i  ]  = float(temp[2])
        r[3*i+1]  = float(temp[3])
        r[3*i+2]  = float(temp[4])
        mass[i]   = float(temp[5])
    return NAtoms, symbol, number, r, mass

# Inverse to read_geom_Columbus7
def write_geom_Columbus7(GeomFile:Path, NAtoms:int, symbol:List, number:List, r:List, mass:List) -> None:
    with open(GeomFile,'a') as f:
        for i in range(NAtoms):
            print((' %2s  %5.1f%14.8f%14.8f%14.8f%14.8f')%\
                (symbol[i],number[i],r[3*i],r[3*i+1],r[3*i+2],mass[i]),file=f)

# Read xyz file, return:
#     NAtoms (number of atoms)
#     symbol (element symbol of each atom)
#     r      (Cartesian coordinate in angstrom)
def read_geom_xyz(GeomFile:Path) -> (int, numpy.ndarray, numpy.ndarray):
    with open(GeomFile,'r') as f: lines=f.readlines()
    NAtoms = int(lines[0])
    symbol = numpy.empty(NAtoms,dtype=str)
    r      = numpy.empty(int(3*NAtoms))
    for i in range(NAtoms):
        temp = lines[i+2].split()
        symbol[i] = temp[0].strip()
        r[3*i  ]  = float(temp[1])
        r[3*i+1]  = float(temp[2])
        r[3*i+2]  = float(temp[3])
    return NAtoms, symbol, r

# Inverse to read_geom_xyz
def write_geom_xyz(GeomFile:Path, NAtoms:int, symbol:List, r:List) -> None:
    with open(GeomFile,'a') as f:
        print(NAtoms,file=f)
        print(file=f)
        for i in range(NAtoms): print(('%2s%20.14f%20.14f%20.14f')%\
            (symbol[i],r[3*i],r[3*i+1],r[3*i+2]),file=f)

# Read internal coordinate vector file (3 numbers/line)
def read_vector_int(GeomFile:Path, intdim:int) -> numpy.ndarray:
    with open(GeomFile,'r') as f: lines=f.readlines()
    vector = numpy.empty(intdim)
    n = len(lines); m = intdim % 3
    for i in range(n-1):
        temp = lines[i].split()
        vector[3*i  ] = float(temp[0])
        vector[3*i+1] = float(temp[1])
        vector[3*i+2] = float(temp[2])
    if m == 0:
        temp = lines[n-1].split()
        vector[intdim-3] = float(temp[0])
        vector[intdim-2] = float(temp[1])
        vector[intdim-1] = float(temp[2])
    elif m == 1:
        vector[intdim-1] = float(lines[n-1])
    else: # 2
        temp = lines[n-1].split()
        vector[intdim-2] = float(temp[0])
        vector[intdim-1] = float(temp[1])
    return vector

# Inverse to read_vector_int
def write_vector_int(GeomFile:Path, vector:List) -> None:
    intdim = len(vector)
    with open(GeomFile,'a') as f:
        n = math.ceil(int(intdim/3)); m = intdim % 3
        for i in range(n-1):
            print(('%20.14f%20.14f%20.14f')%(vector[3*i],vector[3*i+1],vector[3*i+2]), file=f)
        if m == 0:
            print(('%20.14f%20.14f%20.14f')%(vector[intdim-3],vector[intdim-2],vector[intdim-1]), file=f)
        elif m == 1:
            print('%20.14f'%vector[intdim-1], file=f)
        else: # 2
            print(('%20.14f%20.14f')%(vector[intdim-2],vector[intdim-1]), file=f)

# Read mass file (3 numbers/line)
def read_mass(MassFile:Path, NAtoms:int) -> numpy.ndarray:
    with open(MassFile,'r') as f: lines=f.readlines()
    mass = numpy.empty(NAtoms)
    n = len(lines); m = NAtoms % 3
    for i in range(n-1):
        temp = lines[i].split()
        mass[3*i  ] = float(temp[0])
        mass[3*i+1] = float(temp[1])
        mass[3*i+2] = float(temp[2])
    if m == 0:
        temp = lines[n-1].split()
        mass[NAtoms-3] = float(temp[0])
        mass[NAtoms-2] = float(temp[1])
        mass[NAtoms-1] = float(temp[2])
    elif m == 1:
        mass[NAtoms-1] = float(lines[n-1])
    else: # 2
        temp = lines[n-1].split()
        mass[NAtoms-2] = float(temp[0])
        mass[NAtoms-1] = float(temp[1])
    return mass

# Read gradient file, return grad (Cartesian coordinate)
def read_grad(GradFile:Path) -> numpy.ndarray:
    with open(GradFile,'r') as f: lines=f.readlines()
    n = len(lines)
    grad = numpy.empty(int(3*n))
    for i in range(n):
        temp = lines[i].split()
        grad[3*i  ] = float(temp[0].replace('D','e'))
        grad[3*i+1] = float(temp[1].replace('D','e'))
        grad[3*i+2] = float(temp[2].replace('D','e'))
    return grad

# Inverse to read_grad
def write_grad(GradFile:Path, grad:numpy.ndarray) -> None:
    with open(GradFile,'a') as f:
        for i in range(int(grad.shape[0]/3)): print(('%20.14f%20.14f%20.14f')%\
            (grad[3*i],grad[3*i+1],grad[3*i+2]),file=f)