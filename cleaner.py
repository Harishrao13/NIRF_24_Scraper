import pandas as pd

# Read the CSV file
df = pd.read_csv('rankin.csv')

print(df.head(5))
duppler = df.drop_duplicates(subset='Institute ID')

def has_nine_commas(row):
    return any(val.count(',') == 9 for val in row.astype(str))

duppler = duppler[~duppler.apply(has_nine_commas, axis=1)]

duppler.to_csv('ranking.csv', index=False)
