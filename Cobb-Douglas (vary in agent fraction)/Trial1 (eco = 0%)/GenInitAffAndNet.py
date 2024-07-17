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

def GenerateInitialAffiliationsAndNetwork(A,B,C,Gamma,B_c,ImplementSettings):

	#----------------------------------------------------------

	AgentAffiliations = {}
	ImplementCrews = { b:[] for b in B }

	ActiveImplements = { c:B_c[c][:ImplementSettings[c][3]] for c in C }

	i1 = 0
	i2 = 0
	for c in C:
		crewsize0 = ( ImplementSettings[c][0] + 2 )
		for b in ActiveImplements[c]:
			i2 += crewsize0
			if (i2<=len(A)):
				crew0 = A[i1:i2]
			else:
				crew0 = A[i1:]		# remove from active?
			ImplementCrews[b] = crew0
			for a in ImplementCrews[b]:
				AgentAffiliations[a] = b
			i1 = i2 

	#	Exogenous component of social network (here, complete graph) :

	W0 = nx.Graph()
	W0.add_nodes_from(A)
	W0.add_weighted_edges_from( [(pair[0],pair[1],1.) \
									for pair in combinations(A,2) ] )
	W0.add_weighted_edges_from( [(a,a,1.) for a in A ] )

	#	Cooperative component of social network :

	Wc = nx.Graph()
	Wc.add_nodes_from(A)
	Wc.add_weighted_edges_from( [( pair[0], pair[1], \
		float(int(AgentAffiliations[pair[0]]==AgentAffiliations[pair[1]]))) \
			for pair in combinations(A,2) ] )
	Wc.add_weighted_edges_from( [(a,a,1.) for a in A ] )

	#----------------------------------------------------------

	return AgentAffiliations, ImplementCrews, W0, Wc