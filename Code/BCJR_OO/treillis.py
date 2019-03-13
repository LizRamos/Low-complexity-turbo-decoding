#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 10:39:53 2019

@author: root


"""
import numpy as np




class Node():
    def __init__(self,state,instant):
        self.state=state
        self.instant=instant
        self.outlinks=[]
        
    def addOutlink(self,nextState,outp):
        self.outlinks+=[[nextState,outp]]
 
    def hasOutlinks(self):
        return (self.outlinks!=[])
       
    def visited(self):
        return (self.outlinks!=[])


class Treillis():
    def __init__(self,Encoder,size):
        self.size=size
        self.nbStates=2**(Encoder.M)
        self.transitions=Encoder.TableauTransition()
        self.tableau=np.zeros([self.nbStates,self.size+1],dtype=object)
        self.addNextStates(0,0,0,self.size+1)
        self.addNextStates(0,1,0,self.size+1)
        
        
    def addNextStates(self,state,inp,l,Lp1):
        nextState=self.transitions[state][inp][1]
        outp=self.transitions[state][inp][2]
  
        #Ajouter la transition sortante de l'état courant
        if (self.tableau[state][l]==0):
            currentNode=Node(state,l)
        else:
            currentNode=self.tableau[state][l]
        currentNode.addOutlink(nextState,outp)
        self.tableau[state][l]=currentNode
        
        nextStateReached=False
        if (self.tableau[nextState][l+1]==0):
            self.tableau[nextState][l+1]=Node(nextState,l+1)
        else:
            nextStateReached=True
            
        
        #Poursuivre la reccurence si l'état atteint l'a alors été pour
        #la première fois et que la limite droite du tableau ne sera pas 
        #dépassée
        continueRecursion=(l<Lp1-2 and not nextStateReached)
        #print(continueRecursion)
        if (continueRecursion):   
            self.addNextStates(nextState,0,l+1,Lp1)
            self.addNextStates(nextState,1,l+1,Lp1)
    

    def lecture(self):
        cardStates=np.size(self.tableau,0)
        cardInstants=np.size(self.tableau,1)
        for instant in range(cardInstants):
            print("instant",instant)
            for state in range(cardStates):
                if (self.tableau[state][instant]!=0):
                    currentNode=self.tableau[state][instant]
                    print("  état",state) 
                    if (currentNode.hasOutlinks()):
                        for inp in [0,1]:
                            outLink=currentNode.outlinks[inp]
                            print("     o---> pour entrée",inp,"vers etat",
                              outLink[0], "avec sortie",outLink[1])        

                         
    
    def etatsSortants(self,state,instant):
        res=[]
        if (self.tableau[state][instant]!=0):
            currentNode=self.tableau[state][instant]
            if (currentNode.hasOutlinks):
                for inp in [0,1]:
                    res+=[currentNode.outlinks[inp][0]]
        return res

