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

# generates identifiers for agents and implements, 
# sorts and groups implements based on settings, and builds connections between them.
def GenerateAgentsAndImplements(M,ImplementSettings):

	A = [ str(i+1).zfill(3) for i in range(M) ]				# List of agents
	C = sorted( list(ImplementSettings.keys()) , \
		key=lambda x:ImplementSettings[x][0] , reverse=True )
	B =  [ (str(q+1).zfill(3)) \
			for q in range(np.sum([ImplementSettings[c][2] for c in C])) ]
	GammaIndexList = \
		sum([ list(ci*np.ones(ImplementSettings[c][2],int)) \
							for ci,c in enumerate(C) ],[])
	Gamma = { b:C[GammaIndexList[bi]] for bi,b in enumerate(B) }
	B_c = { c:[ b for b in B if ( Gamma[b]==c ) ]  for c in C }

	#----------------------------------------------------------

	return A, B, C, Gamma, B_c 
