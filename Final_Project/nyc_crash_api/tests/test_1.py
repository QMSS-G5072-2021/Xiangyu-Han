from nyc_crash_api import nyc_crash_api

import os
import requests
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv(dotenv_path = '/Users/humphreyhan/Documents/GitHub/Xiangyu_Han/Final_Project/crash_env') 
app_token = os.getenv('CRASH_TOKEN')
end_point = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json'


def test_borough_crashes():
    df = nyc_crash_api.get_borough_crashes(app_token,'BRONX','2019-07-04T00:00:00','2019-07-04T00:00:00')
    assert type(df) == pd.DataFrame, 'The function did not return the right datatype.'

def test_zipcode_crashes():
    df = nyc_crash_api.get_zipcode_crashes(app_token,'10025','2019-07-04T00:00:00','2019-07-05T00:00:00')
    assert type(df) == pd.DataFrame, 'The function did not return the right datatype.'

def test_crashes_count_by_boroughs():
    df = nyc_crash_api.get_crashes_count_by_boroughs(app_token,'2019-07-04T00:00:00','2019-07-06T00:00:00')
    assert type(df) == pd.DataFrame, 'The function did not return the right datatype.'

def test_time_cycle():
    df = nyc_crash_api.get_time_cycle(app_token,'2020-06-06T00:00:00','2020-07-06T00:00:00','all')
    assert type(df) == pd.DataFrame, 'The function did not return the right datatype.'
