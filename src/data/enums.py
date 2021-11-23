import os
from enum import Enum


class Constants(Enum):
    CACHE_PATH = os.getcwd() + '/cache'
    RSS_REPOSITORY = CACHE_PATH + '/rss_repository'
    CITY_LIST = CACHE_PATH + '/current.city.list.json'
    CITY_LIST_GZ = CACHE_PATH + '/current.city.list.json.gz'
    CONFIG = os.getcwd() + '/config/basic_config.json'
    MAIL_REPOSITORY = CACHE_PATH + '/repository.json'
    SAVED_WEIGHTS = os.getcwd() + '/dnn/saved-weigths.h5'


class Time(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
