#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 10:28:21 2019

@author: root
"""

#méthode encodage série -> codage -> P/S
from Encoders import Encoder_57

import numpy as np
import sys



encoder=Encoder_57()
message=[-99]
#on suppose que tous les bits sont concaténés
seq=str(sys.argv[1])
for i in range(len(seq)):
    message+=[int(seq[i])]
 
message=np.array(message)
encoded_message=encoder.encode_message(message)

serial_encoded_message=np.reshape(encoded_message[1:],len(encoded_message[1:])*2)



s=""
for bit in serial_encoded_message:
    s+=(str(bit))
print(s)
#
