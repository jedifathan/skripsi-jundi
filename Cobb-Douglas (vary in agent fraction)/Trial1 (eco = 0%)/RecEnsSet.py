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

###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def RecordEnsembleSettings( experiment, M, Pu, Pn, Recruitable, tf, \
						ImplementSettings, ResourceSettings ):

	settingspath = './sim/' + experiment + '/' + experiment \
		+ '_settings.txt'
	expsettingstxt = open( settingspath , 'w' )
	expsettingstxt.write( 'M:' + str(M) + '\n' )
	expsettingstxt.write( 'Pu:' + str(Pu) + '\n' )
	expsettingstxt.write( 'Pn:' + str(Pn) + '\n' )
	expsettingstxt.write( 'Recruitable:' + str(Recruitable) \
		+ '\n' )
	expsettingstxt.write( 'tf:' + str(tf) + '\n' )
	expsettingstxt.write( 'ImplementSettings:' + '\n' )
	for c in ImplementSettings.keys():
		expsettingstxt.write( c + ':' + \
			str(ImplementSettings[c]) + '\n' )
	expsettingstxt.write( 'ResourceSettings:' + '\n' )
	for c in ResourceSettings.keys():
		expsettingstxt.write( c + ':' \
			+ str(ResourceSettings[c]) + '\n' )
	expsettingstxt.close()