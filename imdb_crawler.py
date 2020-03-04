
# coding: utf-8
'''
imdb crawler

collects title, year, imgsrc, country, genre, time, director, oscar, award, budget, opening_wknd, openingUSA, grossUSA, grossWorld
country, genre, director can have one or more elements
'''

import urllib.request
from bs4 import BeautifulSoup
from contextlib import contextmanager
from collections import defaultdict

@contextmanager
def ignored(self, *exceptions):
    try:
        yield
    except exceptions:
        pass

def ignore_exception(func):

     def func_wrapper(*args, **kwargs):

         try:
            return func(*args, **kwargs)

         except Exception as e:
             pass

     return func_wrapper

@ignore_exception
def get_money_stuff(soup, stuff):
    h4 = soup.find('h4', string = stuff)
    item = h4.next_sibling
    num = ''.join(item.split()).replace(',','')
    return num

def crawler(t):
    url = 'https://www.imdb.com/title/' + t
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    title_wrapper =  soup.find('div', {'class': 'title_wrapper'})
    title = title_wrapper.h1.find(text=True, recursive=False).replace('\xa0', '')
    
    str_item = defaultdict(str)

    with ignored(Exception):
        str_item['imgsrc'] = soup.find('div', {'class': 'poster'}).find('img').get('src')

    with ignored(Exception):
        str_item['year'] = title_wrapper.find('span', {'id':'titleYear'}).a.text
    with ignored(Exception):
        str_item['time'] = title_wrapper.find('time')['datetime']
    with ignored(Exception):
        str_item['budget'] = get_money_stuff(soup, 'Budget:')
    with ignored(Exception):
        str_item['opening_wknd'] = get_money_stuff(soup, 'Opening Weekend:')
    with ignored(Exception):
        str_item['opening_USA'] = get_money_stuff(soup, 'Opening Weekend USA:')
    with ignored(Exception):
        str_item['grossUSA'] = get_money_stuff(soup, 'Gross USA:')
    with ignored(Exception):
        str_item['grossWorld'] = get_money_stuff(soup, 'Cumulative Worldwide Gross:')
    
    list_item = defaultdict(list)

    with ignored(Exception):
        htag = soup.find('h4', string = 'Country:')
        list_item['country'] = [a.text for a in htag.parent.find_all('a')]

    with ignored(Exception):
        list_item['genre'] = [a.text for a in title_wrapper.find_all('a') if 'title?genres=' in a['href']]

    # fill in the blank items with an empty string or list
    str_dict = {k: str_item[k] for k in ['imgsrc', 'year', 'time', 'budget', 'opening_wknd', 'opening_USA', 'grossUSA', 'grossWorld']}
    list_dict = {k: list_item[k] for k in ['country', 'genre']}

    return dict(str_dict, **list_dict)


if __name__ == "__main__":
    crawler('tt0108052')
