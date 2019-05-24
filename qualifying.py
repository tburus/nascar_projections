'''
Created on May 23, 2019

@author: Todd

PURPOSE: scrape data of Cup qualifying results for the week
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, csv, time

#get race name
race = input('Which race is this for?: ')

#change directory
os.chdir('C:\\NASCAR_Data\\NASCAR_2019\\' + race + '\\')

#get race number
race_num = int(input('Give race number: '))
    
    #scrape qualifying data
if race_num < 10:     
    url = 'http://racing-reference.info/getqualify/2019-0' + str(race_num) + '/W'
    page = requests.get(url)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'html.parser')
    
    table = soup.find_all(class_ = 'tb')
    headers = [th.text for th in table[2].select("tr th")]
    
    with open(race + "_qualify.csv", "w", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(headers)
        wr.writerows([[td.text 
                       for td in row.find_all("td")] 
                       for row in table[2].select("tr + tr") 
                       if row.select_one('td')])
    #edit Driver column to match API calls
    df = pd.read_csv(race + "_qualify.csv", encoding = "ISO-8859-1")
    
    df['Driver'] = df['Driver'].str.strip()
    df['Driver'] = df['Driver'].str.replace('.', '')
    df['Driver'] = df['Driver'].str.replace(',', '')
    df['Driver'] = df['Driver'].str.lower()
    
    #strip whitespace
    df['Time'] = df['Time'].str.strip()
    df['Speed'] = df['Speed'].str.strip()
    
    #cut columns in df
    df = df[['Rank', 'Driver', 'Time', 'Speed']]
    df.rename(index=str, columns={'Rank':'qualifying'}, inplace=True)
    
    df.to_csv(race + "_qualify.csv", encoding='utf-8', index=False)
    
else:
    url = 'http://racing-reference.info/getqualify/2019-' + str(race_num) + '/W'
    page = requests.get(url)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'html.parser')
    
    table = soup.find_all(class_ = 'tb')
    headers = [th.text for th in table[2].select("tr th")]
    
    with open(race + "_qualify.csv", "w", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(headers)
        wr.writerows([[td.text 
                       for td in row.find_all("td")] 
                       for row in table[2].select("tr + tr") 
                       if row.select_one('td')])
    #edit Driver column to match API calls
    df = pd.read_csv(race + "_qualify.csv", encoding = "ISO-8859-1")
    
    df['Driver'] = df['Driver'].str.strip()
    df['Driver'] = df['Driver'].str.replace('.', '')
    df['Driver'] = df['Driver'].str.replace(',', '')
    df['Driver'] = df['Driver'].str.lower()
    
    #strip whitespace
    df['Time'] = df['Time'].str.strip()
    df['Speed'] = df['Speed'].str.strip()
    
    #cut columns in df
    df = df[['Rank', 'Driver', 'Time', 'Speed']]
    df.rename(index=str, columns={'Rank':'qualifying'}, inplace=True)
    
    df.to_csv(race + "_qualify.csv", encoding='utf-8', index=False)
    

    
