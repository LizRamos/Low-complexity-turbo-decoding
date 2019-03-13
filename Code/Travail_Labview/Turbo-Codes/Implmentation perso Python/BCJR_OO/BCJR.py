#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 19:47:52 2019
@author: root
"""

import numpy as np

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


class BCJR:
    def __init__(self,treillis):
        self.treillis=treillis
        self.nbStates,self.L=treillis.nbStates,treillis.size
        self.alpha_mat=np.zeros([self.nbStates,self.L+1])
        self.beta_mat=np.zeros([self.nbStates,self.L+1])
        self.gamma_mat=np.zeros([self.L+1,self.nbStates,self.nbStates])
        
 
    def compute_gamma(self, received_codeword,transition_codeword,sigma2):
        res=0
        m=len(received_codeword)
        for i in range(m):
            res+=-(received_codeword[i]-transition_codeword[i])**2
        if (res!=0 and sigma2!=0):
            res/=(2*sigma2)
        if (res!=0 and sigma2==0):
            res=-np.inf
        return res
    
        

    def compute_gamma_mat(self,received_message,sigma2):
        for l in range(1,self.L+1):
            for s in range(self.nbStates):
                for si in range(self.nbStates):
                    self.gamma_mat[l][s][si]=-np.inf 
                    
                outStates=self.treillis.etatsSortants(s,l-1)
                if (outStates!=[]): 
                    outLinks=self.treillis.tableau[s][l-1].outlinks
                    outLink_inp0=outLinks[0] 
                    outLink_inp1=outLinks[1]
                    self.gamma_mat[l][s][outLink_inp0[0]]=self.compute_gamma(
                            received_message[l],outLink_inp0[1],sigma2)
                    self.gamma_mat[l][s][outLink_inp1[0]]=self.compute_gamma(
                            received_message[l],outLink_inp1[1],sigma2) 
                
    def compute_alpha_mat(self):
        self.alpha_mat[0][0]=0
        for state in range(1,self.nbStates):
            self.alpha_mat[state][0]=-np.inf
        for l in range(1,self.L+1):
            for state in range(0,self.nbStates):
                Liste=[]
                for state_pr in range(0,self.nbStates):
                    gamma_tildelsspr=self.gamma_mat[l][state_pr][state]
                    if (state in self.treillis.etatsSortants(state_pr,l-1)): 
                        Liste+=[self.alpha_mat[state_pr,l-1]+
                                      gamma_tildelsspr]
                if (len(Liste)!=0):
                    self.alpha_mat[state][l]=max_star(Liste)
                else:
                    self.alpha_mat[state][l]=-np.inf
    
    
    def compute_beta_mat(self):
        self.beta_mat[0][self.L]=0
        for state in range(0,self.nbStates):
            self.beta_mat[state][self.L]=-np.log(4)

        for l in range(self.L,1,-1):
            for state in range(0,self.nbStates):
                Liste=[]
                outStates=self.treillis.etatsSortants(state,l-1)
                if (outStates!=[]): #J'ai un lien state --> qqc
                    for state_next in outStates:
                        gamma_tildelssnxt=self.gamma_mat[l][state][state_next]
            
                        Liste+=[self.beta_mat[state_next,l]+
                                          gamma_tildelssnxt]
                if (len(Liste)!=0):
                    self.beta_mat[state][l-1]=max_star(Liste)
                else:
                    self.beta_mat[state][l-1]=-np.inf
      
        
    def compute_decision(self):
        decoded_message=[-99]
        for l in range(1,self.L+1):
            cand_uplus=[]
            cand_umoins=[]
            for state_pr in range(self.nbStates):
                for state in self.treillis.etatsSortants(state_pr,l-1):
                    currentNode=self.treillis.tableau[state_pr][l-1]
                    abg=self.alpha_mat[state_pr][l-1]
                    abg+=self.gamma_mat[l][state_pr][state]+self.beta_mat[state][l]
                            
                    if (state==currentNode.outlinks[0][0]): 
                        cand_umoins+=[abg]
                    if (state==currentNode.outlinks[1][0]):
                        cand_uplus+=[abg]
     
            LAPul=max_star(cand_uplus)-max_star(cand_umoins)
            decoded_message+=[1*(LAPul>0)]
        return decoded_message