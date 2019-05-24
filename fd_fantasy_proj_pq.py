'''
Created on Jul 27, 2018

@author: burust
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import reduce

proj_dir = input('Give a data directory: ')
os.chdir(proj_dir)

tr_name = input('Which race is this for?: ')

#open fantasy projections
proj_file = pd.read_csv('fd_fantasy_' + tr_name + '.csv')

#open entry list
entry_file = pd.read_csv('entry_list_' + tr_name + '.csv')

entry_file = entry_file[['Driver']]

#open qualifying results
qual_file = pd.read_csv(tr_name + '_qualify.csv')

qual_file = qual_file[['Driver', 'qualifying']]

#merge files
entry_qual = pd.merge(entry_file, qual_file, on='Driver', how='left')
df = pd.merge(proj_file, entry_qual, on='Driver', how='left')

#calculate qualifying adjustments
c1 = (df['qualifying'] - df['avg_pd'] < 1)
c2 = (df['qualifying'] > df['avg_start'])
c3 = (df['qualifying'] + df['avg_pd'] > 40)

o1 = df['qualifying'] - 1
o2 = df['qualifying'] - df['avg_finish']
o3 = 40 - df['qualifying']

df['pd_pq'] = np.select([c1, c2, c3], [o1, o2, o3], default=df.avg_pd)

#calculate points for revised pd -- 'pd_pq_pts'
df['pd_pq_pts'] = df['pd_pq'] * 0.5

#total other stats with pd_pq_pts -- 'total_pq_pts'
df['total_pq_pts'] = df['pd_pq_pts'] + \
                                df['lc_pts'] + \
                                df['ll_pts'] + \
                                df['finish_pts']

#write new file to dk_fantasy_proj.csv
df.to_csv('fd_fantasy_pq_' + tr_name + '.csv', index=False)