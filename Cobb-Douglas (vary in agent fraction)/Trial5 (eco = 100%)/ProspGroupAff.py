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
from TrustFact import TrustFactor
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------
def ProspectiveGroupAffinity( a , b , ImplementSettings , Gamma , \
			ReturnsDistributions , ProspectiveCrew , W0 , Wc , d ):

	#----------------------------------------------------------

	p_values = ReturnsDistributions[Gamma[b]][0]
	Pp_values = ReturnsDistributions[Gamma[b]][1]
	Ex_p = np.sum([ Pp_values[pi]*p for pi,p in enumerate(p_values) ])
	EcologicalFactor_a_b = Ex_p

	TrustFactor_a_b = \
		TrustFactor( a, list(set(ProspectiveCrew+[a])), W0 , Wc , d )

	G = EcologicalFactor_a_b*TrustFactor_a_b

	#----------------------------------------------------------

	return G, EcologicalFactor_a_b, TrustFactor_a_b