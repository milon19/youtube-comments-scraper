import json

from scraper import *
from video_urls import urls

numOfScrolls = 3


def write_data(raw_data):
    with open('data.json', 'w+', encoding='utf-8') as file:
        json.dump(raw_data, file)
    print('Data have saved in JSON format...')

def main():
    raw_data = run_scraper(urls, numOfScrolls=numOfScrolls)
    write_data(raw_data)


if __name__ == '__main__':
    main()