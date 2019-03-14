#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 19:47:52 2019

@author: root

"""

import numpy as np
from interleaver import Interleave



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
      
        
        
        
    def compute_gamma(received_message,l,transition_codeword,
                      permutation,extrinsicLLR,sigma2):
        return 0
        
    

    
    #Le LLR extrinsèque est dans l'ordre attendu par le décodeur.
    def compute_gamma_mat(self,received_message,
                          permutation,extrinsicLLR_vec,sigma2):
        for l in range(1,self.L+1):
            for s in range(self.nbStates):
                for si in range(self.nbStates):
                    self.gamma_mat[l][s][si]=-np.inf #initialisation
                    
                outStates=self.treillis.etatsSortants(s,l-1)
                if (outStates!=[]): #si j'ai des liens sortants
                    outLinks=self.treillis.tableau[s][l-1].outlinks
                    outLink_inp0=outLinks[0] #[nextState,outp]
                    outLink_inp1=outLinks[1]
                    self.gamma_mat[l][s][outLink_inp0[0]]=self.compute_gamma(
                            received_message,l,outLink_inp0[1],permutation,
                            extrinsicLLR_vec[l],sigma2)
                    self.gamma_mat[l][s][outLink_inp1[0]]=self.compute_gamma(
                            received_message,l,outLink_inp1[1],permutation,
                            extrinsicLLR_vec[l],sigma2) 
                
                    
        
        
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
    
    

     

    def disp_gamma_mat(self):
        for l in range(1,self.L+1):
            for state in range(self.nbStates):
                for next_state in range(self.nbStates):
                    if (self.gamma_mat[l][state][next_state]!=-np.inf):
                        print("gamma(l =",l,",",state,"-->",next_state,") =",
                              self.gamma_mat[l][state][next_state])
    
    
    def disp_alpha_mat(self):    
        for l in range(self.L+1):
            print("instant",l)
            for state in range(self.nbStates):
                print("   alpha_tilde(",state,",",l,") =",self.alpha_mat[state][l])
        
            
    def disp_beta_mat(self):
        for l in range(1,self.L+1):
            print("instant",l)
            for state in range(self.nbStates):
                print("   beta_tilde(",state,",",l,") =",self.beta_mat[state][l])       

class BCJR_D1(BCJR):
    
    def __init__(self,treillis):
        BCJR.__init__(self,treillis)
       
        
    #!!! On suppose que le LLR arrive dans le bonne ordre
    def compute_gamma(self,received_message,l,transition_codeword,
                      permutation,extrinsicLLR,sigma2):
        res=0
        uk,pk=transition_codeword[0],transition_codeword[1]
        yku,ykp=received_message[l][0],received_message[l][1]
        res=sigma2*uk*extrinsicLLR/2 + uk*yku+ pk*ykp
        if (res!=0 and sigma2!=0):
            res/=(sigma2)
        if (res!=0 and sigma2==0):
            res=-np.inf
        return res

    def compute_beta_mat(self):
        
        #Modification cause encodeur RSC impossible à réinitialiser
       # self.beta_mat[0][self.L]=0
#        for state in range(1,self.nbStates):
#            self.beta_mat[state][self.L]=-np.inf
        for state in range(0,self.nbStates):
            self.beta_mat[state][self.L]=self.alpha_mat[state][self.L]
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

    def compute_extrinsic_LLR(self,received_message,treillis,
                              permutation,sigma2):

        LE12=[-99]
        L=len(received_message)-1
        for l in range(1,L+1):
            cand_uplus=[]
            cand_umoins=[]
            ykp=received_message[l][1]
            for state_pr in range(self.nbStates):
                for state in treillis.etatsSortants(state_pr,l-1):
                    abg=self.alpha_mat[state_pr][l-1]+self.beta_mat[state][l]
                    currentNode=treillis.tableau[state_pr][l-1]
                    if (state==currentNode.outlinks[0][0]):       
                        pk=currentNode.outlinks[0][1][0]
                        abg+=(ykp*pk)/sigma2
                        cand_umoins+=[abg]
                    if (state==currentNode.outlinks[1][0]):
                        pk=currentNode.outlinks[1][1][0]
                        abg+=(ykp*pk)/sigma2
                        cand_uplus+=[abg]
     
            LAPul=max_star(cand_uplus)-max_star(cand_umoins)
            LE12+=[LAPul]
        return LE12
    
    def compute_decision(self,received_message,LE12,LE21,permutation,sigma2):
        L=len(received_message)-1
        LLR=[-99]
        for l in range(1,L+1):
            yku=received_message[l][0]  
            #!!!!!! ne pas oublier LE21[permutation[l]]
            LLR+=[2*yku/sigma2+LE12[l]+LE21[l]]
        return LLR
        
class BCJR_D2(BCJR): 
    
    def __init__(self,treillis):
        BCJR.__init__(self,treillis)
    #!!! Attention à l'ordre 
    def compute_gamma(self,received_message,l,transition_codeword,
                      permutation,extrinsicLLR,sigma2):
        res=0
       # print(transition_codeword)
        uk,qk=transition_codeword[0],transition_codeword[1]
        yku=Interleave(received_message,permutation)[l][0]
        ykq=received_message[l][2]
        res=sigma2*uk*extrinsicLLR/2 + uk*yku+ qk*ykq
        if (res!=0 and sigma2!=0):
            res/=(sigma2)
        if (res!=0 and sigma2==0):
            res=-np.inf
        return res
    
    def compute_beta_mat(self):

        for state in range(0,self.nbStates):
            self.beta_mat[state][self.L]=self.alpha_mat[state][self.L]
        for l in range(self.L,1,-1):
            for state in range(0,self.nbStates):
                Liste=[]
                outStates=self.treillis.etatsSortants(state,l-1)
                if (outStates!=[]): 
                    for state_next in outStates:
                        gamma_tildelssnxt=self.gamma_mat[l][state][state_next]
            
                        Liste+=[self.beta_mat[state_next,l]+
                                          gamma_tildelssnxt]
                if (len(Liste)!=0):
                    self.beta_mat[state][l-1]=max_star(Liste)
                else:
                    self.beta_mat[state][l-1]=-np.inf
                    
                    
    
    def compute_extrinsic_LLR(self,received_message,treillis,
                              permutation,sigma2):
   
        LE21=[-99]
        L=len(received_message)-1
        for l in range(1,L+1):
            cand_uplus=[]
            cand_umoins=[]
            ykq=received_message[l][2]
            for state_pr in range(self.nbStates):
                for state in treillis.etatsSortants(state_pr,l-1):
                    abg=self.alpha_mat[state_pr][l-1]+self.beta_mat[state][l]
                    currentNode=treillis.tableau[state_pr][l-1]
                    if (state==currentNode.outlinks[0][0]):       
                        qk=currentNode.outlinks[0][1][1]
                        abg+=(ykq*qk)/sigma2
                        cand_umoins+=[abg]
                    if (state==currentNode.outlinks[1][0]):
                        qk=currentNode.outlinks[1][1][1]
                        abg+=(ykq*qk)/sigma2
                        cand_uplus+=[abg]
        
            LAPul=max_star(cand_uplus)-max_star(cand_umoins)
            LE21+=[LAPul]    
        return LE21
    
    def compute_decision(self,received_message,LE21,LE12,permutation,sigma2):
        L=len(received_message)-1
        LLR=[-99]
       
        for l in range(1,L+1):
            yku=Interleave(received_message,permutation)[l][0]  
            LLR+=[2*yku/sigma2+LE21[l]+LE12[l]]
        return LLR
    
    


     
