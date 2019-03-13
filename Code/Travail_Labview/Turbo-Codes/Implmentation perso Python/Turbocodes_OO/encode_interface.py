#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 10:28:21 2019

@author: root
"""

from Encoders import UMTS_Encoder

import numpy as np
import random as rd






encoder=UMTS_Encoder()
import sys

#lecture permutation
f=open("permutation.dat","r")    
permutation=[int(line) for line in f]



message=[-99]
#on suppose que tous les bits sont concaténés
seq=str(sys.argv[1])
for i in range(len(seq)):
    message+=[int(seq[i])]
 
message=np.array(message)

L=len(message)-1

permutation=np.arange(L)
rd.shuffle(permutation)

f=open("permutation.dat","w")   
for i in range(L):
    f.write(str(permutation[i]))
    if (i!=L-1):
        f.write("\n")
f.close()


encoded_message=encoder.turbo_encode_message(message,permutation)

        

serial_encoded_message=np.reshape(encoded_message[1:],len(encoded_message[1:])*3)
serial_encoded_message=[1*(serial_encoded_message[i]>0) for i in range(3*L)]


s=""
for bit in serial_encoded_message:
    s+=(str(bit))
print(s)
#
