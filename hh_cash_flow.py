# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.2
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
import math

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
players_cash_flows = {}

_summaries = summaries[:]
for index, summary in enumerate(_summaries):
    
    players_info = [s for s in summary if s.startswith('Seat')]
    hand_info = {}
    
    for player_info in players_info:
        nickname = player_info.split(': ')[1].split()[0]
        balance = int(player_info[player_info.find('(')+1:player_info.find(')')])
        if balance != 0:
            hand_info[nickname] = balance
    winners = dict(filter(lambda player: player[1] > 0, hand_info.items()))
    loosers = dict(filter(lambda player: player[1] < 0, hand_info.items()))

    if len(loosers) == 0:
        print('--- Have no loosers! ---')
        print(hand_info)
        continue
    
    if len(winners) == 1 and len(loosers) == 1:
        
        winner = list(winners.keys())[0]
        win = list(winners.values())[0]
        looser = list(loosers.keys())[0]
        loose = list(loosers.values())[0]
        
        winner_cash_flows = players_cash_flows[winner] if winner in players_cash_flows else {looser: 0}
        looser_cash_flows = players_cash_flows[looser] if looser in players_cash_flows else {winner: 0}
        
        win_prev = winner_cash_flows[looser] if looser in winner_cash_flows else 0
        winner_cash_flows[looser] = win + win_prev
        players_cash_flows[winner] = winner_cash_flows
        
        loose_prev = looser_cash_flows[winner] if winner in looser_cash_flows else 0
        looser_cash_flows[winner] = loose + loose_prev
        players_cash_flows[looser] = looser_cash_flows
    
    elif len(winners) == 1:
        
        winner = list(winners.keys())[0]
        win = list(winners.values())[0]
        
        for looser, loose in loosers.items():
        
            winner_cash_flows = players_cash_flows[winner] if winner in players_cash_flows else {looser: 0}
            looser_cash_flows = players_cash_flows[looser] if looser in players_cash_flows else {winner: 0}

            win_prev = winner_cash_flows[looser] if looser in winner_cash_flows else 0
            winner_cash_flows[looser] = win_prev - loose
            players_cash_flows[winner] = winner_cash_flows

            loose_prev = looser_cash_flows[winner] if winner in looser_cash_flows else 0
            looser_cash_flows[winner] = loose + loose_prev
            players_cash_flows[looser] = looser_cash_flows

    else:
        
        for winner, win in winners.items():
                                
            for looser, loose in loosers.items():
                
                loose /= len(winners)
#                 if math.modf(loose)[0] != 0:
#                     print(f'math.modf(loose)[0] != 0 {loose}, {index}')
#                     print(hand_info)
                loose = round(loose)
        
                winner_cash_flows = players_cash_flows[winner] if winner in players_cash_flows else {looser: 0}
                looser_cash_flows = players_cash_flows[looser] if looser in players_cash_flows else {winner: 0}

                win_prev = winner_cash_flows[looser] if looser in winner_cash_flows else 0
                winner_cash_flows[looser] = win_prev - loose
                players_cash_flows[winner] = winner_cash_flows

                loose_prev = looser_cash_flows[winner] if winner in looser_cash_flows else 0
                looser_cash_flows[winner] = loose + loose_prev
                players_cash_flows[looser] = looser_cash_flows

        
print(players_cash_flows)

# %%
