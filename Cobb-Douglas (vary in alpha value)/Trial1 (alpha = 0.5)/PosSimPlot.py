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

def PostSimulationPlots( experiment , tag , eta , trial , \
						N_t_c , B_active_t_c , Pp1_t_series ):

	#----------------------------------------------------------

	picpath = './pic/' + experiment + '/results/'
	pictag = picpath + tag + '/' + tag + '_' \
			+ str(eta).replace('.','o') + '_' + str(trial)
	TryPath( picpath )
	TryPath( picpath + tag )
	Colors = { 'S':'green', 'M':'orange' , 'L':'blue' }
	Labels = { 'S':'Solitary/Small-group', \
			   'M':'Medium-group' , \
			   'L':'Large-group' }
	fig, ax = plt.subplots(figsize=(9,6))
	C = list(N_t_c.keys())
	for c in C:
		ax.plot( N_t_c[c] , \
			color=Colors[c], label=Labels[c] )
	ax.set_xlabel( 'Iteration', fontsize=18 )
	ax.set_ylabel( 'Number of affiliated agents ' \
					+ '$N(c)$' , fontsize=18 )
	ax.legend(fontsize=18)
	fig.savefig( pictag + '_AffilAgents.png' , \
		bbox_inches='tight' , dpi = 300 )
	#plt.show()
	plt.close(fig)

	if not (('aff' in tag) or ('pow' in tag)):
		fig, ax = plt.subplots(figsize=(9,6))
		for c in C:
			ax.plot( B_active_t_c[c] , \
				color=Colors[c], label=Labels[c] )
		ax.set_xlabel( 'Iteration', fontsize=18 )
		ax.set_ylabel( 'Number of active implements ' \
						+ '$B_{\\mathrm{active}}(c)$',fontsize=18 )
		ax.legend(fontsize=18)
		fig.savefig( pictag + '_ActiveImp.png' , \
			bbox_inches='tight' , dpi = 300 )
		#plt.show()
		plt.close(fig)

	if Pp1_t_series:

		fig, ax = plt.subplots(figsize=(9,6))
		for c in C:
			ax.plot( Pp1_t_series[c] , \
				color=Colors[c], label=Labels[c] )
		ax.set_xlabel( 'Iteration', fontsize=18 )
		ax.set_ylabel( 'Probability of successful appropriation $P\\left(p_{1}\\right)$' \
						+ '$B_{\\mathrm{active}}(c)$',fontsize=18 )
		ax.legend(fontsize=18)
		fig.savefig( pictag + '_ResourceDynamics.png' , \
			bbox_inches='tight' , dpi = 300 )
		#plt.show()
		plt.close(fig)
