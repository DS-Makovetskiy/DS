import pandas as pd
import numpy as np


def date_conversion(df:     pd.DataFrame, 
                    title:  str) -> pd.DataFrame:
    """
        Преобразование даты из unix формата в DateTime

    Args:
        df (pd.DataFrame): DataFrme
        title (str):       Признак

    Returns:
        pd.DataFrame: Преобразованный DataFrame
    """
    
    df['date']  = pd.to_datetime(df[title], unit='ms', origin='unix')
    df          = df.drop(title, axis=1)
    
    return df


def get_memory_usage(df):
    """
    Функция для получения объема занимаемой памяти датафрейма.

    Параметры:
    - df: pandas.DataFrame, входной датафрейм.

    Возвращает:
    - float, объем занимаемой памяти в мегабайтах.
    """
    
    memory_usage = df.memory_usage(deep=True).sum() / (1024**2)  # в мегабайтах
    
    return memory_usage.round(1)


def optimize_numeric_columns(df):
    """
    Оптимизирует типы данных числовых столбцов DataFrame в зависимости от диапазона значений.
    
    Параметры:
    - df: pd.DataFrame, входной DataFrame.
    
    Возвращает:
    - pd.DataFrame, оптимизированный DataFrame.
    """
    optimized_df = df.copy()

    for col in df.select_dtypes(include=[np.number]).columns:
        col_data = df[col]
        col_min, col_max = col_data.min(), col_data.max()

        int_types = [np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64]
        float_types = [np.float32, np.float64]

        for int_type in int_types:
            if np.issubdtype(col_data.dtype, np.integer) and col_min >= np.iinfo(int_type).min and col_max <= np.iinfo(int_type).max:
                optimized_df[col] = col_data.astype(int_type)
                break

        for float_type in float_types:
            if np.issubdtype(col_data.dtype, np.floating) and col_min >= np.finfo(float_type).min and col_max <= np.finfo(float_type).max:
                optimized_df[col] = col_data.astype(float_type)
                break

    return optimized_df


def ilif(df):
    """
    identify_low_information_features
    Определяет неинформативные числовые признаки в DataFrame.

    Параметры:
    - df (pd.DataFrame): DataFrame, содержащий числовые признаки.

    Возвращает:
    - low_information_cols (list): Список названий неинформативных признаков.

    Функция анализирует каждый числовой признак в DataFrame и определяет его как неинформативный,
    если либо доля наиболее часто встречающегося значения превышает 95%, либо отношение уникальных
    значений к общему числу значений превышает 95%.
    """
    # список неинформативных признаков
    low_information_cols = [] 

    for col in df.columns:
        top_freq = df[col].value_counts(normalize=True).max()
        nunique_ratio = df[col].nunique() / df[col].count()

        if top_freq > 0.95:
            low_information_cols.append(col)
            print(f'{col}: {round(top_freq*100, 2)}% одинаковых значений')

        if nunique_ratio > 0.95:
            low_information_cols.append(col)
            print(f'{col}: {round(nunique_ratio*100, 2)}% уникальных значений')

    # return low_information_cols


def create_dataframe(df, visitor_list):

    array_for_df = []
    for index in visitor_list:

        #создаем новый df, в котором visitorid равен index
        v_df = df[df['visitorid'] == index]

        temp = []
        #добавляем индексы
        temp.append(index)

        #добавляем общее количество просмотренных уникальных товаров
        temp.append(v_df[v_df.event == 'view'].itemid.unique().size)

        #добавляем общее количество просмотров независимо от типа продукта
        temp.append(v_df[v_df.event == 'view'].event.count())

        #добавляем общее количество покупок
        number_of_items_bought = v_df[v_df.event == 'transaction'].event.count()
        temp.append(number_of_items_bought)

        #Затем поставим ноль либо единицу, если была совершена покупка
        if(number_of_items_bought == 0):
            temp.append(0)
        else:
            temp.append(1)

        array_for_df.append(temp)

    return pd.DataFrame(array_for_df, columns=['visitorid', 'num_items_viewed', 'view_count', 'bought_count', 'purchased'])