# Проект 5. Задача регрессии

## Оглавление  
[1. Постановка задачи](#Постановка-задачи)  
[2. Бизнес-задача](#Бизнес-задача)  
[3. Техническая задача](#Техническая-задача)  
[4. Цель проекта](#Цель-проекта)  
[5. Этапы проекта](#Этапы-проекта)  
[6. Метрика качества](#Метрика-качества)  


## Постановка задачи
Представьте, что вы заказываете такси из одной точки Нью-Йорка в другую, причём необязательно, что конечная точка должна находиться в пределах города. Сколько вы должны будете заплатить за поездку?

Известно, что стоимость такси в США рассчитывается на основе фиксированной ставки и тарифной стоимости, величина которой зависит от времени и расстояния. Тарифы варьируются в зависимости от города.

В свою очередь, время поездки зависит от множества факторов, таких как направление поездки, время суток, погодные условия и так далее.

Необходимо разработать алгоритм, способный определять длительность поездки. Так мы сможем прогнозировать стоимость поездки самым тривиальным образом, например, просто умножая стоимость на заданный тариф.

## Бизнес-задача
Определить характеристики и с их помощью спрогнозировать длительность поездки на такси.

## Техническая задача  
Построить модель машинного обучения, которая на основе предложенных характеристик клиента будет предсказывать числовой признак — время поездки такси, то есть решить задачу регрессии.

## Цель проекта
* Сформировать набор данных на основе нескольких источников информации.
* Спроектировать новые признаки с помощью Feature Engineering и выявить наиболее значимые при построении модели.
* Исследовать предоставленные данные и выявить закономерности.
* Построить несколько моделей и выбрать из них ту, которая показывает наилучший результат по заданной метрике.
* Спроектировать процесс предсказания длительности поездки для новых данных.
* Загрузить своё решение на платформу Kaggle.

## Этапы проекта
1. Первичная обработка данных
2. Разведывательный анализ данных (EDA)
3. Отбор и преобразование признаков
4. Решение задачи регрессии: линейная регрессия и деревья решений
5. Решение задачи регрессии: ансамбли моделей и построение прогноза

## Метрика качества
Результаты оцениваются по метрике RMSLE


[&#8679; к оглавлению](#оглавление)