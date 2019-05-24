'''
Created on Oct 27, 2018

@author: burust
'''
import pandas as pd
import numpy as np
from random import sample

#ask for file input and DFS site
proj = input('Give file to test: ')
site = input('Give DFS site: ')

#read csv to dataframe
df1 = pd.read_csv(proj)

n = len(df1.index)
#specify for site
k = 0
while k == 0:
    if site == 'fd':
        s = 5
        cost = 'fd_cost'
        pts = 'fd_pts'
        k += 1
    elif site == 'dk': 
        s = 6
        cost = 'dk_cost'
        pts = 'dk_pts'
        k += 1
    else: 
        site = input('Re-enter site: ')
    

#choose 370 random lineups to calibrate
i = 0

calibrate = []

for i in range(0,3700):
    j = sample(range(0,n), s)
    df2 = df1.ix[j]
    if df2[cost].sum() <= 50000 and min(df2[cost]) > 6000:
        calibrate.append(df2[pts].sum())
    i += 1

#choose up to 630 random lineups and compare to all previous 
for i in range(3701, 10001):
    j = sample(range(0,n), s)
    df2 = df1.ix[j]
    if df2[cost].sum() <= 50000 and min(df2[cost]) > 6000:
        p = df2[pts].sum()
        if p > max(calibrate):
            print('Lineup tested: ' + str(i))
            print(df2[['Driver', pts, cost]])
            print('Expected points: ', p)
            break
    else:
        i += 1
        
i += 1
if i == 10001:
    print('No lineup found')