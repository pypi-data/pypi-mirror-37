import pandas as pd
import numpy as np
import time
from  tqdm import tqdm
import matplotlib.pyplot as plt


def window(x):
    return np.exp(-x)


def transform(x, d):
    return 1 / (1 + np.exp(-x*d))


def values(df):
    players = set([j for i in df.attendence.str.split(',').values for j in i])

    turns = pd.DataFrame(index=df.index, columns=players) * 0
    misses = turns.copy()
    attendences = turns.copy()
    for player in players:
        turns[player] = df['turn'] == player
        misses[player] = df['attendence'].apply(lambda x: player not in x)
        misses.loc[:misses[player].idxmin(), player] = False
        attendences[player] = df['attendence'].apply(lambda x: player in x)
    return turns, misses, attendences


def weightings(df):
    turns, misses, attendences = values(df)
    weight = misses.astype(float).copy() * 0

    for i in df.index:
        m = misses.loc[i].values[None, :] * window(attendences.loc[i:].cumsum()).values
        weight.loc[i:] += m

        t = turns.loc[i].values[None, :] * window((~turns).loc[i:].cumsum()).values  # [:, None]
        weight.loc[i:] -= t

    return weight, misses, turns


def algorithm(df, attended):
    if len(df) == 0:
        return pd.DataFrame([[1./len(attended)]*len(attended)], columns=attended, index=[0])
    weights, misses, turns = weightings(df)
    probs = transform(weights, len(weights.columns))
    probs = probs.div(probs.sum('columns'), 'index')
    return probs