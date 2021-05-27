#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 19:39:45 2021

@author: mathieubiava
"""
seeds_partition = [50] # int
number_repetition = 1 # int 
max_severity = 4 # int 
max_mesh = 4 # int 
max_iteration = 3 # int 

time_rem=[]
time_sets=[]
time_boundary=[]
time_job=[]
time_stress=[]
time_image=[]
time_total=[]

for number_partition in seeds_partition :
    for repetition in range(number_repetition) :
        for severity in range(1, max_severity + 1) :
            for E in range(1, max_mesh + 1) :
                for iteration in range(max_iteration + 1): 
                    
                    """"""""""""""""""""" Load the numpy files """""""""""""""""""""
                    
                    if E<3:
                        inp_name = 'E1E2/Run 3/JobPart%sRep%sSev%sE%sIte%s'%(number_partition, repetition, severity, E, iteration)
                    	
                        # stress_distrib = inp_name + "stress.npy"
                        image_name = inp_name + ".txt"
                        
                        # stresses = np.load(stress_distrib)
                        
                        filin = open(image_name, "r")#[[[1., 0., 1.],[1., 0., 1.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 0.],[1., 0., 1.]],
                                 #[[1., 0., 0.],[1., 0., 1.],[1., 0., 1.]]]#np.loadtxt(image_name).reshape(50,50,50)
                    else :
                        inp_name = 'Run 3/%s/JobPart%sRep%sSev%sE%sIte%s'%(severity,number_partition, repetition, severity, E, iteration)
                        	
                        # stress_distrib = inp_name + "stress.npy"
                        image_name = inp_name + ".txt"
                        filin = open(image_name, "r")
                        
                    for i in filin:
                        a=i.split()
                        print(a)
                        for j in a:
                            if j=='remove':
                                time_rem.append(float(a[3]))
                            elif j=='sets':
                                time_sets.append(float(a[3]))
                            elif j=='boundary':
                                time_boundary.append(float(a[4]))
                            elif j=='job':
                                time_job.append(float(a[3]))
                            elif j=='stress':
                                time_stress.append(float(a[3]))
                            elif j=='image':
                                time_image.append(float(a[3]))
                                
                    time_total.append(float(a[2]))
                                
                 
                                
                                