#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 10:32:11 2020

@author: mathieubiava
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

sys.setrecursionlimit(10**6)

def check(x,y,z,clustsize,ima) :
    imsize = len(ima)
    
    if x!=imsize-1 :
        if ima[x+1][y][z] == 1 :
            ima[x+1][y][z] = 2 
            clustsize+=1
            ima, clustsize = check(x+1,y,z,clustsize,ima)
            
    if x!=0 :      
        if ima[x-1][y][z] == 1 : 
            clustsize+=1
            ima[x-1][y][z] = 2 
            ima, clustsize = check(x-1,y,z,clustsize,ima)
            
    if y!=imsize-1 :
        if ima[x][y+1][z] == 1 :
            ima[x][y+1][z] = 2 
            clustsize+=1
            ima, clustsize = check(x,y+1,z,clustsize,ima)
            
    if y!=0 :       
        if ima[x][y-1][z] == 1 : 
            clustsize+=1
            ima[x][y-1][z] = 2 
            ima, clustsize = check(x,y-1,z,clustsize,ima)
            
    if z!=imsize-1 :
        if ima[x][y][z+1] == 1 :
            clustsize+=1
            ima[x][y][z+1] = 2 
            ima, clustsize = check(x,y,z+1,clustsize,ima)
            
    if z!=0  :
        if ima[x][y][z-1] == 1 : 
            clustsize+=1
            ima[x][y][z-1] = 2 
            ima, clustsize = check(x,y,z-1,clustsize,ima)
            
    return ima,clustsize



seeds_partition = [50] # int
number_repetition = 1 # int 
max_severity = 3 # int 
max_mesh = 4 # int 
max_iteration = 3 # int 

ra=[]
nb_clusters=[]
d1 =[]
i1=[]
r2_1=[]
d2=[]
i2=[]
r2_2=[]


