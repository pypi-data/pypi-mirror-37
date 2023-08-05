import pandas as pd
import numpy as np
import time
from  tqdm import tqdm
import matplotlib.pyplot as plt


def window(x):
    return np.exp(-x)


def transform(x, d):
    return 1 / (1 + np.exp(-x*d))


def record(df):
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
    turns, misses, attendences = record(df)
    weight = misses.astype(float).copy() * 0

    for i in df.index:
        m = misses.loc[i].values[None, :] * window(attendences.loc[i:].cumsum()).values
        weight.loc[i:] += m

        t = turns.loc[i].values[None, :] * window((~turns).loc[i:].cumsum()).values  # [:, None]
        weight.loc[i:] -= t

    return weight, misses, turns


def simulate(initial_df, prob_miss, niter):
    df = initial_df.copy()

    for i in tqdm(range(len(df), niter+len(df))):
        weights, misses, turns = weightings(df)
        probs = transform(weights, len(weights.columns))
        probs = probs.div(probs.sum('columns'), 'index')
        missed = np.asarray([np.random.choice([1, 0], p=[p, 1-p]) for p in prob_miss], dtype=bool)
        if not missed.all():
            choice = probs.iloc[-1].sample(weights=probs.iloc[-1] * ~missed).index[0]
            df.loc[i] = [','.join([p for here, p in zip(~missed, probs.columns) if here]), choice]

    return df

if __name__ == '__main__':
    players ='a,b,c,d'.split(',')
    n = len(players)
    prob_miss = pd.Series(np.random.uniform(0.001, 0.5, size=n), index=players)

    # initial = pd.DataFrame({'attendence': [','.join(players[:-1]), ','.join(players[2:])], 'turn': ['a', 'a']}, index=[0, 1])
    # initial = pd.DataFrame({'attendence': ['a,b'], 'turn': ['a']})
    initial = pd.DataFrame(
        {'attendence': ['a,b', 'b,c', 'b,c', 'b', 'a,b,c', 'a,b,c', 'a,b,c,d'], 'turn': ['b'] * 5 + ['a']*2})

    after = simulate(initial, prob_miss, 50)
    weights, misses, turns = weightings(after)

    print(after)
    print(prob_miss)

    weights.plot()
    probs = transform(weights, len(weights.columns))
    probs = probs.div(probs.sum('columns'), 'index')
    print(probs.iloc[-1])
    # probs.plot()
    # plt.show()