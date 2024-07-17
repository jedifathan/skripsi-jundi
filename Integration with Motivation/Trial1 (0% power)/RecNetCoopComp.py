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
from UpdateCoopComp import UpdateCooperativeComponent
from TPath import TryPath
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def RecoverNetworkCooperativeComponent( beta_t_a , mT , A , \
							B , experiment, tag, eta, trial, bawel=False ):

	#----------------------------------------------------------

	# Idea: track distributions of link weights over time. or maybe diameter (or in this case average weighted path length)

	dfile = './post/' + experiment + \
			'/txt/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + str(trial) + \
			'_Density.txt' 
	qfile = './post/' + experiment + \
			'/txt/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + str(trial) + \
			'_Modularity.txt' 
	lfile = './post/' + experiment + \
			'/txt/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + str(trial) + \
			'_Modularity.txt' 


	if not os.path.isfile(dfile) and not os.path.isfile(qfile):

		print('\tComputing time series: Social network density and modularity (cooperative component)')

		tf = len(beta_t_a[A[0]])

		crews0 = []
		for b in B:
			crew0 = [ a for a in A if ( beta_t_a[a][0]==b ) ]
			if crew0:
				crews0.append( set(crew0) )

		Wc = nx.Graph()
		Wc.add_nodes_from(A)
		Wc.add_weighted_edges_from( [( pair[0], pair[1], \
			float(int(beta_t_a[pair[0]][0]==beta_t_a[pair[1]][0]))) \
				for pair in combinations(A,2) ] )
		#Wc.add_weighted_edges_from( [(a,a,1.) for a in A ] )		# We might want to remove these for the purposes of computing threshold (so it approaches 0), though note that they ARE included when agents compute trust factor

		# Wc_inv = nx.Graph()
		# Wc_inv.add_nodes_from(A)
		# Wc_inv.add_weighted_edges_from( [( pair[0], pair[1], \
		# 	1/(Wc[pair[0]][pair[1]]['edge'])) for edge in Wc.edges() ] )
		# #Wc.add_weighted_edges_from( [(a,a,1.) for a in A ] )		# We might want to remove these for the purposes of computing threshold (so it approaches 0), though note that they ARE included when agents compute trust factor


		D = np.sum([ Wc[edge[0]][edge[1]]['weight'] \
			for edge in Wc.edges() ])/(len(A)*(len(A)-1))
		Q = nx.community.modularity( Wc, crews0, weight='weight' )

		if (mT!='infty'):

			WcTimeSeries = \
				{ edge:[Wc[edge[0]][edge[1]]['weight']] \
					for edge in Wc.edges() }

			DensityTimeSeries = [D]
			ModularityTimeSeries = [Q]

			for t in range( 1 , tf ):

				beta_a = { a:beta_t_a[a][t] for a in A }

				Wc = UpdateCooperativeComponent( Wc , beta_a , mT )

				for edge in Wc.edges():
					WcTimeSeries[edge].append(Wc[edge[0]][edge[1]]['weight'])

				D = np.sum([ Wc[edge[0]][edge[1]]['weight'] \
					for edge in Wc.edges() ])/(len(A)*(len(A)-1))
				Q = nx.community.modularity( Wc, crews0, weight='weight' )

				DensityTimeSeries.append(D)
				ModularityTimeSeries.append(Q)

		else:

			# WcTimeSeries = \
			# 	{ edge:[ Wc[edge[0]][edge[1]]['weight'] for t in range(tf) ] \
			# 		for edge in Wc.edges() }

			WcTimeSeries = \
				{ edge:[ Wc[edge[0]][edge[1]]['weight'] ] \
					for edge in Wc.edges() }

			DensityTimeSeries = [ D for t in range(tf) ]
			ModularityTimeSeries = [ Q for t in range(tf) ]

			#print(t,D,Q)

		#----------------------------------------------------------

		TryPath( './post/' + experiment + '/txt/' + tag )
		TryPath( './post/' + experiment + '/pic/' + tag )

		dtxt =open( './post/' + experiment + \
				'/txt/' + tag + '/' + tag + '_' + \
				str(eta).replace('.','o') + '_' + str(trial) + \
				'_Density.txt' , 'w' )
		for x in DensityTimeSeries[:-1]:
		 	dtxt.write(str(x) + ',')
		dtxt.write(str(DensityTimeSeries[-1]))
		dtxt.close()
		qtxt =open( './post/' + experiment + \
				'/txt/' + tag + '/' + tag + '_' + \
				str(eta).replace('.','o') + '_' + str(trial) + \
				'_Modularity.txt' , 'w' )
		for x in ModularityTimeSeries[:-1]:
		 	qtxt.write(str(x) + ',')
		qtxt.write(str(ModularityTimeSeries[-1]))
		qtxt.close()

		#----------------------------------------------------------

		fig, ax = plt.subplots(figsize=(9,6))
		count = 0
		for edge in WcTimeSeries.keys():		
			if ((np.sum(WcTimeSeries[edge])>0.) and (count<=5000)):
				plt.plot( WcTimeSeries[edge] )
				count += 1
				print(count)
		#plt.show()
		ax.set_xlabel( 'Iteration', fontsize=18 )
		ax.set_ylabel( 'Strength of cooperative component' , \
			fontsize=18 )
		#ax.legend(fontsize=18)
		fig.savefig( './post/' + experiment + \
			'/pic/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + str(trial) + \
			'_Wct.png' , bbox_inches='tight' , dpi = 300 )
		#plt.show()
		plt.close(fig)

		fig, ax = plt.subplots(figsize=(9,6))
		#for edge in WcTimeSeries.edges():
		plt.plot( DensityTimeSeries )
		#plt.show()
		ax.set_xlabel( 'Iteration', fontsize=18 )
		ax.set_ylabel( 'Network density (cooperative component)' , \
			fontsize=18 )
		#ax.legend(fontsize=18)
		fig.savefig( './post/' + experiment + \
			'/pic/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + \
				str(trial) + '_Dens.png' , \
			bbox_inches='tight' , dpi = 300 )
		#plt.show()
		plt.close(fig)

		fig, ax = plt.subplots(figsize=(9,6))
		#for edge in WcTimeSeries.edges():
		plt.plot( ModularityTimeSeries )
		#plt.show()
		ax.set_xlabel( 'Iteration', fontsize=18 )
		ax.set_ylabel( 'Network modularity $Q$ (cooperative component)' , \
			fontsize=18 )
		#ax.legend(fontsize=18)
		fig.savefig( './post/' + experiment + \
			'/pic/' + tag + '/' + tag + '_' + \
			str(eta).replace('.','o') + '_' + \
				str(trial) + '_Mod.png' , \
			bbox_inches='tight' , dpi = 300 )
		#plt.show()
		plt.close(fig)

	else:

		print('\tLoading previously-computed time series: ' + \
			'Social network density and modularity (cooperative component)')

		DensityTimeSeries = \
			[ float(d) for d in open(dfile).read().split(',') ]

		ModularityTimeSeries = \
			[ float(q) for q in open(qfile).read().split(',') ]

	#----------------------------------------------------------

	return DensityTimeSeries, ModularityTimeSeries
