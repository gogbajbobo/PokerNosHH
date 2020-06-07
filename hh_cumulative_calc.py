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
def get_flop_textures(flop):

    doubled_flop = 0
    tripled_flop = 0
    suited_flop = 0

    cards = flop.split()
    values = [card[0] for card in cards]
    suites = [card[1] for card in cards]
    if len(set(values)) == 2:
        doubled_flop = 1
    if len(set(values)) == 1:
        tripled_flop = 1
    if len(set(suites)) == 1:
        suited_flop = 1

    return doubled_flop, tripled_flop, suited_flop


# %%
flops = np.array([])
hands_count = 0
df_cummulative_count = [0]
tf_cummulative_count = [0]
sf_cummulative_count = [0]

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
                    doubled_flop, tripled_flop, suited_flop = get_flop_textures(flop)
                    df_count = df_cummulative_count[-1] + doubled_flop
                    tf_count = tf_cummulative_count[-1] + tripled_flop
                    sf_count = sf_cummulative_count[-1] + suited_flop
                    df_cummulative_count.append(df_count)
                    tf_cummulative_count.append(tf_count)
                    sf_cummulative_count.append(sf_count)
                hands_count += 1

print(f'all hands: {hands_count}')                
print(f'flops: {flops.size}')

doubled_flops_calc = 3/51 + 6/50 - 3/51 * 2/50
tripled_flops_calc = 3/51 * 2/50
suited_flops_calc = 12/51 * 11/50
print(f'doubled flops calc: {100 * doubled_flops_calc : .2f}%')
print(f'tripled flops calc: {100 * tripled_flops_calc : .2f}%')
print(f'suited flops calc: {100 * suited_flops_calc : .2f}%')

# %%
df_cummulative_percent = [x/index[0] if index[0] else None for index, x in np.ndenumerate(df_cummulative_count)]
tf_cummulative_percent = [x/index[0] if index[0] else None for index, x in np.ndenumerate(tf_cummulative_count)]
sf_cummulative_percent = [x/index[0] if index[0] else None for index, x in np.ndenumerate(sf_cummulative_count)]

figsize = (20, 10)

plt.figure(figsize=figsize)
plt.plot(df_cummulative_percent)
plt.hlines(y=doubled_flops_calc, xmin=0, xmax=flops.size+1, linewidth=1, color='r')
plt.ylim(0.05, 0.18)
plt.title('doubled flops')

plt.figure(figsize=figsize)
plt.plot(tf_cummulative_percent)
plt.hlines(y=tripled_flops_calc, xmin=0, xmax=flops.size+1, linewidth=1, color='r')
plt.ylim(0, 0.01)
plt.title('tripled flops')

plt.figure(figsize=figsize)
plt.plot(sf_cummulative_percent)
plt.hlines(y=suited_flops_calc, xmin=0, xmax=flops.size+1, linewidth=1, color='r')
plt.ylim(0, 0.2)
plt.title('suited flops')

# %%
