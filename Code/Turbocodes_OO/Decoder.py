#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 15:57:59 2019

@author: root
"""

import numpy as np
from interleaver import Interleave,Interleaver_Reverse_Permutation
from treillis import Treillis
from BCJR import BCJR_D1, BCJR_D2






class Turbo_Decoder():
    def __init__(self,Encoder,permutation,L,nbIterations):
        self.Encoder=Encoder
        self.permutation=permutation
        self.reverse_permutation=Interleaver_Reverse_Permutation(permutation)
        self.L=L
        self.treillis=Treillis(self.Encoder,L)
        self.nbIterations=nbIterations

    def decode(self,received_message,sigma2):
        decoder1=BCJR_D1(self.treillis)
        decoder2=BCJR_D2(self.treillis)
        decoded_messages=np.zeros([self.nbIterations,self.L+1])
        LLR21ord=[-99]+self.L*[0]
        
        
        for iteration in range(self.nbIterations):
            decoder1.compute_gamma_mat(received_message,self.permutation,LLR21ord,sigma2)
            decoder1.compute_alpha_mat()
            decoder1.compute_beta_mat()
            
            LLR12=decoder1.compute_extrinsic_LLR(received_message,
                                                 self.treillis,self.permutation,sigma2)
            LLR12perm=Interleave(LLR12,self.permutation)
            LLR1=decoder1.compute_decision(received_message,LLR12,
                                          LLR21ord,self.permutation,sigma2)

            decoded_message1=[-99]+[int(lr) for lr in 0.5*(np.sign(LLR1)[1:]+1)]
            decoded_messages[iteration]=decoded_message1    
            ##############################################################################
                    
            decoder2.compute_gamma_mat(received_message,self.permutation,LLR12perm,sigma2)
            decoder2.compute_alpha_mat()
            decoder2.compute_beta_mat()
            
            
            LLR21=decoder2.compute_extrinsic_LLR(received_message,self.treillis,
                                                 self.permutation,sigma2)
            

            
            LLR21previous=LLR21ord
            LLR21ord=Interleave(LLR21,self.reverse_permutation)
            diffLLR21_2=np.square(np.subtract(LLR21ord[1:],LLR21previous[1:]))
            print(np.mean(np.floor(LLR21ord)))
            LLR1exp=np.exp(LLR1[1:])
            Mi=np.sum([diffLLR21_2[k]/LLR1exp[k] for k in range(self.L)])
            if (iteration==0):
                M1=Mi
            if (iteration!=0 and Mi<0.01*M1):
                break
            print(iteration,Mi)
        return decoded_messages