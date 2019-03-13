#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 19:56:55 2019

@author: root
"""

import numpy as np
import random as rd
from interleaver import Interleave






class Encoder():

    def __init__(self,M):
        self.M=M
        
    def out(self,inp,state):
        pass
        
    def TableauTransition(self):
        tableau=[]
        for state in range(2**(self.M)):
            entry=[]
            for inp in [0,1]:
                outp,nextState=self.out(inp,state)    
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                outp=[2*outp[0]-1,2*outp[1]-1]
                entry+=[[state,nextState,outp]]
            tableau+=[entry]
        return tableau
    
    def encode_message(self,message):
        state=0
        res=[-99]
        for b in range(1,len(message)):
            bit=message[b]
            outp,state=self.out(bit,state)
            codeword= outp
            res+=[codeword]
        return res



    def turbo_encode_message(self,message,permutation):
        state1,state2=0,0
        res=[-99]
        L=len(message)-1
        interleaved_message=Interleave(message,permutation)
        for b in range(1,L+1):
            bit1=message[b]
            bit11=interleaved_message[b]
            bit2,state1=self.out(bit1,state1)
            bit3,state2=self.out(bit11,state2)
            bit2,bit3=bit2[1],bit3[1]
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            codeword= [2*bit1-1,2*bit2-1,2*bit3-1]
            res+=[codeword]
        return res


class UMTS_Encoder(Encoder):
    
    def __init__(self):
        super()
        self.M=3
 

    def out(self,inp,state):
        Di_m1=(np.bitwise_and(state,4))>>2
        Di_m2=(np.bitwise_and(state,2))>>1
        Di_m3=np.bitwise_and(state,1)
        
        Di=(inp+Di_m2+Di_m3)%2
        Zi=(Di+Di_m1+Di_m3)%2
        nextState=(Di<<2) + (state>>1)
        
        return [inp,Zi],nextState
    
    def TableauTransition(self):
        return super().TableauTransition()

