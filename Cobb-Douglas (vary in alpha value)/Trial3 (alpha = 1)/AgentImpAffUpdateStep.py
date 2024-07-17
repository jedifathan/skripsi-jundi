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
from AttemptCrewForm import AttemptCrewFormation
from IntMov import intrinsic_motivation, pow_motive, aff_motive
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

# Updates agent affiliations with implements, handling both rational and random updating decisions.
def AgentImplementAffiliationUpdateStep( A , Pu , Pn , B , B_c , d , mE, caps, \
		AgentAffiliations , ImplementCrews , ImplementCrewSizes_t , Gamma , \
		ImplementSettings , GroupReturn_series , W0 , Wc , K , Recruitable , \
				ReturnsDistributions , AgentTypes=[] ):

	#----------------------------------------------------------

	# Randomly select agents to consider updating

	Random = [ random.random() for a in A ]
	RationalUpdateCandidates = \
		[ A[ri] for ri,r in enumerate(Random) if ( r<Pu ) ]
	RandomUpdateCandidates = \
		[ A[ri] for ri,r in enumerate(Random) \
			if (( r>=Pu ) and ( r<(Pu+Pn) )) ]
	ProspectiveUpdaters = \
		RationalUpdateCandidates + RandomUpdateCandidates
	random.shuffle(ProspectiveUpdaters)

	JoinedNewCrew = []
	C = B_c.keys()
	Joined = { c:0 for c in C }
	Left = { c:0 for c in C }
	Activated = { c:0 for c in C }
	# Deactivated = { c:0 for c in C }

	ProspectiveImplements = { a:(random.choices( list(set(B)-set(AgentAffiliations[a])) )[0]) \
		for a in ProspectiveUpdaters }

	for a in ProspectiveUpdaters:

		if not a in JoinedNewCrew:

			b_old = AgentAffiliations[a]
			b_new = ProspectiveImplements[a]

			if ( np.sum([ int(len(ImplementCrews[bc])>=ImplementSettings[Gamma[b_new]][0]) for bc in B_c[Gamma[b_new]] ]) < caps[Gamma[b_new]] ):	# If the imposed cap hasn't yet been reached

				if ( len(ImplementCrews[b_new]) >= ImplementSettings[Gamma[b_new]][0] ):

					if ( len(ImplementCrews[b_new]) < ImplementSettings[Gamma[b_new]][1] ):	# If the maximum group size hasn't been reached

						if ( a in RationalUpdateCandidates ):

							G_old, E_old, T_old = GroupAffinity( a , b_old , GroupReturn_series[b_old] , \
									mE , ImplementCrewSizes_t[b_old], ImplementSettings, \
										Gamma, ReturnsDistributions , ImplementCrews[b_old] ,\
											W0 , Wc , d )
							G_new, E_new, T_new = GroupAffinity( a , b_new , GroupReturn_series[b_new] , \
									mE , ImplementCrewSizes_t[b_new], ImplementSettings, \
										Gamma, ReturnsDistributions , ImplementCrews[b_new] ,\
											W0 , Wc , d )

							# plt.plot(np.linspace(-1,1,10),[pow_motive(x) for x in np.linspace(-1,1,10)])
							# print('power',[pow_motive(x) for x in np.linspace(-1,1,10)])
							# print('affil',[aff_motive(x) for x in np.linspace(-1,1,10)])
							
							# plt.show()

							if AgentTypes:

								for at in AgentTypes.keys():
									if (a in AgentTypes[at]):
										agenttype = at

								DeltaGK = np.max([(G_new-G_old)/K,0.])

								if (agenttype=='pow'): 
									# affinity = pow_motive(DeltaGK)
									affinity = ((E_new**(1))*(T_new**(2-1)) - (E_old**(1))*(T_old**(2-1)))/K
								elif (agenttype=='aff'):
									affinity = aff_motive(DeltaGK)
							else:
								affinity = DeltaGK

							P_trans = affinity
							rand = random.random()
							# print("rand = ", rand)
							# print("P_trans = ", P_trans)

							# if agenttype=='pow':
							# 	print('POWER: ',a,DeltaGK,affinity)
							# elif agenttype=='aff':
							# 	print('AFFIL: ',a,DeltaGK,affinity)

							if ( rand <= P_trans ):

								AgentAffiliations[a] = b_new
								ImplementCrews[b_old].remove( a )
								ImplementCrews[b_new].append( a )	
								Left[Gamma[b_old]] += 1			
								Joined[Gamma[b_new]] += 1

								# if agenttype=='pow':
								# 	print('POWER made a move: ',a,DeltaGK,affinity)
								# elif agenttype=='aff':
								# 	print('AFFIL made a move: ',a,DeltaGK,affinity)

						elif ( a in RandomUpdateCandidates ):

							if ( len(ImplementCrews[b_new]) <= ImplementSettings[Gamma[b_new]][0] ):		# need to make sure this is updating this each time so that there won't be conflict from current round (e.g. 2 join at same time and exceed limit). it's firstcome firstserve, but they are shuffled

								AgentAffiliations[a] = b_new
								ImplementCrews[b_old].remove( a )
								ImplementCrews[b_new].append( a )
								Left[Gamma[b_old]] += 1			
								Joined[Gamma[b_new]] += 1

				else:	# If the prosp implement is inactive (though remember it might still have some crew; alternatively, only do this with unmanned implements. However this leaves one case unaddressed (inactive but manned imp.). Although if you just above condition the other thing to unmanned vessels, people CAN join ailing ships, but probably won't.

					if ( a in RationalUpdateCandidates ):

						ActivateImplement, InitialCrew, Remove = AttemptCrewFormation( a , b_new , A , B , \
								W0 , Wc , d , mE, Recruitable , ImplementSettings , ImplementCrewSizes_t , \
									ImplementCrews , Gamma, GroupReturn_series, ReturnsDistributions, AgentAffiliations , K , False , AgentTypes )		# This will apply to S implements, so check that it's operating properly

						# also if an agent joins a crew, remove it from the running for other updates
					elif ( a in RandomUpdateCandidates ):

						ActivateImplement, InitialCrew, Remove = AttemptCrewFormation( a , b_new , A , B , \
								W0 , Wc , d , mE, Recruitable , ImplementSettings , ImplementCrewSizes_t , \
									ImplementCrews , Gamma, GroupReturn_series, ReturnsDistributions, AgentAffiliations , K , True , AgentTypes )		# This will apply to S implements, so check that it's operating properly

					if ActivateImplement:
						Activated[Gamma[b_new]] += 1
						# print(b_new,"activated")
						# print(Gamma[b_new],InitialCrew)
						# plt.show()

						for ab in InitialCrew:
							AgentAffiliations[ab[0]] = b_new
							ImplementCrews[ab[1]].remove(ab[0])
							ImplementCrews[b_new].append(ab[0])
							JoinedNewCrew.append(ab[0])
							Left[Gamma[ab[1]]] += 1			
							Joined[Gamma[b_new]] += 1

						for a1 in Remove:		# but where do they go? make them random updaters? without updating, they'll still be on the crew
							[]

	#----------------------------------------------------------

	return AgentAffiliations, ImplementCrews, \
									Joined, Left, Activated