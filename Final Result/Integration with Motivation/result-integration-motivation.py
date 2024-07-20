import matplotlib.pyplot as plt

data = {
    "0": {
        "Large-group": ([0, 25, 50, 75, 100], [0.017495, 0.040350833333333336, 0.03062041666666667, 0.0373525, 0.05252541666666668]),
        # "Medium-group": ([0, 25, 50, 75, 100], [0.0, 0.0, 0.0, 0.0, 0.0]),
        "Solitary/Small-group": ([0, 25, 50, 75, 100], [0.9825049999999999, 0.9596491666666667, 0.9693795833333333, 0.9626475000000001, 0.9474745833333335])
    },
    "20": {
        "Large-group": ([0, 25, 50, 75, 100], [0.013519999999999999, 0.016451249999999997, 0.01725583333333333, 0.028698333333333333, 0.05094083333333334]),
        "Medium-group": ([0, 25, 50, 75, 100], [0.2869183333333333, 0.30639250000000007, 0.28315500000000005, 0.22351291666666667, 0.14437208333333335]),
        "Solitary/Small-group": ([0, 25, 50, 75, 100], [0.6995616666666667, 0.6771562499999999, 0.6995891666666668, 0.74778875, 0.8046870833333334])
    }
}

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
data_keys = ["0", "20"]

colors = {'Large-group': 'blue', 'Medium-group': 'orange', 'Solitary/Small-group': 'green'}

for ax, key in zip(axes, data_keys):
    for subgroup, (x, y) in data[key].items():
        ax.plot(x, y, 'o-', color=colors[subgroup], label=f'{subgroup} ({key})')
    
    ax.set_xlabel('Percentage of Agents with Power Motivation vs Affiliation Motivation')
    ax.set_ylabel('Fraction of affiliated agents $N_c$')
    ax.legend()
    # ax.set_title(f'Number of Johnson Boat : {key}')
    ax.set_xticks([0, 25, 50, 75, 100])

plt.tight_layout()
plt.savefig('integration_motivation.png')
plt.show()