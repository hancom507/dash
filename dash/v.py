
import pandas as pd
import datetime



df = pd.read_csv('../data/zoneVisitorDay.csv')
df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
'''
y = 2021
m = 8
d = 5
data =df[df['TIME'].dt.year==y]
data = data[df['TIME'].dt.month==m]
data = data[df['TIME'].dt.day==d]
print(data)

k=df.query("TIME >= '2021-08-05 00:00' and TIME <= '2021-08-05 23:59'")
print(k)
'''

week = df.query("'2021-08-22 00:00' <= TIME <= '2021-08-29 23:59'")
print(week)
#df['day'] = df['TIME'].dt.day

