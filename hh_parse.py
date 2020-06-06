# -*- coding: utf-8 -*-
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
import json
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# %%
hh_data_dirname = 'hh_data'
files = [f for f in listdir(hh_data_dirname) if path.isfile(path.join(hh_data_dirname, f)) and f.endswith('.txt')]
files.sort()
for file in files:
    print(file)

# %%
flops = np.array([])
no_flop_count = 0

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
                flops = np.append(flops, flop) if len(flop) else flops
                no_flop_count += 1 if not len(flop) else 0

print(f'all hands: {flops.size + no_flop_count}')                
print(f'flops: {flops.size}')
print(f'no flop: {no_flop_count}')

# %%
doubled_flops = []
tripled_flops = []
suited_flops = []

for flop in flops:
    cards = flop.split()
    values = [card[0] for card in cards]
    suites = [card[1] for card in cards]
    if len(set(values)) == 2:
        doubled_flops.append(flop)
    if len(set(values)) == 1:
        tripled_flops.append(flop)
    if len(set(suites)) == 1:
        suited_flops.append(flop)
        
df_count = len(doubled_flops)
tf_count = len(tripled_flops)
sf_count = len(suited_flops)
        
print(f'doubled flops: {df_count} — {100 * df_count / flops.size : .2f}%')
print(f'doubled flops calc: {100 * (3/51 + 6/50) : .2f}%')
print(f'tripled flops: {tf_count} — {100 * tf_count / flops.size : .2f}%')
print(f'tripled flops calc: {100 * (3/51 * 2/50) : .2f}%')
print(f'suited flops: {sf_count} — {100 * sf_count / flops.size : .2f}%')
print(f'suited flops calc: {100 * (12/51 * 11/50) : .2f}%')

# %%
tripled_flops.sort()
print(tripled_flops)

# %%
df_values = []
for flop in doubled_flops:
    cards = flop.split()
    values = [card[0] for card in cards]
    values.sort()
    values = ''.join(values)
    df_values.append(values)

df_values.sort()

unique_elements, counts_elements = np.unique(df_values, return_counts=True)

# %%
x = [x for _, x in sorted(zip(counts_elements, unique_elements))]
y = sorted(counts_elements)

plt.figure(figsize=(50, 10))
plt.xticks(rotation=90)
plt.bar(x, y)

# %%
df_values_short = []

for hand in df_values:
    short = Counter(hand)
    for key, value in short.items():
        if value == 2:
            df_values_short.append(key)

df_values_short = [f'{v}{v}x' for v in df_values_short]
unique_elements, counts_elements = np.unique(df_values_short, return_counts=True)

# %%
x = [x for _, x in sorted(zip(counts_elements, unique_elements))]
y = sorted(counts_elements)

plt.figure(figsize=(20, 5))
plt.xticks(rotation=90)
plt.bar(x, y)

# %%
sf_suites = []
for flop in suited_flops:
    cards = flop.split()
    suite = cards[0][1]
    sf_suites.append(suite)

sf_suites.sort()

unique_elements, counts_elements = np.unique(sf_suites, return_counts=True)
print(unique_elements, counts_elements)

# %%
plt.figure(figsize=(10, 5))
plt.bar(unique_elements, counts_elements)

# %%
