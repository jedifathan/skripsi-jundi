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

def GenerateSyntheticReturnsDistribution( p0, p1, Pp1, Ex_p ):

	#----------------------------------------------------------

	Pp0 = 1. - Pp1

	p_values = [ p0 , p1 ]
	Pp_values = [ Pp0 , Pp1 ]
	CDF_values = [ Pp0 , 1. ]

	#----------------------------------------------------------

	return p_values, Pp_values, CDF_values