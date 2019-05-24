'''
Created on Jul 10, 2018

@author: burust
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, csv, time

year = input('Select year: ')

os.chdir('C:\\NASCAR_Data\\NASCAR_' + year)

for i in range(1, 37):
    if i < 10:     
        url = 'http://racing-reference.info/loopdata/' + year + '-0' + str(i) + '/W'
        page = requests.get(url)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, 'html.parser')
        
        table = soup.find_all(class_ = 'tb')
        headers = [th.text for th in table[2].select("tr th")]
        
        with open(url.split('/')[-2] + ".csv", "w", newline='') as f:
            wr = csv.writer(f)
            wr.writerow(headers)
            wr.writerows([[td.text 
                           for td in row.find_all("td")] 
                           for row in table[2].select("tr + tr") 
                           if row.select_one('td')])
            
        #edit Driver column to match API calls
        df = pd.read_csv(url.split('/')[-2] + ".csv")
        df['Driver'] = df['Driver'].str.replace('.', '')
        df['Driver'] = df['Driver'].str.replace(',', '')
        df['Driver'] = df['Driver'].str.lower()
        
        #create Pct. Fastest column
        laps = max(df['Total Laps'])
        df['Pct. Fastest'] = round(df['Fastest Lap']/laps*100, 1)
        
        #rename DRIVER RATING
        df.rename(index=str, columns={'DRIVER RATING': 'Driver Rating'}, 
                  inplace=True)
        
        #save to csv
        df.to_csv(url.split('/')[-2] + ".csv", index=False)
        time.sleep(5)
    else:
        url = 'http://racing-reference.info/loopdata/' + year \
            + '-' + str(i) + '/W'
        page = requests.get(url)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(page.text, 'html.parser')
        
        table = soup.find_all(class_ = 'tb')
        headers = [th.text for th in table[2].select("tr th")]
        
        with open(url.split('/')[-2] + ".csv", "w", newline='') as f:
            wr = csv.writer(f)
            wr.writerow(headers)
            wr.writerows([[td.text 
                           for td in row.find_all("td")] 
                           for row in table[2].select("tr + tr")])

        #edit Driver column to match API calls
        df = pd.read_csv(url.split('/')[-2] + ".csv")
        df['Driver'] = df['Driver'].str.replace('.', '')
        df['Driver'] = df['Driver'].str.replace(',', '')
        df['Driver'] = df['Driver'].str.lower()
        
        #create Pct. Fastest column
        laps = max(df['Total Laps'])
        df['Pct. Fastest'] = round(df['Fastest Lap']/laps*100, 1)
        
        #rename DRIVER RATING
        df.rename(index=str, columns={'DRIVER RATING': 'Driver Rating'}, 
                  inplace=True)
        
        #save to csv
        df.to_csv(url.split('/')[-2] + ".csv", index=False)
        time.sleep(5)

