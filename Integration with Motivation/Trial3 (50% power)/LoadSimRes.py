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
from TPath import TryPath
from GenAgenAndImp import GenerateAgentsAndImplements
from GenInitAffAndNet import GenerateInitialAffiliationsAndNetwork
from GenTag import GenerateTag
from PlotCrewSizeTS import PlotCrewSizeTimeSeries
from PosSimPlot import PostSimulationPlots
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def LoadSimulationResults( experiment, d, mE, mT, eta, caps, \
		trial, ImplementSettings, ResourceSettings, M, tf , bawel=False , AgentTypes = [] ):

	#----------------------------------------------------------

	tag = GenerateTag( experiment , d , mE, mT , eta , caps )
	path = './sim/' + experiment + '/' + tag

	filepath = path + '/' + tag + '_' \
		+ str(eta).replace('.','o') + '_' + str(trial) + '_AffilUpdates.txt'
	TryPath( './post/' + experiment + '/txt/' + tag )
	outputpath = './post/' + experiment + '/txt/' + tag + '/' \
			+ tag + '_' + str(eta).replace('.','o') + '_' + str(trial)

	ATpath = path + '/' + tag + '_' \
		+ str(eta).replace('.','o') + '_' + str(trial) + '_AgentTypes.txt'

	if os.path.isfile(ATpath):
		AgentTypes = { line.split(':')[0]:[ a for a in line.split(':')[1].split(',') ] for line in open(ATpath).read().splitlines() }
	else:
		AgentTypes = []

	A,B,C,Gamma,B_c = GenerateAgentsAndImplements( M, ImplementSettings )
	AgentAffiliations0, ImplementCrews, W0, Wc = \
		GenerateInitialAffiliationsAndNetwork( A, B, C, \
			Gamma, B_c, ImplementSettings )
	beta_t_a = {'pop':{}}
	Transitions = {'pop':{}}
	for at in list(AgentTypes.keys()):
		beta_t_a[at] = {}
		Transitions[at] = {}

	if bawel:
		print('\tLoading simulation results (agent-implement affiliation time series) from ...')
		print('\t\t'+filepath)

	for line in open(filepath).read().splitlines():

		a = line.split(':')[0]

		if AgentTypes:
			for at in list(AgentTypes.keys()):
				if a in AgentTypes[at]:
					agenttype = at

		beta_t_a['pop'][a] = []		
		if AgentTypes: 
			beta_t_a[agenttype][a] = []		

		Updates = [ ( int(pair.split(',')[0]) , pair.split(',')[1] ) \
			for pair in line.split(':')[1].split(';') if ((',' in (pair)) and (pair!='')) ]
		for ui,tb in enumerate(Updates[:-1]):
			beta_t_a['pop'][a].extend([ tb[1] for x in range(tb[0],Updates[ui+1][0]) ]) 
			if AgentTypes:
				beta_t_a[agenttype][a].extend([ tb[1] for x in range(tb[0],Updates[ui+1][0]) ])
		beta_t_a['pop'][a].extend([ Updates[-1][1] for x in range(Updates[-1][0],tf) ])
		if AgentTypes:
			beta_t_a[agenttype][a].extend([ Updates[-1][1] for x in range(Updates[-1][0],tf) ])
		Transitions['pop'][a] = \
			sorted( [ ( Updates[ui][0], Gamma[Updates[ui-1][1]], Gamma[Updates[ui][1]] ) \
				for ui in range(1,len(Updates)) ] , \
					key=lambda x:x[0] )
		if AgentTypes:
			Transitions[agenttype][a] = \
				sorted( [ ( Updates[ui][0], Gamma[Updates[ui-1][1]], Gamma[Updates[ui][1]] ) \
					for ui in range(1,len(Updates)) ] , \
						key=lambda x:x[0] )

	cspath = outputpath + '_CrewSizes.txt'
	if not os.path.isfile( cspath ):
		if bawel:
			print('\tComputing time series: Crew sizes by implement')
		ImplementCrewSizes_t = { b:[ np.sum([ int(beta_t_a['pop'][a][t]==b) for a in A ]) \
				for t in range(tf) ] for b in B }
		cstxt = open( cspath , 'w' )
		for b in B:
			cstxt.write( b + ':' )
			for ics in ImplementCrewSizes_t[b][:-1]:
				cstxt.write( str(ics) + ',' )
			cstxt.write( str(ImplementCrewSizes_t[b][-1]) + '\n' )
		cstxt.close()
	else:
		if bawel:
			print('\tLoading previously-computed time series: Crew sizes by implement')
		ImplementCrewSizes_t = \
			{ line.split(':')[0]:[ int(ics) for ics in line.split(':')[1].split(',')] \
					for line in open(cspath).read().splitlines() }

	ntcpath = outputpath + '_NumAgentsByType.txt'
	if not os.path.isfile( ntcpath ):
		N_t_c = {}
		if bawel:
			print('\tComputing time series: Numbers of affiliated agents by implement type')
		N_t_c['pop'] = { c:[ np.sum([ ImplementCrewSizes_t[b][t] for b in B_c[c] ]) \
					for t in range(tf) ] for c in C }
		nctxt = open( ntcpath , 'w' )
		for c in C:
			nctxt.write( c + ':' )
			for ntc in N_t_c['pop'][c][:-1]:
				nctxt.write( str(ntc) + ',' )
			nctxt.write( str(N_t_c['pop'][c][-1]) + '\n' )
		nctxt.close()
	else:
		if bawel:
			print('\tLoading previously-computed time series: Numbers of affiliated agents by implement type')
		N_t_c = {}
		N_t_c['pop'] = \
			{ line.split(':')[0]:[ int(ntc) for ntc in line.split(':')[1].split(',')] \
					for line in open(ntcpath).read().splitlines()}

	if AgentTypes:
		ntcpathD = {at:(outputpath + '_NumAgentsByType_' + at + '.txt') for at in AgentTypes.keys()}
		for at in AgentTypes.keys():
			if not os.path.isfile( ntcpathD[at] ):
				N_t_c[at] = { c:[ np.sum( [ (Gamma[beta_t_a[at][a][t]]==c) for a in beta_t_a[at].keys() ] ) for t in range(tf)] for c in C }
				nctxtd = open( ntcpathD[at] , 'w' )
				for c in C:
					nctxtd.write( c + ':' )
					for ntc in N_t_c[at][c][:-1]:
						nctxtd.write( str(int(ntc)) + ',' )
					nctxtd.write( str(int(N_t_c[at][c][-1])) + '\n' )
				nctxtd.close()
			else:
				if bawel:
					print('\tLoading previously-computed time series: Numbers of affiliated agents by implement type')
				N_t_c[at] = \
					{ line.split(':')[0]:[ int(ntc) for ntc in line.split(':')[1].split(',')] \
							for line in open(ntcpathD[at]).read().splitlines()}

	bapath = outputpath + '_ActiveImpsByType.txt'
	if not os.path.isfile( bapath ):
		if bawel:
			print('\tComputing time series: Numbers of active implements by type')
		B_active_t_c = { c:[ np.sum([ int(ImplementCrewSizes_t[b][t]>=ImplementSettings[Gamma[b]][0]) \
					for b in B_c[c]]) for t in range(tf) ] for c in C }
		batxt = open( bapath , 'w' )
		for c in C:
			batxt.write( c + ':' )
			for ba in B_active_t_c[c][:-1]:
				batxt.write( str(ba) + ',' )
			batxt.write( str(B_active_t_c[c][-1]) + '\n' )
		batxt.close()
	else:
		if bawel:
			print('\tLoading previously-computed time series: Numbers of active implements by type')
		B_active_t_c = \
			{ line.split(':')[0]:[ int(ntc) for ntc in line.split(':')[1].split(',')] \
					for line in open(bapath).read().splitlines() }

	PlotCrewSizeTimeSeries( ImplementCrewSizes_t, B, Gamma, \
								experiment, tag, eta, trial )

	if AgentTypes:
		for at in AgentTypes.keys():
			PostSimulationPlots( experiment , tag+'_'+at , eta , trial , \
				N_t_c[at] , B_active_t_c , [])	

	#---------------------------------------------------------
	#----------------------------------------------------------

	return beta_t_a, N_t_c, B_active_t_c, \
		ImplementCrewSizes_t, Transitions, A, B, C, tag, filepath, AgentTypes
