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
from collections import Counter

# %%
hh_data_dirname = 'hh_data'
files_filter = lambda f: path.isfile(path.join(hh_data_dirname, f)) and f.endswith('.txt') and f.startswith('2020-')
files = [f for f in listdir(hh_data_dirname) if files_filter(f)]
files.sort()
for file in files:
    print(file)

# %%
hands_count = 0
summaries = []
blinds = []

for filename in files:
    with open(path.join(hh_data_dirname, filename), 'r') as file:
        data = json.load(file)
        hh_data = np.asarray(data['Data'])
        hand_starts = np.core.defchararray.startswith(hh_data, 'Hand #')
        hand_indices = np.where(hand_starts == True)[0]
        hands = np.array_split(hh_data, hand_indices)
        for hand in hands:
            if hand.size:
                summary_string = hand[np.core.defchararray.startswith(hand, '** Summary **')]
                if summary_string.size > 0:
                    game_info = hand[np.core.defchararray.startswith(hand, 'Game: ')][0].split()
                    game_blinds = game_info[game_info.index('Blinds') + 1]
                    big_blind = int(game_blinds.split('/')[1])
                    blinds.append(big_blind)
                    summary_string_index = list(hand).index(summary_string)
                    summary_section = hand[summary_string_index:]
                    summaries.append(summary_section)
                    hands_count += 1

print(f'all hands: {hands_count}')
print(f'summaries: {len(summaries)}')

# %%
players_balances = {}

for index, summary in enumerate(summaries):
    players_info = [s for s in summary if s.startswith('Seat')]
    for player_info in players_info:
        nickname = player_info.split(': ')[1].split()[0]
        balance = int(player_info[player_info.find('(')+1:player_info.find(')')])
        if balance != 0:
            p_balances = players_balances[nickname] if nickname in players_balances else []
            balance /= blinds[index]
            p_balances.append(balance)
            players_balances[nickname] = p_balances

for player in players_balances:
    p_balances = np.asarray(players_balances[player])
    p_b_win = np.asarray([b for b in p_balances if b > 0])
    p_b_lose = np.asarray([b for b in p_balances if b < 0])
    print(f'nickname: {player}')
    print('all')
    print(f'mean: {p_balances.mean() : .2f}')
    print(f'std: {p_balances.std() : .2f}')
    print(f'count: {p_balances.size}')
    print('win')
    print(f'max: {p_balances.max()}')
    print(f'mean: {p_b_win.mean() : .2f}')
    print(f'count: {p_b_win.size}')
    print('lose')
    print(f'max: {p_balances.min()}')
    print(f'mean: {p_b_lose.mean() : .2f}')
    print(f'count: {p_b_lose.size}')
    print('\n')
    plt.figure(figsize=(20, 5))
    plt.hist(p_balances, bins=400)
    plt.yscale('log')
    plt.title(player)

# %%
