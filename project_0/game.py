"""Игра угадай число.
Компьютер сам загадывает и угадывает число
"""

import numpy as np

def random_predict(number:int=1) -> int:
    """Компьютер случайным образом загадывает число от 1 (min_number) до 100 (max_number)
       c учетом информации о том, больше или меньше случайное число нужного нам числа.

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
        predict_number = np.random.randint(min_number, max_number + 1)
        
        if number > predict_number:
            min_number = predict_number
        elif number < predict_number:
            max_number = predict_number
        else:
            break

    return(count)


def score_games(random_predict) -> int:
    """За какое количество попыток в среднем из 1000 подходов угадывает наш алгоритм

    Args:
        random_predict ([type]): функция угадывания

    Returns:
        int: среднее количество попыток
    """
    
    count_ls = []
    np.random.seed(1)
    random_array = np.random.randint(1, 101, size=(1000))
    
    for number in random_array:
        count_ls.append(random_predict(number))
    
    score = int(np.mean(count_ls))
    
    print(f"Ваш алгоритм угадывает число в среднем за: {score} попыток")
    return(score)

if __name__ == '__main__':
    score_games(random_predict)