# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:16:24 2019

@author: pc-labview
"""

import numpy as np
import random as rd




f=open("permutation.dat","w")   

L=30
permutation=np.arange(L)
rd.shuffle(permutation)

for i in range(L):
    f.write(str(permutation[i]))
    if (i!=L-1):
        f.write("\n")
#
#
f.close()