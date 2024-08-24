import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from scrape1 import biographies

req=requests.get('https://www.espncricinfo.com/records/decade/batting-most-runs-career/2020s-202/one-day-internationals-2?team=6')
soup=BeautifulSoup(req.content,"html.parser")
player=[]
player_column=[]
player_data=[]
for i in soup.find_all('a',class_="ds-inline-flex ds-items-start ds-leading-none"):
    player.append(i.get('href'))
for link in player.copy():
    if link.startswith('https'):
        player.remove(link)
player=['https://www.espncricinfo.com' + link for link in player]
if(len(player_column)<1):
    req=requests.get(player[0])
    soup=BeautifulSoup(req.content,'html.parser')
    for i in soup.find_all('p',class_='ds-text-tight-m ds-font-regular ds-uppercase ds-text-typo-mid3'):
        player_column.append(i.text) 
for link in player:
    req=requests.get(link)
    soup=BeautifulSoup(req.content,'html.parser')
    for i in soup.find_all('span',class_='ds-text-title-s ds-font-bold ds-text-typo'):
        player_data.append(i.text)
data=pd.DataFrame(columns=player_column)
for i in range(10*6):
   player_data.pop()
for i in range(10):
   biographies.pop()
for index,i in enumerate(player_data):
   if(i=='Akshar Patel' or i=='Deepak Chahar' or i=='Venkatesh Iyer'):
      player_data.remove(i)
r=len(player_data)
c=len(player_column)
row_data=[player_data[i:i+c] for i in range(0,r,c)]
for i in range(0,r//c):
   data.loc[i]=row_data[i]
data['Bio']=biographies
data['Bio']=data['Bio'].str.replace(r'[\n\xa0]','',regex=True)
data.index=data.index+1
data.to_csv(r'D:\python\info.csv',index=True,header=True)




