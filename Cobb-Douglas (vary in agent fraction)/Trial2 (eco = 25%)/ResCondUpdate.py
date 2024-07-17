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

def ResourceConditionsUpdate( C, B_c, ResourceSettings , \
				ReturnsDistributions , ImplementCrews , Chi , k ):

	#----------------------------------------------------------

	for c in C:

		parameters = ResourceSettings[c]
		alpha_r, alpha_p, Kappa = parameters[0], parameters[1], parameters[2]

		Pp1 = ReturnsDistributions[c][1][-1]
		Predation = \
			np.sum([ Chi[c][ len(ImplementCrews[b]) ] for b in B_c[c] ] ) 

		dPp1dt = ( alpha_r*( 1 - Pp1/Kappa ) - alpha_p*Predation )*Pp1

		Pp1 = np.min([ np.max([ ( Pp1 + k*dPp1dt ) , 0. ]) , 1. ])

		ReturnsDistributions[c] = \
			( ReturnsDistributions[c][0] , \
				[ (1.-Pp1), Pp1 ] , [ (1.-Pp1), 1.  ] )

	#----------------------------------------------------------

	return ReturnsDistributions