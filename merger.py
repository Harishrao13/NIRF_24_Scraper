import pandas as pd
import pdfplumber
import re
import os

df1 = pd.read_csv('rankings/nirf_university_rankings.csv')
df2 = pd.read_csv('ranking.csv')
df3 = pd.read_csv('test.csv')

df4 = pd.merge(df1, df2, on='Institute ID')
df5 = pd.merge(df4, df3, on='Institute ID')
df5.to_csv('FINAL/nirf_university_rankings.csv', index=False)

os.remove('rankin.csv')
os.remove('ranking.csv')
os.remove('test.csv')

