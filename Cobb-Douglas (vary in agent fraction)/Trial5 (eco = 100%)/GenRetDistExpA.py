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
from GenSynRetDist import GenerateSyntheticReturnsDistribution
from TPath import TryPath
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def GenerateReturnsDistributionsExpA( experiment, eta, \
			ImplementSettings,	ResourceSettings , plots=True ):

	#----------------------------------------------------------

	n0_S = ImplementSettings['S'][0]
	n0_M = ImplementSettings['M'][0]
	n0_L = ImplementSettings['L'][0]

	Ex_p_S = ResourceSettings['Ex_p_S']
	p0_S = ResourceSettings['p0_S']
	Pp0_S = ResourceSettings['Pp0_S']

	Pp1_S = ( 1. - Pp0_S )
	p1_S = Ex_p_S / Pp1_S
	p_values_S, Pp_values_S, CDF_values_S = \
		GenerateSyntheticReturnsDistribution( p0_S, p1_S, \
											  Pp1_S, Ex_p_S )

	p0_M = p0_S
	p1_M = ( n0_M / n0_S )*p1_S
	Ex_p_M = Ex_p_S + \
		Ex_p_S*( eta - 1 )*( ( n0_M - n0_S )/( n0_L - n0_S ) )
	Pp1_M = ( Ex_p_M - p0_M )/( p1_M - p0_M )
	p_values_M, Pp_values_M, CDF_values_M = \
		GenerateSyntheticReturnsDistribution( p0_M, p1_M, \
											  Pp1_M, Ex_p_M )

	p0_L = p0_S
	p1_L = ( n0_L / n0_S )*p1_S
	Ex_p_L = eta*Ex_p_S
	Pp1_L = ( Ex_p_L - p0_L )/( p1_L - p0_L )
	p_values_L, Pp_values_L, CDF_values_L = \
		GenerateSyntheticReturnsDistribution( p0_L, p1_L, \
											  Pp1_L, Ex_p_L )

	ReturnsDistributions = { 'S':( p_values_S, Pp_values_S, CDF_values_S ),
							 'M':( p_values_M, Pp_values_M, CDF_values_M ),
							 'L':( p_values_L, Pp_values_L, CDF_values_L ) }

	#----------------------------------------------------------

	path = './pic/' + experiment + \
		'/dist/ReturnsDists_eta_' + str(eta).replace('.','o') + '.png'
	if (plots and (not os.path.isfile(path))):

		TryPath( './pic/' )
		TryPath( './pic/' + experiment )
		TryPath( './pic/' + experiment + '/dist')
		
		Colors = { 'S':'green', 'M':'orange' , 'L':'blue' }
		Labels = { 'S':'Solitary/Small-group', \
				   'M':'Medium-group' , \
				   'L':'Large-group' }
		fig, ax = plt.subplots(figsize=(9,6))
		for c in ReturnsDistributions.keys():
			p_values = ReturnsDistributions[c][0]
			Pp_values = ReturnsDistributions[c][1]
			for pi,p in enumerate( p_values ):
				if pi==0:
					ax.plot( [ p , p ], [ 0 , Pp_values[pi] ], \
						'o-', color=Colors[c], label=Labels[c] )
				else:
					ax.plot( [ p , p ], [ 0 , Pp_values[pi] ], \
						'o-', color=Colors[c] )
		ax.set_xlabel( 'Available returns', fontsize=18 )
		ax.set_ylabel( 'Frequency',fontsize=18 )
		ax.legend(fontsize=18)
		fig.savefig( path , bbox_inches='tight' , dpi = 300 )
		plt.close(fig)

	#----------------------------------------------------------

	return ReturnsDistributions