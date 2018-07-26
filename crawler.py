#! /usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import division
import requests
from bs4 import BeautifulSoup
import xlrd
import csv
import xlwt

BASE_URL = 'https://www.imdb.com/title/'

def get_data(movie_id):
    '''
    get the movie released date and storyline.
    :param movie_id: string, '114709'
    :return: (date, storyline), ('1995-07-01', 'A little boy named Andy loves to be in his room')
    '''
    if len(movie_id) > 5:
        movie_url = BASE_URL + 'tt0' + movie_id + '/'
    else:
        movie_url = BASE_URL + 'tt' + '0' * (7-len(movie_id)) + movie_id + '/'
    result = requests.get(movie_url)
    c = result.content
    soup = BeautifulSoup(c, 'lxml')
    date_ = soup.find('meta', {'itemprop': 'datePublished'})
    try:
        date = date_['content']
    except:
        date = ''
    storyline_ = soup.find('span', {'itemprop': 'description'})
    try:
        storyline = storyline_.get_text()
    except:
        storyline = ''
    return (date, storyline)


def ml_20_crawler(file_path, write_path):
    '''
    crawler for movielens 20M dataset
    :param file_path: file path of links.csv
    :return: write a csv file
    '''
    with open(file_path) as f1:
        with open(write_path, 'w') as f2:
            conten = csv.reader(f1)
            conten_w = csv.writer(f2)
            i = 0
            for row in conten:
                if i == 0:
                    i += 1
                    continue
                ml_id = row[0]
                imdb_id = row[1]
                (date, storyline) = get_data(imdb_id)
                conten_w.writerow([ml_id, date, storyline])

if __name__ == '__main__':
    file_path = '../data/ml-20m/links.csv'
    write_path = '../data/ml-20m/datemap.csv'
    ml_20_crawler(file_path, write_path)
