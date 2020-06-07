# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
from os import path
from os import listdir
import numpy as np
import json
import matplotlib.pyplot as plt

# %%
hh_data_dirname = 'hh_data'
files = [f for f in listdir(hh_data_dirname) if path.isfile(path.join(hh_data_dirname, f)) and f.endswith('.txt')]
files.sort()
for file in files:
    print(file)

# %%
flops = np.array([])
hands_count = 0

for filename in files:
    with open(path.join(hh_data_dirname, filename), 'r') as file:
        data = json.load(file)
        hh_data = np.asarray(data['Data'])
        hand_starts = np.core.defchararray.startswith(hh_data, 'Hand #')
        hand_indices = np.where(hand_starts == True)[0]
        hands = np.array_split(hh_data, hand_indices)
        for hand in hands:
            if hand.size:
                flop_line = np.core.defchararray.startswith(hand, '** Flop **')
                flop_string = hand[flop_line]
                flop_string = flop_string[0] if flop_string.size else ''
                flop = flop_string[flop_string.find('[')+1:flop_string.find(']')]
                if len(flop):
                    flops = np.append(flops, flop)
                hands_count += 1

print(f'all hands: {hands_count}')                
print(f'flops: {flops.size}')

# %%
card_values = np.array([])
card_suites = np.array([])

for flop in flops:
    cards = flop.split()
    values = [card[0] for card in cards]
    suites = [card[1] for card in cards]
    card_values = np.append(card_values, values)
    card_suites = np.append(card_suites, suites)

# %%
unique_elements, counts_elements = np.unique(card_values, return_counts=True)
print(f'mean: {np.mean(counts_elements) : .2f}, std: {np.std(counts_elements) : .2f}')

# %%
x = [x for _, x in sorted(zip(counts_elements, unique_elements))]
y = sorted(counts_elements)

print(x)
print(y)

plt.figure(figsize=(20, 10))
plt.bar(x, y)

# %%
unique_elements, counts_elements = np.unique(card_suites, return_counts=True)
print(f'mean: {np.mean(counts_elements) : .2f}, std: {np.std(counts_elements) : .2f}')

# %%
x = [x for _, x in sorted(zip(counts_elements, unique_elements))]
y = sorted(counts_elements)

print(x)
print(y)


plt.figure(figsize=(20, 10))
plt.bar(x, y)

# %%
