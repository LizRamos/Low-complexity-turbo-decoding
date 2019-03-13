#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 15:57:59 2019

@author: root
"""




import numpy as np
from treillis import Treillis
from BCJR import BCJR


class BCJR_Decoder():
    def __init__(self,Encoder,L):
        self.Encoder=Encoder
        self.L=L
        self.treillis=Treillis(self.Encoder,L)


    def decode(self,received_message,sigma2):
        decoder=BCJR(self.treillis)
        decoder.compute_gamma_mat(received_message,sigma2)
        decoder.compute_alpha_mat()
        decoder.compute_beta_mat()    
        LLR=decoder.compute_decision()
        decoded_message=[-99]+[int(lr) for lr in 0.5*(np.sign(LLR)[1:]+1)]
            
        return decoded_message