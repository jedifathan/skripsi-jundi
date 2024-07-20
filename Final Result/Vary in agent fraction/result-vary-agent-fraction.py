import matplotlib.pyplot as plt

data = {
    "0": {
        "Large-group": ([0, 25, 50, 75, 100], [0.3559379166666667, 0.37949, 0.3932941666666666, 0.4046945833333333, 0.4366470833333333]),
        # "Medium-group": ([0, 25, 50, 75, 100], [0.0, 0.0, 0.0, 0.0, 0.0]),
        "Solitary/Small-group": ([0, 25, 50, 75, 100], [0.6440620833333333, 0.62051, 0.6067058333333334, 0.5953054166666667, 0.5633529166666666])
    },
    "20": {
        "Large-group": ([0, 25, 50, 75, 100], [0.30255208333333333, 0.2776125, 0.16925249999999997, 0.09895458333333335, 0.06026708333333333]),
        "Medium-group": ([0, 25, 50, 75, 100], [0.023083333333333334, 0.06436499999999999, 0.16387625, 0.2461658333333333, 0.3285425]),
        "Solitary/Small-group": ([0, 25, 50, 75, 100], [0.6743645833333334, 0.6580224999999998, 0.6668712499999999, 0.6548795833333334, 0.6111904166666666])
    }
}

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
data_keys = ["0", "20"]

colors = {'Large-group': 'blue', 'Medium-group': 'orange', 'Solitary/Small-group': 'green'}

for ax, key in zip(axes, data_keys):
    for subgroup, (x, y) in data[key].items():
        ax.plot(x, y, 'o-', color=colors[subgroup], label=f'{subgroup} ({key})')
    
    ax.set_xlabel('Percentage of Agents with Higher Weight on Ecological Factor vs Trust Factor')
    ax.set_ylabel('Fraction of affiliated agents $N_c$')
    ax.legend()
    # ax.set_title(f'Number of Johnson Boat : {key}')
    ax.set_xticks([0, 25, 50, 75, 100])

plt.tight_layout()
plt.savefig('vary_agent_fraction.png')
plt.show()