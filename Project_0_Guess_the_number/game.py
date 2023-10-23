"""
    Игра угадай число.
    Компьютер сам загадывает и угадывает число
"""

import numpy as np

def adaptive_random_guess(number:int=1) -> int:
    """
        Компьютер использует алгоритм слчуйчного угадывания 
        c учетом информации о том, больше или меньше 
        случайное число нужного нам числа.

    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    
    count       = 0
    min_number  = 1
    max_number  = 100
    
    while True:
        count += 1
        predict_number = np.random.randint(min_number, max_number + 1)
        
        if number > predict_number:
            min_number = predict_number
        elif number < predict_number:
            max_number = predict_number
        else:
            break

    return(count)


def binary_search_predict(number: int = 1) -> int:
    """
        Компьютер использует алгоритм бинарного поиска
        для угадывания числа от 1 до 100.

    Args:
        number (int, optional): Загаданное число. Defaults to 1.

    Returns:
        int: Число попыток
    """
    
    count = 0
    min_number = 1
    max_number = 100
    
    while True:
        count += 1
        predict_number = (min_number + max_number) // 2
        
        if number > predict_number:
            min_number = predict_number + 1
        elif number < predict_number:
            max_number = predict_number - 1
        else:
            break

    return count


def score_games(predict_function) -> int:
    """
        За какое количество попыток в среднем 
        из 1000 подходов угадывает наш алгоритм

    Args:
        predict_function (function): Функция угадывания

    Returns:
        int: Среднее количество попыток
    """
    
    count_ls = []
    np.random.seed(1)
    random_array = np.random.randint(1, 101, size=(1000))
    
    for number in random_array:
        count_ls.append(predict_function(number))
    
    score = int(np.mean(count_ls))
    
    return(score)

if __name__ == '__main__':
    print("Результаты для алгоритма случайного угадывания:")
    score_games(adaptive_random_guess)
    print("\nРезультаты для алгоритма бинарного поиска:")
    score_games(binary_search_predict)