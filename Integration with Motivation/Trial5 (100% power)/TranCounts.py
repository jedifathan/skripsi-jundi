###############################################################
#
#		"WhaleHuntGame" by Andy Schauf (2023)
#				a.schauf@nus.edu.sg
#				andyschauf@gmail.com
#	'The Whale Hunt game: A model of technology-mediated
#		social atomization in Lamalera and beyond'
#
###############################################################

import os, sys
import errno

import numpy as np
import random
import networkx as nx
from itertools import combinations

import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'Source Sans Pro'
# JASSS font (may need to install: 
#	'pip install font-source-sans-pro')
from matplotlib import colors

###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def TransitionCounts( Transitions , A , C , experiment , tag, \
					eta, trial, t_intervals=[], bawel=False ):

	#----------------------------------------------------------

	path = './post/' + experiment + \
			'/txt/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + str(trial) 
	file2 = path + '_TransCounts2.txt'
	file3 = path + '_TransCounts3.txt'
	file3a = path + '_TransCounts3a.txt'

	if ((not os.path.isfile(file2)) \
			or (not os.path.isfile(file3)) \
			or (not os.path.isfile(file3a))):

		if bawel:
			print('\tComputing transition counts')

		TwoStep = {}
		ThreeStepM = {}
		ThreeStepMa = {}
		if t_intervals:
			TwoStep_int = \
				{ }
			ThreeStepM_int = \
				{ }
			ThreeStepMa_int = \
				{ }			

		for at in Transitions.keys():

			TwoStep[at] = { c1:{ c2:0 for c2 in C } for c1 in C }
			ThreeStepM[at] = { c1:{ c2:0 for c2 in C } for c1 in C }
			ThreeStepMa[at] = { c1:{ c2:0 for c2 in C } for c1 in C }

			if t_intervals:
				TwoStep_int[at] = \
					{ t_int:{ c1:{ c2:0 for c2 in C } for c1 in C } for t_int in t_intervals }
				ThreeStepM_int[at] = \
					{ t_int:{ c1:{ c2:0 for c2 in C } for c1 in C } for t_int in t_intervals }
				ThreeStepMa_int[at] = \
					{ t_int:{ c1:{ c2:0 for c2 in C } for c1 in C } for t_int in t_intervals }
			else:
				TwoStep_int[at] = []
				ThreeStepM_int[at] = []
				ThreeStepMa_int[at] = []

		for at in Transitions.keys():
			print(at)
			#for a in A:
			for a in (Transitions[at].keys()):
				if Transitions[at][a]:
					
					sequence = Transitions[at][a][0][1]
					times = [0]

					sequence += \
							''.join([ ( t[2] ) for t in Transitions[at][a] ])
					times += [ ( t[0] ) for t in Transitions[at][a] ]
					sequence0 = \
							sequence[0] + \
							''.join([ sequence[si] for si in range(1,len(sequence)) \
								if (sequence[si]!=sequence[si-1])])
					times0 = \
							[times[0]] + \
								[ times[si] for si in range(1,len(sequence)) \
								if (sequence[si]!=sequence[si-1])]

					for c1 in C:
						for c2 in C:
							times2 = \
								[ times[i+1] for i in range(len(sequence)) \
									if sequence.startswith(c1+c2,i) ]
							times3 = \
								[ times[i+1] for i in range(len(sequence)) \
									if sequence.startswith(c1+'M'+c2,i) ]
							times3a = \
								[ times[i+1] for i in range(len(sequence0)) \
									if sequence0.startswith(c1+'M'+c2,i) ]
							TwoStep[at][c1][c2] += len(times2)
							ThreeStepM[at][c1][c2] += len(times3)
							ThreeStepMa[at][c1][c2] += len(times3a)

							if t_intervals:
								for t_int in t_intervals:

									TwoStep_int[at][t_int][c1][c2] += \
										len([t for t in times2 if ((t>=t_int[0]) and (t<t_int[1]))])
									ThreeStepM_int[at][t_int][c1][c2] += \
										len([t for t in times3 if ((t>=t_int[0]) and (t<t_int[1]))])
									ThreeStepMa_int[at][t_int][c1][c2] += \
										len([t for t in times3a if ((t>=t_int[0]) and (t<t_int[1]))])

			if (at=='pop'):
				addtag = ''
			else:
				addtag = '_' + at

			file2 = path + addtag + '_TransCounts2.txt'
			file3 = path + addtag + '_TransCounts3.txt'
			file3a = path + addtag + '_TransCounts3a.txt'

			tctxt = open( file2 , 'w' )
			tctxt.write('ALL:')
			for c1 in C:
				for c2 in C:
					tctxt.write(c1+'-'+c2+','+str(TwoStep[at][c1][c2])+';')
			tctxt.write('\n')
			if t_intervals:
				for t_int in t_intervals:			
					tctxt.write(str(t_int[0])+'-'+str(t_int[1])+':')
					for c1 in C:
						for c2 in C:
							tctxt.write(c1+'-'+c2+','+str(TwoStep_int[at][t_int][c1][c2])+';')
					tctxt.write('\n')
			tctxt.close()

			tctxt = open( file3 , 'w' )
			tctxt.write('ALL:')
			for c1 in C:
				for c2 in C:
					tctxt.write(c1+'-M-'+c2+','+str(ThreeStepM[at][c1][c2])+';')
			tctxt.write('\n')
			if t_intervals:
				for t_int in t_intervals:			
					tctxt.write(str(t_int[0])+'-'+str(t_int[1])+':')
					for c1 in C:
						for c2 in C:
							tctxt.write(c1+'-M-'+c2+','+str(ThreeStepM_int[at][t_int][c1][c2])+';')
					tctxt.write('\n')
			tctxt.close()

			tctxt = open( file3a , 'w' )
			tctxt.write('ALL:')
			for c1 in C:
				for c2 in C:
					tctxt.write(c1+'-M-'+c2+','+str(ThreeStepMa[at][c1][c2])+';')
			tctxt.write('\n')
			if t_intervals:
				for t_int in t_intervals:			
					tctxt.write(str(t_int[0])+'-'+str(t_int[1])+':')
					for c1 in C:
						for c2 in C:
							tctxt.write(c1+'-M-'+c2+','+str(ThreeStepMa_int[at][t_int][c1][c2])+';')
					tctxt.write('\n')
			tctxt.close()

	else:

		if bawel:
			print('\tLoading previously-computed transition counts')

		TwoStep = { }
		ThreeStepM = { }
		ThreeStepMa = { }
		if t_intervals:
			TwoStep_int = {}
			ThreeStepM_int = {}
			ThreeStepMa_int = {}


		for at in Transitions.keys():

			if (at=='pop'):
				addtag = ''
			else:
				addtag = '_' + at

			file2 = path + addtag + '_TransCounts2.txt'
			file3 = path + addtag + '_TransCounts3.txt'
			file3a = path + addtag + '_TransCounts3a.txt'

			TwoStep[at] = { c1:{ c2:0 for c2 in C } for c1 in C }
			ThreeStepM[at] = { c1:{ c2:0 for c2 in C } for c1 in C }
			ThreeStepMa[at] = { c1:{ c2:0 for c2 in C } for c1 in C }
			if t_intervals:
				TwoStep_int[at] = {}
				ThreeStepM_int[at] = {}
				ThreeStepMa_int[at] = {}

			line = open(file2).read().splitlines()[0]
			S2 = { (cn.split(',')[0].split('-')[0],cn.split(',')[0].split('-')[1]):int(cn.split(',')[1]) for cn in line.split(':')[1].split(';') if (cn!='') }
			for c1c2 in S2.keys():
				TwoStep[at][c1c2[0]][c1c2[1]] = S2[c1c2]
			if (len(open(file2).read().splitlines())>1):
				for line in open(file2).read().splitlines()[1:]:
					t_int = ( int(line.split(':')[0].split('-')[0]) , \
							  int(line.split(':')[0].split('-')[1]) )
					TwoStep_int[at][t_int] = { c1:{ c2:0 for c2 in C } for c1 in C }
					S2 = { (cn.split(',')[0].split('-')[0],cn.split(',')[0].split('-')[1]):int(cn.split(',')[1]) for cn in line.split(':')[1].split(';') if (cn!='') }
					for c1c2 in S2.keys():
						TwoStep_int[at][t_int][c1c2[0]][c1c2[1]] = S2[c1c2]

			line = open(file3).read().splitlines()[0]
			S3 = { (cn.split(',')[0].split('-')[0],cn.split(',')[0].split('-')[2]):int(cn.split(',')[1]) for cn in line.split(':')[1].split(';') if (cn!='') }
			for c1c2 in S3.keys():
				ThreeStepM[at][c1c2[0]][c1c2[1]] = S3[c1c2]
			if (len(open(file3).read().splitlines())>1):
				for line in open(file3).read().splitlines()[1:]:
					t_int = ( int(line.split(':')[0].split('-')[0]) , \
							  int(line.split(':')[0].split('-')[1]) )
					ThreeStepM_int[at][t_int] = { c1:{ c2:0 for c2 in C } for c1 in C }
					S3 = { (cn.split(',')[0].split('-')[0],cn.split(',')[0].split('-')[2]):int(cn.split(',')[1]) for cn in line.split(':')[1].split(';') if (cn!='') }
					for c1c2 in S3.keys():
						ThreeStepM_int[at][t_int][c1c2[0]][c1c2[1]] = S3[c1c2]

			line = open(file3a).read().splitlines()[0]
			S3a = { (cn.split(',')[0].split('-')[0],cn.split(',')[0].split('-')[2]):int(cn.split(',')[1]) for cn in line.split(':')[1].split(';') if (cn!='') }
			for c1c2 in S3a.keys():
				ThreeStepMa[at][c1c2[0]][c1c2[1]] = S3[c1c2]
			if (len(open(file3a).read().splitlines())>1):
				for line in open(file3a).read().splitlines()[1:]:
					t_int = ( int(line.split(':')[0].split('-')[0]) , \
							  int(line.split(':')[0].split('-')[1]) )
					ThreeStepMa_int[at][t_int] = { c1:{ c2:0 for c2 in C } for c1 in C }
					S3a = { (cn.split(',')[0].split('-')[0],cn.split(',')[0].split('-')[2]):int(cn.split(',')[1]) for cn in line.split(':')[1].split(';') if (cn!='') }
					for c1c2 in S3a.keys():
						ThreeStepMa_int[at][t_int][c1c2[0]][c1c2[1]] = S3a[c1c2]

	#----------------------------------------------------------	

	return TwoStep, ThreeStepM, ThreeStepMa, \
			TwoStep_int, ThreeStepM_int, ThreeStepMa_int