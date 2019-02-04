#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 10:39:53 2019

@author: root


"""
import numpy as np


#M signifie le nombre de cases mémoires de l'encodeur
def TableauTransition(Encoder,M):
    tableau=[]
    for state in range(2**M):
        entry=[]
        for inp in [0,1]:
            outp=Encoder(inp,state)        
            nextState=(inp<<(M-1)) + (state>>1)
            entry+=[[state,nextState,outp]]
        tableau+=[entry]
    return tableau


 

def addNextStates(treillis,state,inp,TableauTransition,l,Lp1):
    #Récuperer le prochain état et la sortie associée
    #à l'état et l'instant considéré
    nextState=TableauTransition[state][inp][1]
    outp=TableauTransition[state][inp][2]
    
    #Ajouter la transition sortante de l'état courant
    if (treillis[state][l][0]==0):
        treillis[state][l][0]=[]
    treillis[state][l][0]+=[[nextState,outp]]
    
    #Ajouter la transition entrante à l'état atteint
    if (treillis[nextState][l+1][1]==0):
        treillis[nextState][l+1][1]=[]
    treillis[nextState][l+1][1]+=[[state,inp,outp]]
    
    #Poursuivre la reccurence si l'état atteint l'a alors été pour
    #la première fois et que la limite droite du tableau ne sera pas 
    #dépassée
    continueRecursion=(l<Lp1-2 and treillis[nextState][l+1][0]==0)
    if (continueRecursion):   
        addNextStates(treillis,nextState,0,TableauTransition,l+1,Lp1)
        addNextStates(treillis,nextState,1,TableauTransition,l+1,Lp1)


def treillis(Encoder,M,L):
    transitions=TableauTransition(Encoder,M)
    treillis=np.zeros([2**M,L+1,2],dtype=object)
    addNextStates(treillis,0,0,transitions,0,L+1)
    addNextStates(treillis,0,1,transitions,0,L+1)
    return treillis


def lectureTreillis(treillis):
    cardStates=np.size(treillis,0)
    cardInstants=np.size(treillis,1)
    for instant in range(cardInstants):
        print("instant",instant)
        for state in range(cardStates):
            if (treillis[state][instant][0]!=0 or
                treillis[state][instant][1]!=0):
                print("  état",state)            
            if (treillis[state][instant][0]!=0):
                for inp in [0,1]:
                    outLink=treillis[state][instant][0][inp]
                    print("     o---> pour entrée",inp,"vers etat",
                      outLink[0], "avec sortie",outLink[1])        
            if (treillis[state][instant][1]!=0):
                for inLink in (treillis[state][instant][1]):
                    print("     --->o depuis etat",
                          inLink[0], "via entrée", inLink[1],
                          "avec sortie", inLink[2])
             


def etatsSortants(treillis,state,instant):
    res=[]
    if (treillis[state][instant][0]!=0):
        for inp in [0,1]:
            res+=[treillis[state][instant][0][inp][0]]
    return res
    
