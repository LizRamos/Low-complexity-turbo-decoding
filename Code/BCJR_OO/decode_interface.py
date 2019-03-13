#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 10:28:21 2019

@author: root
"""

#méthode décodage série ->S/P - décodage -> série
from Encoders import Encoder_1315
from Decoder import BCJR_Decoder
import numpy as np
import sys


encoder=Encoder_1315()


notb,nots=False,False
if (not "-b" in sys.argv):
    print("-b option missing")
    notb=True
if (not "-s" in sys.argv):
    print("-s option missing") 
    nots=True
if (notb or nots):
    sys.exit()
    
serial_received_message=[]
sigma2=0

bits_reading=False
sigma2_reading=False
for i in range(1,len(sys.argv)):
    if (bits_reading and not (sys.argv[i] in ["-b","-s"])):
        serial_received_message+=[int(sys.argv[i])]
    if (sigma2_reading):
        sigma2=float(sys.argv[i])
    if (str(sys.argv[i])=="-b"):
        bits_reading=True
        sigma2_reading=False
    if (str(sys.argv[i])=="-s"):
        bits_reading=False
        sigma2_reading=True
    
#print(serial_received_message)
#print(sigma2)
L=int(len(serial_received_message)/2)

serial_received_message=np.array(serial_received_message)
received_message=np.reshape(serial_received_message,[L,2])
received_message=[-99]+received_message.tolist()
#print(received_message)
decoder=BCJR_Decoder(encoder,L)
decoded_message=decoder.decode(received_message,sigma2)
#print(decoded_message)
s=""
for bit in decoded_message[1:]:
    s+=(str(bit)+" ")
print(s)
