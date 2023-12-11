import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
# Also needs openpyxl 

url = 'https://www.imdb.com/chart/top/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
moviesData = soup.find_all('li', class_="ipc-metadata-list-summary-item sc-3f724978-0 enKyEL cli-parent")
csv_filename = "movies_data1.csv"
movies = []

with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    header = ['Rank', 'Name', 'Year', 'Rating']
    writer.writerow(header)
    for movie in moviesData:
        name = movie.find('div', class_='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-43986a27-9 gaoUku cli-title').a.text.split('.')[1]
        rank = movie.find('div', class_='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-43986a27-9 gaoUku cli-title').a.text.split('.')[0]
        year = movie.find('div', class_='sc-43986a27-7 dBkaPT cli-title-metadata').span.text
        rating = movie.find('div', class_='sc-e3e7b191-0 jlKVfJ sc-43986a27-2 bvCMEK cli-ratings-container').span.text
        rating = rating[0:3]
        movies.append([rank, name, year, rating])

df = pd.DataFrame(movies, columns=['Rank', 'Title', 'Year', 'Rating'])
pd.set_option('display.max_rows', None)
time.sleep(1)
# Exports DataFrame as an excel file
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, index=False)
