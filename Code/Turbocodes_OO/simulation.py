#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 21:06:40 2019

@author: root
"""



from Encoders import UMTS_Encoder
from Channel import Channel
from Decoder import Turbo_Decoder
from print_TEB import execute

import numpy as np
import random as rd





nbIterations=100
nbTrials=1
encoder=UMTS_Encoder()

EB_N0_db_range= np.linspace(-3.5,-4,1)
TEB=np.zeros([len(EB_N0_db_range),nbIterations])
EB_N0_index=0
for EB_N0_db in EB_N0_db_range:
    
    EB_N0=10**(EB_N0_db/10)
    sigma2=1/(2*EB_N0)
    
    TEB_vec_trial=np.zeros([nbIterations,nbTrials])
    for trial in range(nbTrials):
        message=[-99]+[rd.randint(0,1) for k in range(20)]+[0,0,0,0,0,0,0,1]
        L=len(message)-1
        permutation=np.arange(L)
        rd.shuffle(permutation)
        encoded_message=encoder.turbo_encode_message(message,permutation)
        C=Channel(sigma2)
        received_message=C.addNoise(encoded_message)
        decoder=Turbo_Decoder(encoder,permutation,L,nbIterations)
        decoded_messages=decoder.decode(received_message,sigma2)
        #print(decoded_messages)
        
        for iteration in range(nbIterations):
            TEB_vec_trial[iteration][trial]=np.sum(
                    [message[i]!=decoded_messages[iteration][i] 
                    for i in range(1,L+1)])/L
    
    TEB[EB_N0_index]=np.mean(TEB_vec_trial,1)
    EB_N0_index+=1


execute(TEB,EB_N0_db_range)

