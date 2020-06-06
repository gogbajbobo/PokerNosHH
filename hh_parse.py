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

# %%
hh_data_dirname = 'hh_data'
files = [f for f in listdir(hh_data_dirname) if path.isfile(path.join(hh_data_dirname, f)) and f.endswith('.txt')]
files.sort()
for file in files:
    print(file)

# %%
flops = np.array([])

for filename in files:
    with open(path.join(hh_data_dirname, filename), 'r') as file:
        data = json.load(file)
        hh_data = np.asarray(data['Data'])
        hand_starts = np.core.defchararray.startswith(hh_data, 'Hand #')
        hand_indices = np.where(hand_starts == True)[0]
        hands = np.array_split(hh_data, hand_indices)
        for hand in hands:
            flop_line = np.core.defchararray.startswith(hand, '** Flop **')
            flop_string = hand[flop_line]
            flop_string = flop_string[0] if flop_string.size else ''
            flop = flop_string[flop_string.find('[')+1:flop_string.find(']')]
            flops = np.append(flops, flop) if len(flop) else flops

print(f'all flops: {flops.size}')

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
        
print(f'doubled flops: {len(doubled_flops)} — {100 * len(doubled_flops) / flops.size : .2f}%')
print(f'doubled flops calc: {100 * (3/51 + 6/50) : .2f}%')
print(f'tripled flops: {len(tripled_flops)} — {100 * len(tripled_flops) / flops.size : .2f}%')
print(f'tripled flops calc: {100 * (3/51 * 2/50) : .2f}%')
print(f'suited flops: {len(suited_flops)} — {100 * len(suited_flops) / flops.size : .2f}%')
print(f'suited flops calc: {100 * (12/51 * 11/50) : .2f}%')

# %%
print(tripled_flops)

# %%
