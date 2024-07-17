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

def SummaryGraphics( experiment, M, C, \
	ImplementSettings, ResourceSettings, Pu, Pn, \
	mE_values, mT_values, d_values, eta_values , Chi , K , \
	cap_M_values , Recruitable , tf, trials ,\
		tQ_all,  N_c_all, B_active_c_all, N_c_means_all, B_active_c_means_all, \
		DensityTimeSeries_all, ModularityTimeSeries_all, \
		Density_means_all, Modularity_means_all, \
		TransCounts2_all, TransCounts3_all, TransCounts3a_all, \
		CrewSizeCurves_all, TimeActive_all, TimeToClear_all, bawel=False , Q0=[] , AgentTypes=[] ):
					
	#------------------------------------------

	# Mean fractions of affiliated agents
	#	and numbers of active implements by type

	#Colors = { 'S':'green', 'M':'orange' , 'L':'blue' }
	Colors = { 'S':colors.to_rgba('green'), \
			   'M':colors.to_rgba('orange'), \
			   'L':colors.to_rgba('blue') }
	Labels = { 'S':'Solitary/Small-group', \
			   'M':'Medium-group' , \
			   'L':'Large-group' }

	LineWidths_cap = { cap_M:(cmi+1) for cmi,cap_M in enumerate(sorted(cap_M_values)) }
	LineWidths_c2 = { c2:(ci+1) for ci,c2 in enumerate(reversed(C)) }

	#---------------

	print('Plotting mean fractions of affiliated agents by implement type versus Eta, and ')
	print('Plotting mean numbers of active implements by implement type versus Eta')

	for d in d_values:
		TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') )
		TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') )
		for mE in mE_values:
			TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/' )
			TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/' )
			for mT in mT_values:

				TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' )
				TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/')
				TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' )
				TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' )

				for at in (list(AgentTypes.keys())+['pop']):

					if (at=='pop'):
						addtag = ''
					else:
						addtag = '_'+at

					txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
						+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_MeanFractionAffiliatedByTypeVsEta_ALL.txt'
					txt = open( txtfile , 'w' )	
					
					fig, ax = plt.subplots(figsize=(9,6))
					fig.gca().invert_xaxis()
					for cap_M in cap_M_values:
						txt.write( str(cap_M) + ':' )
						for c in C:					
							
							N_c_meansVsEta = [ np.mean([ N_c_means_all[d][mE][mT][cap_M][eta][trial]['ALL'][at][c] for trial in trials ])/M for eta in eta_values ]
							ax.plot(eta_values,N_c_meansVsEta,'o-',color=Colors[c],linewidth=LineWidths_cap[cap_M],label=Labels[c]+' ('+str(cap_M)+')')
							
							txt.write( c + ':' )
							for eta in eta_values[:-1]:
								txt.write( str(eta) + ',' )
							txt.write( str(eta_values[-1]) + ';' )
							for nc in N_c_meansVsEta[:-1]:
								txt.write( str(nc) + ',' )
							txt.write( str(N_c_meansVsEta[-1]) + ';' )
						txt.write('\n')	
					txt.close()					

					ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
					ax.set_ylabel( 'Fraction of affiliated agents $N_c$' , \
						fontsize=18 )
					ax.legend(fontsize=12)
					fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
						+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_MeanFractionAffiliatedByTypeVsEta_ALL.png' , bbox_inches='tight' , dpi = 300 )
					#plt.show()
					plt.close(fig)	

					for eta in eta_values:

						txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_' + str(eta).replace('.','o') + addtag + '_FractionAffiliatedVsTime.txt'
						txt = open( txtfile , 'w' )	
						
						for cap_M in cap_M_values:
							fig, ax = plt.subplots(figsize=(9,6))
							txt.write( str(cap_M) + ':' )
							for c in C:					
								
								for trial in trials:
									clr = ( np.min([1.,np.max([0.,Colors[c][0] + .4*(random.random()-.5)])]) , \
											np.min([1.,np.max([0.,Colors[c][1] + .4*(random.random()-.5)])]) , \
											np.min([1.,np.max([0.,Colors[c][2] + .4*(random.random()-.5)])]) , )
									ax.plot( [ (n/M) for n in N_c_all[d][mE][mT][cap_M][eta][trial]['ALL'][at][c] ],color=clr,linewidth=1)
								N_c_meansVsTime = [ np.mean([ N_c_all[d][mE][mT][cap_M][eta][trial]['ALL'][at][c][t] for trial in trials ])/M for t in range(tf) ]
					
								ax.plot(N_c_meansVsTime,color=Colors[c],linewidth=2,label=Labels[c]+' ('+str(cap_M)+')')

								txt.write( c + ':' )
								for nc in N_c_meansVsTime[:-1]:
									txt.write( str(nc) + ',' )
								txt.write( str(N_c_meansVsTime[-1]) + ';' )

							ax.set_xlabel( 'Iteration $t$', fontsize=18 )
							ax.set_ylabel( 'Fraction of affiliated agents $N_c$' , \
								fontsize=18 )
							ax.legend(fontsize=12)
							fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
								+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_' + str(eta).replace('.','o') + addtag + '_FractionAffiliatedVsTime_ALL_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
							#plt.show()
							plt.close(fig)	

							txt.write('\n')	
						txt.close()					
								
				fig, ax = plt.subplots(figsize=(9,6))
				fig.gca().invert_xaxis()

				txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanActiveImplementsByTypeVsEta_ALL.txt'
				txt = open( txtfile , 'w' )	
				
				for cap_M in cap_M_values:
					txt.write( str(cap_M) + ':' )
					for c in C:
						
						B_active_c_meansVsEta = [ np.mean([ B_active_c_means_all[d][mE][mT][cap_M][eta][trial]['ALL'][c] for trial in trials ]) for eta in eta_values ]
						ax.plot(eta_values,B_active_c_meansVsEta,'o-',color=Colors[c],linewidth=LineWidths_cap[cap_M],label=Labels[c]+' ('+str(cap_M)+')')
						
						txt.write( str(c) + ':' )
						for eta in eta_values[:-1]:
							txt.write( str(eta) + ',' )
						txt.write( str(eta_values[-1]) + ';' )
						for nc in B_active_c_meansVsEta[:-1]:
							txt.write( str(nc) + ',' )
						txt.write( str(B_active_c_meansVsEta[-1]) + ';' )
					txt.write('\n')	
				txt.close()
				
				ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
				ax.set_ylabel( 'Number of active implements $B_{\\mathrm{active},c}$' , \
					fontsize=18 )
				ax.legend(fontsize=12)
				fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanActiveImplementsByTypeVsEta_ALL.png' , bbox_inches='tight' , dpi = 300 )
				#plt.show()
				plt.close(fig)	

				for eta in eta_values:

					txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' \
						+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_' + str(eta).replace('.','o') + '_ActiveImplementsVsTime.txt'
					txt = open( txtfile , 'w' )	
										
					for cap_M in cap_M_values:
						fig, ax = plt.subplots(figsize=(9,6))
						txt.write( str(cap_M) + ':' )
						for c in C:					
							
							for trial in trials:
								clr = ( np.min([1.,np.max([0.,Colors[c][0] + .4*(random.random()-.5)])]) , \
										np.min([1.,np.max([0.,Colors[c][1] + .4*(random.random()-.5)])]) , \
										np.min([1.,np.max([0.,Colors[c][2] + .4*(random.random()-.5)])]) , )
								ax.plot( B_active_c_all[d][mE][mT][cap_M][eta][trial]['ALL'][c],color=clr,linewidth=1)
							B_active_c_meansVsTime = [ np.mean([ B_active_c_all[d][mE][mT][cap_M][eta][trial]['ALL'][c][t] for trial in trials ]) for t in range(tf) ]
				
							ax.plot(B_active_c_meansVsTime,color=Colors[c],linewidth=2,label=Labels[c]+' ('+str(cap_M)+')')
							
							txt.write( c + ':' )
							for nc in B_active_c_meansVsTime[:-1]:
								txt.write( str(nc) + ',' )
							txt.write( str(B_active_c_meansVsTime[-1]) + ';' )
						txt.write('\n')	
						ax.set_xlabel( 'Iteration $t$', fontsize=18 )
						ax.set_ylabel( 'Number of active implements $B_c$' , \
							fontsize=18 )
						ax.legend(fontsize=12)
						fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_' + str(eta).replace('.','o') + '_ActiveImplementsVsTime_ALL_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
						#plt.show()
						plt.close(fig)	
					txt.close()					
							
				txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_TimeActiveByTypeVsEta_ALL.txt'
				txt = open( txtfile , 'w' )	
				
				fig, ax = plt.subplots(figsize=(9,6))
				fig.gca().invert_xaxis()
				for cap_M in cap_M_values:
					txt.write( str(cap_M) + ':' )
					for c in C:					
						TimeActiveList = { eta:[] for eta in eta_values }
						for eta in eta_values:
							for trial in trials:
								TimeActiveList[eta].extend(TimeActive_all[d][mE][mT][cap_M][eta][trial]['ALL'][c])
						TimeActive_meansVsEta = [ np.mean([ ta for ta in TimeActiveList[eta] if not np.isnan(ta) ]) for eta in eta_values ]
						ax.plot(eta_values,TimeActive_meansVsEta,'o-',color=Colors[c],linewidth=LineWidths_cap[cap_M],label=Labels[c]+' ('+str(cap_M)+')')
						txt.write( c + ':' )
						for eta in eta_values[:-1]:
							txt.write( str(eta) + ',' )
						txt.write( str(eta_values[-1]) + ';' )
						for nc in TimeActive_meansVsEta[:-1]:
							txt.write( str(nc) + ',' )
						txt.write( str(TimeActive_meansVsEta[-1]) + ';' )
					txt.write('\n')	
				txt.close()		

				ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
				ax.set_ylabel( 'Mean active duration' , \
					fontsize=18 )
				ax.legend(fontsize=12)
				fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_TimeActiveByTypeVsEta_ALL.png' , bbox_inches='tight' , dpi = 300 )
				#plt.show()
				plt.close(fig)	

				txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_TimeToClearByTypeVsEta_ALL.txt'
				txt = open( txtfile , 'w' )	
				
				fig, ax = plt.subplots(figsize=(9,6))
				fig.gca().invert_xaxis()
				for cap_M in cap_M_values:
					txt.write( str(cap_M) + ':' )
					for c in C:					
						TimeToClearList = { eta:[] for eta in eta_values }
						for eta in eta_values:
							for trial in trials:
								TimeToClearList[eta].extend(TimeToClear_all[d][mE][mT][cap_M][eta][trial]['ALL'][c])
						TimeToClear_meansVsEta = [ np.mean([ ta for ta in TimeToClearList[eta] if not np.isnan(ta) ]) for eta in eta_values ]
						ax.plot(eta_values,TimeToClear_meansVsEta,'o-',color=Colors[c],linewidth=LineWidths_cap[cap_M],label=Labels[c]+' ('+str(cap_M)+')')
						txt.write( c + ':' )
						for eta in eta_values[:-1]:
							txt.write( str(eta) + ',' )
						txt.write( str(eta_values[-1]) + ';' )
						for nc in TimeToClear_meansVsEta[:-1]:
							txt.write( str(nc) + ',' )
						txt.write( str(TimeToClear_meansVsEta[-1]) + ';' )
					txt.write('\n')	
				txt.close()		

				ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
				ax.set_ylabel( 'Mean time to clear' , \
					fontsize=18 )
				ax.legend(fontsize=12)
				fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_TimeToClearByTypeVsEta_ALL.png' , bbox_inches='tight' , dpi = 300 )
				#plt.show()
				plt.close(fig)	

				#------

				fig, ax = plt.subplots(figsize=(9,6))
				fig.gca().invert_xaxis()

				txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanDensityVsEta_ALL.txt'
				txt = open( txtfile , 'w' )	
				
				for cap_M in cap_M_values:
					txt.write( str(cap_M) + ':' )
						
					Density_meansVsEta = [ np.mean([ Density_means_all[d][mE][mT][cap_M][eta][trial]['ALL'] for trial in trials ]) for eta in eta_values ]
					ax.plot(eta_values,Density_meansVsEta,'o-',linewidth=LineWidths_cap[cap_M],label=str(cap_M))
					for eta in eta_values[:-1]:
						txt.write( str(eta) + ',' )
					txt.write( str(eta_values[-1]) + ';' )
					for nc in Density_meansVsEta[:-1]:
						txt.write( str(nc) + ',' )
					txt.write( str(Density_meansVsEta[-1]) + ';' )
					txt.write('\n')	
				txt.close()
				
				ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
				ax.set_ylabel( 'Mean cooperative network density' , \
					fontsize=18 )
				ax.legend(fontsize=12)
				fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanDensityVsEta_ALL.png' , bbox_inches='tight' , dpi = 300 )
				#plt.show()
				plt.close(fig)	


				fig, ax = plt.subplots(figsize=(9,6))
				fig.gca().invert_xaxis()

				txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanModularityVsEta_ALL.txt'
				txt = open( txtfile , 'w' )	
				
				for cap_M in cap_M_values:
					txt.write( str(cap_M) + ':' )
						
					Modularity_meansVsEta = [ np.mean([ Modularity_means_all[d][mE][mT][cap_M][eta][trial]['ALL'] for trial in trials ]) for eta in eta_values ]
					ax.plot(eta_values,Modularity_meansVsEta,'o-',linewidth=LineWidths_cap[cap_M],label=str(cap_M))
					for eta in eta_values[:-1]:
						txt.write( str(eta) + ',' )
					txt.write( str(eta_values[-1]) + ';' )
					for nc in Modularity_meansVsEta[:-1]:
						txt.write( str(nc) + ',' )
					txt.write( str(Modularity_meansVsEta[-1]) + ';' )
					txt.write('\n')	
				txt.close()
				
				ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
				ax.set_ylabel( 'Mean cooperative network modularity' , \
					fontsize=18 )
				ax.legend(fontsize=12)
				fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
					+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanModularityVsEta_ALL.png' , bbox_inches='tight' , dpi = 300 )
				#plt.show()
				plt.close(fig)	


				if Q0:

					fig, ax = plt.subplots(figsize=(9,6))
					fig.gca().invert_xaxis()
					txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
						+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanThresholdTimeVsEta.txt'
					txt = open( txtfile , 'w' )	
					for cap_M in cap_M_values:

						tQ_meansVsEta = [ np.mean([ tQ_all[d][mE][mT][cap_M][eta][trial] for trial in trials ]) for eta in eta_values ]
						ax.plot(eta_values,tQ_meansVsEta,'o-',linewidth=LineWidths_cap[cap_M],label=str(cap_M))

						txt.write( str(cap_M) + ':' )
						for eta in eta_values[:-1]:
							txt.write( str(eta) + ',' )
						txt.write( str(eta_values[-1]) + ';' )
						for nc in tQ_meansVsEta[:-1]:
							txt.write( str(nc) + ',' )
						txt.write( str(tQ_meansVsEta[-1]) + '\n' )
					txt.close()	

					ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
					ax.set_ylabel( 'Threshold time $t_{Q}$' , \
						fontsize=18 )
					ax.legend(fontsize=12)
					fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
						+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanThresholdTimeVsEta.png' , bbox_inches='tight' , dpi = 300 )
					#plt.show()
					plt.close(fig)

					for ti in [0,1]:

						for at in AgentTypes.keys():

							if (at=='pop'):
								addtag = ''
							else:
								addtag = '_' + at

							fig, ax = plt.subplots(figsize=(9,6))
							fig.gca().invert_xaxis()

							TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' )
							TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' )

							txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
								+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_MeanFractionAffiliatedByTypeVsEta_ALL.txt'

							txt = open( txtfile , 'w' )	

							for cap_M in cap_M_values:
								txt.write( str(cap_M) + ':' )
								for c in C:

									N_c_meansVsEta = [ np.mean([ N_c_means_all[d][mE][mT][cap_M][eta][trial][ti][at][c] for trial in trials ])/M for eta in eta_values ]
									ax.plot(eta_values,N_c_meansVsEta,'o-',color=Colors[c],linewidth=LineWidths_cap[cap_M],label=Labels[c]+' ('+str(cap_M)+')')

									txt.write( c + ':' )
									for eta in eta_values[:-1]:
										txt.write( str(eta) + ',' )
									txt.write( str(eta_values[-1]) + ';' )
									for nc in N_c_meansVsEta[:-1]:
										txt.write( str(nc) + ',' )
									txt.write( str(N_c_meansVsEta[-1]) + ';' )
								txt.write('\n')	
							txt.close()					
							
							ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
							ax.set_ylabel( 'Fraction of affiliated agents $N_c$' , \
								fontsize=18 )
							ax.legend(fontsize=12)
							fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
								+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_MeanFractionAffiliatedByTypeVsEta_' + str(ti) + '.png' , bbox_inches='tight' , dpi = 300 )
							#plt.show()
							plt.close(fig)			

							fig, ax = plt.subplots(figsize=(9,6))
							fig.gca().invert_xaxis()

						txtfile = './means/' + experiment + '/txt/d'+ str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanActiveImplementsByTypeVsEta_' + str(ti) + '.txt'
						txt = open( txtfile , 'w' )	

						for cap_M in cap_M_values:
							for c in C:

								B_active_c_meansVsEta = [ np.mean([ B_active_c_means_all[d][mE][mT][cap_M][eta][trial][ti][c] for trial in trials ]) for eta in eta_values ]
								ax.plot(eta_values,B_active_c_meansVsEta,'o-',color=Colors[c],linewidth=LineWidths_cap[cap_M],label=Labels[c]+' ('+str(cap_M)+')')

								txt.write( str(c) + ':' )
								for eta in eta_values[:-1]:
									txt.write( str(eta) + ',' )
								txt.write( str(eta_values[-1]) + ';' )
								for nc in B_active_c_meansVsEta[:-1]:
									txt.write( str(nc) + ',' )
								txt.write( str(B_active_c_meansVsEta[-1]) + ';' )
							txt.write('\n')	
						txt.close()

						ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
						ax.set_ylabel( 'Number of active implements $B_{\\mathrm{active},c}$' , \
							fontsize=18 )
						ax.legend(fontsize=12)
						fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanActiveImplementsByTypeVsEta_' + str(ti) + '.png' , bbox_inches='tight' , dpi = 300 )
						#plt.show()
						plt.close(fig)	


						fig, ax = plt.subplots(figsize=(9,6))
						fig.gca().invert_xaxis()

						txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanDensityVsEta_' + str(ti) + '.txt'
						txt = open( txtfile , 'w' )	
						
						for cap_M in cap_M_values:
							txt.write( str(cap_M) + ':' )
								
							Density_meansVsEta = [ np.mean([ Density_means_all[d][mE][mT][cap_M][eta][trial][ti] for trial in trials ]) for eta in eta_values ]
							ax.plot(eta_values,Density_meansVsEta,'o-',linewidth=LineWidths_cap[cap_M],label=Labels[c]+' ('+str(cap_M)+')')
							for eta in eta_values[:-1]:
								txt.write( str(eta) + ',' )
							txt.write( str(eta_values[-1]) + ';' )
							for nc in Density_meansVsEta[:-1]:
								txt.write( str(nc) + ',' )
							txt.write( str(Density_meansVsEta[-1]) + ';' )
							txt.write('\n')	
						txt.close()
						
						ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
						ax.set_ylabel( 'Mean cooperative network density' , \
							fontsize=18 )
						ax.legend(fontsize=12)
						fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanDensityVsEta_' + str(ti) + '.png' , bbox_inches='tight' , dpi = 300 )
						#plt.show()
						plt.close(fig)	

						fig, ax = plt.subplots(figsize=(9,6))
						fig.gca().invert_xaxis()

						txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanModularityVsEta_' + str(ti) + '.txt'
						txt = open( txtfile , 'w' )	
						
						for cap_M in cap_M_values:
							txt.write( str(cap_M) + ':' )
								
							Modularity_meansVsEta = [ np.mean([ Modularity_means_all[d][mE][mT][cap_M][eta][trial][ti] for trial in trials ]) for eta in eta_values ]
							ax.plot(eta_values,Modularity_meansVsEta,'o-',linewidth=LineWidths_cap[cap_M],label=str(cap_M))
							for eta in eta_values[:-1]:
								txt.write( str(eta) + ',' )
							txt.write( str(eta_values[-1]) + ';' )
							for nc in Modularity_meansVsEta[:-1]:
								txt.write( str(nc) + ',' )
							txt.write( str(Modularity_meansVsEta[-1]) + ';' )
							txt.write('\n')	
						txt.close()
						
						ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
						ax.set_ylabel( 'Mean cooperative network modularity' , \
							fontsize=18 )
						ax.legend(fontsize=12)
						fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanModularityVsEta_' + str(ti) + '.png' , bbox_inches='tight' , dpi = 300 )
						#plt.show()
						plt.close(fig)	


				#--------------------------------------------------------------

				TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/network' )

				# Cooperative network density / modularity mean time series

				for eta in eta_values:
					fig, ax = plt.subplots(figsize=(9,6))
					for cap_M in cap_M_values:
						MeanDensityTimeSeries = [ np.mean([DensityTimeSeries_all[d][mE][mT][cap_M][eta][trial][t] for trial in trials]) for t in range(tf) ]
						ax.plot(MeanDensityTimeSeries,linewidth=LineWidths_cap[cap_M],label=str(cap_M))
					ax.set_xlabel( 'Iteration $t$', fontsize=18 )
					ax.set_ylabel( 'Cooperative network density $D$' , \
						fontsize=18 )
					ax.legend(fontsize=12)
					fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
						'/network/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanDensityTimeSeries_eta' + str(eta).replace('.','o') + '.png' , bbox_inches='tight' , dpi = 300 )
					#plt.show()
					plt.close(fig)

				for eta in eta_values:
					fig, ax = plt.subplots(figsize=(9,6))
					for cap_M in cap_M_values:
						MeanModularityTimeSeries = [ np.mean([ModularityTimeSeries_all[d][mE][mT][cap_M][eta][trial][t] for trial in trials]) for t in range(tf) ]
						ax.plot(MeanModularityTimeSeries,linewidth=LineWidths_cap[cap_M],label=str(cap_M))
					ax.set_xlabel( 'Iteration $t$', fontsize=18 )
					ax.set_ylabel( 'Cooperative network modularity $Q$' , \
						fontsize=18 )
					ax.legend(fontsize=12)
					fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/' \
						'/network/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanModularityTimeSeries_eta' + str(eta).replace('.','o') + '.png' , bbox_inches='tight' , dpi = 300 )
					#plt.show()
					plt.close(fig)

				#----------------------------------------------------------

				# Transition counts 

				TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts' )
				TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts' )

				for at in AgentTypes.keys():

					if (at=='pop'):
						addtag = ''
					else:
						addtag = '_'+at

					for cap_M in cap_M_values:

						fig, ax = plt.subplots(figsize=(9,6))
						fig.gca().invert_xaxis()

						txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts2VsEta_ALL_M' + str(cap_M) + '.txt'
						txt = open( txtfile , 'w' )	

						for c1 in C:
							for c2 in C:

								TwoStep_meansVsEta = [ np.mean([ TransCounts2_all[d][mE][mT][cap_M][eta][trial]['ALL'][at][c1][c2] for trial in trials ])/tf for eta in eta_values ]
								ax.plot(eta_values,TwoStep_meansVsEta,'o-',color=Colors[c1],linewidth=LineWidths_c2[c2],label=c1+'$\\to$'+c2)

								txt.write( str(c1) + '-' + str(c2) + ':' )
								for eta in eta_values[:-1]:
									txt.write( str(eta) + ',' )
								txt.write( str(eta_values[-1]) + ';' )
								for nc in TwoStep_meansVsEta[:-1]:
									txt.write( str(nc) + ',' )
								txt.write( str(TwoStep_meansVsEta[-1]) + ';' )
							txt.write('\n')	
						txt.close()

						ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
						ax.set_ylabel( 'Rate of transitions' , \
							fontsize=18 )
						ax.legend(fontsize=12)
						fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts2VsEta_ALL_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
						#plt.show()
						plt.close(fig)		

					for cap_M in cap_M_values:

						fig, ax = plt.subplots(figsize=(9,6))
						fig.gca().invert_xaxis()

						txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3VsEta_ALL_M' + str(cap_M) + '.txt'
						txt = open( txtfile , 'w' )	

						for c1 in C:
							for c2 in C:

								# maybe divide by time (as in number of transitions per time unit)
								ThreeStepM_meansVsEta = [ np.mean([ TransCounts3_all[d][mE][mT][cap_M][eta][trial]['ALL'][at][c1][c2] for trial in trials ])/tf for eta in eta_values ]
								ax.plot(eta_values,ThreeStepM_meansVsEta,'o-',color=Colors[c1],linewidth=LineWidths_c2[c2],label=c1+'$\\to$M$\\to$'+c2)

								txt.write( str(c1) + '-' + str(c2) + ':' )
								for eta in eta_values[:-1]:
									txt.write( str(eta) + ',' )
								txt.write( str(eta_values[-1]) + ';' )
								for nc in ThreeStepM_meansVsEta[:-1]:
									txt.write( str(nc) + ',' )
								txt.write( str(ThreeStepM_meansVsEta[-1]) + ';' )
							txt.write('\n')	
						txt.close()

						ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
						ax.set_ylabel( 'Rate of transitions' , \
							fontsize=18 )
						ax.legend(fontsize=12)
						fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3VsEta_ALL_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
						#plt.show()
						plt.close(fig)

					for cap_M in cap_M_values:

						fig, ax = plt.subplots(figsize=(9,6))
						fig.gca().invert_xaxis()

						txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3aVsEta_ALL_M' + str(cap_M) + '.txt'
						txt = open( txtfile , 'w' )	

						for c1 in C:
							for c2 in C:

								# maybe divide by time (as in number of transitions per time unit)
								ThreeStepMa_meansVsEta = [ np.mean([ TransCounts3a_all[d][mE][mT][cap_M][eta][trial]['ALL'][at][c1][c2] for trial in trials ])/tf for eta in eta_values ]
								ax.plot(eta_values,ThreeStepMa_meansVsEta,'o-',color=Colors[c1],linewidth=LineWidths_c2[c2],label=c1+'$\\to$M$\\to$'+c2)

								txt.write( str(c1) + '-' + str(c2) + ':' )
								for eta in eta_values[:-1]:
									txt.write( str(eta) + ',' )
								txt.write( str(eta_values[-1]) + ';' )
								for nc in ThreeStepMa_meansVsEta[:-1]:
									txt.write( str(nc) + ',' )
								txt.write( str(ThreeStepMa_meansVsEta[-1]) + ';' )
							txt.write('\n')	
						txt.close()

						ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
						ax.set_ylabel( 'Rate of transitions' , \
							fontsize=18 )
						ax.legend(fontsize=12)
						fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/transcounts/' \
							+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3aVsEta_ALL_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
						#plt.show()
						plt.close(fig)

					if Q0:
						for ti in [0,1]:

							TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/transcounts/' )
							TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + '/transcounts/' )

							# SHOULD THESE BE DIVIDED BY THE TIME OF THE TIME INTERVAL?? 

							for cap_M in cap_M_values:

								fig, ax = plt.subplots(figsize=(9,6))
								fig.gca().invert_xaxis()

								txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + \
									'/transcounts/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts2VsEta_' + str(ti) + '_M' + str(cap_M) + '.txt'
								txt = open( txtfile , 'w' )	

								for c1 in C:
									for c2 in C:

										# maybe divide by time (as in number of transitions per time unit)											
										TwoStep_meansVsEta = [ np.mean([ TransCounts2_all[d][mE][mT][cap_M][eta][trial][ti][at][c1][c2] for trial in trials ])/([ (tQ_all[d][mE][mT][cap_M][eta][trial] - 0) , (tf - tQ_all[d][mE][mT][cap_M][eta][trial]) ][ti]) for eta in eta_values ]
										ax.plot(eta_values,TwoStep_meansVsEta,'o-',color=Colors[c1],linewidth=LineWidths_c2[c2],label=c1+'$\\to$'+c2)

										txt.write( str(c1) + '-' + str(c2) + ':' )
										for eta in eta_values[:-1]:
											txt.write( str(eta) + ',' )
										txt.write( str(eta_values[-1]) + ';' )
										for nc in TwoStep_meansVsEta[:-1]:
											txt.write( str(nc) + ',' )
										txt.write( str(TwoStep_meansVsEta[-1]) + ';' )
									txt.write('\n')	
								txt.close()

								ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
								ax.set_ylabel( 'Rate of transitions' , \
									fontsize=18 )
								ax.legend(fontsize=12)
								fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + \
									'/transcounts/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts2VsEta_' + str(ti) + '_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
								#plt.show()
								plt.close(fig)		

							for cap_M in cap_M_values:

								fig, ax = plt.subplots(figsize=(9,6))
								fig.gca().invert_xaxis()

								txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + \
									'/transcounts/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3VsEta_' + str(ti) + '_M' + str(cap_M) + '.txt'
								txt = open( txtfile , 'w' )	

								for c1 in C:
									for c2 in C:

										# maybe divide by time (as in number of transitions per time unit)
										ThreeStepM_meansVsEta = [ np.mean([ TransCounts3_all[d][mE][mT][cap_M][eta][trial][ti][at][c1][c2] for trial in trials ])/([ (tQ_all[d][mE][mT][cap_M][eta][trial] - 0) , (tf - tQ_all[d][mE][mT][cap_M][eta][trial]) ][ti]) for eta in eta_values ]
										ax.plot(eta_values,ThreeStepM_meansVsEta,'o-',color=Colors[c1],linewidth=LineWidths_c2[c2],label=c1+'$\\to$M$\\to$'+c2)

										txt.write( str(c1) + '-' + str(c2) + ':' )
										for eta in eta_values[:-1]:
											txt.write( str(eta) + ',' )
										txt.write( str(eta_values[-1]) + ';' )
										for nc in ThreeStepM_meansVsEta[:-1]:
											txt.write( str(nc) + ',' )
										txt.write( str(ThreeStepM_meansVsEta[-1]) + ';' )
									txt.write('\n')	
								txt.close()

								ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
								ax.set_ylabel( 'Rate of transitions' , \
									fontsize=18 )
								ax.legend(fontsize=12)
								fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + \
									'/transcounts/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3VsEta_' + str(ti) + '_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
								#plt.show()
								plt.close(fig)

							for cap_M in cap_M_values:

								fig, ax = plt.subplots(figsize=(9,6))
								fig.gca().invert_xaxis()

								txtfile = './means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) \
									+ '/transcounts/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3aVsEta_' + str(ti) + '_M' + str(cap_M) + '.txt'
								txt = open( txtfile , 'w' )	

								for c1 in C:
									for c2 in C:

										ThreeStepMa_meansVsEta = [ np.mean([ TransCounts3a_all[d][mE][mT][cap_M][eta][trial][ti][at][c1][c2] for trial in trials ])/([ (tQ_all[d][mE][mT][cap_M][eta][trial] - 0) , (tf - tQ_all[d][mE][mT][cap_M][eta][trial]) ][ti]) for eta in eta_values ]
										ax.plot(eta_values,ThreeStepMa_meansVsEta,'o-',color=Colors[c1],linewidth=LineWidths_c2[c2],label=c1+'$\\to$M$\\to$'+c2)

										txt.write( str(c1) + '-' + str(c2) + ':' )
										for eta in eta_values[:-1]:
											txt.write( str(eta) + ',' )
										txt.write( str(eta_values[-1]) + ';' )
										for nc in ThreeStepMa_meansVsEta[:-1]:
											txt.write( str(nc) + ',' )
										txt.write( str(ThreeStepMa_meansVsEta[-1]) + ';' )
									txt.write('\n')	
								txt.close()

								ax.set_xlabel( 'Relative expected returns $\\eta$', fontsize=18 )
								ax.set_ylabel( 'Rate of transitions' , \
									fontsize=18 )
								ax.legend(fontsize=12)
								fig.savefig( './means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/' + str(ti) + \
									'/transcounts/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + addtag + '_TransCounts3aVsEta_' + str(ti) + '_M' + str(cap_M) + '.png' , bbox_inches='tight' , dpi = 300 )
								#plt.show()
								plt.close(fig)

			 	#----------------------------------------------------------

				MeanCurves = {}
				for d in d_values:
					MeanCurves[d] = {}
					for mE in mE_values:	
						MeanCurves[d][mE] = {}
						for mT in mT_values:
							MeanCurves[d][mE][mT] = {}		

							TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/crewsize/' )
							TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/crewsize/' )
							for cap_M in cap_M_values:

								TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/crewsize/capM' + str(cap_M) + '/' )
								TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o') + '/mE' + str(mE) + '/mT' + str(mT) + '/ALL/crewsize/capM' + str(cap_M) + '/' )

								MeanCurves[d][mE][mT][cap_M] = {}
								for eta in eta_values:
									MeanCurves[d][mE][mT][cap_M][eta] = {}

									txtfile = './means/' + experiment + \
										'/txt/d' + str(d).replace('.','o') +'/mE'+str(mE)+'/mT'+str(mT)+'/ALL/crewsize/capM'+str(cap_M)+'/' \
										+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanCrewSizeCurves_ALL_' + str(eta).replace('.','o') + '_M' + str(cap_M) + '.txt'
									txt = open( txtfile , 'w' )	

									for c in C:

										TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/ALL/crewsize/capM'+str(cap_M)+'/'+str(c))
										#TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/ALL/crewsize/cap_M'+str(cap_M)+'/'+str(c))

										fig, ax = plt.subplots(figsize=(9,6))
										curves = []

										for trial in trials:
											for curve in CrewSizeCurves_all[d][mE][mT][cap_M][eta][trial]['ALL'][0][c]:
												ax.plot( curve )
												curves.append(curve)

										MeanCurves[d][mE][mT][cap_M][eta][c] = \
											[ np.mean([ curve[t] for curve in curves if not np.isnan(curve[t]) ]) for t in range(tf) ]

										ax.plot( MeanCurves[d][mE][mT][cap_M][eta][c] , 'k', linewidth=3 )

										txt.write( c + ':' )
										for mc in MeanCurves[d][mE][mT][cap_M][eta][c][:-1]:
											txt.write( str(mc) + ',' )
										txt.write( str(MeanCurves[d][mE][mT][cap_M][eta][c][-1]) + '\n')

										ax.set_ylabel( 'Crew size $n$', fontsize=18 )
										ax.set_xlabel( 'Iterations since activation' , \
											fontsize=18 )
										ax.set_title( '$\\eta=$'+str(eta) + ", " + Labels[c] , fontsize=18 )
										#ax.legend(fontsize=12)
										fig.savefig( './means/' + experiment + \
											'/pic/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/ALL/crewsize/capM'+str(cap_M)+'/' + str(c) + '/' \
											+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanCrewSizeCurves_ALL_' + str(eta).replace('.','o') + '_M' + str(cap_M) + '_' + c + '.png' , bbox_inches='tight' , dpi = 300 )
										#plt.show()
										plt.close(fig)		

									txt.close()

				if Q0:
					for ti in [0,1]:
						TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/'+ str(ti) + '/crewsize/capM'+str(cap_M)+'/')
						TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/'+ str(ti) + '/crewsize/capM'+str(cap_M)+'/')
						# TryPath('./means/' + experiment + '/pic/crewsize/' + str(ti) + '/')
						# TryPath('./means/' + experiment + '/txt/crewsize/' + str(ti) + '/')
						MeanCurves = {}
						for d in d_values:
							MeanCurves[d] = {}
							for mE in mE_values:
								MeanCurves[d][mE] = {}
								for mT in mT_values:
									MeanCurves[d][mE][mT] = {}		
									for cap_M in cap_M_values:
										MeanCurves[d][mE][mT][cap_M] = {}
										for eta in eta_values:
											MeanCurves[d][mE][mT][cap_M][eta] = {}

											TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/' + str(ti) + '/crewsize/capM'+str(cap_M)+'/' )
											TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/' + str(ti) + '/crewsize/capM'+str(cap_M)+'/' )

											txtfile = './means/' + experiment + \
												'/txt/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/'+ str(ti) + '/crewsize/capM'+str(cap_M)+'/'\
												+ experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanCrewSizeCurves_' + str(ti) + '_' + str(eta).replace('.','o') + '_M' + str(cap_M) + '.txt'
											txt = open( txtfile , 'w' )	

											for c in C:

												TryPath('./means/' + experiment + '/pic/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/' + str(ti) + '/crewsize/capM'+str(cap_M)+'/' + str(c) + '/' )
												TryPath('./means/' + experiment + '/txt/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/' + str(ti) + '/crewsize/capM'+str(cap_M)+'/' + str(c) + '/' )

												fig, ax = plt.subplots(figsize=(9,6))
												curves = []

												for trial in trials:
													tQ = tQ_all[d][mE][mT][cap_M][eta][trial]
													t_intervals = [ (0,tQ) , (tQ,tf) ]
													t_int = t_intervals[ti]
													for ci,curve in enumerate(CrewSizeCurves_all[d][mE][mT][cap_M][eta][trial]['ALL'][0][c]):
														act = CrewSizeCurves_all[d][mE][mT][cap_M][eta][trial]['ALL'][1][c][ci]
														if ((act>=t_int[0]) and (act<t_int[1])):
															ax.plot( curve )
															curves.append(curve)
												MeanCurves[d][mE][mT][cap_M][eta][c] = \
													[ np.mean([ curve[t] for curve in curves if not np.isnan(curve[t]) ]) for t in range(tf) ]

												txt.write( c + ':' )
												for mc in MeanCurves[d][mE][mT][cap_M][eta][c][:-1]:
													txt.write( str(mc) + ',' )
												txt.write( str(MeanCurves[d][mE][mT][cap_M][eta][c][-1]) + '\n')

												ax.plot( MeanCurves[d][mE][mT][cap_M][eta][c] , 'k', linewidth=3 )
												ax.set_ylabel( 'Crew size $n$', fontsize=18 )
												ax.set_xlabel( 'Iterations since activation' , \
													fontsize=18 )
												ax.set_title( '$\\eta=$'+str(eta) + ", " + Labels[c] , fontsize=18 )
												#ax.legend(fontsize=12)
												fig.savefig( './means/' + experiment + \
													'/pic/d' + str(d).replace('.','o')+'/mE'+str(mE)+'/mT'+str(mT)+'/' + str(ti) + '/crewsize/capM'+str(cap_M)+'/'+ str(c) + '/' + experiment + '_' + str(d).replace('.','o') + '_' + str(mE) + '_' + str(mT) + '_MeanCrewSizeCurves_' + str(ti) + '_' + str(eta).replace('.','o') + '_M' + str(cap_M) + '_' + c + '.png' , bbox_inches='tight' , dpi = 300 )
												#plt.show()
												plt.close(fig)		
											txt.close()
