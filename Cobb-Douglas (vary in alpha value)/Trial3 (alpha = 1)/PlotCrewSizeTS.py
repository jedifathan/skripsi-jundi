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
from TPath import TryPath
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def PlotCrewSizeTimeSeries( ImplementCrewSizes_t, B, Gamma, \
								experiment, tag, eta, trial ):

	#---------------------------------------------------------

	TryPath( './post/' )
	TryPath( './post/' + experiment )
	TryPath( './post/' + experiment + '/pic/' )
	TryPath( './post/' + experiment + '/pic/' + tag )

	cspic = './post/' + experiment + \
			'/pic/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + str(trial) + \
			'_CrewSizes.png'

	if not os.path.isfile( cspic ):
		Colors = { 'S':colors.to_rgba('green'), \
				   'M':colors.to_rgba('orange'), \
				   'L':colors.to_rgba('blue') }
		fig, ax = plt.subplots(figsize=(9,6))
		for b in B:
			c = Gamma[b]
			clr = ( np.min([1.,np.max([0.,Colors[c][0] + .4*(random.random()-.5)])]) , \
				    np.min([1.,np.max([0.,Colors[c][1] + .4*(random.random()-.5)])]) , \
				    np.min([1.,np.max([0.,Colors[c][2] + .4*(random.random()-.5)])]) , )
			plt.plot( ImplementCrewSizes_t[b] , \
				color=clr )
		ax.set_xlabel( 'Iteration', fontsize=18 )
		ax.set_ylabel( 'Crew size $n$' , \
			fontsize=18 )
		fig.savefig( './post/' + experiment + \
			'/pic/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + str(trial) + \
			'_CrewSizes.png' , bbox_inches='tight' , dpi = 300 )
		#plt.show()
		plt.close(fig)