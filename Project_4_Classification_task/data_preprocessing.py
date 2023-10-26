import pandas as pd

def outliers_iqr_mf(data:    pd.DataFrame, 
                    feature: str, 
                    left:    int = 1.5, 
                    right:   int = 1.5):
    """
        Анализ выбросов по методу Тьюки

    Args:
        data (pd.DataFrame):   Исходный набор данных
        feature (str):         Название признака
        left (int, optional):  Левая граница. Defaults to 1.5.
        right (int, optional): Правая граница. Defaults to 1.5.

    Returns:
        outliers (pd.DataFrame): Выбросы
        cleaned (pd.DataFrame):  Очищенные данные
    """
    
    x = data[feature]
    quartile_1, quartile_3 = x.quantile(0.25), x.quantile(0.75),
    
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * left)
    upper_bound = quartile_3 + (iqr * right)
    print(f'lower_bound: {round(lower_bound)}, upper_bound: {round(upper_bound)}')
    
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x >= lower_bound) & (x <= upper_bound)]
    
    return outliers, cleaned