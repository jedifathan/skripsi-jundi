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
from EcoFact import EcologicalFactor
from TrustFact import TrustFactor
from IntMov import intrinsic_motivation
###############################################################
#					AUXILIARY FUNCTIONS :
#		 ( reorganize by theme/functionality later)
#--------------------------------------------------------------

def GroupAffinity(a, b, GroupReturn_series_b, mE, 
                  ImplementCrewSize_t_b, ImplementSettings, Gamma, 
                  ReturnsDistributions, ImplementCrew_b, W0, Wc, d):
    # print("a:", a) # refer to the agent (using ID)
    # print("b:", b) # refer to the implement of the agent
    # print("GroupReturn_series_b:", GroupReturn_series_b) 
    # print("mE:", mE) # refer to the ecological memory 
    # print("ImplementCrewSize_t_b:", ImplementCrewSize_t_b) 
    # print("ImplementSettings:", ImplementSettings) # refer to the setup of the implement
    # print("Gamma:", Gamma) 
    # print("ReturnsDistributions:", ReturnsDistributions) 
    # print("ImplementCrew_b:", ImplementCrew_b) # refer to the agent that are in the same implement
    # print("W0:", W0) # refer to exogenous component
    # print("Wc:", Wc) # refer to cooperative component
    # print("d:", d) # refer to the relative weight of the cooperative component
    # print()
    
    #----------------------------------------------------------

    EcologicalFactor_a_b = EcologicalFactor(b, GroupReturn_series_b, 
                                            mE, ImplementCrewSize_t_b, 
                                            ImplementSettings, Gamma, ReturnsDistributions)

    TrustFactor_a_b = TrustFactor(a, list(set(ImplementCrew_b + [a])), W0, Wc, d)
    # note, this always includes the agent itself (once)
    # Exponen = random.choice([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]) 
    # Exponen = 0

    # G = (EcologicalFactor_a_b**Exponen)*(TrustFactor_a_b**(2-Exponen))
    G = EcologicalFactor_a_b * TrustFactor_a_b

    # print(f"Eco : {EcologicalFactor_a_b}, Trust : {TrustFactor_a_b}, GroupAff : {G}")
    #----------------------------------------------------------

    return G, EcologicalFactor_a_b, TrustFactor_a_b