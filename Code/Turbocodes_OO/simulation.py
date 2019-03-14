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


nbIterations=12
nbTrials=50
encoder=UMTS_Encoder()

EB_N0_db_range= np.linspace(-4,-2.5,4)
TEB=np.zeros([len(EB_N0_db_range),nbIterations])
EB_N0_index=0
for EB_N0_db in EB_N0_db_range:
    
    EB_N0=10**(EB_N0_db/10)
    sigma2=1/(2*EB_N0)
    TEB_vec_trial=np.zeros([nbIterations])
    
    trial=0
    nbErrors=0
    while(trial<nbTrials):
	print(EB_N0_index,trial,nbErrors)
	trial+=1
        message=[-99]+[rd.randint(0,1) for k in range(350)]+[0,0,0,0,0,0,0,1]
        L=len(message)-1
        permutation=np.arange(L)
        rd.shuffle(permutation)
        encoded_message=encoder.turbo_encode_message(message,permutation)
        C=Channel(sigma2)
        received_message=C.addNoise(encoded_message)
        decoder=Turbo_Decoder(encoder,permutation,L,nbIterations)
        decoded_messages=decoder.decode(received_message,sigma2)

        for iteration in range(nbIterations):
            TEB_vec_trial[iteration]+=np.sum(np.bitwise_xor(message[1:],decoded_messages[iteration][1:]))
            print(TEB_vec_trial[iteration])

	nbErrors=TEB_vec_trial[11]
    TEB[EB_N0_index]=TEB_vec_trial/float(L*trial)
    print("****",EB_N0_db,TEB[EB_N0_index])
    EB_N0_index+=1
    
print(TEB)

execute(TEB,EB_N0_db_range)

