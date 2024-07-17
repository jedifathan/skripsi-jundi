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
from RecEnsSet import RecordEnsembleSettings
from GenTag import GenerateTag
from RunSim import RunSimulation
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def RunEnsembleSimulationsA( experiment, M, \
	ImplementSettings, ResourceSettings, Pu, Pn, \
	mE_values, mT_values, d_values, eta_values , Chi , K , \
					cap_M_values , Recruitable , tf, trials ,\
						bawel , FracTypes = [] ):

	#----------------------------------------------------------

	TryPath( './sim/' )
	TryPath( './sim/' + experiment )
	RecordEnsembleSettings(experiment, M, Pu, Pn, Recruitable, \
						tf, ImplementSettings, ResourceSettings)

	#----------------------------------------------------------

	for d in d_values:
		for mE in mE_values:
			for mT in mT_values:
				for trial in trials:
					for eta in eta_values:
						for cap_M in cap_M_values:

							caps = {'S':ImplementSettings['S'][2] , \
									'M':cap_M , \
								    'L':ImplementSettings['L'][2] }

							tag = GenerateTag( experiment , d , mE, mT , eta , caps )
							path = './sim/' + experiment + '/' + tag
							TryPath( path )
							simtag = path + '/' + tag + '_' \
								+ str(eta).replace('.','o') + '_' + str(trial)

							if not os.path.isfile(simtag + '_AffilUpdates.txt'):

								RunSimulation( simtag, experiment, M , Pu , Pn , \
									d , mE, mT , eta , caps , trial, \
									ImplementSettings , ResourceSettings , \
										tf, Chi , K, Recruitable, [], False, 0., bawel , FracTypes )

							else:
								print("Already done.",simtag)

	#----------------------------------------------------------

	return []