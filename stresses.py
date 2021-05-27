#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 19:03:19 2021

@author: mathieubiava
"""
import sys

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

seeds_partition = [50] # int
number_repetition = 1 # int 
max_severity = 3 # int 
max_mesh = 2 # int 
max_iteration = 3 # int 

ra=[0.0]
nb_clusters=[0.0]

d2=[[0.0]]
i2=[0.0]
r2_2=[0.0]


for number_partition in seeds_partition :
    for repetition in range(number_repetition) :
        for severity in range(1, max_severity + 1) :
            for E in range(2, max_mesh + 1) :
                for iteration in range(3,max_iteration + 1): 
                    
                    """"""""""""""""""""" Load the numpy files """""""""""""""""""""
                    
                    if E<3:
                        inp_name = 'JobPart%sRep%sSev%sE%sIte%simage'%(number_partition, repetition, severity, E, iteration)
                    	
                        stress_distrib = inp_name + "stress.npy"
                        image_name = inp_name + ".txt"
                        
                        stresses = np.load(stress_distrib)
                        
                        #image =  np.loadtxt(image_name).reshape(50,50,50) #[[[1., 0., 1.],[1., 0., 1.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 0.],[1., 0., 1.]],
                                 #[[1., 0., 0.],[1., 0., 1.],[1., 0., 1.]]]#np.loadtxt(image_name).reshape(50,50,50)
                    else :
                        inp_name = 'JobPart%sRep%sSev%sE%sIte%s'%(number_partition, repetition, severity, E, iteration)
                        	
                        stress_distrib = inp_name + "stress.npy"
                        image_name = inp_name + ".npy"
                        
                        stresses = np.load(stress_distrib)
                        
                        #image = np.load(image_name) #[[[1., 0., 1.],[1., 0., 0.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 0.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 1.],[1., 0., 0.]]]
                        
                        # np.load(image_name) 
                    x = plt.hist(stresses, bins = 10)
                    plt.show()
                    