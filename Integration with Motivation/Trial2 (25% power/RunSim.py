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
from GenTag import GenerateTag
from GenRetDistExpA import GenerateReturnsDistributionsExpA
from GenRetDistExpB import GenerateReturnsDistributionsExpB
from SampMeanDist import SampleMeanDistributions
from GenAgenAndImp import GenerateAgentsAndImplements
from GenInitAffAndNet import GenerateInitialAffiliationsAndNetwork
from ResAppStep import ResourceAppropriationStep
from AgentImpAffUpdateStep import AgentImplementAffiliationUpdateStep
from PosSimPlot import PostSimulationPlots
from SaveSimRes import SaveSimulationResults
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def RunSimulation( simtag , experiment , M , Pu , Pn , d , mE, mT , eta , caps , \
				trial , ImplementSettings , ResourceSettings , tf , Chi, K , Recruitable, \
				OtherInputs=[] , DynamicResources=False , k=0. , bawel=False , FracTypes = [] ):

	#----------------------------------------------------------

	tag = GenerateTag( experiment , d , mE, mT , eta , caps )

	if ( experiment in ['A','C'] ):
		ReturnsDistributions = \
			GenerateReturnsDistributionsExpA( experiment, eta, \
				ImplementSettings,	ResourceSettings , True )
	elif ( experiment=='B' ):
		p0_M = OtherInputs['p0_M'] 
		p1_M = OtherInputs['p1_M']
		Ex_p_M = OtherInputs['Ex_p_M']
		ReturnsDistributions = \
			GenerateReturnsDistributionsExpB( eta, p0_M, p1_M, Ex_p_M , \
				ImplementSettings,	ResourceSettings , True )
	SampleMeanDistributions( ReturnsDistributions , experiment, mE , eta, 5000 , True )

	A,B,C,Gamma,B_c = GenerateAgentsAndImplements( M, ImplementSettings )
	AgentAffiliations, ImplementCrews, W0, Wc = \
		GenerateInitialAffiliationsAndNetwork( A, B, C, \
			Gamma, B_c, ImplementSettings )
	ImplementCrewSizes_t = { b:[len(ImplementCrews[b])] for b in B }

	# Note: If agents aren't shuffled prior to Motivation Profile assignments,
	#	then the initial condition will contain several L groups with all Type-1, all Type-2, etc...

	AgentTypes = []
	if FracTypes:
		AgentTypes = {}
		A_2 = [ a for a in A ]    # A_2 = copy.deepcopy(A)
		for ift,ft in enumerate(FracTypes.keys()):
			Aft = random.sample( A_2, round(M*FracTypes[ft]) )
			A_2 = list(set(A_2) - set(Aft))
			AgentTypes[ft] = list(Aft)

	# Time series:
	beta_t_a = { a:[AgentAffiliations[a]] for a in A }
	GroupReturn_series = { b:[] for b in B }
	N_t_c = \
		{ c:[np.sum([len(ImplementCrews[b]) for b in B_c[c] ])] for c in C }
	B_active_t_c = \
		{ c:[np.sum([ int(len(ImplementCrews[b])>=ImplementSettings[Gamma[b]][0]) \
			for b in B_c[c] ])] for c in C }
	if DynamicResources:
		Pp1_t_series = \
			{ c:[ReturnsDistributions[c][1][-1]] for c in C }
		for c in C:
			ResourceSettings[c] = ( ResourceSettings[c][0], ResourceSettings[c][1], ReturnsDistributions[c][1][-1] )
	else:
		Pp1_t_series = []

	#----------------------------------------------------------

	for t in range(tf):

		if bawel:
			print('t='+str(t)+':')
			for c in C:
				print('\t'+c+': Active implements='\
					+str(B_active_t_c[c][-1])+\
					', Affiliated agents='+str(N_t_c[c][-1]))

		# RESOURCE APPROPRIATION STEP :

		GroupReturn, Wc, ReturnsDistributions = \
			ResourceAppropriationStep( ReturnsDistributions , \
				B, C, Gamma , B_c, Chi , ImplementCrews , \
					ImplementSettings , ResourceSettings, \
					AgentAffiliations , Wc , mT , \
						DynamicResources , k )

		for b in B:
			GroupReturn_series[b].append( GroupReturn[b] )
		if DynamicResources:
			if bawel:
				print('\tAppropriation step:')
			for c in C:
				Pp1_t_series[c].append( ReturnsDistributions[c][1][-1] )
				if bawel:
					print('\t\t'+c+': Delta P(p1) = '+\
						str(Pp1_t_series[c][-1]-Pp1_t_series[c][-2]) + \
							' P(p1) = ' + str(Pp1_t_series[c][-1]) )

		# AGENT-IMPLEMENT AFFILIATION UPDATE STEP :

		AgentAffiliations, ImplementCrews, Joined, Left, Activated = \
			AgentImplementAffiliationUpdateStep( A , Pu , Pn , B , B_c , d , mE , caps , \
				AgentAffiliations , ImplementCrews , ImplementCrewSizes_t , Gamma , \
					ImplementSettings , GroupReturn_series , W0 , Wc , K , \
						Recruitable , ReturnsDistributions , AgentTypes )

		for a in A:
			beta_t_a[a].append(AgentAffiliations[a])
		Deactivated = { c:0 for c in C }
		for b in B:
			ImplementCrewSizes_t[b].append( len(ImplementCrews[b]) )
			n0 = ImplementSettings[Gamma[b]][0]
			if ((ImplementCrewSizes_t[b][-2]>=n0) and (ImplementCrewSizes_t[b][-1]<n0)):
				Deactivated[Gamma[b]] += 1

		for c in C:
			N_t_c[c].append( \
				np.sum([len(ImplementCrews[b]) for b in B_c[c] ])  )
			B_active_t_c[c].append( \
				np.sum([ int(len(ImplementCrews[b])>=ImplementSettings[Gamma[b]][0]) \
					for b in B_c[c] ]))

		if bawel:
			print('\tUpdate step:')
			for c in C:
				print('\t\t'+c+': Activated implements='\
					+str(Activated[c])+', Deactivated implements='\
					+str(Deactivated[c])+'; Agents joined='\
					+str(Joined[c])+', Agents leaving='+str(Left[c])) 
			print('\n')

		#------------------------------------------------------
	#----------------------------------------------------------

	# Consider plotting Expected returns instead of catch probability
	#	to facilitate comparison between implement types
	# ExP_t_series = []
	# if DynamicResources:
	# 	ExP_t_series = \
	# 		{ c:[ p*ReturnsDistributions[c][0][-1] for p in Pp1_t_series[c] ] for c in C }

	PostSimulationPlots( experiment , tag , eta , trial , \
		N_t_c , B_active_t_c , Pp1_t_series )	
	SaveSimulationResults( simtag , beta_t_a )

	if AgentTypes:
		[]	# save the AgentTypes dicts

		btxt = open( simtag + '_AgentTypes.txt' , 'w' )
		for at in AgentTypes.keys():
			btxt.write( at + ':')
			if AgentTypes[at]:
				for a in AgentTypes[at][:-1]:
					btxt.write( a + ',')
				btxt.write(AgentTypes[at][-1])
			btxt.write('\n')
		btxt.close()

	#----------------------------------------------------------

	return []