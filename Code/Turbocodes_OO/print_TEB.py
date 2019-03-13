#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 12:05:25 2019

@author: root
"""

import time
import numpy as np

def execute(TEB,SNR_range):

    n,p=np.size(TEB,0),np.size(TEB,1)
    tab=np.zeros([n+1,p+1],dtype="object")
    tab[1:,0]=SNR_range
    tab[1:,1:(p+1)]=TEB
    
    S=["SNR"]
    for j in range(p):
        S+=["it"+str(j)]
    print(S)
    tab[0,:]=S

    tab_str=np.zeros([n+1,p+1])
    filename="results "+str(int(time.time()))+".txt"
    f=open(filename,"w+")
    s=""
    for i in range(n+1):
        for j in range(p+1):
            tab_str[i][j]=len(str(tab[i][j]))
    print(tab_str)
    columns_size=np.max(tab_str,0)
    

        
    
    for i in range(n+1):
        for j in range(p+1):
            columns_size_j=columns_size[j]
            s+=(str(tab[i][j]))+(" "*int(columns_size_j-tab_str[i][j]+2))
        s+="\n"
    f.write(s)
    f.close()
    
    
#
#TEB=np.array([[0.12233333,0.6232,0.93994,0.3333],
#              [0.3333,0.232,0.361994,0.6545545545],
#              [0.3333,0.232,0.361994,0.6545545545],
#              [0.54533333,0.25532,0.53994,0.9545]])
#
#execute(TEB,np.linspace(-5,-3,4))
