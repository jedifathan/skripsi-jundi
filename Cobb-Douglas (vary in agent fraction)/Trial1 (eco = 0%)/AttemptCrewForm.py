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
from GroupAff import GroupAffinity
from ProspGroupAff import ProspectiveGroupAffinity
from IntMov import intrinsic_motivation, pow_motive, aff_motive
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def AttemptCrewFormation(a, b, A, B, W0, Wc, d, mE, Recruitable,\
		ImplementSettings, ImplementCrewSizes_t,ImplementCrews,Gamma,\
				GroupReturn_series,ReturnsDistributions,\
					AgentAffiliations,K,RandomUpdate=False,AgentTypes=[]):

	# Seems like somehow the maxes are being exceeded.
	# Or else maybe that was just hangers-on to inacctive vessels.

	if AgentTypes:
		for at in AgentTypes.keys():
			if (a in AgentTypes[at]):
				agenttype = at

	#----------------------------------------------------------

	RemainingCrew = ImplementCrews[b]		# Do we add them to Prosp Crew later?
	Peers = [ (a1) for a1 in A \
		if (( a1!=a ) and not (a1 in RemainingCrew)) ]
	#random.shuffle( Peers )

	Weights0 = [ ( (1-d)*W0[a][a1]['weight'] \
					+ d*Wc[a][a1]['weight'] ) \
							for a1 in Peers ]
	sumWeights0 = np.sum(Weights0)
	Weights = [ ( w/sumWeights0 ) for w in Weights0 ]

	# Idea: Let Recruitable be randomly chosen from between n_0 and n_max. Could weight the lower ones more.

	# note: all affinity calculations should include the agent itself
	ProspectiveCrew = list(np.random.choice( Peers , \
		size=Recruitable-len(RemainingCrew) , \
			replace=False, p=Weights ))
	random.shuffle(ProspectiveCrew)
	#ProspectiveCrew.append(a)

	b_old = AgentAffiliations[a]
	Crew_old = ImplementCrews[b_old]
	G_old,E_old,T_old = GroupAffinity( a , b_old , GroupReturn_series[b_old] , \
				mE , ImplementCrewSizes_t[b_old], ImplementSettings, \
					Gamma, ReturnsDistributions , ImplementCrews[b_old] ,\
						W0 , Wc , d )
	G_new,E_new,T_new = ProspectiveGroupAffinity( a , b , ImplementSettings , Gamma , \
			ReturnsDistributions , ProspectiveCrew , W0 , Wc , d )

	
	DeltaGK = np.max([( G_new - G_old )/K,0.])		# max unnecessary because rand always po

	if (agenttype=='aff'):
		# P_trans = aff_motive(DeltaGK)
		P_trans = ((E_new**(0.5))*(T_new**(2-0.5)) - (E_old**(0.5))*(T_old**(2-0.5)))/K
	elif (agenttype=='pow'):
		# P_trans = pow_motive(DeltaGK)
		P_trans = ((E_new**(1.5))*(T_new**(2-1.5)) - (E_old**(1.5))*(T_old**(2-1.5)))/K
	else:
		P_trans = DeltaGK

	rand = random.random()
	if (( rand <= P_trans ) or (RandomUpdate)):
		InitialCrew = [ ( a , b_old ) ]								# DO WE ALSO ADD THE RUMP FACTION? I think in the current version, it waits to clear first
		if ( len(InitialCrew)<ImplementSettings[Gamma[b]][1] ):
			for a1 in ProspectiveCrew:

				for at in AgentTypes.keys():
					if a1 in AgentTypes[at]:
						agenttype1 = at

				b_old1 = AgentAffiliations[a1]
				G_old1,E_old1,T_old1 = GroupAffinity( a1 , b_old1 , GroupReturn_series[b_old1] , \
							mE , ImplementCrewSizes_t[b_old1], ImplementSettings, \
								Gamma, ReturnsDistributions , ImplementCrews[b_old1] ,\
									W0 , Wc , d )
				G_new1,E_new1,T_new1 = ProspectiveGroupAffinity( a1 , b_old1 , ImplementSettings , Gamma , \
						ReturnsDistributions , ProspectiveCrew+[a] , W0 , Wc , d )

				DeltaGK1 = np.max([( G_new1 - G_old1 )/K,0.])

				if (agenttype1=='aff'):
					# P_trans = aff_motive(DeltaGK1)
					P_trans = ((E_new1**(0.5))*(T_new1**(2-0.5)) - (E_old1**(0.5))*(T_old1**(2-0.5)))/K
				elif (agenttype1=='pow'):
					# P_trans = pow_motive(DeltaGK1)
					P_trans = ((E_new1**(1.5))*(T_new1**(2-1.5)) - (E_old1**(1.5))*(T_old1**(2-1.5)))/K
				else:
					P_trans = DeltaGK1

				rand = random.random()
				if ( rand <= P_trans ) and (len(InitialCrew)<ImplementSettings[Gamma[b]][1]):
					InitialCrew.append((a1,b_old1))

		n0 = ImplementSettings[Gamma[b]][0]
		if ( len(InitialCrew)>=n0 ):

			if ( Gamma[b]==Gamma[b_old] ):

				if ((len(set(Crew_old).intersection(set([ ab[0] for ab in InitialCrew])))<n0)):		# How does this work for same-type transitions, and different?

						# The criteria only matters in the case that it's the same type. 
						# Otherwise, as long as they have enough, they go for it.

					ActivateImplement = True
					Remove = [ a1 for a1 in RemainingCrew if (not (a1 in InitialCrew)) ]

				else:

					ActivateImplement = False
					Remove = []

			else:
				ActivateImplement = True
				Remove = [ a1 for a1 in RemainingCrew if (not (a1 in InitialCrew)) ]				
		else:
			ActivateImplement = False
			Remove = []

	else:
		ActivateImplement = False
		InitialCrew = []
		Remove = []

	#----------------------------------------------------------

	return ActivateImplement, InitialCrew, Remove