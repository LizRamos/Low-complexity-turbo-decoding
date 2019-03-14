#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 20:09:49 2019

@author: root
"""


import numpy as np
import random as rd


class Channel():
    def __init__(self,sigma2):
        self.sigma2=sigma2
    
    def addNoise(self,encoded_message):
        output=[-99]
        n=len(encoded_message[1])
        for w in range(1,len(encoded_message)):
            word=encoded_message[w]
            outpword=np.add(word,
                            [rd.normalvariate(0,np.sqrt(self.sigma2))
                            for k in range(n)])
            output+=[outpword]
        return output
