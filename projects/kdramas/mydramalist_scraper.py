from bs4 import BeautifulSoup
import requests
import pandas as pd

titles, ratings, release_info, more_info, genres, cast = [], [], [], [], [], []
for i in range(1, 50):
    page = requests.get(f"https://mydramalist.com/shows/top?page={i}")
    soup = BeautifulSoup(page.content, 'lxml')
    scraped_dramas = soup.find_all('div', class_ = 'col-xs-9 row-cell content')
    for drama in scraped_dramas:
        release = drama.find('span', class_ = 'text-muted').get_text()
        if 'Korean' in release:
            title = drama.find('h6', class_ = 'text-primary title').get_text().replace('\n', '')
            print(title)
            rating = drama.find('span', class_ = 'p-l-xs score').get_text()
            more_info = 'https://mydramalist.com' + drama.h6.a['href']

            drama_page = requests.get(more_info)
            soupp = BeautifulSoup(drama_page.content, 'lxml')
            scraped_genres = soupp.find('li', class_ = 'list-item p-a-0 show-genres').get_text()
            series_cast = []
            scraped_cast = soupp.find_all('li', class_ = 'list-item col-sm-4')
            for actor in scraped_cast:
                series_cast.append(actor.find('b', itempropx = 'name').get_text())

            titles.append(title)
            ratings.append(rating)
            release_info.append(release)
            genres.append(scraped_genres)
            cast.append(series_cast)

drama_data = pd.DataFrame()
drama_data['Title'] = titles
drama_data['Rating'] = ratings
drama_data['Release Information'] = release_info
drama_data['Genre'] = genres
drama_data['Cast'] = cast
drama_data.to_csv('mydramalist.csv', index = False)