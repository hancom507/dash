from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('./zoneVisitorDay.csv')
del df['Unnamed: 0']
#df = df.set_index(keys=['TIME'])
#df['TIME']= pd.to_datetime(df['TIME'], format='%Y-%m-%d %H:%M')
#지난주의 일요일 날짜 구함
#today= datetime.today()
#today = datetime.today()-timedelta(67)
#startDate = today - timedelta(today.weekday())-timedelta(8)
#df = df[(df['TIME']>=startDate) & (df['TIME']<startDate+timedelta(7))]
#df.sum(axis=1)
data = df.iloc[-1]
deltas = df.iloc[-2]
