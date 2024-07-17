import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Define the equations
def achievement_motivation(Ps_G, S_ach=1, M_ach_plus=0.4, M_ach_minus=0.6, p_ach=20):
    I_res_plus = S_ach / (1 + np.exp(p_ach * (M_ach_plus - Ps_G)))
    I_res_minus = (S_ach / (1 + np.exp(p_ach * (M_ach_minus - Ps_G)))) * 1
    return I_res_plus - I_res_minus  # Return the difference between approach and avoidance


def aff_motive(Ps_G, S_aff=1., M_aff_plus=0.07, M_aff_minus=0.02, p_aff=100, p_aff2=100):
    I_res_plus = S_aff / (1 + np.exp(p_aff * (Ps_G - M_aff_plus)))
    I_res_minus = (S_aff / (1 + np.exp(p_aff2 * (Ps_G - M_aff_minus)))) * 1
    return I_res_plus - I_res_minus  # Return the difference between approach and avoidance

def pow_motive(Ps_G, S_pow=1, M_pow_plus=0.07, M_pow_minus=0.9, p_pow=100):
    I_res_plus = S_pow / (1 + np.exp(p_pow * (M_pow_plus - Ps_G)))
    I_res_minus = 0#(S_pow / (1 + np.exp(p_pow * (M_pow_minus - Ps_G)))) * 1
    return I_res_plus - I_res_minus  # Return the difference between approach and avoidance

def intrinsic_motivation(Ps_G):
    profile1_motivated_agents = affiliation_motivation(Ps_G, S_aff=2, M_aff_plus=0.3, M_aff_minus=0.1, p_aff=20)
    profile2_motivated_agents = achievement_motivation(Ps_G, S_ach=2, M_ach_plus=0.4, M_ach_minus=0.6, p_ach=20)
    profile3_motivated_agents = power_motivation(Ps_G, S_pow=2, M_pow_plus=0.7, M_pow_minus=0.9, p_pow=20)
    return profile1_motivated_agents

# def aff_motive(Ps_G):
#     profile1_motivated_agents = affiliation_motivation(Ps_G, S_aff=1, M_aff_plus=0.3, M_aff_minus=0.1, p_aff=20)
#     return profile1_motivated_agents

# def ach_motive(Ps_G):
#     profile2_motivated_agents = achievement_motivation(Ps_G, S_ach=1, M_ach_plus=0.4, M_ach_minus=0.6, p_ach=20)
#     return profile2_motivated_agents

# def pow_motive(Ps_G):
#     profile3_motivated_agents = power_motivation(Ps_G, S_pow=1, M_pow_plus=0.7, M_pow_minus=0.9, p_pow=20)
#     return profile3_motivated_agents
