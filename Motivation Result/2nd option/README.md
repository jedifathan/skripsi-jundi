We try to use the motivation calculation as : 
```python
P_trans = intrinsic_motivation(( G_new - G_old )/K)
```
The difference between sigmoid and profile is how to get the sum of the P_trans

The motivation calculation it self is like this : 
```python
def achievement_motivation(Ps_G, S_ach=1, M_ach_plus=0.4, M_ach_minus=0.6, p_ach=20):
    I_res_plus = S_ach / (1 + np.exp(p_ach * (M_ach_plus - Ps_G)))
    I_res_minus = (S_ach / (1 + np.exp(p_ach * (M_ach_minus - Ps_G)))) * 1
    return I_res_plus - I_res_minus  # Return the difference between approach and avoidance

def affiliation_motivation(Ps_G, S_aff=1, M_aff_plus=0.3, M_aff_minus=0.1, p_aff=20):
    I_res_plus = S_aff / (1 + np.exp(p_aff * (Ps_G - M_aff_plus)))
    I_res_minus = (S_aff / (1 + np.exp(p_aff * (Ps_G - M_aff_minus)))) * 1
    return I_res_plus - I_res_minus  # Return the difference between approach and avoidance

def power_motivation(Ps_G, S_pow=1, M_pow_plus=0.6, M_pow_minus=0.9, p_pow=20):
    I_res_plus = S_pow / (1 + np.exp(p_pow * (M_pow_plus - Ps_G)))
    I_res_minus = (S_pow / (1 + np.exp(p_pow * (M_pow_minus - Ps_G)))) * 1
    return I_res_plus - I_res_minus  # Return the difference between approach and avoidance
```
- Sigmoid : we just use it straight away
```python
def intrinsic_motivation(Ps_G):
    profile1_motivated_agents = affiliation_motivation(Ps_G, S_aff=2, M_aff_plus=0.3, M_aff_minus=0.1, p_aff=20)
    profile3_motivated_agents = power_motivation(Ps_G, S_pow=2, M_pow_plus=0.7, M_pow_minus=0.9, p_pow=20)
    return profile1_motivated_agents
```

- Profile : we sum each motivation and adjust the weight of each motivation according to the profile that was defined at the beginning
```python3
def intrinsic_motivation(Ps_G):
    profile1_motivated_agents = [affiliation_motivation(Ps_G, S_aff=2, M_aff_plus=0.3, M_aff_minus=0.1, p_aff=20) +
                              power_motivation(Ps_G, S_pow=1, M_pow_plus=0.7, M_pow_minus=0.9, p_pow=20) +
                              achievement_motivation(Ps_G, S_ach=0.8, M_ach_plus=0.4, M_ach_minus=0.6, p_ach=20)]
    profile3_motivated_agents = [achievement_motivation(Ps_G, S_ach=1.5, M_ach_plus=0.4, M_ach_minus=0.6, p_ach=20) +
                              affiliation_motivation(Ps_G, S_aff=1, M_aff_plus=0.3, M_aff_minus=0.1, p_aff=20) +
                              power_motivation(Ps_G, S_pow=2, M_pow_plus=0.7, M_pow_minus=0.9, p_pow=20)]
    return profile1_motivated_agents[0]
```
