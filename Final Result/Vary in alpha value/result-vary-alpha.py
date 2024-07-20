import matplotlib.pyplot as plt

# Updated data
data = {
    "0": {
        "Large-group": ([0.5, 0.75, 1, 1.25, 1.5], [0.35103375, 0.3056808333333334, 0.28247791666666666, 0.32030708333333335, 0.4363041666666667]),
        #"Medium-group": ([0.5, 0.75, 1, 1.25, 1.5], [0.0, 0.0, 0.0, 0.0, 0.0]),
        "Solitary/Small-group": ([0.5, 0.75, 1, 1.25, 1.5], [0.64896625, 0.6943191666666668, 0.7175220833333333, 0.6796929166666668, 0.5636958333333333])
    },
    "20": {
        "Large-group": ([0.5, 0.75, 1, 1.25, 1.5], [0.3204520833333333, 0.24833374999999996, 0.17306624999999998, 0.10749708333333334, 0.05812708333333333]),
        "Medium-group": ([0.5, 0.75, 1, 1.25, 1.5], [0.025872083333333334, 0.07436208333333333, 0.15318708333333333, 0.24820041666666667, 0.33535916666666665]),
        "Solitary/Small-group": ([0.5, 0.75, 1, 1.25, 1.5], [0.6536758333333332, 0.677304166666666, 0.6737466666666667, 0.6443024999999999, 0.6065137500000001])
    }
}

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
data_keys = ["0", "20"]
colors = {'Large-group': 'blue', 'Medium-group': 'orange', 'Solitary/Small-group': 'green'}

for ax, key in zip(axes, data_keys):
    for subgroup, (x, y) in data[key].items():
        ax.plot(x, y, 'o-', color=colors[subgroup], label=f'{subgroup} ({key})')
    ax.set_xlabel('Alpha Value of Agent')
    ax.set_ylabel('Fraction of affiliated agents $N_c$')
    ax.legend()
    # ax.set_title(f'Number of Johnson Boat : {key}')
    ax.set_xticks([0.5, 0.75, 1, 1.25, 1.5])

plt.tight_layout()
plt.savefig('Vary_in_Alpha_Value.png')
plt.show()
