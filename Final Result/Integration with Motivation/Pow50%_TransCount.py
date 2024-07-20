import matplotlib.pyplot as plt
import numpy as np

# Updated data for affinity
data_aff = {
    'L-L': 0.003,
    'L-M': 0.015583333333333333,
    'L-S': 0.07866666666666668,
    'M-L': 0.0025,
    'M-M': 0.5293333333333333,
    'M-S': 1.6345,
    'S-L': 0.008416666666666666,
    'S-M': 1.6415,
    'S-S': 1.78925
}

# Updated data for power
data_pow = {
    'L-L': 0.002333333333333333,
    'L-M': 0.044333333333333336,
    'L-S': 0.04875,
    'M-L': 0.008,
    'M-M': 0.5888333333333333,
    'M-S': 0.5018333333333334,
    'S-L': 0.00175,
    'S-M': 0.4776666666666667,
    'S-S': 0.074
}

# Organize data
initial_states = ['L', 'M', 'S']
final_states = ['L', 'M', 'S']
colors = {'L': '#1f77b4', 'M': '#ff7f0e', 'S': '#2ca02c'}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

y_pos = np.arange(len(data_aff))
bar_height = 0.8

# Function to plot data
def plot_data(ax, data, title):
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
    ax.set_title(title)

    # Create a custom legend
    custom_lines = [plt.Line2D([0], [0], color=color, lw=4) for color in colors.values()]
    ax.legend(custom_lines, colors.keys(), title='Final State', loc='center left', bbox_to_anchor=(1, 0.5))

# Plot affinity data
plot_data(ax1, data_aff, 'Affinity')

# Plot power data
plot_data(ax2, data_pow, 'Power')

plt.tight_layout()
plt.savefig('Aff_Pow_TransCount_Comparison.png')
plt.show()