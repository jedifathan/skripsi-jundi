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

def RunEnsembleSimulationsB( experiment, M, \
	ImplementSettings, ResourceSettings, Pu, Pn, \
	mE_values, mT_values, d_values, eta_values , Chi, K , \
	p0_M, Ex_p_M_values, p1_M_values, \
					cap_M_values , Recruitable , tf, trials, \
						bawel ):

	#----------------------------------------------------------

	TryPath( './sim/' )
	TryPath( './sim/' + experiment )
	RecordEnsembleSettings(experiment, M, Pu, Pn, Recruitable, \
						tf, ImplementSettings, ResourceSettings)

	# Need to modify this to include static values in settings.

	#----------------------------------------------------------

	# Decide which to include as ranges and which as individual values.

	for d in d_values:
		for mE in mE_values:
			for mT in mT_values:
				for trial in trials:
					for eta in eta_values:
						for Ex_p_M in Ex_p_M_values:
							for p1_M in p1_M_values:
								OtherInputs = \
									{ 'p0_M':p0_M , \
									  'p1_M':p1_M , \
									  'Ex_p_M':Ex_p_M  }
								for cap_M in cap_M_values:

									caps = {'S':ImplementSettings['S'][2] , \
											'M':cap_M , \
										    'L':ImplementSettings['L'][2] }

									tag = GenerateTag( experiment , d , mE, mT , \
													eta , caps , OtherInputs )
									path = './sim/' + experiment + '/' + tag
									TryPath( path )
									simtag = path + '/' + tag + '_' \
										+ str(eta).replace('.','o') + '_' \
										+ str(p0_M).replace('.','o') + '_' \
										+ str(p1_M).replace('.','o') + '_' \
										+ str(Ex_p_M).replace('.','o') + '_' \
										+ str(trial)

									RunSimulation( simtag ,experiment, M , Pu , Pn , \
										d , mE, mT , eta , caps , trial, \
										ImplementSettings , ResourceSettings , \
											tf , Chi, K, Recruitable, OtherInputs, False, 0., bawel )

	#----------------------------------------------------------

	return []