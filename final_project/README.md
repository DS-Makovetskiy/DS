# Итоговый проект первого года обучения. Агентство недвижимости

## Оглавление  
[1. Какой кейс решаем?](#какой-кейс-решаем)  
[2. Цель проекта](#цель-проекта)  
[3. Задачи проекта](#задачи-проекта)  
[4. Метрика качества](#метрика-качества)  

## Описание проекта
К вам обратился представитель крупного агентства недвижимости со следующей проблемой:

«Мои риелторы тратят катастрофически много времени на сортировку объявлений и поиск выгодных предложений. Поэтому их скорость реакции, да и, сказать по правде, качество анализа не дотягивают до уровня конкурентов. Это сказывается на наших финансовых показателях. 

Ваша задача — разработать модель, которая позволила бы обойти конкурентов по скорости и качеству совершения сделок».

## Задача проекта  
**Бизнес-задача:** определить характеристики для быстрой оценки стоимости объекта недвижимости, не тратя время на сортировку объявлений и поиск выгодных предложений, что позволило бы обойти конкурентов по скорости и качеству сделок.

**Техническая задача:** создать модель машинного обучения, которая на основе предложенных признаков объекта недвижимости будет прогнозировать его стоимость.

## Описание признаков
* **status** (статус недвижимости)
* **private pool** (наличие бассейна)
* **propertyType** (тип недвижимости)
* **street** (улица)
* **baths** (количество ваных комнат)
* **homeFacts** (информация об объекте недвижимости)
* **fireplace** (наличие камина)
* **city** (город)
* **schools** (школы)
* **sqft** (площадь)
* **zipcode** (почтовый индекс)
* **beds** (количество спален)
* **state** (штат)
* **stories** (этажи)
* **mls-id** (номер службы множественного листинга)
* **PrivatePool** (наличие бассейна)
* **MlsId** (номер службы множественного листинга)
* **target** (цена недвижимости, целевая переменная)

## Метрика качества
Результаты оцениваются по метрике **MAPE**

## Сравне метрик разных моделей машинного обучения
Model | MAPE | MAE
---|---|---
Stacking Regressor | 3.997 | 23.766
Random Forest | 4.179 | 23.333
XGBoost | 6.967 | 38.559
CatBoost Regressor | 7.667 | 37.919
Baseline | 21.049 | 182.162
Linear Regression | 24.655 | 168.366

## Ссылки на наборы данных и сохраненную модель

[Исходный набор данных](https://drive.google.com/file/d/1NN3ru8Qe-yIeGzFCGtMgoaxPjIIMKu37/view?usp=sharing)  
[Обработанный набор данных](https://drive.google.com/file/d/1P-lBGvHg6D9tYO6iL0bf7hXlrI4SyWi7/view?usp=sharing)

[Сохраненная модель StackingRegressor](https://drive.google.com/file/d/18Na5_7uHvFkkHOTLQKIzqeDGYUZLN4F6/view?usp=sharing)


[:arrow_up: к оглавлению](#Оглавление)