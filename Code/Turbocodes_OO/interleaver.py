#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:38:54 2019

@author: root
"""



import random as rd
import numpy as np



def Interleaver_Permutation(WordLength):
    Liste=np.arange(WordLength)
    rd.shuffle(Liste)
    return Liste

def Interleaver_Reverse_Permutation(permutation):
    Liste=[0]*(len(permutation))
    for k in range(len(permutation)):
        Liste[permutation[k]]=int(k)
    return Liste


def Interleave(word,permutation):
    res=[word[0]]
    for k in range(len(word)-1):
        #print(res)
        res+=[word[permutation[k]+1] ]
    return res

def deInterleave(word,permutation):
    return Interleave(word,Interleaver_Reverse_Permutation(permutation))


#r=[-99, 11, 22, 33, 44, 55, 66]
#dr=[]
#p=[1,0,3,5,2,4]
#
#
#
#print(Interleave(r,p))
#intrlv=Interleave(r,p)
#print(deInterleave(intrlv,p))