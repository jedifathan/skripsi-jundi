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
from GenRetAvail import GenerateReturnsAvailable
from RetExt import ReturnsExtracted
from UpdateCoopComp import UpdateCooperativeComponent
from ResCondUpdate import ResourceConditionsUpdate
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def ResourceAppropriationStep( ReturnsDistributions , B, C, Gamma , B_c, \
		Chi , ImplementCrews , ImplementSettings , ResourceSettings , AgentAffiliations , \
			Wc , mT , DynamicResources , k ):

	#----------------------------------------------------------

	# Returns extracted by implement : ------------------------

	p_b_t = GenerateReturnsAvailable( ReturnsDistributions , \
											B , Gamma )
	GroupReturn = ReturnsExtracted( p_b_t , Chi , \
			ImplementCrews , ImplementSettings , B , Gamma )

	# Update cooperative component of network : ---------------

	Wc = UpdateCooperativeComponent( Wc , AgentAffiliations , mT )

	# Update resource conditions (where applicable) : ---------

	if DynamicResources:

		ReturnsDistributions = \
			ResourceConditionsUpdate( C, B_c, ResourceSettings , \
				ReturnsDistributions , ImplementCrews , Chi , k )

	#----------------------------------------------------------

	return GroupReturn, Wc, ReturnsDistributions