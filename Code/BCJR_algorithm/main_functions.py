#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 20:09:49 2019

@author: root
"""

from BCJR import max_star
from treillis import etatsSortants
import numpy as np
import random as rd


L=2500
M=3

def encode_message(Encoder,message):
    state=0
    res=[-99]
    for b in range(1,L+1):
        bit=message[b]
        codeword=Encoder(bit,state)
        state=(bit<<(M-1)) + (state>>1)
        res+=[codeword]
    return res


def channel(encoded_message,sigma2):
    output=[-99]
    n=len(encoded_message[1])
    for w in range(1,L+1):
        word=encoded_message[w]
        outpword=np.add(word,
                        [rd.normalvariate(0,np.sqrt(sigma2))
                        for k in range(n)])
        output+=[outpword]
    return output



def decoder(received_message,treillis,alpha_mat,beta_mat,gamma_mat):
    LAP=[]
    decoded_message=[]
    L=len(received_message)-1
    for l in range(1,L+1):
        cand_uplus=[]
        cand_umoins=[]
        for state_pr in range(2**M):
            for state in etatsSortants(treillis,state_pr,l-1):
                abg=alpha_mat[state_pr][l-1]
                abg+=gamma_mat[l][state_pr][state]+beta_mat[state][l]
                        
                if (state==treillis[state_pr][l-1][0][0][0]): 
                    cand_umoins+=[abg]
                if (state==treillis[state_pr][l-1][0][1][0]):
                    cand_uplus+=[abg]
 
        LAPul=max_star(cand_uplus)-max_star(cand_umoins)
        LAP+=[LAPul]
        decoded_message+=[1*(LAPul>0)]
    return decoded_message