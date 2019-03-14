#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 19:56:55 2019

@author: root
"""

import numpy as np




def Encoder1(inp,state):
    inp_m1=(np.bitwise_and(state,4))>>2
    inp_m2=(np.bitwise_and(state,2))>>1
    inp_m3=np.bitwise_and(state,1)
    Y=[inp,(inp+inp_m2)%2, (inp_m1+inp_m3)%2,(inp+inp_m1+inp_m2)%2]
    return Y




