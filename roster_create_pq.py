'''
Created on Aug 8, 2018

@author: burust
'''
import pandas as pd
import os

#get into project directory
proj_dir = input('Give a data directory: ')
os.chdir(proj_dir)

#ask for race
race = input('Which race is this for: ')

#read entry list, fd_proj and dk_proj
entry = pd.read_csv('roster_' + race + '.csv')
dk_file = pd.read_csv('dk_fantasy_pq_' + race + '.csv')
fd_file = pd.read_csv('fd_fantasy_pq_' + race + '.csv')

#pull points from fd and dk into roster
roster = pd.merge(entry, dk_file, on='Driver', how ='left')
roster['dk_pts'] = roster['total_pq_pts']
roster = roster[['Driver', 'dk_pts', 'dk_cost', 'fd_cost']]


roster = pd.merge(roster, fd_file, on='Driver', how='left')
roster['fd_pts'] = roster['total_pq_pts']
roster = roster[['DriverID', 'Number','Driver', 'dk_pts', 'dk_cost', 'fd_pts', 'fd_cost']]

#fill Position
roster['position'] = 'dr'

#fill NaNs
roster.fillna(0, inplace=True)

#write to roster file
roster.to_csv('roster_' + race + '_pq.csv', index=False)