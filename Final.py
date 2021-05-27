# -*- coding: mbcs -*-

""" 

University : ULB

Master Thesis : Development of a validated 3D Numerical model of the Human Lung 
				to predict COVID-19 Tissue Damage and Degeneration

Author : Mathieu Biava

Versions : ABAQUS/CAE 2019

Description : 	Simulation of emphysema in a lung for different severities. The geometry is a cube. 
				An orphan mesh is used. The material property is isotropic, linear and homogeneous. 
				The boundary condition is a displacement applied at the borders. 


"""


import random
import operator
import time
import numpy as np

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from odbAccess import *	

	

""""""""""""""""""""" General Parameters """""""""""""""""""""""""""

version = "ABAQUS/CAE 2019"

seeds_partition = [50] # int
number_repetition = 20 # int 
max_severity = 4 # int 
max_mesh = 4 # int 
max_iteration = 3 # int 

cube_size = 0.03 # in meters 

young_modulus = 800 # in Pascals
poisson_s_ratio = 0.3	

strain = 0.2 

percentage_mises = 0.7





for number_partition in seeds_partition :

	for repetition in range(number_repetition) :
		
		for severity in range(1, max_severity + 1) :
		
		
			""""""""""""""""""""" Create Random Mask """""""""""""""""""""""""""
		
			total = number_partition * number_partition * number_partition
			
			if (severity==1) :
				N = int(total * 0.005)
				Smax = 10
			elif(severity==2) :
				N = int(total * 0.0075)
				Smax = 15
			elif(severity==3) :
				N = int(total * 0.01125)
				Smax = 20
			elif(severity==4) :
				N = int(total * 0.02)
				Smax = 25
			
			rem_nodes = []
			
			for i in range(N) :

				N_x = random.randint(0,number_partition) 
				N_y = random.randint(0,number_partition)	
				N_z = random.randint(0,number_partition)
				S = random.randint(1,Smax + 1)
				
				for j in range(S) :
				
					if (j!=0) :
					
						direction = random.randint(0,5)
						if (direction==0) :
							N_x += 1 ;
						elif(direction==1) :
							N_x -= 1 ;
						elif(direction==2) :
							N_y += 1 ;
						elif(direction==3) :
							N_y -= 1 ;
						elif(direction==4) :
							N_z += 1;
						elif(direction==5) :
							N_z -= 1 ;
						else :
							print("Error Mask")
								
					rem_nodes.append((N_x, N_y, N_z))
			
			
			for E in range(1, max_mesh + 1) :
			
				start = time.time()
			
			
				""""""""""""""""""""" Parameters Definition """""""""""""""""""""""""""
				
				scale = cube_size * 2
				origin_x = 0 # origin required 
				origin_y = 0
				origin_z = 0
				
				partition_param = operator.truediv(1 , number_partition)
				size_partition = partition_param * cube_size
				semi_part = size_partition * 0.5
				
				size_mesh = operator.truediv(size_partition, E)
				semi_mesh = operator.truediv(size_mesh, 2)
				
				displacement_applied = strain * cube_size
				
				
				""""""""""""""""""""" Formation of a Cube Orphan Mesh """""""""""""""""""""""""""
				
				start_cube = time.time()

				mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=scale)
				mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(origin_x, origin_y), 
					point2=(cube_size, cube_size)) 
				mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
					DEFORMABLE_BODY)
				mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth= cube_size, sketch=
					mdb.models['Model-1'].sketches['__profile__'])
				del mdb.models['Model-1'].sketches['__profile__']

				mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, 
					minSizeFactor=0.1, size=size_mesh)
				mdb.models['Model-1'].parts['Part-1'].generateMesh()
				mdb.models['Model-1'].parts['Part-1'].PartFromMesh(copySets=True, name=
					'Part-1-mesh-1')
					
				del mdb.models['Model-1'].parts['Part-1']
					
				end_cube = time.time()
				

				""""""""""""""""""""" Remove Random Nodes """""""""""""""""""""""""""
				
				start_remove = time.time() 
				
				for m in rem_nodes :

					N_x = m[0] * size_partition
					N_y = m[1] * size_partition		
					N_z = m[2] * size_partition
					
					mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
									mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
									N_x-size_partition+semi_mesh,
									N_y-size_partition+semi_mesh,
									N_z-size_partition+semi_mesh,
									N_x+size_partition-semi_mesh,
									N_y+size_partition-semi_mesh,
									N_z+size_partition-semi_mesh ))
				
				end_remove = time.time()
				
										
				""""""""""""""""""""" Sets """""""""""""""""""""""""""		
				
				start_sets = time.time()
									
				mdb.models['Model-1'].parts['Part-1-mesh-1'].Set(name='Set-1', elements=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].elements.getByBoundingBox(
					-semi_part,-semi_part,-semi_part,
					cube_size+semi_part,cube_size+semi_part,cube_size+semi_part  ))
										
				mdb.models['Model-1'].parts['Part-1-mesh-1'].Set(name='Set-BC-1', nodes=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox(
					-semi_part,-semi_part,-semi_part,semi_part,cube_size+semi_part,cube_size+semi_part  ))
					
				mdb.models['Model-1'].parts['Part-1-mesh-1'].Set(name='Set-BC-2', nodes=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox(
					-semi_part,-semi_part,-semi_part,cube_size+semi_part,semi_part,cube_size+semi_part  ))
					
				mdb.models['Model-1'].parts['Part-1-mesh-1'].Set(name='Set-BC-3', nodes=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox(
					-semi_part,-semi_part,-semi_part,cube_size+semi_part,cube_size+semi_part,semi_part  ))

				mdb.models['Model-1'].parts['Part-1-mesh-1'].Set(name='Set-BC-4', nodes=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox(
					-semi_part,-semi_part,cube_size-semi_part,cube_size+semi_part,cube_size+semi_part,cube_size+semi_part  ))

				mdb.models['Model-1'].parts['Part-1-mesh-1'].Set(name='Set-BC-5', nodes=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox(
					-semi_part,cube_size-semi_part,-semi_part,cube_size+semi_part,cube_size+semi_part,cube_size+semi_part  ))

				mdb.models['Model-1'].parts['Part-1-mesh-1'].Set(name='Set-BC-6', nodes=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox(
					cube_size-semi_part,-semi_part,-semi_part,cube_size+semi_part,cube_size+semi_part,cube_size+semi_part  ))
				
				end_sets = time.time()
				
				
				""""""""""""""""""""" Section Assignment """""""""""""""""""""""""""	
			
				mdb.models['Model-1'].Material(name='Material-1')
				mdb.models['Model-1'].materials['Material-1'].Elastic(table=((young_modulus, poisson_s_ratio), ))

				mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
					'Section-1', thickness=None)
					
				mdb.models['Model-1'].parts['Part-1-mesh-1'].SectionAssignment(offset=0.0, 
					offsetField='', offsetType=MIDDLE_SURFACE, region=
					mdb.models['Model-1'].parts['Part-1-mesh-1'].sets['Set-1'], sectionName=
					'Section-1', thicknessAssignment=FROM_SECTION)	
					
					
				""""""""""""""""""""" Assembly """""""""""""""""""""""""""		
			
				# Assembly Features
					
				mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)

				# Assembly Instance

				mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
					part=mdb.models['Model-1'].parts['Part-1-mesh-1'])
				
				
				""""""""""""""""""""" Step and Boundary Conditions """""""""""""""""""""""""""

				start_bc = time.time()
					
				mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
				mdb.models['Model-1'].steps['Step-1'].setValues(adaptiveDampingRatio=None, 
					continueDampingFactors=False, matrixSolver=ITERATIVE, matrixStorage=
					SOLVER_DEFAULT, solutionTechnique=FULL_NEWTON, stabilizationMethod=NONE)
							
				mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
					distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
					'BC-1', region=
					mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-BC-1'], 
					u1=-displacement_applied, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
					
				mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
					distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
					'BC-2', region=
					mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-BC-2'], 
					u1=UNSET, u2=-displacement_applied, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
					
				mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
					distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
					'BC-3', region=
					mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-BC-3'], 
					u1=UNSET, u2=UNSET, u3=-displacement_applied, ur1=UNSET, ur2=UNSET, ur3=UNSET)
					
				mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
					distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
					'BC-4', region=
					mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-BC-4'], 
					u1=UNSET, u2=UNSET, u3=displacement_applied, ur1=UNSET, ur2=UNSET, ur3=UNSET)
					
				mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
					distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
					'BC-5', region=
					mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-BC-5'], 
					u1=UNSET, u2=displacement_applied, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
					
				mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
					distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
					'BC-6', region=
					mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].sets['Set-BC-6'], 
					u1=displacement_applied, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
					
				end_bc = time.time()
				
				
				""""""""""""""""""""" Field Output Request """""""""""""""""""""
			
				mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
					'S','E','PE', 'PEMAG', 'U', 'COORD')) 
					
					
				for iteration in range(max_iteration + 1): 
					
					
					""""""""""""""""""""" Redefined Parameters """""""""""""""""""""
				
					inp_name = 'JobPart%sRep%sSev%sE%sIte%s'%(number_partition, repetition, severity, E, iteration)
					stress_distrib = inp_name + "stress.npy"
					image_name = inp_name + ".npy"
					odbPath = inp_name + ".odb"
					text_name = inp_name + ".txt"
					
					image = np.ones((number_partition,number_partition,number_partition))
					remove_nodes = []
					
				
					""""""""""""""""""""" Remove Elements with high stress """""""""""""""""""""""""""
					
					if iteration != 0 :
					
						start = time.time()
						start_remove = time.time()
						
						if iteration == 1 :

							max_mises = 0
							threshold = 0
						
							for svalue in s.values :
								if svalue.mises > max_mises :
									max_mises = svalue.mises

							threshold = percentage_mises * max_mises
							
						for svalue in s.values :
							if svalue.mises > threshold :
								if svalue.nodeLabel not in remove_nodes :
									remove_nodes.append(svalue.nodeLabel)
							
						for node in initial_nodes :
							
							if node[0] in remove_nodes :
								
								pos_part = (node[1]//size_partition)*size_partition
								rel_pos = node[1] - pos_part
								
								if rel_pos[0]== 0 :
									if rel_pos[1]== 0 :
										if rel_pos[2] == 0 : 
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]-size_partition+semi_mesh,
															pos_part[1]-size_partition+semi_mesh,
															pos_part[2]-size_partition+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))
										else :
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]-size_partition+semi_mesh,
															pos_part[1]-size_partition+semi_mesh,
															pos_part[2]+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))
									else : 
										if rel_pos[2] == 0 : 
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]-size_partition+semi_mesh,
															pos_part[1]+semi_mesh,
															pos_part[2]-size_partition+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))
										else :
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]-size_partition+semi_mesh,
															pos_part[1]+semi_mesh,
															pos_part[2]+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))
															
								else : 
									if rel_pos[1]== 0 :
										if rel_pos[2] == 0 : 
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]+semi_mesh,
															pos_part[1]-size_partition+semi_mesh,
															pos_part[2]-size_partition+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))
										else :
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]+semi_mesh,
															pos_part[1]-size_partition+semi_mesh,
															pos_part[2]+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))
									else : 
										if rel_pos[2] == 0 : 
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]+semi_mesh,
															pos_part[1]+semi_mesh,
															pos_part[2]-size_partition+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))
										else :
											mdb.models['Model-1'].parts['Part-1-mesh-1'].deleteNode(nodes=
															mdb.models['Model-1'].parts['Part-1-mesh-1'].nodes.getByBoundingBox( 
															pos_part[0]+semi_mesh,
															pos_part[1]+semi_mesh,
															pos_part[2]+semi_mesh,
															pos_part[0]+size_partition-semi_mesh,
															pos_part[1]+size_partition-semi_mesh,
															pos_part[2]+size_partition-semi_mesh ))				
										
						end_remove = time.time()
					
						
					""""""""""""""""""""" Job """""""""""""""""""""""""""	
					
					start_job = time.time()
					
					mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
						explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
						memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
						multiprocessingMode=DEFAULT, name=inp_name, nodalOutputPrecision=SINGLE, 
                                                numCpus=4, numDomains=4, parallelizationMethodExplicit=DOMAIN,
						#parallel=DOMAIN, domains=4,
                                                numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
						ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)	
						
					# mdb.jobs[inp_name].writeInput(consistencyChecking=OFF)
					mdb.jobs[inp_name].submit(consistencyChecking=OFF)
					mdb.jobs[inp_name].waitForCompletion()
					
					end_job = time.time()
					
					
					""""""""""""""""""""" Post Processing """""""""""""""""""""""""""
					
					odb = openOdb(path=odbPath)
					assembly = odb.rootAssembly
					
					
					""""""""""""""""""""" Generate Stresses """""""""""""""""""""""""""
					
					start_stress = time.time()
					
					s = odb.steps['Step-1'].frames[-1].fieldOutputs['S'].getSubset(position = ELEMENT_NODAL )
					
					stresses = []
					
					for svalue in s.values :
						stresses.append((svalue.elementLabel , svalue.nodeLabel , svalue.mises))
					
					try :
						np.save(stress_distrib , stresses)
					except : 
						print('Error numpy stress')
					
					end_stress = time.time()
					
					
					""""""""""""""""""""" Generate Image """""""""""""""""""""""""""
					
					start_image = time.time()
					
					u = odb.steps['Step-1'].frames[-1].fieldOutputs['U']
					coord = odb.steps['Step-1'].frames[0].fieldOutputs['COORD']
					
					if len(u.values) != len(coord.values) : 
						print "Error"
						
					initial_nodes = []
					
					for i in range(len(u.values)):
					
						uvalue = u.values[i]
						coordvalue = coord.values[i]
						
						if coordvalue.nodeLabel == uvalue.nodeLabel :
						
							initial_nodes.append((coordvalue.nodeLabel,coordvalue.data))
						
							node = coordvalue.data + uvalue.data
							node -= (semi_part,semi_part,semi_part)
							node //= size_partition
							
							if node[0]>=0 and node[0]<number_partition :
								if node[1]>=0 and node[1]<number_partition :
									if node[2]>=0 and node[2]<number_partition :
										x = int(node[0])
										y = int(node[1])
										z = int(node[2])
										image[x][y][z] = 0			
								
						else : 
						
							print 'Error Node Label '
					
					try :
						np.save(image_name , image)
					except : 
						print('Error numpy image')
						
					end_image = time.time()
					
					end = time.time()
					
					
					""""""""""""""""""""" Time """""""""""""""""""""""""""
					
					time_cube = end_cube - start_cube
					time_remove = end_remove - start_remove
					time_sets = end_sets - start_sets
					time_bc = end_bc - start_bc
					time_job = end_job - start_job
					time_stress = end_stress - start_stress
					time_image = end_image - start_image
					time_prog = end - start 
					
					
					""""""""""""""""""""" File with the general parameters """""""""""""""""""""""""""

					f = open(text_name,"w")
					
					f.write(version+"\n")
					
					f.write("Number partition : %s \n" %number_partition)
					
					f.write("Repetition : %s \n" %repetition)
					
					f.write("Severity : %s \n" %severity)
					
					f.write("E : %s \n" %E)
					
					f.write("Iteration : %s \n" %iteration)
					
					f.write("Cube size : %s \n" %cube_size)
					
					f.write("Young Modulus : %s, Poisson's ratio : %s \n" %(young_modulus,poisson_s_ratio))
					
					f.write("N : %s, Smax : %s \n" %(N,Smax) )
					
					f.write("Strain : %s \n" %strain) 
					
					f.write("Percentage Mises : %s \n \n" %percentage_mises)
					
					f.write("Time cube : %s seconds / %s \n" %(time_cube,
						time.strftime("%H:%M:%S", time.gmtime(time_cube)) ))
						
					f.write("Time remove : %s seconds / %s \n" %(time_remove,
						time.strftime("%H:%M:%S", time.gmtime(time_remove)) ))
						
					f.write("Time sets : %s seconds / %s \n" %(time_sets,
						time.strftime("%H:%M:%S", time.gmtime(time_sets)) ))
						
					f.write("Time boundary conditions : %s seconds / %s \n" %(time_bc,
						time.strftime("%H:%M:%S", time.gmtime(time_bc)) ))
						
					f.write("Time job : %s seconds / %s \n" %(time_job,
						time.strftime("%H:%M:%S", time.gmtime(time_job)) ))
						
					f.write("Time stress : %s seconds / %s \n" %(time_stress,
						time.strftime("%H:%M:%S", time.gmtime(time_stress)) ))
						
					f.write("Time image : %s seconds / %s \n" %(time_image,
						time.strftime("%H:%M:%S", time.gmtime(time_image)) ))
	
					f.write("Time : %s seconds / %s \n" %(time_prog,
						time.strftime("%H:%M:%S", time.gmtime(time_prog)) ))
						
					f.close()

				
