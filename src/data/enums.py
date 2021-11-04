from enum import Enum


class Constants(Enum):
    CACHE_PATH = 'src/cache'
    RSS_REPOSITORY = CACHE_PATH + '/rss_repository'
    CITY_LIST = CACHE_PATH + '/current.city.list.json'
    CITY_LIST_GZ = CACHE_PATH + '/current.city.list.json.gz'
    CONFIG = 'src/config/basic_config.json'
    MAIL_REPOSITORY = CACHE_PATH + '/repository.json'


class Time(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
