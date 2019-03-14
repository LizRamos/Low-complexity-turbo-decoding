#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 19:47:52 2019

@author: root      
"""

import numpy as np
from treillis import etatsSortants

L=2500
M=3



def max_star(L):
   # print(len(L))
    if (len(L)==1):
        return L[0]
    elif (len(L)==2):
        if (L[0]==-np.inf and L[1]==-np.inf):
            return -np.inf
        if (L[0]==-np.inf and L[1]!=-np.inf):
            return L[1]
        if (L[0]!=-np.inf and L[1]==-np.inf):
            return L[0]
        else:
            res=max(L)+np.log(1+np.exp(-np.abs(L[0]-L[1])))
            return res
    else:
        return max_star([max_star(L[0:-1]),L[-1]])

#En BPSK
def compute_gamma(received_codeword,transition_codeword,sigma2):
    res=0

    m=len(received_codeword)
    for i in range(m):
        res+=-(received_codeword[i]-transition_codeword[i])**2
    if (res!=0 and sigma2!=0):
        res/=(2*sigma2)
    if (res!=0 and sigma2==0):
        res=-np.inf
    return res
    

#On suppose que received_ressage arrive par liste de taille L de 3 éléments
#correspondant aux trois valeurs de sortie du codeur.

def gamma_tilde(treillis,received_message,sigma2):
    gamma_mat=np.zeros([L+1,2**M,2**M])
    for l in range(1,L+1):
        for s in range(2**M):
            if (treillis[s][l-1][0]!=0): #si j'ai des liens sortants
                outLinks=treillis[s][l-1][0]
                outLink_inp0=outLinks[0] #[nextState,outp]
                outLink_inp1=outLinks[1]
                gamma_mat[l][s][outLink_inp0[0]]=compute_gamma(
                        received_message[l], outLink_inp0[1],sigma2)
                gamma_mat[l][s][outLink_inp1[0]]=compute_gamma(
                        received_message[l], outLink_inp1[1],sigma2)
                
    return gamma_mat


def alpha_tilde(gamma_tilde,treillis):
    alpha_mat=np.zeros([2**M,L+1])
    alpha_mat[0][0]=0
    for state in range(1,2**M):
        alpha_mat[state][0]=-np.inf
    for l in range(1,L+1):
        for state in range(0,2**M):
            Liste=[]
            for state_pr in range(0,2**M):
                gamma_tildelsspr=gamma_tilde[l][state_pr][state]
                if (state in etatsSortants(treillis,state_pr,l-1)): 
                    Liste+=[alpha_mat[state_pr,l-1]+
                                  gamma_tildelsspr]
            if (len(Liste)!=0):
                alpha_mat[state][l]=max_star(Liste)
            else:
                alpha_mat[state][l]=-np.inf
    return alpha_mat


def beta_tilde(gamma_tilde,treillis):
    beta_mat=np.zeros([2**M,L+1])
    beta_mat[0][L]=0
    for state in range(1,2**M):
        beta_mat[state][L]=-np.inf
    for l in range(L,1,-1):
        for state in range(0,2**M):
            Liste=[]
            if (treillis[state][l-1][0]!=0): #J'ai un lien state --> qqc
                for state_next in etatsSortants(treillis,state,l-1):
                    gamma_tildelssnxt=gamma_tilde[l][state][state_next]
        
                    Liste+=[beta_mat[state_next,l]+
                                      gamma_tildelssnxt]
            if (len(Liste)!=0):
                beta_mat[state][l-1]=max_star(Liste)
            else:
                beta_mat[state][l-1]=-np.inf
    return beta_mat
     
    
    

       
    












