import pandas as pd
import re
from IPython.display import display

def search_null_values(df: pd.DataFrame):
    """
        Функция по определению пропусков в признаках

    Args:
        df (pd.DataFrame): DataFrame, в котором необходимо 
        обнаружить пропуски
    """
    
    null_cols = df.isnull().sum()

    if null_cols.mean() > 0:
        print('Количество пропусков в признаках:')
        display(null_cols[null_cols > 0])
    else:
        print('Пропусков не обнаружено')


def clean_tags(arg: str) -> list:
    """
        Функция по очистке тегов и приведения их к списку

    Args:
        arg (str): Исходная строка для преобразования

    Returns:
        list: Очищенный список тегов
    """
    
    tmp      = arg.replace("[' ", "").replace(" ']", '')
    tag_list = tmp.split(" ', ' ")
    
    return tag_list


def get_number_of_nights(arg: list) -> int:
    """
        Функция по извлечению количества проведенных
        ночей из тегов в отдельный признак.

    Args:
        arg (list): Список тегов

    Returns:
        int: Количество проведенных ночей
    """
    stayed_n_nights = r'Stay.*\s.*\snight.*'
    
    for el in arg:
        if re.findall(stayed_n_nights, el):
            return el.split()[1]