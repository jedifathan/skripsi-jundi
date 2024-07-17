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

def SaveSimulationResults( simtag , beta_t_a ):

	#----------------------------------------------------------

	btxt = open( simtag + '_AffilUpdates.txt' , 'w' )
	for a in beta_t_a.keys():
		btxt.write( a + ':')
		Updates = [ ( 0 , beta_t_a[a][0] ) ]
		UpdatesT = [ (ti+1,b) for ti,b in enumerate(beta_t_a[a][1:]) \
			if ( beta_t_a[a][ti+1]!=beta_t_a[a][ti] ) ]
		if UpdatesT:
			Updates.extend( UpdatesT )
			for tb in Updates[:-1]:
				btxt.write( str(tb[0]) + ',' + tb[1] + ';')
			btxt.write( str(Updates[-1][0]) + ',' \
				+ Updates[-1][1] + '\n' )
		else:
			btxt.write( '0,' + str(beta_t_a[a][0]) + '\n' )
	btxt.close()