for number_partition in seeds_partition :
    for repetition in range(number_repetition) :
        for severity in range(1, max_severity + 1) :
            for E in range(3, max_mesh + 1) :
                for iteration in range(max_iteration + 1): 
                    
                    
                    """"""""""""""""""""" Load the numpy files """""""""""""""""""""
                    
                    inp_name = 'JobPart%sRep%sSev%sE%sIte%s'%(number_partition, repetition, severity, E, iteration)
                    	
                    # stress_distrib = inp_name + "stress.npy"
                    image_name = inp_name + ".npy"
                    
                    # stresses = np.load(stress_distrib)
                    
                    image = np.load(image_name) #[[[1., 0., 1.],[1., 0., 0.],[1., 0., 0.]],
                             #[[1., 0., 0.],[1., 0., 0.],[1., 0., 0.]],
                             #[[1., 0., 0.],[1., 0., 1.],[1., 0., 0.]]]
                    
                    # np.load(image_name) 
                    
                    imsize = len(image)
                    
                    ima = image.copy()
                    
                    print(inp_name)
                    print("Severity : ",severity, "/ E : ", E, "/ Iteration : ", iteration)
                    
                    """"""""""""""""""""" Computation of the relative area """""""""""""""""""""
                    
                    nbpix = np.count_nonzero(image)
                    # print(image)
                    pix = imsize*imsize*imsize
                    
                    # print(nbpix , pix)
                    
                    print("RA : ",nbpix/pix)
                    
                    ra.append(nbpix/pix)
                    
                    """"""""""""""""""""" Count clusters and cluster sizes """""""""""""""""""""
                    
                    clustlist = []
                    
                    clustsize = 0 
                    clust = 0 
                    
                    for x in range(imsize):
                        for y in range(imsize):
                            for z in range(imsize):
                                
                                if ima[x][y][z] == 1 : 
                                    clustsize = 1
                                    clust += 1
                                    ima[x][y][z] = 2 
                                    
                                    ima, clustsize = check(x,y,z,clustsize,ima)
                                    clustlist.append(clustsize)
                    
                    maxcl = max(clustlist)  
                    mincl = min(clustlist)
                    
                    # also bar
                    
                    print("Number of clusters : ",clust)
                    # print("Sizes cluster : ",clustlist)
                    
                    nb_clusters.append(clust)
                    
                    # t = plt.hist(clustlist, range(mincl, maxcl+2,1))   
                    # plt.show() 
                    
                    #fe = t[1][0:-1]
                    
                    
                    """"""""""""""""""""" Cumulative function and linear regression """""""""""""""""""""
                    
                    num = np.zeros(maxcl)
                    
                    for i in clustlist :
                        num[i-1]+=1
                    # print("Number by size : ",num)
                    
                    cumul = np.zeros(maxcl)
                    cum=0
                    count=0
                    
                    for i in num :
                        cum+=i
                        cumul[count]=cum
                        count+=1
                    
                    # print("Cumulation increasing : ",cumul )
                    
                    cumul2 = np.zeros(maxcl)
                    cum2=0
                    
                    for i in range(len(num)-1,-1,-1) :
                        
                        cum2+=num[i]
                        cumul2[i]=cum2
                        
                    # print("Cumulation decreasing : ", cumul2)
                    
                    x = np.arange(1, maxcl+1, 1)
                    # print(x)
                    
                    #plt.plot(x,cumul)
                    #plt.ylabel('cumul')
                    #plt.show()
                    
                    #plt.plot(x,cumul2)
                    #plt.ylabel('cumul2')
                    #plt.show()
                    
                    c=cumul[3:]
                    # print(cumul,c,len(cumul),len(c))
                    
                    m=0
                    for i in cumul2:
                        if i>=5:
                            m+=1
                    
                    c2=cumul2[3:m]
                    # print(cumul2,c2,len(cumul2),len(c2))
                    
                    reg = c.reshape((-1, 1))
                    # print(reg, np.log10(cumul))
                    
                    x_reg = np.arange(1, maxcl+1).reshape((-1, 1))
                    # print(x_reg,np.log10(x_reg))
                    
                    x_reg2 = np.arange(1, maxcl+1).reshape((-1, 1))
                    
                    
                    #plt.plot(np.log10(x_reg),np.log10(cumul))
                    #plt.ylabel()
                    #plt.show()
                    
                    plt.plot(np.log10(x_reg2),np.log10(cumul2))
                    plt.ylabel("%s %s %s"%(severity, E, iteration))
                    plt.show()
                    
                    
                    x_reg = np.arange(4, maxcl+1).reshape((-1, 1))
                    # print(x_reg,np.log10(x_reg))
                    
                    x_reg2 = np.arange(4, m+1).reshape((-1, 1))
                    
                    #plt.plot(np.log10(x_reg2),np.log10(c2))
                    #plt.ylabel("%s %s %s"%(severity, E, iteration))
                    #plt.show()
                    
                    reg_lin =  LinearRegression().fit(np.log10(x_reg),np.log10(c))
        
    
                    
                    print("D 1 : ",reg_lin.coef_)
                    print("Intercept 1 : ",reg_lin.intercept_)
                    print("Coefficient of determination 1 : ",reg_lin.score(np.log10(x_reg),np.log10(c)))
                    
                    d1.append(reg_lin.coef_)
                    i1.append(reg_lin.intercept_)
                    r2_1.append(reg_lin.score(np.log10(x_reg),np.log10(c)))
                    
                    reg_lin2 =  LinearRegression().fit(np.log10(x_reg2),np.log10(c2))
                    
    
                    
                    print("D 2 : ",reg_lin2.coef_)
                    print("Intercept 2 : ",reg_lin2.intercept_)
                    print("Coefficient of determination 2 : ",reg_lin2.score(np.log10(x_reg2),np.log10(c2)))
                    
                    d2.append(reg_lin2.coef_)
                    i2.append(reg_lin2.intercept_)
                    r2_2.append(reg_lin2.score(np.log10(x_reg2),np.log10(c2)))
                    
                    print("\n")
                    
                    """"""""""""""""""""" Stress distribution """""""""""""""""""""
                    
                    # x = plt.hist(stresses, bins = 10)
                    # plt.show()
                    






