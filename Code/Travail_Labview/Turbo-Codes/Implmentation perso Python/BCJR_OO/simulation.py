#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 21:06:40 2019

@author: root
"""



from Encoders import Encoder_1315
from Channel import Channel
from Decoder import BCJR_Decoder

import numpy as np
import random as rd
import matplotlib.pyplot as plt



nbTrials=50
encoder=Encoder_1315()

TEB=[]
EB_N0_range=np.linspace(-5,8,130)
for EB_N0_db in EB_N0_range:
    
    EB_N0=10**(EB_N0_db/10)
    sigma2=1/(2*EB_N0)
    
    TEB_vec_trial=[]
    for trial in range(nbTrials):
        message=[-99]+[rd.randint(0,1) for k in range(200)]+[1,1,1,0,0,0,0,0]
        L=len(message)-1

        encoded_message=encoder.encode_message(message)
        C=Channel(sigma2)
        received_message=C.addNoise(encoded_message)
        decoder=BCJR_Decoder(encoder,L)
        decoded_message=decoder.decode(received_message,sigma2)
        
        TEB_vec_trial+=[np.sum([message[i]!=decoded_message[i]
          for i in range(1,L+1)])/L]
        
    print(EB_N0_db,np.mean(TEB_vec_trial))
    TEB+=[np.mean(TEB_vec_trial)]

plt.plot(EB_N0_range,TEB)