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

# generate a nested dictionary structure representing a parameter space 
# for an ensemble of simulations
def CreateEnsembleDict( d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials ):

	#----------------------------------------------------------	

	Dict = { d:{ mE:{ mT:{ cap_M:{ eta:{ trial:{} for trial in trials } \
				for eta in eta_values } for cap_M in cap_M_values } \
						for mT in mT_values } for mE in mE_values } \
								for d in d_values }


	#----------------------------------------------------------	

	return Dict