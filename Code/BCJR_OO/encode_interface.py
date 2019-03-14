#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 10:28:21 2019

@author: root
"""

#méthode encodage série -> codage -> P/S
from Encoders import Encoder_1315

import numpy as np
import sys



encoder=Encoder_1315()
message=[-99]
for i in range(1,len(sys.argv)):
    message+=[int(sys.argv[i])]
 
message=np.array(message)
encoded_message=encoder.encode_message(message)

serial_encoded_message=np.reshape(encoded_message[1:],len(encoded_message[1:])*2)
s=""
for bit in serial_encoded_message:
    s+=(str(bit)+" ")
print(s)
#
