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
from GenAgenAndImp import GenerateAgentsAndImplements
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def CrewSizeVsTimeCurves( ImplementCrewSizes_t , M, \
	ImplementSettings, tf, bawel=False ):

	#----------------------------------------------------------

	_,B,C,Gamma,_ = \
		GenerateAgentsAndImplements( M, ImplementSettings )

	Curves = { c:[] for c in C }
	ActTimes = { c:[] for c in C }
	Finished = { c:[] for c in C }
	TimeActive = { c:[] for c in C }
	TimeToClear = { c:[] for c in C }

	for b in B:

		act = []
		if (ImplementCrewSizes_t[b][0]>=ImplementSettings[Gamma[b]][0]):
			act = [0]
		act += [ t for t in range(1,tf) \
				if ((ImplementCrewSizes_t[b][t]>=ImplementSettings[Gamma[b]][0]) \
					and (ImplementCrewSizes_t[b][t-1]<ImplementSettings[Gamma[b]][0])) ]

		if act:
			for at in act:
				curve0 = ImplementCrewSizes_t[b][at:]
				deactivate = [ ti for ti,n in enumerate(curve0) \
					if (n<ImplementSettings[Gamma[b]][0]) ]
				clear = [ ti for ti,n in enumerate(curve0) if (n==0) ]
				if clear:
					curve = curve0[:clear[0]] + [ 0 for x in range(tf-clear[0]) ]
					finished = 1
				else:
					curve = curve0 + [ np.nan for x in range(tf-len(curve0)) ]
					finished = 0

				Curves[Gamma[b]].append(curve)
				ActTimes[Gamma[b]].append(at)
				Finished[Gamma[b]].append(finished)
				if deactivate:
					TimeActive[Gamma[b]].append(deactivate[0])
				else:
					TimeActive[Gamma[b]].append(np.nan)
				if clear:
					TimeToClear[Gamma[b]].append(clear[0])
				else:
					TimeToClear[Gamma[b]].append(np.nan)

	#----------------------------------------------------------	

	return Curves, ActTimes, Finished, TimeActive, TimeToClear