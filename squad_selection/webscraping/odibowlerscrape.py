import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
req=requests.get("https://www.espncricinfo.com/records/decade/bowling-most-wickets-career/2020s-202/one-day-internationals-2?team=6")
soup=BeautifulSoup(req.content,"html.parser")
rows=[]
columns=[]
for i in soup.find_all('thead',class_="ds-bg-fill-content-alternate ds-text-left"):
  for j in i.find_all('td',class_="ds-min-w-max"):
   columns.append(j.text)
c=len(columns)
#print(len(columns))
for i in soup.find_all('tbody'):
  for j in i.find_all('td'):
   rows.append(j.text)
#data will stored in the list name rows
r=len(rows)
#making the list into sublists
row_data=[rows[i:i+c] for i in range(0,r,c)]
#print(len(row_data))
#print(row_data)
#creating data frame with columns
data=pd.DataFrame(columns=columns)
#inserting row data 
#len(rows)=r//c
for i in range(0,r//c):
   data.loc[i]=row_data[i]
data=data.drop(columns=['Span','Balls','Inns','Overs','Runs','BBI','4'])
data=data.replace('-',0)
new_columns={'Mat':'Matches','Mdns':'Maidens','Wkts':'Wickets','BBM':'Best','Ave':'Average','Econ':'Economy','SR':'Strikerate','5':'Fifer'}
data=data.rename(columns=new_columns)
print(data)
data.to_csv(r'D:\python\bowler.csv',index=False,header=True)