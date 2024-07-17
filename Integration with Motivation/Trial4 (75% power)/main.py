###############################################################
#
#		"WhaleHuntGame" by Andy Schauf (2023)
#				a.schauf@nus.edu.sg
#				andyschauf@gmail.com
#	'The Whale Hunt game: A model of technology-mediated
#		social atomization in Lamalera and beyond'
#
#	Note: Go down to the 'def main(args=None):' part at the
#		bottom to change settings and alter how simulations are run.
#		Everything above that are auxiliary functions called
#		by the main functions appearing in 'main'.
#		Set things how you like, and then run from e.g. the command
#		line: 'python main.py' 
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
from library import * 
#--------------------------------------------------------------
###############################################################

#					MAIN FUNCTION :
#	Parameters are set here and then functions are executed
#	 from here.

###############################################################

def main(args=None):
	"""The main routine."""
	if args is None:
	    args = sys.argv[1:]

	#----------------------------------------------------------

	#                  PARAMETER SETTINGS :

	#		Agents :	---------------------------------------

	M = 200							# Number of agents
	Pu = .3							# Probability of 'rational' update
	Pn = .0							# Probablity of 'random' update (noise)
	mE_values = [ 5 ]		# Ecological 'memory' parameter
	mT_values = [ 2500 ]	# Trust 'memory' parameter ('infty' means the initial social ties never change)
	d_values = [.99]				# Social network cooperative 
									# 		component weight parameter values # (now needs to be <1)
	Recruitable = 10     #16        # Number of agents approached during new crew formation. 
									#   If it's high, there is a better change of crew formation, 
									#    EXCEPT this also tends to reduce the group affinity scores of prospective joiners

	#		Implements :	-----------------------------------

	# ( minumum crew size, maximum crew size )

	n0_S, nX_S = 1, 2			# Solitary implements
	n0_M, nX_M = 4, 8			# Medium-group implements
	n0_L, nX_L = 8, 16			# Large-group implements

	cap_M_values = [ 0, 20 ]	# The maximum number of Medium-group implements
									# that can operate simultaneously
									# (here, 40 means no restriction.
									#  5 means that there is an imposed cap of 5.
									#  0 means none can operate.)

				 # min ,  max , No. available  , No. initially active 
	ImplementSettings = \
		{ 'S': ( n0_S , nX_S , round(M/n0_S) , 0 ),
		  'M': ( n0_M , nX_M , round(M/n0_M) , 0 ),
		  'L': ( n0_L , nX_L , round(M/n0_L) , round(M/(n0_L+2)) )  }

	n_values = list(range(M))
	Chi = { c:[ float(int( n >= ImplementSettings[c][0] )) for n in n_values ] \
				for c in ImplementSettings.keys() }

	#		Resources :	---------------------------------------

	Ex_p_S = 1.	# Expected return for Solitary implement
	p0_S = 0.	# Return in case of failure for Solitary implements
	Pp0_S = .10

	eta_values = [4.00] # higher values of this parameter η describe conditions 
				   			# that are relatively more favorable to Large-group hunting

	alpha_r_S, alpha_p_S = 0., 0.
	alpha_r_M, alpha_p_M = 0., 0.
	alpha_r_L, alpha_p_L = 0., 0.

	ResourceSettings = { 'Ex_p_S': Ex_p_S ,
					     'p0_S': p0_S ,
					     'Pp0_S': Pp0_S ,
						 'S': ( alpha_r_S , alpha_p_S ),
						 'M': ( alpha_r_M , alpha_p_M ),
						 'L': ( alpha_r_L , alpha_p_L ) }

	K = ( ( n0_L/n0_S )*( Ex_p_S/( 1. - Pp0_S ) ) )	# max. possible returns value
	k = 0.										# Forward Euler factor

	#		Simulation : --------------------------------------

	tf = 1200 #12000 # 12000
	trials = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	bawel = False
	
	#----------------------------------------------------------
	#----------------------------------------------------------

	#			 RUN NUMERICAL EXPERIMENTS 

	#	EXPERIMENT A: Fixed resource conditions,
	#				   synthetic returns distributions -------

	t1 = .75
	FracTypes = { 'pow':t1 , 'aff':(1-t1) }

	experiment = 'A'
	RunEnsembleSimulationsA( experiment, M, \
		ImplementSettings, ResourceSettings, Pu, Pn, \
		mE_values, mT_values, d_values, eta_values , Chi , K , \
		cap_M_values , Recruitable , \
			tf, trials , bawel , FracTypes )
	#print(stop)
	Q0 = .40 # 10**-3		# Modularity value that divides "first" and "second" stages of dynamics in post-processing
	C, tQ_all, N_c_all, B_active_c_all, N_c_means_all, B_active_c_means_all, \
		DensityTimeSeries_all, ModularityTimeSeries_all, \
		Density_means_all, Modularity_means_all, \
		TransCounts2_all, TransCounts3_all, TransCounts3a_all, \
		CrewSizeCurves_all, TimeActive_all, TimeToClear_all, AgentTypes = \
	PostProcess( experiment, M, \
		ImplementSettings, ResourceSettings, Pu, Pn, \
		mE_values, mT_values, d_values, eta_values , Chi , K , \
		cap_M_values , Recruitable , \
			tf, trials , bawel , Q0 )
	SummaryGraphics( experiment, M, C, \
	ImplementSettings, ResourceSettings, Pu, Pn, \
	mE_values, mT_values, d_values, eta_values , Chi , K , \
	cap_M_values , Recruitable , tf, trials ,\
		tQ_all,  N_c_all, B_active_c_all, \
		N_c_means_all, B_active_c_means_all, \
		DensityTimeSeries_all, ModularityTimeSeries_all, \
		Density_means_all, Modularity_means_all, \
		TransCounts2_all, TransCounts3_all, TransCounts3a_all, \
		CrewSizeCurves_all, TimeActive_all, TimeToClear_all, bawel, Q0 , AgentTypes)
	#print(cc)
	#	EXPERIMENT B: Fixed resource conditions,	
	#		  empirically-based returns distributions --------

	# experiment = 'B'

	# K = ( ( n0_L/n0_S )*( Ex_p_S/( 1. - Pp0_S ) ) )	# max. possible returns value
	# k = 0.										# Forward Euler factor


	# eta_values = [6.00]

	# p0_M = 0.
	# Ex_p_M_values = [.4]#[ 1.50 , .60 , .70 , .80 ]
	# p1_M_values = [1.5]#[ .25 , .50 , .75 , 1.00 , 1.25 ]	# Make them multiples of the fishing payoff

	# Run first with no jonson over a range of eta, then use to choose constant value of eta for other experiment

	# RunEnsembleSimulationsB( experiment, M, \
	# 	ImplementSettings, ResourceSettings, Pu, Pn, \
	# 	mE_values, mT_values, d_values, eta_values , Chi , K , \
	# 	p0_M, Ex_p_M_values, p1_M_values, \
	# 	cap_M_values , Recruitable , \
	# 	tf, trials , bawel )

	#	EXPERIMENT C: Varying resource conditions
	#								(Lotka-Volterra) ---------

	# experiment = 'C'

	# mT_values = 'infty'

	# DynamicResources = True

	# alpha_r_S, alpha_p_S = .0, .0
	# alpha_r_M, alpha_p_M = .01, .01
	# alpha_r_L, alpha_p_L = 0., 0.

	# ResourceSettings = { 'Ex_p_S': Ex_p_S ,
	# 				     'p0_S': p0_S ,
	# 				     'Pp0_S': Pp0_S ,
	# 					 'S': ( alpha_r_S , alpha_p_S ),
	# 					 'M': ( alpha_r_M , alpha_p_M ),
	# 					 'L': ( alpha_r_L , alpha_p_L ) }

	# K = ( ( n0_L/n0_S )*( Ex_p_S/( 1. - Pp0_S ) ) )	# max. possible returns value
	# k = 1.										# Forward Euler factor


	# d_values = [.25]
	# mE_values = [5]
	# mT_values = [100]
	# eta_values = [4.00]

	# # test over different parameter ranges

	# RunEnsembleSimulationsC( experiment, M, \
	# 	ImplementSettings, ResourceSettings, Pu, Pn, \
	# 	mE_values, mT_values, d_values, eta_values , Chi , K , \
	# 	cap_M_values , Recruitable , \
	# 		tf, trials , k, bawel )
	# print(stop)
	# Q0 = .40 # 10**-3
	# PostProcess( experiment, M, \
	# 	ImplementSettings, ResourceSettings, Pu, Pn, \
	# 	mE_values, mT_values, d_values, eta_values , Chi , K , \
	# 	cap_M_values , Recruitable , \
	# 		tf, trials , bawel , Q0 )

	#---------------------------------------------------------
#-------------------------------------------------------------

###############################################################

if __name__ == "__main__":
    main()