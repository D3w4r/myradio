import json
import os
import logging
import requests
import gzip

from src.enums import Constants

logging.basicConfig(level=logging.INFO)


def download_city_list():
    url = "https://bulk.openweathermap.org/sample/current.city.list.json.gz"
    city_list = requests.get(url)
    if not os.path.exists(Constants.CITY_LIST.value):
        logging.info('Downloading city list from source')
        with open(Constants.CITY_LIST_GZ.value, 'wb') as file:
            file.write(city_list.content)
        block_size = 65536
        with gzip.open(Constants.CITY_LIST_GZ.value, 'rb') as source, \
                open(Constants.CACHE_PATH.value + '/current.city.list.json', 'wb') as dest:
            while True:
                block = source.read(block_size)
                if not block:
                    break
                else:
                    dest.write(block)
        os.remove(Constants.CITY_LIST_GZ.value)


class Weather:
    """This class manages weather info through the OpenWeatherMap API"""

    api_key = os.environ.get('OPENWEATHERMAP_ID')

    def __init__(self, city):
        self.city = city
        download_city_list()

    def weather_info(self):
        """
        :return: the weather info in json format
        """
        logging.info('Getting weather info...')
        with open('/src/cache/current.city.list.json', 'r', encoding='utf-8') as file:
            cities = json.load(file)
        url = "https://api.openweathermap.org/data/2.5/weather?id=%s&appid=%s&lang=%s&units=metric" % (
            self.get_city_id(cities), self.api_key, "hu")
        response = requests.get(url)
        return json.loads(response.text)

    def get_city_id(self, cities):
        to_return_id = None
        for city in cities:
            if city['name'] == self.city:
                to_return_id = city['id']
        return to_return_id


if __name__ == "__main__":
    w = Weather('Budapest')
    print(w.weather_info())
