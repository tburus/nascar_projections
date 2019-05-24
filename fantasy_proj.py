'''
Created on Jan 2, 2019

@author: Todd

PURPOSE:
create DK and FD fantasy projections
'''
import pandas as pd
import os
from dk_proj import dk_proj                                                                                                                                                                                                                                                                                                                                                             
from fd_proj import fd_proj

pd.options.mode.chained_assignment = None

proj_dir = input('Give a data directory: ')
os.chdir(proj_dir)

#get race name
race = input('Which race is this for?: ')

#get track name
track = input('Give track name: ')

#get race number
race_num = int(input('Give race number: '))

#get number of laps
laps = input('How many laps in race: ')

#make entry list file name
entry = 'NASCAR_2019\\' + race + '\\entry_list_' + race + '.csv'

#find last 4 races at track
df = pd.read_csv('race_list_14-19.csv')
tr_races = df.index[df['Track'] == track].tolist()
print(tr_races)

tr_hist = []

for i in range(4):
    if df['Race'].loc[tr_races[-1]] > race_num:
        year = df['Year'].loc[tr_races[-3-i]]
        num = df['Race'].loc[tr_races[-3-i]]
    else:
        year = df['Year'].loc[tr_races[-2-i]]
        num = df['Race'].loc[tr_races[-2-i]]
    if num < 10:
        tr_hist.append('NASCAR_' + str(year) +
                    '\\' + str(year) + '-0' + str(num) + '.csv')
    else:
        tr_hist.append('NASCAR_' + str(year) +
                    '\\' + str(year) + '-' + str(num) + '.csv')
    print(tr_hist[i])

#find last 4 races of season
rec_races = df.index.tolist()

rec_hist = []

for i in range(4):
    year = df['Year'].loc[rec_races[215-(37-race_num)-i]]
    num = df['Race'].loc[rec_races[215-(37-race_num)-i]]
    if num < 10:
        rec_hist.append('NASCAR_' + str(year) +
                    '\\' + str(year) + '-0' + str(num) + '.csv')
    else:
        rec_hist.append('NASCAR_' + str(year) +
                    '\\' + str(year) + '-' + str(num) + '.csv')
    print(rec_hist[i])
    
dk_proj(race, laps, entry, tr_hist[0], tr_hist[1], tr_hist[2], 
           tr_hist[3], rec_hist[0], rec_hist[1], rec_hist[2], rec_hist[3])


fd_proj(race, laps, entry, tr_hist[0], tr_hist[1], tr_hist[2], 
           tr_hist[3], rec_hist[0], rec_hist[1], rec_hist[2], rec_hist[3])