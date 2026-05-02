import os
import sys
from scipy.interpolate import interpn
from mpi4py import MPI
import numpy as np
from MRI_EVP_Solver import MRI_Solver
CW = MPI.COMM_WORLD

#search for already finished cases.
Re = 6.0
myRe = 10**Re
shear = 1

neigs = 32
myrank = CW.rank
mynn = 32
#ellvals = [128,192]
ellvals = [256,384]

M = -5.5
Mstr="{:.2f}".format(M)
myM = 10**M
print(CW.size)

while shear <= 16:

    if (myrank<21):
        guesses = np.linspace(-0.03,0.03,21)
        for ii in range(4):
            for myell in ellvals:
                guess = guesses[myrank] + 0.005j*(ii+1)
                print(M,myell,guess)
                solver = MRI_Solver(shear, 0,myell,mynn,myRe,myM,neigs,guess,MPI.COMM_SELF,label='{:.4f}j_{:.4f}'.format(guess.imag,guess.real))
    else:
        guesses = 1j*np.linspace(0.03,0.14,12)
        for ii in range(4):
            for myell in ellvals:
                guess = guesses[4*(myrank-21) + ii]
                print(M,myell,guess)
                solver = MRI_Solver(shear, 0,myell,mynn,myRe,myM,neigs,guess,MPI.COMM_SELF,label='{:.4f}j_{:.4f}'.format(guess.imag,guess.real))

    shear += 1
