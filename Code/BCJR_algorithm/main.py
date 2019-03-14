#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 16:16:10 2019

@author: root
"""
from treillis import treillis
from BCJR import gamma_tilde,alpha_tilde,beta_tilde
from main_functions import encode_message,channel,decoder
from Encoders import Encoder1

import numpy as np
import random as rd
import matplotlib.pyplot as plt



L=2500
M=3

treillis=treillis(Encoder1,M,L+1)

EB_N0_vec=[]
TEB_vec=[]

for EB_N0_db in np.linspace(-1,6,30):
    
    EB_N0=10**(EB_N0_db/10)
    sigma2=1/(2*EB_N0)
    
    TEB_vec_trial=[]
    for trial in range(100):
        
        message=[-99]
        message+=[rd.randint(0,1) for k in range(L-2)]
        message+=[0,0]
        
        encoded_message=encode_message(Encoder1,message) 
        received_message=channel(encoded_message,sigma2)
    
        gamma_mat=gamma_tilde(treillis,received_message,sigma2)
        beta_mat=beta_tilde(gamma_mat,treillis)
        alpha_mat=alpha_tilde(gamma_mat,treillis)
        
        decoded_message=decoder(received_message,treillis,alpha_mat,beta_mat,gamma_mat) 
        decoded_message=[-99]+decoded_message
        
        TEB_vec_trial+=[np.sum(np.bitwise_xor(decoded_message,message))/L]
    
    TEB_vec+=[np.mean(TEB_vec_trial)]
    EB_N0_vec+=[EB_N0_db]
    
    print(EB_N0_db,"TEB =",np.mean(TEB_vec_trial))


plt.plot(EB_N0_vec,TEB_vec)



