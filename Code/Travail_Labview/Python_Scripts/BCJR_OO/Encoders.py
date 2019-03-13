#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 19:56:55 2019

@author: root
"""

import numpy as np

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


class Encoder_1315(Encoder):
    
    def __init__(self):
        super()
        self.M=3
 
    def out(self,inp,state):
        inp_m1=(np.bitwise_and(state,4))>>2
        inp_m2=(np.bitwise_and(state,2))>>1
        inp_m3=np.bitwise_and(state,1)
        outp=[(inp+inp_m2+inp_m3)%2, (inp+inp_m1+inp_m3)%2]
        nextState= (inp<<2) + (state>>1)
        return outp,nextState
    
    def TableauTransition(self):
        return super().TableauTransition()

		
class Encoder_57(Encoder):
    
    def __init__(self):
        super()
        self.M=2
 
    def out(self,inp,state):
        inp_m1=(np.bitwise_and(state,2))>>1
        inp_m2=np.bitwise_and(state,1)
        outp=[(inp+inp_m2)%2, (inp+inp_m1+inp_m2)%2]
        nextState= (inp<<1) + (state>>1)
        return outp,nextState
    
    def TableauTransition(self):
        return super().TableauTransition()
		
		
#
#message=[-99]+[1,0,1,1,1,0,0,1,0,1,1,1,0,0,0]
#E=Encoder_1315()
#print(E.encode_message(message))

