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
from os import path
import json
import numpy as np

# %%
hh_data_dirname = 'hh_data'
filename = '2020-05-07-Ring Game #02.txt'
with open(path.join(hh_data_dirname, filename), 'r') as file:
    data = json.load(file)
    hh_data = np.asarray(data['Data'])
    hand_starts = np.core.defchararray.startswith(hh_data, 'Hand #')
    hand_indices = np.where(hand_starts == True)[0]
    hands = np.array_split(hh_data, hand_indices)
    flops = np.array([])
    for hand in hands:
        flop_line = np.core.defchararray.startswith(hand, '** Flop **')
        flop_string = hand[flop_line]
        flop_string = flop_string[0] if flop_string.size else ''
        flop = flop_string[flop_string.find('[')+1:flop_string.find(']')]
        flops = np.append(flops, flop) if len(flop) else flops
    print(flops)

# %%
