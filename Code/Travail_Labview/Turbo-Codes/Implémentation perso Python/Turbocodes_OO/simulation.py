#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 21:06:40 2019

@author: root
"""



from Encoders import UMTS_Encoder
from Channel import Channel
from Decoder import Turbo_Decoder

import numpy as np
import random as rd





nbIterations=7
nbTrials=1
encoder=UMTS_Encoder()

for EB_N0_db in np.linspace(-5,0,1):
    
    EB_N0=10**(EB_N0_db/10)
    sigma2=1/(2*EB_N0)
    
    TEB_vec_trial=[[]]*nbIterations
    for trial in range(nbTrials):
        message=[-99]+[rd.randint(0,1) for k in range(20)]+[0,0,0,0,0,0,0,1]
        print("message=   ", message)
        L=len(message)-1
        permutation=np.arange(L)
        rd.shuffle(permutation)
        encoded_message=encoder.turbo_encode_message(message,permutation)
        C=Channel(sigma2)
        received_message=C.addNoise(encoded_message)
        decoder=Turbo_Decoder(encoder,permutation,L,nbIterations)
        decoded_message=decoder.decode(received_message,sigma2)
        for iteration_index in range(nbIterations):
            print("iteration",iteration_index,decoded_message[iteration_index],np.sum([message[i]!=decoded_message[iteration_index][i]
            for i in range(1,L+1)])/L)
            TEB_vec_trial[iteration_index]+=[np.sum([message[i]!=decoded_message[iteration_index][i]
            for i in range(1,L+1)])/L]
            #print(TEB_vec_trial[iteration_index])
    s=""
    for iteration_index in range(nbIterations):
        s+=str(np.mean(TEB_vec_trial[iteration_index],0))+" "
    print(s)
    
