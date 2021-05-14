import matplotlib.pyplot as plt
import numpy as np

rng = np.random.RandomState(42)
data = rng.randint(0, 2, 20)

rule_number = 30
rule_string = np.binary_repr(rule_number, 8)
rule = np.array([int(bit) for bit in rule_string])

# for i in range(8):
#     triplet = np.binary_repr(i, 3)
#     print(f"input: {triplet}, index: {7 - i}, output: {rule[7 - i]}")


def rule_index(triplet):
    L, C, R = triplet
    index = 7 - (4 * L + 2 * C + R)
    return int(index)


# all_triplets = np.stack([np.roll(data, 1), data, np.roll(data, -1)])
# new_data = rule[np.apply_along_axis(rule_index, 0, all_triplets)]
# print(new_data)

def CA_run(initial_state, n_steps, rule_number):
    rule_string = np.binary_repr(rule_number, 8)
    rule = np.array([int(bit) for bit in rule_string])

    m_cells = len(initial_state)
    result = np.zeros((n_steps, m_cells))
    result[0, :] = initial_state

    for step in range(1, n_steps):
        all_triplets = np.stack(
            [
                np.roll(result[step - 1, :], 1),
                result[step - 1, :],
                np.roll(result[step - 1, :], -1),
            ]
        )
        result[step, :] = rule[np.apply_along_axis(
            rule_index, 0, all_triplets)]

    return result


# initial = np.array([0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
#                    0, 0, 0, 0, 1, 0, 1, 1, 1, 0])
# data = CA_run(initial, 10, 30)
# print(data)

plt.rcParams['image.cmap'] = 'binary'
rng = np.random.RandomState(0)
data = CA_run(rng.randint(0, 2, 300), 150, 30)
fig, ax = plt.subplots(figsize=(16, 9))
ax.matshow(data)
ax.axis(False)
