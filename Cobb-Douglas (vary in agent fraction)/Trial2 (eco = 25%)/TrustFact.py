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

def TrustFactor( a , ImplementCrew_b , W0 , Wc , d ):

	#----------------------------------------------------------

	SocialTies = [ ((1-d)*W0[a][a1]['weight'] \
		+ d*Wc[a][a1]['weight']) for a1 in ImplementCrew_b ]
	TrustFactor = np.mean(SocialTies)

	#----------------------------------------------------------
	# print(f"Trust Factor : {TrustFactor}")
	return TrustFactor