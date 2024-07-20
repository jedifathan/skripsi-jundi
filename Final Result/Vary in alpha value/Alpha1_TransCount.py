import matplotlib.pyplot as plt
import numpy as np

# Updated data
data = {
    'L-L': 0.0021666666666666666,
    'L-M': 0.04658333333333333,
    'L-S': 0.1225,
    'M-L': 0.00025,
    'M-M': 0.003916666666666666,
    'M-S': 0.03925,
    'S-L': 0.0022500000000000003,
    'S-M': 0.015166666666666667,
    'S-S': 0.05966666666666666
}

# Organize data
initial_states = ['L', 'M', 'S']
final_states = ['L', 'M', 'S']
colors = {'L': '#1f77b4', 'M': '#ff7f0e', 'S': '#2ca02c'}

fig, ax = plt.subplots(figsize=(12, 8))

y_pos = np.arange(len(data))
bar_height = 0.8

for i, initial in enumerate(initial_states):
    group_data = [data[f'{initial}-{final}'] for final in final_states]
    group_colors = [colors[final] for final in final_states]
    
    ax.barh(y_pos[i*3:(i+1)*3], group_data, bar_height, 
            color=group_colors, align='center', label=initial)
    
    for j, value in enumerate(group_data):
        ax.text(value, y_pos[i*3+j], f'{value:.6f}', 
                va='center', ha='left', fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels([f'{i}-{f}' for i in initial_states for f in final_states])
ax.invert_yaxis()

ax.set_xlabel('Rate of transitions')

# Create a custom legend
custom_lines = [plt.Line2D([0], [0], color=color, lw=4) for color in colors.values()]
ax.legend(custom_lines, colors.keys(), title='Final State', loc='center left', bbox_to_anchor=(1, 0.5))

plt.tight_layout()
plt.savefig('Alpha1_TransCount.png')
plt.show()