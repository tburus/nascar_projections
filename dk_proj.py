'''
Created on Dec 3, 2018

@author: Todd

PURPOSE: function for creating DK projection; imported to fantasy_proj.py
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from functools import reduce

pd.options.mode.chained_assignment = None

def dk_proj(outfile, laps, entry_file, tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8):
    #projection based on track and recent history
    
    #create file rec_stats
    rec_stats = pd.read_csv(entry_file).fillna(0)
    rec_stats['Driver'] = rec_stats['Driver'].str.lower()
    
    #read relevant history
    track1 = pd.read_csv(tr1)
    track2 = pd.read_csv(tr2)
    track3 = pd.read_csv(tr3)
    track4 = pd.read_csv(tr4)
    track5 = pd.read_csv(tr5)
    track6 = pd.read_csv(tr6)
    track7 = pd.read_csv(tr7)
    track8 = pd.read_csv(tr8)
    
    #subset dataframes
    track1_cut = track1[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    track2_cut = track2[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    track3_cut = track3[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    track4_cut = track4[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    track5_cut = track5[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    track6_cut = track6[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    track7_cut = track7[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    track8_cut = track8[['Driver', 'Start', 'Finish', 'Fastest Lap', 
                         'Laps Led', 'Total Laps']]
    
    tracks = [track1_cut, track2_cut, track3_cut, track4_cut,
              track5_cut, track6_cut, track7_cut, track8_cut]
    fantasy_stats = ['races', 'avg_start', 'avg_finish', 'avg_pd', 'fl', 
                     'll', 'lc', 'tl']
    track_stats = ['Start', 'Finish', 'Fastest Lap', 'Laps Led', 'Total Laps']
    
    #zero out columns of interest
    for stat in fantasy_stats:
        rec_stats[stat] = 0
    
    #load in historical data
    for track in tracks:
        rec_stats = pd.merge(rec_stats, track, 
                                 on='Driver', how='left').fillna(0)
                                 
        race_len = rec_stats['Total Laps'].max()
        
        rec_stats.loc[rec_stats['Finish'] > 0,'races'] += 1
        
        rec_stats['avg_start'] = rec_stats['avg_start'] + rec_stats['Start']
        rec_stats['avg_finish'] = rec_stats['avg_finish'] + rec_stats['Finish']
        rec_stats['avg_pd'] = rec_stats['avg_pd'] + \
                                (rec_stats['Start'] - rec_stats['Finish'])
        rec_stats['fl'] = rec_stats['fl'] + rec_stats['Fastest Lap']
        rec_stats['ll'] = rec_stats['ll'] + rec_stats['Laps Led']
        rec_stats['lc'] = rec_stats['lc'] + rec_stats['Total Laps']
        rec_stats['tl'] = rec_stats['tl'] + race_len
        
        rec_stats.drop(track_stats, axis=1, inplace=True)
    
    #average out data over number of races run
    rec_stats['avg_start'] = rec_stats['avg_start'] / rec_stats['races']
    rec_stats['avg_finish'] = rec_stats['avg_finish'] / rec_stats['races']
    rec_stats['avg_pd'] = rec_stats['avg_pd'] / rec_stats['races']
    rec_stats['percent_fl'] = rec_stats['fl'] / rec_stats['lc']
    rec_stats['percent_ll'] = rec_stats['ll'] / rec_stats['lc']
    rec_stats['percent_lc'] = rec_stats['lc'] / rec_stats['tl']
    
    #drop unneeded columns
    rec_stats.drop(['fl', 'll', 'lc', 'tl'], axis=1, inplace=True)
    
    #fill in any NaN values  
    rec_stats['avg_start'].fillna(40, inplace=True)
    rec_stats['avg_finish'].fillna(40, inplace=True)   
    rec_stats['avg_pd'].fillna(0, inplace=True)
    rec_stats['percent_fl'].fillna(0, inplace=True)
    rec_stats['percent_ll'].fillna(0, inplace=True)
    
    #rank relevant columns
    rec_stats['finish_rank'] = rec_stats['avg_finish'].rank()
    rec_stats['pd_rank'] = rec_stats['avg_pd'].rank(ascending=False)
    rec_stats['fl_rank'] = rec_stats['percent_fl'].rank(ascending=False)
    rec_stats['ll_rank'] = rec_stats['percent_ll'].rank(ascending=False)
    
    rec_stats['overall'] = rec_stats['finish_rank'] + \
                                        rec_stats['pd_rank'] + \
                                        rec_stats['fl_rank'] + \
                                        rec_stats['ll_rank']
    
    rec_stats['overall_rank'] = rec_stats['overall'].rank()
    
    #compute points in Draft Kings
    rec_stats['pd_pts'] = rec_stats['avg_pd'] 
    rec_stats['fl_pts'] = rec_stats['percent_fl'] * int(laps) * 0.5
    rec_stats['ll_pts'] = rec_stats['percent_ll'] * int(laps) * 0.25
    rec_stats['finish_pts'] = (47 - rec_stats['finish_rank'])
    rec_stats['total_pts'] = rec_stats['pd_pts'] + \
                                rec_stats['fl_pts'] + \
                                rec_stats['ll_pts'] + \
                                rec_stats['finish_pts']
    
    #save to csv
    year = '20' + outfile[-2:]

    if not os.path.exists('NASCAR_' + year + '\\' + outfile + '\\'):
        os.mkdir('NASCAR_' + year + '\\' + outfile + '\\')
        
    rec_stats.to_csv('NASCAR_' + year + '\\' + outfile + '\\' + 
                     'dk_fantasy_' + outfile + '.csv', index = False)
