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

def SampleMeanDistributions( ReturnsDistributions , experiment , mE , \
				eta , NumberOfSamples=100 , plots=False ):

	meanp_values = {}
	Pmeanp_values = {}
	CDF_Pmeanp_values = {}

	C = ReturnsDistributions.keys()

	for ci,c in enumerate(C):

		p_values = ReturnsDistributions[c][0]
		Pp_values = ReturnsDistributions[c][1]
		CDF_values = ReturnsDistributions[c][2]

		samplemeans = []
		for n in range(NumberOfSamples):
			sample = [ float( p ) for p \
				in random.choices( p_values , \
					cum_weights=CDF_values, k = mE ) ]
			samplemeans.append( np.mean(sample) )

		bins0 = sorted([ ( (n/mE)*p_values[0] \
			+ (1 - n/mE)*p_values[-1] ) for n in range(mE+1) ])

		binspacing = (bins0[1]-bins0[0])
		bins = [ (b-binspacing/2) for b in bins0 ]
		bins.append(np.max(bins0)+binspacing/2)

		F_meanp,bins1 = np.histogram(samplemeans, \
			bins=bins,density=True)	
		bincenters = (bins1[:-1] + bins1[1:])/2
		sumF_meanp = np.sum(F_meanp)

		meanp_values[c] = bincenters
		Pmeanp_values[c] = \
			[ (F/sumF_meanp) for F in F_meanp ]
		CDF_Pmeanp_values[c] = \
			np.cumsum( Pmeanp_values[c] )

	#----------------------------------------------------------					

	path = './pic/' + experiment + \
		'/dist/ReturnsSampleMeanDists_size_' \
		+ str(mE) + '_eta_' + str(eta).replace('.','o') + '.png'
	if ( plots and (not os.path.isfile(path)) ):

		TryPath( './pic/' )
		TryPath( './pic/' + experiment )
		TryPath( './pic/' + experiment + '/dist')
			
		Colors = { 'S':'green', 'M':'orange' , 'L':'blue' }
		Labels = { 'S':'Solitary/Small-group', \
				   'M':'Medium-group' , \
				   'L':'Large-group' }
		fig, ax = plt.subplots(figsize=(9,6))
		for c in C:
			for pi,p in enumerate( p_values ):
				if pi==0:
					ax.plot( meanp_values[c], Pmeanp_values[c], \
						'o-', color=Colors[c], label=Labels[c] )
				else:
					ax.plot( meanp_values[c], Pmeanp_values[c], \
						'o-', color=Colors[c] )
		ax.set_xlabel( 'Sample mean available returns' \
				+ ' (sample size '+str(mE)+')', fontsize=18 )
		ax.set_ylabel( 'Frequency',fontsize=18 )
		ax.legend(fontsize=18)
		fig.savefig( path , bbox_inches='tight' , dpi = 300 )
		plt.close(fig)

	#----------------------------------------------------------

	return meanp_values, Pmeanp_values, CDF_Pmeanp_values