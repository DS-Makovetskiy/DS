import pandas as pd
import numpy as np
from sklearn import cluster

def add_datetime_features(df: pd.DataFrame) -> pd.DataFrame:
    """
        Принимает на вход DataFrame и извлекает  
        дополнительные три признака - дата, час и 
        день недели, в которые был включен счетчик. 

    Args:
        df (pd.DataFrame): Набор с данными

    Returns:
        pd.DataFrame: Обновленный DataFrame
    """
    
    df['pickup_date'] = df['pickup_datetime'].dt.date
    df['pickup_date'] = pd.to_datetime(df['pickup_date'])
    
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_day_of_week'] = df['pickup_datetime'].dt.day_name()
    
    return df


def add_holiday_features(taxi_df:    pd.DataFrame, 
                         holiday_df: pd.DataFrame) -> pd.DataFrame:
    """
        Принимает на вход DataFrame с данными о поездках и 
        праздничных днях. Добавляет признак "pickup_holiday" 
        с ключом "1", если поездка начата в праздничный день 
        и "0" если в обычный день.

    Args:
        taxi_df    (pd.DataFrame): Данные о поездках
        holiday_df (pd.DataFrame): Данные о праздничных днях

    Returns:
        pd.DataFrame: Обновленный DataFrame
    """
    
    holiday_df['date'] = pd.to_datetime(holiday_df['date'])
    
    merged = taxi_df.merge(
        holiday_df[['date']],
        left_on = 'pickup_date',
        right_on = 'date',
        how='left'
    )
    
    merged['date'] = merged['date'].fillna(0)
    merged['date'] = merged['date'].apply(lambda x: x if x == 0 else 1)
    merged = merged.rename(columns={'date':'pickup_holiday'})
    
    return merged


def add_osrm_features(taxi_df: pd.DataFrame, 
                      osrm_df: pd.DataFrame) -> pd.DataFrame:
    """
        Принимает на вход DataFrame с данными о поездках и 
        данными их OSRM. Объеденяет данные по признаку "id"
        и добавляет признаки - "total_distance", 
        "total_travel_time", "number_of_steps".

    Args:
        taxi_df (pd.DataFrame): Данные о поездках
        osrm_df (pd.DataFrame): Данные из OSRM

    Returns:
        pd.DataFrame: Обновленный DataFrame
    """
    
    merged = taxi_df.merge(
        osrm_df[['id', 'total_distance', 'total_travel_time', 'number_of_steps']],
        on = 'id',
        how='left'
    )
    
    return merged


def get_haversine_distance(lat1: pd.Series, 
                           lng1: pd.Series, 
                           lat2: pd.Series, 
                           lng2: pd.Series):
    """
        Функция для вычисления расстояния Хаверсина (в километрах)

    Args:
        lat1 (pd.Series): вектор-столбец с широтой первой точки
        lng1 (pd.Series): вектор-столбец с долготой первой точки
        lat2 (pd.Series): вектор-столбец с широтой второй точки
        lng2 (pd.Series): вектор-столбец с долготой второй точки

    Returns:
        str: расстояние между двумя точками на сфере (в километрах)
    """
    
    # переводим углы в радианы
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    
    # радиус земли в километрах
    EARTH_RADIUS = 6371 
    
    # считаем кратчайшее расстояние h по формуле Хаверсина
    lat_delta = lat2 - lat1
    lng_delta = lng2 - lng1
    d = np.sin(lat_delta * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng_delta * 0.5) ** 2
    h = 2 * EARTH_RADIUS * np.arcsin(np.sqrt(d))
    
    return h


def get_angle_direction(lat1: pd.Series, 
                        lng1: pd.Series, 
                        lat2: pd.Series, 
                        lng2: pd.Series):
    """
        Функция для вычисления угла направления движения (в градусах)

    Args:
        lat1 (pd.Series): вектор-столбец с широтой первой точки
        lng1 (pd.Series): вектор-столбец с долготой первой точки
        lat2 (pd.Series): вектор-столбец с широтой второй точки
        lng2 (pd.Series): вектор-столбец с долготой второй точки

    Returns:
        str: угол направления движения от первой точки ко второй
    """
    
    # переводим углы в радианы
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    
    # считаем угол направления движения alpha по формуле угла пеленга
    lng_delta_rad = lng2 - lng1
    y = np.sin(lng_delta_rad) * np.cos(lat2)
    x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lng_delta_rad)
    alpha = np.degrees(np.arctan2(y, x))
    
    return alpha


