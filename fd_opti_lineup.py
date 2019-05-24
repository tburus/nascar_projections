'''
Created on Jul 27, 2018

@author: burust
'''
from gurobipy import *
import numpy as np
import pandas as pd

points = "fd_pts"
salary = "fd_cost"
position = "position"

race = input('Give race: ')
postq = input('Post-qualifying?: ')

if postq == 'yes':
    race2 = race + '_pq'
else:
    race2 = race

def optimize(player_names, player_data):
    varbs = {}  # key: player name, value : var

    m = Model()

    for p in player_names:
        varbs[p] = m.addVar(vtype=GRB.BINARY, name = p)

    m.update()

    all_const = LinExpr()
    for p in player_names:
            all_const.addTerms(1,varbs[p])
    all_const = all_const == 5

    #Pick Drivers
    dr_const = LinExpr()
    for p in player_names:
        if player_data.loc[p, position] == "dr":
            dr_const.addTerms(1,varbs[p])
    dr2_const =  4 <= dr_const.copy()
    dr_const =  dr_const <= 5

    sal_const = LinExpr()
    for p in player_names:
        if type(player_data.loc[p, position]) == type(''):
            sal_const.addTerms(player_data.loc[p,salary],varbs[p])
    sal_const = sal_const <= 50000


    m.addConstr(all_const, "team number constraint")
    m.addConstr(dr_const, "dr constraint")
    m.addConstr(dr2_const, "dr2 constraint")
    m.addConstr(sal_const, 'salary constraint')

    # Objective
    obj = LinExpr()
    for p in player_names:
        if type(player_data.loc[p, points]) == np.float64:
            obj.add(varbs[p], player_data.loc[p, points])

    m.setObjective(obj, sense= GRB.MAXIMIZE)
    m.update()

    m.optimize()

    sal = 50000
    team = []
    print('Your optimal lineup is:')
    for v in m.getVars():
        if v.x ==1:
            sal -= player_data.loc[v.varName, salary]
            #print('\t %s %g' % (v.varName, player_data.loc[v.varName, points]))
            print('\t %s' % v.varName)
            team += [v.varName]
            
    total_pts = m.objVal
    leftover = str(sal)

    print('Total Points: %g' % total_pts)
    print("Salary leftover: " + leftover)
    


def main():

    player_data = pd.read_csv('C:\\NASCAR_Data\\NASCAR_2019\\' + race 
                              + '\\roster_' + race2 + '.csv', 
                              index_col='Driver' )
    player_data[points] = player_data[points].astype(np.float64) # Fixes issue around data types
    optimize(player_data.index, player_data)

if __name__ == '__main__':
    main()
    
