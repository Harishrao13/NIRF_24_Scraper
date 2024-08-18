import pandas as pd

df = pd.read_csv('rankings/nirf_university_rankings.csv')

df['Stream'] = 'University'
# df = df.drop('stream', axis=1)
print(df.head())

df.to_csv('rankings/nirf_university_rankings.csv', index=False)
