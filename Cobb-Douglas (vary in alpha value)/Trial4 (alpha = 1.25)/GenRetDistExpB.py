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

def GenerateReturnsDistributionsExpB( eta, p0_M, p1_M, Ex_p_M , \
			ImplementSettings,	ResourceSettings , plots=True ):

	#----------------------------------------------------------

	# 'Sapa' returns histogram data from Alvard and Nolin (2002)
	# (NOTE: Used "Plot Digitizer Online App" at https://plotdigitizer.com/app)
	#	Maybe re-do more carefully before submission.

	p_values_S = [0., .25, .50, .75, 1., 1.25, \
					1.50, 1.75, 2. , 2.25 , 2.5, 2.75 ]
	ReturnsHist_S = [ 5.77586563532168,53.36206841553863,17.3275870403693,\
					9.568970149535476,4.310344544092083,3.620693363275651,\
					2.1551722720460416,1.0344866368204033,0.17241772800197938,\
					0.7758633333493485,1.120692212289479,1.8103499701697396 ]
	sumReturns_S = np.sum(ReturnsHist_S)
	Pp_values_S = [ (R/sumReturns_S) for R in ReturnsHist_S ]
	CDF_values_S = np.cumsum(Pp_values_S)
	Ex_p_S = np.mean([ Pp_values_S[pi]*p for pi,p in enumerate(p_values_S) ])

	# 'Tena' returns histogram data from Alvard and Nolin (2002)

	p_values_L = [0., .25, .50, .75, 1., 1.25, 1.50, 1.75, 2.]
	ReturnsHist_L = [ 84.3243244520382,0.4053992286979604,2.16216014970109,\
			1.3513513823122867,1.891883687242926,1.4864844585449464,\
			1.0810749198541036,0.8108087673888031,0.6756756911561433,\
			4.864862914325682 ]
	sumReturns_L = np.sum(ReturnsHist_L)

	Target_Ex_p_L = eta*Ex_p_S
	p_max_L = ( sumReturns_L*Target_Ex_p_L \
		- np.sum([R*ReturnsHist_L[Ri] \
			for Ri,R in enumerate(p_values_L)]) )/ReturnsHist_L[-1]
	p_values_L.append(p_max_L)

	Pp_values_L = [ (R/sumReturns_L) for R in ReturnsHist_L ]
	CDF_values_L = np.cumsum(Pp_values_L)

	#------------------------------------------------------------

	Pp1_M = ( Ex_p_M - p0_M )/( p1_M - p0_M )
	p_values_M, Pp_values_M, CDF_values_M = \
		GenerateSyntheticReturnsDistribution( p0_M, p1_M, \
											  Pp1_M, Ex_p_M )

	ReturnsDistributions = { 'S':( p_values_S, Pp_values_S, CDF_values_S ),
							 'M':( p_values_M, Pp_values_M, CDF_values_M ),
							 'L':( p_values_L, Pp_values_L, CDF_values_L ) }

	#----------------------------------------------------------

	experiment = 'B'
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
			if ( c=='M' ):
				for pi,p in enumerate( p_values ):
					if pi==0:
						ax.plot( [ p , p ], [ 0 , Pp_values[pi] ], \
							'o-', color=Colors[c], label=Labels[c] )
					else:
						ax.plot( [ p , p ], [ 0 , Pp_values[pi] ], \
							'o-', color=Colors[c] )
			else:
				ax.plot( p_values , Pp_values , \
					'o-', color=Colors[c], label=Labels[c] )
		ax.set_xlabel( 'Available returns', fontsize=24 )
		ax.set_ylabel( 'Frequency',fontsize=24 )
		ax.legend(fontsize=18)
		fig.savefig( path , bbox_inches='tight' , dpi = 300 )
		plt.close(fig)

	#----------------------------------------------------------

	return ReturnsDistributions
