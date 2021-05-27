#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 14:03:10 2021

@author: mathieubiava
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from sklearn.linear_model import LinearRegression
import random

sys.setrecursionlimit(10**6)

def check(x,y,z,clustsize,ima) :
    imsize = ima.shape
    
    if x!=imsize[0]-1 :
        if ima[x+1][y][z] == 1 :
            ima[x+1][y][z] = 2 
            clustsize+=1
            ima, clustsize = check(x+1,y,z,clustsize,ima)
            
    if x!=0 :      
        if ima[x-1][y][z] == 1 : 
            clustsize+=1
            ima[x-1][y][z] = 2 
            ima, clustsize = check(x-1,y,z,clustsize,ima)
            
    if y!=imsize[1]-1 :
        if ima[x][y+1][z] == 1 :
            ima[x][y+1][z] = 2 
            clustsize+=1
            ima, clustsize = check(x,y+1,z,clustsize,ima)
            
    if y!=0 :       
        if ima[x][y-1][z] == 1 : 
            clustsize+=1
            ima[x][y-1][z] = 2 
            ima, clustsize = check(x,y-1,z,clustsize,ima)
            
    if z!=imsize[2]-1 :
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
max_severity = 1 # int 
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
                    	
                        # stress_distrib = inp_name + "stress.npy"
                        image_name = inp_name + ".txt"
                        
                        # stresses = np.load(stress_distrib)
                        
                        image = np.loadtxt(image_name).reshape(50,50,50) #[[[1., 0., 1.],[1., 0., 0.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 0.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 1.],[1., 0., 0.]]]
                    else :
                        inp_name = 'JobPart%sRep%sSev%sE%sIte%s'%(number_partition, repetition, severity, E, iteration)
                        	
                        # stress_distrib = inp_name + "stress.npy"
                        image_name = inp_name + ".npy"
                        
                        # stresses = np.load(stress_distrib)
                        
                        image =  np.load(image_name)#[[[0., 1., 1.],[1., 0., 0.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 0.],[1., 0., 0.]],
                                 #[[1., 0., 0.],[1., 0., 1.],[1., 0., 0.]]] #n p.load(image_name)
                        
                        # np.load(image_name) 
                    
                    imsize = len(image)
                    
                    if severity==3:
                        noise=200
                    elif severity==2:
                        noise=1000
                    elif severity==1:
                        noise=1500
                    
                    for ran in range(noise):
                        n_x=random.randint(0, imsize-1)
                        n_y=random.randint(0, imsize-1)
                        n_z=random.randint(0, imsize-1)
                        
                        image[n_x,n_y,n_z]=1
                    
                    
                    ima = image.copy()
                    
                    img=ima[:,:,10]
                            
                    plt.imshow(img,cmap='gray')
                    plt.show()
                    
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
                    #print("Sizes cluster : ",clustlist)
                    
                    nb_clusters.append(clust)
                    
                    # t = plt.hist(clustlist, range(mincl, maxcl+2,1))   
                    # plt.show() 
                    
                    #fe = t[1][0:-1]
                    
                    
                    """"""""""""""""""""" Cumulative function and linear regression """""""""""""""""""""
                    
                    num = np.zeros(maxcl)
                    
                    x=[]
                    
                    for i in clustlist :
                        if i not in x :
                            x.append(i)
                            
                        num[i-1]+=1
                        
                    # print("Number by size : ",num[:20] )
                    
                    x.sort()
                    
                    # print("x: ",x)
                    
                    cumulation = np.zeros(len(x))
                    
                    cum=0
                    
                    for i in num :
                        if i !=0 :
                            cumulation[cum]=i
                            cum+=1
                            
                    # print(cumulation)
                    
                    cumul2 = np.zeros(len(cumulation))
                    
                    cum2=0
                    
                    for i in range(len(cumulation)-1,-1,-1) :
                        cum2+=cumulation[i]
                        cumul2[i]=cum2
                          
                    #print("Cumulation decreasing : ", cumul2)
                    
                    #plt.plot(x,cumul2)
                    #plt.ylabel('cumul2')
                    #plt.show()
                    
                    x_reg=np.zeros(len(x))
                    
                    count=0
                    for i in x:
                        x_reg[count]=i
                        count+=1
                        
                    
                    
                    
                    for a in range(0,1):
                        
                        for n in range(0,1):
                            
                            m=0
                            
                            for i in cumul2:
                                if i>=n:
                                    m+=1
                            
                            c2 = cumul2[a:m]
                            
                            #print(c2)
                            
                            # print(cumul2,c2,len(cumul2),len(c2))
                            
                            
                            #print(x_reg)
                            
                            #plt.plot(np.log10(x_reg2),np.log10(c2))
                            #plt.ylabel("%s %s %s"%(severity, E, iteration))
                            #plt.show()
                            
                            x_reg2 = x_reg[a:m].reshape((-1, 1))
                            
                            # print(x_reg2)
                            
                            reg_lin2 =  LinearRegression().fit(np.log10(x_reg2),np.log10(c2))
                            
                            print("D 2 : ",reg_lin2.coef_)
                            print("Intercept 2 : ",reg_lin2.intercept_)
                            print("Coefficient of determination 2 : ",reg_lin2.score(np.log10(x_reg2),np.log10(c2)))
                            
                            d2.append(reg_lin2.coef_)
                            i2.append(reg_lin2.intercept_)
                            r2_2.append(reg_lin2.score(np.log10(x_reg2),np.log10(c2)))
                            
                            print("\n")
                            
                            y_reg= reg_lin2.coef_ * np.log10(x_reg[a:m]) + reg_lin2.intercept_
                            
                            plt.plot(np.log10(x_reg),np.log10(cumul2),'.', color='red')
                            plt.plot(np.log10(x_reg[a:]),y_reg,color='orange')
                            plt.ylabel("%s %s %s"%(severity, E, iteration))   
                            
                            plt.show()
                            
                            # plt.show()
                            
                            """"""""""""""""""""" Stress distribution """""""""""""""""""""
                            
                            # x = plt.hist(stresses, bins = 10)
                            # plt.show()
                            
                        
                        
                    for ct in range(severity+1,severity+2):
                        
                        if ct==1:
                            
                            img = nib.load('LA950_Model_200_10.nii')
                        
                        elif ct==2:
                            
                            img = nib.load('LA950_Model_300_15.nii')
                        
                        elif ct==3:
                            
                            img = nib.load('LA950_Model_450_20.nii')
                            
                        elif ct==4:
                            
                            img = nib.load('LA950_Model_800_25.nii')
                        
                        print('\n \n CT number : ',ct)
                    
                        data = img.get_fdata()
                        affine = img.affine
                        hdr = img.header
                        
                        #print("Affine: ",affine)
                        #print("Data: ",data)
                        #print("Header: ",hdr)
                        #print("Image: ",img1)
                        
                        '''
                        for i in data:
                            plt.imshow(i,cmap='gray')
                            plt.show()
                        '''  
                        
                        b=data.shape
                        
                        pixelsize = hdr.get_zooms()
                        
                        x_max=0
                        
                        x_min=b[0]
                        
                        for x in range(b[0]):
                            if np.any(data[x]):
                                if x<x_min:
                                    x_min=x
                                elif x>x_max:
                                    x_max=x
                        
                        # print(x_max,x_min)
                            
                        
                        y_max=0
                        
                        y_min=b[1]
                        
                        for y in range(b[1]):
                            if np.any(data[:,y]):
                                if y<y_min:
                                    y_min=y
                                elif y>y_max:
                                    y_max=y
                                    
                        # print(y_max,y_min)
                        
                        z_max=0
                        
                        z_min=b[2]
                        
                        for z in range(b[2]):
                            if np.any(data[:,:,z]):
                                if z<z_min:
                                    z_min=z
                                elif z>z_max:
                                    z_max=z
                                    
                        # print(z_max,z_min)
                        
                        
                        
                        x_coo=50
                        y_coo=int(round(50*pixelsize[0]/pixelsize[1]))
                        z_coo=int(round(50*pixelsize[0]/pixelsize[2]))
                        
                        
                        positions=[]
                        lavlist=[0.0]
                        
                        pix = x_coo*y_coo*z_coo
                        
                        for x in range(x_min,x_max-x_coo+2,10): # x_min
                            for y in range(y_min,y_max-y_coo+2,10):
                                for z in range(z_min,z_max-z_coo+2,10):
                                    
                                    cube = data[x:x+x_coo,y:y+y_coo,z:z+z_coo]
                                    
                                    #if (np.any(data[x:x+x_coo,y:y+y_coo,z:z+z_coo])):
                                    #    print(x,y,z)
                                    
                                    # print(cube.shape)
                                    
                                    
                                    nbpix = np.count_nonzero(cube)
                                    
                                    LAV=nbpix/pix
                                    
                                    # print(LAV)
                                    
                                    if ra[-1]+0.05>LAV>ra[-1]-0.05:
                                        
                                        lavlist.append(LAV)
                                        positions.append((x,y,z))
                        
                        
                        nb_clusters_im=[0.0]
                        d=[[0.0]]
                        inter=[0.0]
                        r2=[0.0]
                        pos=[   (330, 147, 91)]
                        
                        for i in pos:
                            
                            cube1 = data[i[0]:i[0]+x_coo,i[1]:i[1]+y_coo,i[2]:i[2]+z_coo]  
                            
                            cube = cube1.copy()
                            
                            nbpix = np.count_nonzero(cube)
                                    
                            LAV=nbpix/pix
                            img=cube[:,:,round(z_coo/2)]
                            
                            clustlist = []
                            
                            clustsize = 0 
                            clust = 0 
                            
                            for x in range(x_coo):
                                for y in range(y_coo):
                                    for z in range(z_coo):
                                        
                                        if cube[x][y][z] == 1 : 
                                            clustsize = 1
                                            clust += 1
                                            cube[x][y][z] = 2 
                                            
                                            cube, clustsize = check(x,y,z,clustsize,cube)
                                            clustlist.append(clustsize)
                            
                            maxcl = max(clustlist)  
                            mincl = min(clustlist)
                            
                            # also bar
                            
                            
                            #print("Sizes cluster : ",clustlist)
                            
                            nb_clusters_im.append(clust)
                            
                            
                            # t = plt.hist(clustlist, range(mincl, maxcl+2,1))   
                            # plt.show() 
                            
                            #fe = t[1][0:-1]
                            
                            num = np.zeros(maxcl)
                            
                            x=[]
                            
                            for j in clustlist :
                                if j not in x :
                                    x.append(j)
                                    
                                num[j-1]+=1
                                
                            # print("Number by size : ",num[:20] )
                            
                            x.sort()
                            
                            # print("x: ",x)
                            
                            cumulation = np.zeros(len(x))
                            
                            cum=0
                            
                            for j in num :
                                if j !=0 :
                                    cumulation[cum]=j
                                    cum+=1
                                    
                            # print(cumulation)
                            
                            cumul2_im = np.zeros(len(cumulation))
                            
                            cum2=0
                            
                            for j in range(len(cumulation)-1,-1,-1) :
                                cum2+=cumulation[j]
                                cumul2_im[j]=cum2
                                  
                            #print("Cumulation decreasing : ", cumul2)
                            
                            #plt.plot(x,cumul2)
                            #plt.ylabel('cumul2')
                            #plt.show()
                            
                            x_reg_im=np.zeros(len(x))
                            
                            count=0
                            for j in x:
                                x_reg_im[count]=j*pixelsize[1]*pixelsize[2]/(pixelsize[0]*pixelsize[0])
                                count+=1
                            
                            
                            for a in range(0,1):
                                
                                if clust > 50 :
                                    
                                    n=0
                                    
                                    # print(i)
                                    
                                    m=0
                                    
                                    for j in cumul2_im:
                                        if j>=n:
                                            m+=1
                                    
                                    c2 = cumul2_im[a:m]
                                    
                                    #print(c2)
                                    
                                    # print(cumul2,c2,len(cumul2),len(c2))
                                    
                                    
                                    #print(x_reg_im)
                                    
                                    #plt.plot(np.log10(x_reg2),np.log10(c2))
                                    #plt.ylabel("%s %s %s"%(severity, E, iteration))
                                    #plt.show()
                                    
                                    x_reg2 = x_reg_im[a:m].reshape((-1, 1))
                                    
                                    # print(x_reg2)
                                    
                                    reg_lin2_im =  LinearRegression().fit(np.log10(x_reg2),np.log10(c2))
                                    
                                    d.append(reg_lin2_im.coef_)
                                    inter.append(reg_lin2_im.intercept_)
                                    r2.append(reg_lin2_im.score(np.log10(x_reg2),np.log10(c2)))
                                    
                                    if d2[-1]-0.05 < d[-1] < d2[-1]+0.05 and r2[-1]>0.9:
                                    
                                    
                                        print("LAV : " ,LAV) 
                                        print("Number of clusters : ",clust)
                                        print("Positions : ",i)
                                        
                                        
                                        print("D 2 : ",reg_lin2_im.coef_)
                                        print("Intercept 2 : ",reg_lin2_im.intercept_)
                                        print("Coefficient of determination 2 : ",reg_lin2_im.score(np.log10(x_reg2),np.log10(c2)))
                                        
                                        
                                        y_mid= (max(y_reg)+min(y_reg))/2
                                        logx_mid= (max(np.log10(x_reg))+min(np.log10(x_reg)))/2
                                        print(y_mid,logx_mid)
                                        
                                        K = (y_mid-reg_lin2_im.intercept_)/reg_lin2_im.coef_ -logx_mid
                                        
                                        y_im= reg_lin2_im.coef_ * np.log10(x_reg_im[a:m]) + reg_lin2_im.intercept_
                                        
                                        plt.title("Model severity %s, CT severity %s"%(severity, ct))
                                        plt.ylabel("Number of clusters")
                                        plt.xlabel('Cumulative clusters size distribution')
                                           
                                        plt.plot(x_reg[a:],np.power(10,y_reg),"r--", label="Model")
                                        plt.plot(x_reg_im[a:m]*np.power(10,-K),np.power(10,y_im),"b--", label="CT")
                                        
                                        
                                        plt.plot(x_reg,cumul2,".", color='red',label="Model")
                                        plt.plot(x_reg_im*np.power(10,-K),cumul2_im,"+", color='blue',label="CT")
                                        plt.legend(loc="upper right")
                                        # plt.ylabel("%s %s %s %s"%(severity, E, iteration,i))   
                                        plt.yscale('log')
                                        plt.xscale('log')
                                        
                                        plt.show()
                                        
                                        print("\n")
                                
                                        plt.imshow(img,cmap='gray')
                                        plt.show()
                                
                                    
                                
                                
                                
  




