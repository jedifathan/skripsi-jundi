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

def UpdateCooperativeComponent( Wc , AgentAffiliations , mT ):

	#----------------------------------------------------------

	if ( mT!='infty' ):

		for edge in Wc.edges():

			Wc[edge[0]][edge[1]]['weight'] = \
				(1/mT)*float(int( AgentAffiliations[edge[0]]==AgentAffiliations[edge[1]] )) + \
					(1-1/mT)*Wc[edge[0]][edge[1]]['weight']

	#----------------------------------------------------------

	return Wc	