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

# calculates an ecological factor based on various parameters like group size, 
# return values, settings, and probability distributions.
def EcologicalFactor( b , GroupReturn_series_b , mE , \
		ImplementCrewSize_t_b , ImplementSettings , Gamma , \
			ReturnsDistributions ):

	#----------------------------------------------------------

	ImplementCrewSize_t_b = \
			list(np.zeros( np.max([ ( mE - len(ImplementCrewSize_t_b) ) , 0 ]) , int ) ) \
					+ ImplementCrewSize_t_b 

	GroupReturn_series_b = \
			list(np.zeros( np.max([ ( mE - len(GroupReturn_series_b) ) , 0 ]) , int ) ) \
					+ GroupReturn_series_b 

	ActiveIterations = \
			[ int( ImplementCrewSize_t_b[i]>=ImplementSettings[Gamma[b]][0] ) \
					for i in range(-mE,0) ]

	MannedIterations = \
			[ int( ImplementCrewSize_t_b[i]>0 ) \
					for i in range(-mE,0) ]

	p_values = ReturnsDistributions[Gamma[b]][0]
	Pp_values = ReturnsDistributions[Gamma[b]][1]
	Ex_p = np.sum([ Pp_values[pi]*p for pi,p in enumerate(p_values) ])

	# This should maybe have (n+1) instead of (n) in the denominator.
	# Will mostly affect the behavior of 'S' groups (preventing formation of pairs)
	ExpectedIndividualReturns = \
			[ GroupReturn_series_b[i]*( ImplementSettings[Gamma[b]][0]/ImplementCrewSize_t_b[i] ) \
					if ( MannedIterations[i]==1 ) else ( Ex_p ) for i in range(-mE,0) ]

	EcologicalFactor = np.mean(ExpectedIndividualReturns)
	# print(f"Ecological Factor : {EcologicalFactor}")
	#----------------------------------------------------------

	return EcologicalFactor