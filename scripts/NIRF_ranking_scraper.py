from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.nirfindia.org/Rankings/2024/STATEPUBLICUNIVERSITYRanking.html"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

table = soup.find('table')

headers = table.find('tr').find_all('th')
table_headers = [header.text.strip() for header in headers]

# Extract table rows
body = table.find('tbody')
rows = body.find_all('tr')

data = []

for row in rows:
    cells = row.find_all('td')
    
    if len(cells) < 6:
        continue
    
    institute_id = cells[0].text.strip()
    
    name_cell = cells[1]
    name = name_cell.get_text(separator=' ', strip=True).split('More Details')[0].strip()
    
    city = cells[-4].text.strip()
    state = cells[-3].text.strip()
    score = cells[-2].text.strip()
    rank = cells[-1].text.strip()
    
    row_data = [institute_id, name, city, state, score, rank]
    data.append(row_data)

df = pd.DataFrame(data, columns=table_headers)
df.to_csv('nirf_state_public_universities_rankings.csv', index=False)
print(df)
