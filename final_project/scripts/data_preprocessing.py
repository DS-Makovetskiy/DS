import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re



def sns_barplot(data:   pd.DataFrame, 
                title:  str     = '',
                size:   tuple   = (12, 4),
                rotate: int     = 30,
                ylim            = None):
    """
    Визуализация данных при помощи столбчатой
    диаграммы

    Args:
        data (pd.DataFrame):    набор данных
        title  (str):           описание
        size   (tuple):         размер диаграммы
        rotate (int):           угол вращения
        ylim:                   лимит оси y
    """
    
    fig, ax = plt.subplots(figsize=size)

    sns.barplot(
        data=data,
        x=data.columns[0],
        y=data.columns[1]
    )
    ax.xaxis.set_tick_params(rotation=rotate)
    plt.title(
        title, 
        fontweight='bold', 
        fontsize=14
    )
    plt.ylim(ylim);


def HF_feature_extraction(record: str) -> pd.Series:
    """
    Функция для извлечения новых признаков из
    списка словарей признака 'homeFacts' 

    Args:
        record (str): Список словарей

    Returns:
        pd.Series: Обработанный набор данных
    """
    features = {}
    for item in record:
        label = item['factLabel']
        value = item['factValue']
        features[label] = value
    return pd.Series(features)


def df_value_counts(data:       pd.Series,
                    value:      str = 'Значение',
                    count:      str = 'Кол-во',
                    percent:    str = 'Доля %') -> pd.DataFrame:
    """
    Формирование мини датасета 
    с количеством и долей каждого из значений

    Args:
        data (pd.Series):           признак
        value (str, optional):      имя признака значений.
                                    Defaults to 'Значение'.
        count (str, optional):      имя признака количества. 
                                    Defaults to 'Кол-во'.
        percent (str, optional):    имя признака доли. 
                                    Defaults to 'Доля %'.

    Returns:
        pd.DataFrame: _description_
    """
    
    data_values     = data.value_counts()
    data_percent    = round(data.value_counts(normalize=True) * 100, 1)

    value_count_df  = pd.DataFrame({
        value:  data_values.index,
        count:   data_values.values,
        percent:   data_percent
    }).sort_values(by='Кол-во', ascending=False, ignore_index=True)

    print(f'Количество уникальных значений: {data.nunique()}')
    
    return value_count_df


def sns_barplot_binary(data:        pd.Series,
                       title:       str,
                       xticklabels: list = ['Есть', 'Нет']):
    """
    Визуализация графика из бинарного признака (содержит 0 и 1)

    Args:
        data (pd.Series):               Признак
        title (str):                    Заголовок
        xticklabels (list, optional):   Подпись оси X. 
                                        Defaults to ['Есть', 'Нет'].
    """
    
    data_vc = data.value_counts(normalize=True) * 100

    fig, ax = plt.subplots(figsize=(4, 3))

    sns.barplot(
        data=data_vc,
        x=data_vc.index,
        y=data_vc.values
    )
    plt.title(
        title, 
        fontweight='bold', 
        fontsize=14
    )

    # Добавление меток над столбцами
    ax.text(
        data_vc.index[0], 
        data_vc.values[1] + 2, 
        f'{data_vc.values[1]:.1f}%', 
        ha='center'
    )
    ax.text(
        data_vc.index[1], 
        data_vc.values[0] + 2, 
        f'{data_vc.values[0]:.1f}%', 
        ha='center'
    )

    ax.set_xticklabels(xticklabels)
    ax.set_xlabel('')
    ax.set_ylim(0, 100);


def clean_school_rating(lst: list) -> list:
    """
    Очистка признака df['schools_rating']

    Args:
        lst (list): Список для обработки

    Returns:
        list: Обработанный список значений
    """
    
    clean_lst = []
    for value in lst:
        if isinstance(value, str):
            if value.upper() in ['NR', 'NA']:                   # заменяем 'NR' и 'NA' на np.nan
                clean_lst.append(np.nan)
            else:
                clean_value = re.sub(r'(/10|None)', '', value)  # Заменяем '/10' и 'None' на ''
                clean_lst.append(clean_value)
        else:
            clean_lst.append(value)
    return clean_lst


def missing_values(data: pd.Series,
                   zero: bool = False):
    """
    Функция подсчитывает количество пропущенных
    и нулевых значений в признаке

    Args:
        data (pd.Series):       признак
        zero (bool, optional):  считать нулевые значения?. 
                                Defaults to False.
    """
    
    # количество пропусков
    nan_count   = data.isna().sum()
    nan_percent = round((nan_count / data.shape[0]) * 100)
    print(f'Количество пропущенных значений {nan_count}, что составляет {nan_percent} % от общего количества записей')
    
    if zero:
        # количество нулевых значений
        zero_count = sum(data == 0)
        zero_percent = round((zero_count / data.shape[0]) * 100)
        print(f'Количество нулевых значений {zero_count}, что составляет {zero_percent} % от общего количества записей')


def count_schools_grades(row:   list, 
                         grade: str) -> int:
    """
    Функция для подсчета вхождений интервалов в списке значений

    Args:
        row (list):     список оценок школ
        grade (str):    оценка, которая будет посчитана

    Returns:
        int:            количество школ с выбранной оценкой
    """
    
    count = 0
    for value in row:
        if grade in value:
            count += 1
    return count


def check_empty_nan(lst: list):
    """
    Функция для проверки наличия пустых или NaN значений в списке

    Args:
        lst (list): список значений
    """
    return any(pd.isnull(lst)) or any(x == '' for x in lst)


def clean_school_values(lst: list) -> list:
    """Очистка признака от пустных значений

    Args:
        lst (list): список значений

    Returns:
        list: очищенный список
    """
    clean_lst = []
    for value in lst:
        if isinstance(value, str):
            clean_value = re.sub(r'(mi|None|N\/A)', '', value)
            clean_lst.append(clean_value.strip())
        else:
            clean_lst.append(value)
    return clean_lst


def convert_to_sqft(value: str) -> str:
    """
    Функция для конвертации площади из 'acre' в 'sqft'

    Args:
        value (str):    значение площади

    Returns:
        str:            значение площади в sqft
    """
    
    if isinstance(value, str):
        acres = re.search(r'cre', value)
        if acres:
            value = re.sub(r'[^0-9\.\,\s]', '', value).strip()
            value = value.replace(',', '.')
            
            parts = value.split('.')[:2]
            value = '.'.join(parts)
            
            value = float(value) * 43560
            return value
    return value


def outliers_z_score_mod(data, feature, log_scale=False, left=1.5, right=1.5):
    if log_scale:
        x = np.log(data[feature]+1)
    else:
        x = data[feature]
    mu = x.mean()
    sigma = x.std()
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x > lower_bound) & (x < upper_bound)]
    return outliers, cleaned