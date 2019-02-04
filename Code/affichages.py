#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 11:03:23 2019

@author: root
"""

import numpy as np

def disp_gamma_mat(gamma_mat,L,M):
    for l in range(1,L+1):
        for state in range(2**M):
            for next_state in range(2**M):
                if (gamma_mat[l][state][next_state]!=0):
                    print("gamma(l =",l,",",state,"-->",next_state,") =",
                          gamma_mat[l][state][next_state])



def disp_alpha_mat(alpha_mat,L,M):    
    for l in range(L+1):
        print("instant",l)
        for state in range(2**M):
            print("   alpha_tilde(",state,",",l,") =",alpha_mat[state][l])
    
        
def disp_beta_mat(beta_mat,L,M):
    for l in range(1,L+1):
        print("instant",l)
        for state in range(2**M):
            print("   beta_tilde(",state,",",l,") =",beta_mat[state][l])
            

def disp_abg_max(alpha_mat,beta_mat,gamma_mat,L,M):
    for l in range(1,L+1):
        a_max=-np.inf
        b_max=-np.inf
        g_max=-np.inf
        s1_max=""
        s2_max=""
        s3_max=""
        for state in range(2**M):
            if (beta_mat[state][l]>b_max):
                b_max=beta_mat[state][l]
                s2_max="beta_t("+str(state)+","+str(l)+") ="+str(b_max)
            if (alpha_mat[state][l]>a_max):
                a_max=alpha_mat[state][l]
                s3_max="alpha_t("+str(state)+","+str(l)+") ="+str(a_max)
                
            for next_state in range(2**M):
                g_comp=gamma_mat[l][state][next_state]
                if (g_comp!=0 and g_comp>g_max):
                    g_max=gamma_mat[l][state][next_state]
                    s1_max="gamma(l = "+str(l)+" ,"+str(state)+" --> "
                    s1_max+=str(next_state)+" ) ="
                    s1_max+=str(g_max)
        print(s1_max)
        print(s2_max)
        print(s3_max)
        print()
        

