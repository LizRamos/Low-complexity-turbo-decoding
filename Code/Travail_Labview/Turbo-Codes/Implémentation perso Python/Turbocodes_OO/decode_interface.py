# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""







import re
import numpy as np
import sys


from Encoders import UMTS_Encoder
from Decoder import Turbo_Decoder

nbIterations=7
encoder=UMTS_Encoder()

#################################################################
#lecture permutation
f=open("permutation.dat","r")    
permutation=[int(line) for line in f]
f.close()

#################################################################
#Conversion complète des arguments en string unique
cmd_line=""
for i in range(1,len(sys.argv)):
    cmd_line+=str(sys.argv[i])+" "

#récupération de l'option -s indiquant le sigma2
#et remplacement de la virgule par un point
regex_sigma2="-s\s([,\d]+)"
sigma2_vec=re.findall(regex_sigma2, cmd_line)
sigma2=0
if (len(sigma2_vec)!=0):
    sigma2cast=re.findall("(\d+),(\d+)",sigma2_vec[0])
    sigma2rep=(sigma2cast[0][0]+"."+sigma2cast[0][1])
    sigma2=float(sigma2rep)



#################################################################
#Récupération des complexes pour former le vecteur
reg1="\s*-?\d+\s[\+-]\d+\si"

vec=re.findall(reg1,cmd_line)
vec_d=[]
vec_cmplx=[]

for i in range(len(vec)):
    reg2="(\s*-?\d+\s)([\+-]\d+\s)i"
    str_cmplx=vec[i]
    dec=re.findall(reg2,str_cmplx)
    vec_d+=dec
    vec_cmplx+=[float(str(dec[0][0]))+1j*float(str(dec[0][1]))]

vec_cmplx=np.divide(vec_cmplx,100000.0)

#for c in range(len(vec_cmplx)):
#    print(vec_cmplx[c])

#################################################################
#Lancement de l'algorithme de décodage et affichage des résultats
    
serial_received_message=np.multiply(-1,np.imag(vec_cmplx))
#print(serial_received_message)
L=int(len(serial_received_message)/3)

serial_received_message=np.array(serial_received_message)
received_message=np.reshape(serial_received_message,[L,3])
received_message=[-99]+received_message.tolist()
#print(received_message)


decoder=Turbo_Decoder(encoder,permutation,L,nbIterations)
decoded_message_vec=decoder.decode(received_message,sigma2)
decoded_message=decoded_message_vec[-1]
#print(decoded_message)
s=""
for bit in decoded_message[1:]:
    s+=(str(bit))
print(s)

