import os
import requests
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt


def get_borough_crashes(app_token,borough,start_date,end_date):
    
    """
    Get the collision cases in a specific borough, given the date the user want to consult. 

    Parameters
    ----------
    app_token : the token enables users to access the dataset without limit, can be acquired by resgistering an account on NYC OPEN DATA website.
    borough : string, all capital letters, the name of five boroughs in NYC
    start_date : string, must be format "XXXX-XX-XXT00:00:00", the start date of collision that the user want to consult
    end_date: string, must be format "XXXX-XX-XXT00:00:00", the end date of collision that the user want to consult

    Returns
    -------
    dataframe

    """
    
    params = {
        '$$app_token':app_token
    }
    
    end_point = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=1000000"
    filter_total = "&$WHERE=crash_date between '{}' and '{}' AND borough='{}'".format(start_date,end_date,borough)
    r = requests.get(end_point+filter_total)
    
    if r.status_code != 200:
        print('Error occurs: {}'.format(r.status_code))
    else:
        df = pd.json_normalize(r.json())
        return df


### zipcode
def get_zipcode_crashes(app_token,zipcode,start_date,end_date):
    
    """
    Get the collision cases in a specific zipcode area, given the date the user want to consult. 

    Parameters
    ----------
    app_token : the token enables users to access the dataset without limit, can be acquired by resgistering an account on NYC OPEN DATA website.
    zipcode : a string of five numbers, referring to a zipcode area.
    start_date : string, must be format "XXXX-XX-XXT00:00:00", the start date of collision that the user want to consult
    end_date: string, must be format "XXXX-XX-XXT00:00:00", the end date of collision that the user want to consult

    Returns
    -------
    dataframe

    """
    
    params = {
        '$$app_token':app_token
    }
    
    end_point = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=1000000"
    filter_total = "&$WHERE=crash_date between '{}' and '{}' AND zip_code = '{}'".format(start_date,end_date,zipcode)
    
    r = requests.get(end_point+filter_total)
    
    if r.status_code != 200:
        print('Error occurs: {}'.format(r.status_code))
    else:
        
        df = pd.json_normalize(r.json())
        return df

    
### get the borough ranked by number of crashes
def get_crashes_count_by_boroughs(app_token,start_date,end_date):
    
    """
    Get the number of collision cases group by borough, given the date the user want to consult. 

    Parameters
    ----------
    app_token : the token enables users to access the dataset without limit, can be acquired by resgistering an account on NYC OPEN DATA website.
    borough : string, all capital letters, the name of five boroughs in NYC
    start_date : string, must be format "XXXX-XX-XXT00:00:00", the start date of collision that the user want to consult
    end_date: string, must be format "XXXX-XX-XXT00:00:00", the end date of collision that the user want to consult

    Returns
    -------
    dataframe
    """
    
    params = {
        '$$app_token':app_token
    }
    
    end_point = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=1000000"
    filter_select = "&$SELECT=borough,count(*) AS number_of_crashes&$GROUP=borough&$ORDER=number_of_crashes DESC"
    filter_where = "&$WHERE=crash_date between '{}' and '{}' AND borough IS NOT NULL".format(start_date, end_date)

    r = requests.get(end_point+filter_select+filter_where)

    if r.status_code != 200:
        print('Error occurs: {}'.format(r.status_code))
    else:
        
        df = pd.json_normalize(r.json())
        return df
    
    
# map according to the number of crashes by zipcode

def get_heatmap(app_token,start_date,end_date):
    
    """
    create a heatmap, showing which zip code area have more collision cases in a given time. 

    Parameters
    ----------
    app_token : the token enables users to access the dataset without limit, can be acquired by resgistering an account on NYC OPEN DATA website.
    start_date : string, must be format "XXXX-XX-XXT00:00:00", the start date of collision that the user want to consult
    end_date: string, must be format "XXXX-XX-XXT00:00:00", the end date of collision that the user want to consult

    Returns
    -------
    graph
    """
    
    params = {
        '$$app_token':app_token
    }
    
    end_point = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=1000000"
    filter_select = "&$SELECT=zip_code,count(*) AS number_of_crashes&$GROUP=zip_code&$ORDER=number_of_crashes DESC"
    filter_where = "&$WHERE=crash_date between '{}' and '{}' AND zip_code IS NOT NULL".format(start_date, end_date)
    
    r = requests.get(end_point+filter_select+filter_where)
    
    if r.status_code != 200:
        print('Error occurs: {}'.format(r.status_code))
    else:
        df = pd.json_normalize(r.json())
        df['ZIPCODE']=df['zip_code']

        import pkg_resources
        my_file = pkg_resources.resource_filename('nyc_crash_api', 'ZIP_CODE_040114/ZIP_CODE_040114.shp')
        shapefile = gpd.read_file(my_file)

        df_map = df.merge(shapefile, on="ZIPCODE").iloc[:,1:]
        df_map = GeoDataFrame(df_map)
        df_map = df.merge(shapefile, on="ZIPCODE").iloc[:,1:]
        df_map = GeoDataFrame(df_map)

        fig, ax = plt.subplots(1, figsize=(12, 12))
        plt.xticks(rotation=90)

        bar_info = plt.cm.ScalarMappable(cmap="Reds", norm=plt.Normalize(vmin=0, vmax=120))
        bar_info._A = []
        cbar = fig.colorbar(bar_info)

        return df_map.plot(column='number_of_crashes',cmap="Reds", linewidth=0.4, ax=ax, edgecolor=".4")
    
    
