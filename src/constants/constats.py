from enum import Enum


class Constants(Enum):
    CACHE_PATH = 'D:/Data/ProjectLaboratory/myradio/src/cache'
    RSS_REPOSITORY = 'D:/Data/ProjectLaboratory/myradio/src/cache/rss_repository'
    CONFIG = 'D:/Data/ProjectLaboratory/myradio/src/basicconfig/basic_config.json'
    CITY_LIST = 'D:/Data/ProjectLaboratory/myradio/src/cache/current.city.list.json.gz'


class Time(Enum):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3

