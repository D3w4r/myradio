from enum import Enum


class Constants(Enum):
    CACHE_PATH = '/cache'
    RSS_REPOSITORY = 'D:/Data/ProjectLaboratory/myradio/src/cache/rss_repository'
    CONFIG = 'D:/Data/ProjectLaboratory/myradio/src/config/basic_config.json'
    CITY_LIST_GZ = 'D:/Data/ProjectLaboratory/myradio/src/cache/current.city.list.json.gz'
    CITY_LIST = 'D:/Data/ProjectLaboratory/myradio/src/cache/current.city.list.json'


class Time(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3

