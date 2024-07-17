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
from CreateEnsDict import CreateEnsembleDict
from LoadSimRes import LoadSimulationResults
from CSizeVsTCurve import CrewSizeVsTimeCurves
from RecNetCoopComp import RecoverNetworkCooperativeComponent
from TimeDiv import TimeDividers
from TranCounts import TransitionCounts
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def PostProcess( experiment, M, \
	ImplementSettings, ResourceSettings, Pu, Pn, \
	mE_values, mT_values, d_values, eta_values , Chi , K , \
					cap_M_values , Recruitable , tf, trials ,\
						bawel=False , Q0=[] , AgentTypes = []):

 	#----------------------------------------------------------

	for direct in ['post','means']:
		TryPath('./' + direct + '/')
		TryPath('./' + direct + '/' + experiment)
		TryPath('./' + direct + '/' + experiment + '/txt/')
		TryPath('./' + direct + '/' + experiment + '/pic/')
	
 	#----------------------------------------------------------

	tQ_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	N_c_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	B_active_c_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	N_c_means_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	B_active_c_means_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	DensityTimeSeries_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	ModularityTimeSeries_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	Density_means_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	Modularity_means_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	TransCounts2_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	TransCounts3_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	TransCounts3a_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	CrewSizeCurves_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	TimeActive_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )
	TimeToClear_all = CreateEnsembleDict(d_values, mE_values, mT_values, \
					eta_values, cap_M_values, trials )

	#----------------------------------------------------------

	for d in d_values:
		for mE in mE_values:
			for mT in mT_values:		
				for cap_M in cap_M_values:
					for eta in eta_values:				
						for trial in trials:

							if bawel:
								print('\nGathering simulation' \
								+ ' data for post-processing:',\
								d,mE,mT,cap_M,eta,trial,'\n')

							caps = {'S':ImplementSettings['S'][2] , \
									'M':cap_M , \
								    'L':ImplementSettings['L'][2] }

							beta_t_a, N_t_c, B_active_t_c, ImplementCrewSizes_t, \
								Transitions, A, B, C, tag, filepath, AgentTypes = \
								LoadSimulationResults( experiment, d, mE, mT, eta, caps, \
									trial, ImplementSettings, ResourceSettings, M, tf, bawel )

							N_c_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								{'pop':{ c:( N_t_c['pop'][c] ) for c in C }}
							B_active_c_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								{ c:( B_active_t_c[c] ) for c in C }
							N_c_means_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								{'pop':{ c:np.mean( N_t_c['pop'][c] ) for c in C }}
							B_active_c_means_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								{ c:np.mean( B_active_t_c[c] ) for c in C }

							for at in AgentTypes:
								N_c_all[d][mE][mT][cap_M][eta][trial]['ALL'][at] = { c:( N_t_c[at][c] ) for c in C }
								N_c_means_all[d][mE][mT][cap_M][eta][trial]['ALL'][at] = { c:np.mean( N_t_c[at][c] ) for c in C }

							Curves, ActTimes, Finished, TimeActive, TimeToClear = \
								CrewSizeVsTimeCurves( ImplementCrewSizes_t , \
									M, ImplementSettings, tf, bawel )
							CrewSizeCurves_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								(Curves,ActTimes,Finished)
							TimeActive_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								TimeActive
							TimeToClear_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								TimeToClear

							DensityTimeSeries, ModularityTimeSeries = \
								RecoverNetworkCooperativeComponent( beta_t_a['pop'] , \
									mT , A , B, experiment , tag, eta, trial, bawel )
							DensityTimeSeries_all[d][mE][mT][cap_M][eta][trial] = \
								DensityTimeSeries
							ModularityTimeSeries_all[d][mE][mT][cap_M][eta][trial] = \
								ModularityTimeSeries
							Density_means_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								np.mean(DensityTimeSeries)
							Modularity_means_all[d][mE][mT][cap_M][eta][trial]['ALL'] = \
								np.mean(ModularityTimeSeries)
							if Q0:
								tQ = \
									TimeDividers( ModularityTimeSeries, Q0 )
								tQ_all[d][mE][mT][cap_M][eta][trial] = tQ

							t_intervals = [ (0,tQ) , (tQ,tf) ]

							for tii,t_int in enumerate(t_intervals):
								N_c_means_all[d][mE][mT][cap_M][eta][trial][tii] = \
									{'pop':{ c:np.mean( N_t_c['pop'][c][t_int[0]:t_int[1]] ) for c in C }}
								B_active_c_means_all[d][mE][mT][cap_M][eta][trial][tii] = \
									{ c:np.mean( B_active_t_c[c][t_int[0]:t_int[1]] ) for c in C }
								Density_means_all[d][mE][mT][cap_M][eta][trial][tii] = \
									np.mean( DensityTimeSeries[t_int[0]:t_int[1]] )
								Modularity_means_all[d][mE][mT][cap_M][eta][trial][tii] = \
									np.mean( ModularityTimeSeries[t_int[0]:t_int[1]] )
								if AgentTypes:
									for at in AgentTypes.keys():
										N_c_means_all[d][mE][mT][cap_M][eta][trial][tii][at] = \
											{ c:np.mean( N_t_c[at][c][t_int[0]:t_int[1]] ) for c in C }								

							# internal TransCounts needs to update for agenttypes. UPDATE: Done(?)

							S2,S3,S3a,S2i,S3i,S3ai = \
								TransitionCounts( Transitions , A , C , experiment , \
									tag, eta, trial, t_intervals, bawel )					
							TransCounts2_all[d][mE][mT][cap_M][eta][trial]['ALL'] = S2					
							TransCounts3_all[d][mE][mT][cap_M][eta][trial]['ALL'] = S3
							TransCounts3a_all[d][mE][mT][cap_M][eta][trial]['ALL'] = S3a
							for tii,t_int in enumerate(t_intervals):
								TransCounts2_all[d][mE][mT][cap_M][eta][trial][tii] = {}			
								TransCounts3_all[d][mE][mT][cap_M][eta][trial][tii] = {}
								TransCounts3a_all[d][mE][mT][cap_M][eta][trial][tii] = {}
								for at in S2i.keys():
									TransCounts2_all[d][mE][mT][cap_M][eta][trial][tii][at] = S2i[at][t_int]			
									TransCounts3_all[d][mE][mT][cap_M][eta][trial][tii][at] = S3i[at][t_int]
									TransCounts3a_all[d][mE][mT][cap_M][eta][trial][tii][at] = S3ai[at][t_int]

	#----------------------------------------------------------	

	return C, tQ_all, N_c_all, B_active_c_all, N_c_means_all, B_active_c_means_all, \
		DensityTimeSeries_all, ModularityTimeSeries_all, \
		Density_means_all, Modularity_means_all, \
		TransCounts2_all, TransCounts3_all, TransCounts3a_all, \
		CrewSizeCurves_all, TimeActive_all, TimeToClear_all, AgentTypes