def add_geographical_features(df:pd.DataFrame) -> pd.DataFrame:
    """
        Принимает на вход DataFrame с данными о поездках и добавляет
        в него два признака: "haversine_distance" - расстояние 
        Харвесина между точками и "direction" - направление движения.
        Затем возвращает обновленный DataFrame

    Args:
        df (pd.DataFrame): Исходный набор данных

    Returns:
        pd.DataFrame: Обновленный набор данных
    """
    
    df['haversine_distance'] = get_haversine_distance(
                                    df['pickup_latitude'],
                                    df['pickup_longitude'],
                                    df['dropoff_latitude'],
                                    df['dropoff_longitude']
                               )
    
    df['direction'] = get_angle_direction(
                            df['pickup_latitude'],
                            df['pickup_longitude'],
                            df['dropoff_latitude'],
                            df['dropoff_longitude']
                      )
    
    return df


def add_cluster_features(taxi_df:        pd.DataFrame, 
                         kmeans_cluster: cluster.KMeans) -> pd.DataFrame:
    """
        Принимает на вход таблицу с данными о поездках и обученный 
        алгоритм кластеризации, добавляет признак geo_cluster с 
        информацией о географическом кластере, к которому относится поездка

    Args:
        taxi_df        (pd.DataFrame):   Исходный набор данных
        kmeans_cluster (cluster.kmeans): Обученный алгоритм кластеризации 

    Returns:
        pd.DataFrame: Обновленный набор данных
    """
    
    taxi_df['geo_cluster'] = kmeans_cluster.predict(taxi_df[['pickup_latitude', 'pickup_longitude',
                                                             'dropoff_latitude', 'dropoff_longitude']].values)
    
    return taxi_df


def add_weather_features(taxi_df:    pd.DataFrame, 
                         weather_df: pd.DataFrame) -> pd.DataFrame:
    """
        Принимает на вход DataFrame с данными о поездках и данными о 
        погодных условиях на каждый час, добавляет новые признаки с 
        информацией о температуре, видимости, скорости ветра, 
        количества осадков и погодных явлениях.

    Args:
        taxi_df    (pd.DataFrame): Данные о поездках
        weather_df (pd.DataFrame): Данные о погодных условиях

    Returns:
        pd.DataFrame: Обновленный набор данных
    """
    weather_df['time'] = pd.to_datetime(weather_df['time'])
    weather_df['date'] = pd.to_datetime(weather_df['time'].dt.date)
    weather_df['hour'] = weather_df['time'].dt.hour

    weather_df = weather_df.drop('time', axis=1)

    merged = taxi_df.merge(
        weather_df,
        left_on=['pickup_date', 'pickup_hour'],
        right_on=['date', 'hour'],
        how='left'
    )

    merged = merged.drop(['date', 'hour'], axis=1)

    return merged


def fill_null_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
        Принимает на вход DataFrame с данными о поездках и заполняет
        пропуски в данных медианным значением.

    Args:
        df (pd.DataFrame): Исходный набор данных

    Returns:
        pd.DataFrame: Обновленный набор данных
    """
    
    df['temperature'] = df['temperature'].fillna(df.groupby('pickup_date')['temperature'].transform('median'))
    df['visibility']  = df['visibility'].fillna(df.groupby('pickup_date')['visibility'].transform('median'))
    df['wind speed']  = df['wind speed'].fillna(df.groupby('pickup_date')['wind speed'].transform('median'))
    df['precip']      = df['precip'].fillna(df.groupby('pickup_date')['precip'].transform('median'))
    
    df['events'] = df['events'].fillna('None')
    
    df['total_distance']    = df['total_distance'].fillna(df['total_distance'].median())
    df['total_travel_time'] = df['total_travel_time'].fillna(df['total_travel_time'].median())
    df['number_of_steps']   = df['number_of_steps'].fillna(df['number_of_steps'].median())
    
    return df