import json
import os
import logging
import requests
import gzip

from src.constants.constats import Constants

logging.basicConfig(level=logging.INFO)


class Weather:
    """This class manages weather info through the OpenWeatherMap API"""

    api_key = os.environ.get('OPENWEATHERMAP_ID')

    def __init__(self, city):
        self.city = city
        self.download_city_list()

    def download_city_list(self):
        logging.info('Downloading city list from source')
        url = "https://bulk.openweathermap.org/sample/current.city.list.json.gz"
        city_list = requests.get(url)
        if not os.path.exists('D:/Data/ProjectLaboratory/myradio/src/cache/current.city.list.json'):
            with open(Constants.CITY_LIST.value, 'wb') as file:
                file.write(city_list.content)
            block_size = 65536
            with gzip.open(Constants.CITY_LIST.value, 'rb') as source, \
                    open(Constants.CACHE_PATH.value + '/current.city.list.json', 'wb') as dest:
                while True:
                    block = source.read(block_size)
                    if not block:
                        break
                    else:
                        dest.write(block)

    def weather_info(self):
        """
        :return: the weather info in json format
        """
        logging.info('Getting weather info...')
        with open('D:/Data/ProjectLaboratory/myradio/src/cache/current.city.list.json', 'r', encoding='utf-8') as file:
            cities = json.load(file)
        url = "https://api.openweathermap.org/data/2.5/weather?id=%s&appid=%s&lang=%s&units=metric" % (
            self.get_city_id(cities), self.api_key, "hu")
        response = requests.get(url)
        return json.loads(response.text)

    def get_city_id(self, cities):
        id = None
        for city in cities:
            if city['name'] == self.city:
                id = city['id']
        return id


if __name__ == "__main__":
    w = Weather('Budapest')
    print(w.weather_info())