def get_time_cycle(app_token,start_date,end_date,borough):
    
    """
    get the count number of crash cases trend by time in a specific borough (or all city), given the date the user want to consult. 

    Parameters
    ----------
    app_token : the token enables users to access the dataset without limit, can be acquired by resgistering an account on NYC OPEN DATA website.
    start_date : string, must be format "XXXX-XX-XXT00:00:00", the start date of collision that the user want to consult
    end_date: string, must be format "XXXX-XX-XXT00:00:00", the end date of collision that the user want to consult
    borough : string, the name of five boroughs in NYC in capital letters, or "all" to refer to all city


    Returns
    -------
    dataframe

    """
    
    params = {
        '$$app_token':app_token
    }
    
    end_point = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=1000000"
    filter_borough = "&$WHERE=crash_date between '{}' and '{}' AND borough='{}'".format(start_date, end_date,borough)
    filter_all_borough = "&$WHERE=crash_date between '{}' and '{}'".format(start_date, end_date)
    if borough == 'all':
        r = requests.get(end_point+filter_all_borough)
    else:
        r = requests.get(end_point+filter_borough)
        
    if r.status_code != 200:
        print('Error occurs: {}'.format(r.status_code))
    else:
        df = pd.json_normalize(r.json())

        for i in ['number_of_persons_injured','number_of_persons_killed','number_of_pedestrians_injured','number_of_pedestrians_killed', 'number_of_cyclist_injured',
                 'number_of_cyclist_killed', 'number_of_motorist_injured','number_of_motorist_killed']:
            df[i] = pd.to_numeric(df[i])
        df['crash_hour'] = df['crash_time'].apply(lambda x:x.split(':')[0])
        df_time = df[['number_of_persons_injured','number_of_persons_killed','number_of_pedestrians_injured','number_of_pedestrians_killed', 'number_of_cyclist_injured',
                 'number_of_cyclist_killed', 'number_of_motorist_injured','number_of_motorist_killed']].groupby(df['crash_hour']).sum().reset_index()
        df_time['crash_hour'] = pd.to_numeric(df_time['crash_hour'])
        return df_time.sort_values('crash_hour')

    
def get_contributing_factors(app_token,start_date,end_date,borough):
    
    """
    get the ranking of contributing facotrs of crashes in the order of the number of the crash cases a specifc facotr involved.

    Parameters
    ----------
    app_token : the token enables users to access the dataset without limit, can be acquired by resgistering an account on NYC OPEN DATA website.
    start_date : string, must be format "XXXX-XX-XXT00:00:00", the start date of collision that the user want to consult
    end_date: string, must be format "XXXX-XX-XXT00:00:00", the end date of collision that the user want to consult
    borough : string, the name of five boroughs in NYC in capital letters, or "all" to refer to all city


    Returns
    -------
    dataframe

    """
    
    params = {
        '$$app_token':app_token
    }
    
    end_point = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=1000000"
    filter_select = "&$SELECT=contributing_factor_vehicle_1,contributing_factor_vehicle_2,contributing_factor_vehicle_3"
    
    filter_borough = "&$WHERE=crash_date between '{}' and '{}' AND borough='{}'".format(start_date, end_date,borough)
    filter_all_borough = "&$WHERE=crash_date between '{}' and '{}'".format(start_date, end_date)
    
    if borough == 'all':
        r = requests.get(end_point+filter_select+filter_all_borough)
    else:
        r = requests.get(end_point+filter_select+filter_borough)

    if r.status_code == 200:
        df = pd.json_normalize(r.json())
        count = pd.DataFrame(df.unstack().dropna().reset_index(drop=True).value_counts(),columns=['COUNT'])
        return count
    else:
        print('Error occurs: {}'.format(r.status_code))
        
        
def get_vehicle_type(app_token,start_date,end_date,borough):
    
    """
    get the ranking of vehicle types of crashes in the order of the number of crash cases a vehicle type involved.

    Parameters
    ----------
    app_token : the token enables users to access the dataset without limit, can be acquired by resgistering an account on NYC OPEN DATA website.
    start_date : string, must be format "XXXX-XX-XXT00:00:00", the start date of collision that the user want to consult
    end_date: string, must be format "XXXX-XX-XXT00:00:00", the end date of collision that the user want to consult
    borough : string, the name of five boroughs in NYC in capital letters, or "all" to refer to all city


    Returns
    -------
    dataframe
    """
    
    params = {
        '$$app_token':app_token
    }
    
    end_point = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=1000000"
    filter_select = "&$SELECT=vehicle_type_code1,vehicle_type_code2"
    
    filter_borough = "&$WHERE=crash_date between '{}' and '{}' AND borough='{}'".format(start_date, end_date,borough)
    filter_all_borough = "&$WHERE=crash_date between '{}' and '{}'".format(start_date, end_date)
    
    if borough == 'all':
        r = requests.get(end_point+filter_select+filter_all_borough)
    else:
        r = requests.get(end_point+filter_select+filter_borough)
    
    if r.status_code == 200:
        df = pd.json_normalize(r.json())
        count = pd.DataFrame(df.unstack().dropna().reset_index(drop=True).value_counts(),columns=['COUNT'])
        return count
    else:
        print('Error occurs: {}'.format(r.status_code))

        
