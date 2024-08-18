import csv
import os
import requests

csv_file_path = 'rankings/nirf_university_rankings.csv'
folder_name = os.path.splitext(os.path.basename(csv_file_path))[0]

os.makedirs(folder_name, exist_ok=True)

with open(csv_file_path, 'r') as f:
    reader = csv.reader(f)
    
    headers = next(reader)
    
    institute_id_index = headers.index('Institute ID')
    i = 1
    for row in reader:
        institute_id = row[institute_id_index]
        
        pdf_url = f'https://www.nirfindia.org/nirfpdfcdn/2024/pdf/UNIVERSITY/{institute_id}.pdf'
        
        pdf_file_path = os.path.join(folder_name, f'{institute_id}.pdf')
        
        response = requests.get(pdf_url)
        
        if response.status_code == 200:
            with open(pdf_file_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            print(f'{i} Downloaded: {pdf_file_path}')
            i += 1
        else:
            print(f'Failed to download: {pdf_url}')
