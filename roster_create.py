'''
Created on Jul 28, 2018

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
entry = pd.read_csv('entry_list_' + race + '.csv')
dk_file = pd.read_csv('dk_fantasy_' + race + '.csv')
fd_file = pd.read_csv('fd_fantasy_' + race + '.csv')

#pull points and salary from dk into roster
roster = pd.merge(entry, dk_file, 
                  on=['DriverID', 'Number', 'Driver', 'DraftKingsSalary'], 
                  how ='left')
roster['dk_pts'] = roster['total_pts']
roster['dk_cost'] = roster['DraftKingsSalary'] #change column name
roster = roster[['DriverID', 'Number', 'Driver', 'dk_pts', 'dk_cost']]


#pull points from fd into roster
roster = pd.merge(roster, fd_file, on=['DriverID', 'Number', 'Driver'],
                   how='left')
roster['fd_pts'] = roster['total_pts']
roster = roster[['DriverID', 'Number', 'Driver', 'dk_pts', 'dk_cost', 'fd_pts']]
roster['fd_cost'] = 0

#fill Position
roster['position'] = 'dr'

#write to roster file
roster.to_csv('roster_' + race + '.csv', index=False)