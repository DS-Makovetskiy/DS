import numpy as np
import pandas as pd

def get_educational(arg: str) -> str:
    """
        Функция по извлечению уровня образования из строки
        и приведения его к одному из 4 уровней

    Args:
        arg (str): Строка для обработки

    Returns:
        (str): Уровень образования в виде строки
    """
    
    educational_level = [
        'Высшее', 
        'Неоконченное высшее', 
        'Среднее специальное', 
        'Среднее'
    ]
    
    splitted_value = ' '.join(arg.split(' ')[:2])
    
    for value in educational_level:
        if value in splitted_value:
            res = value
            return res


def get_age(arg: str) -> int:
    """
        Функция по извлечению возраста в виде числа

    Args:
        arg (str): Строка для обработки

    Returns:
        (int): Возраст в формате числа
    """
    
    year_list = ['год', 'года', 'лет']
    
    splitted_value = arg.split(' ')
    
    for i, value in enumerate(splitted_value):
       if value in year_list:
           return int(splitted_value[i-1])
       

def get_experience(arg: str) -> float:
    """
        Функция по извлечению опыта работы и преобразованию его
        в виде количества отработанных месяцев

    Args:
        arg (str): Строка для обработки

    Returns:
        (float): Количество отработанных месяцев в числовом формате
    """
    
    month_list = ['месяц', 'месяца', 'месяцев']
    year_list = ['год', 'года', 'лет']
    year, month = 0, 0
    
    if arg == 'Не указано':
        return np.NaN
    elif arg is not np.NaN:
        splitted_value = arg.split(' ')[:6]
        for i, value in enumerate(splitted_value):
            if value in year_list:
                year = int(splitted_value[i-1])
            elif value in month_list:
                month = int(splitted_value[i-1])
        res = year * 12 + month
        return res


def get_cities(arg: str) -> str:
    """
        Функция по извлечению городов и группировки их по категориям

    Args:
        arg (str): Строка для обработки

    Returns:
        (str): Категория города или его название
    """
    
    million_cities = [
        'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 
        'Челябинск', 'Омск', 'Самара', 'Ростов-на-Дону', 
        'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 'Волгоград'
    ]
    
    city = arg.split(',')[0][:-1]
    
    if city in million_cities:
        city = 'город-миллионник'
    elif city not in ['Москва', 'Санкт-Петербург', 'город-миллионник']:
        city = 'другие'
    return city


def get_moving_status(arg: str) -> bool:
    """
        Функция по извлечению статуса готовности к переезду

    Args:
        arg (str): Строка для обработки

    Returns:
        (bool): Возвращает True если готов и False если не готов к переезду
    """
    
    if ('не готов к переезду' in arg) or ('не готова к переезду' in arg):
        return False
    else:
        return True


def get_business_trip(arg: str) -> bool:
    """
        Функция по извлечению статуса готовности к командировкам

    Args:
        arg (str): Строка для обработки

    Returns:
        (bool): Возвращает True если готов и False если не готов к командировкам
    """
    
    business_trip_list = ['готов к редким командировкам', 'готова к командировкам', 
                          'готов к командировкам', 'готова к редким командировкам']
    
    # Более полный список статусов:
    # business_trip_list = ['готов к редким командировкам', 'готова к командировкам', 
    #                       'готов к командировкам', 'готова к редким командировкам', 
    #                       'готов к команд', 'готов к', 'готов к командир']
    
    if arg.split(',')[-1][1:] in business_trip_list:
        return True
    else:
        return False


def get_currency(arg: str) -> str:
    """
        Функция по приведению наименования курсов валют к международному формату

    Args:
        arg (str): Строка для обработки

    Returns:
        (str): Наименование курса валют в международном формате
    """
    
    currency_dict = {
        'USD': 'USD', 'KZT': 'KZT',
        'грн': 'UAH', 'белруб': 'BYN',
        'EUR': 'EUR', 'KGS': 'KGS',
        'сум': 'UZS',  'AZN': 'AZN'
    }
    
    splitted_value = arg.split(' ')[1].replace('.', '')
    
    if splitted_value == 'руб':
        return 'RUB'
    else:
        return currency_dict[splitted_value]


def outliers_z_score(data:      pd.DataFrame, 
                     feature:   str, 
                     log_scale: bool = False, 
                     left:      int  = 3, 
                     right:     int  = 3) -> int:
    """
        Функция реализует алгоритм метода z-отклонения для 
        поиска выбросов в данных

    Args:
        data (pd.DataFrame): DataFrame с данными
        feature (str): Наименование признака
        log_scale (bool, optional): Переключение режима работы функции, 
        в логарифмический масштаб. Если он равен True, то будем 
        логарифмировать рассматриваемый признак, иначе — оставляем 
        его в исходном виде. По умолчанию - False.
        left (int, optional): Количество сигм слева. По умолчанию - 3.
        right (int, optional): Количество сигм справа. По умолчанию - 3.

    Returns:
        outliers (int): Число выбросов по методу z-отклонения
        cleaned (int): Результирующее число записей
    """
    if log_scale:
        x = np.log(data[feature])
    else:
        x = data[feature]
    
    mu    = x.mean()
    sigma = x.std()
    
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned  = data[(x > lower_bound) & (x < upper_bound)]
    
    return outliers, cleaned