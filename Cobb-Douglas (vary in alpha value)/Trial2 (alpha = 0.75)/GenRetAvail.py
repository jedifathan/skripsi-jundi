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
def GenerateReturnsAvailable( ReturnsDistributions , B , Gamma  ):

	#----------------------------------------------------------

	p_b_t = { b:(random.choices( ReturnsDistributions[Gamma[b]][0] , \
		cum_weights=ReturnsDistributions[Gamma[b]][2]  )[0]) for b in B }

	#----------------------------------------------------------

	return p_b_t