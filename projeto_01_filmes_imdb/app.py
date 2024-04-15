import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

http_imdb = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250", headers = headers)
html_imdb = BeautifulSoup(http_imdb.text, 'html.parser')

html_list_body = html_imdb.find(class_='ipc-metadata-list')
html_list_items = html_list_body.find_all('li')

dict_movie_list = []

for item in html_list_items:
    dict_movie = {}
    dict_movie['title'] = item.find(class_="ipc-title").text.split('. ')[1].strip()
    dict_movie['rating'] = item.find(class_="ipc-rating-star").text[:3].strip()
    dict_movie['qtd_votes'] = item.find(class_="ipc-rating-star").text[3:].replace(')','').replace('(','').strip()
    dict_movie['movie_url'] = 'https://www.imdb.com' + item.find(class_="ipc-title").find('a').get("href").strip()


    dict_movie_list.append(dict_movie)

df_movies = pd.DataFrame(dict_movie_list)

today = datetime.today().strftime('%Y_%m_%d')

df_movies.to_csv(f'results/{today}.csv', index= False)
