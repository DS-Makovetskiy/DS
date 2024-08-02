import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Установка глобальных параметров
pd.set_option('display.max_columns', 60)
plt.rcParams['figure.figsize'] = (12, 4)


# def get_top5_for_genre(df, genre, column_list=['title', 'score', 'price', 'contentRating'], sort_by='score'):
#     return df[df[genre] == genre][column_list].sort_values(sort_by, ascending=False).head(5)

def get_top5_for_genre(df, genre):
    return df[df[genre] == genre][['title', genre, 'score', 'price', 'contentRating']].sort_values('score', ascending=False).head(5)

def count_features_per_genre(df, genres_list, title, xlabel, ylabel):
    # Подсчет количества игр в каждом жанре
    genre_counts = df[genres_list].count()

    # Определение индексов трёх наибольших значений
    top3_indices = genre_counts.nlargest(3).index
    # Цвета для столбцов
    colors = ['skyblue' if genre not in top3_indices else 'orange' for genre in genre_counts.index]

    # Построение гистограммы популярности жанров
    genre_counts.plot(kind='bar', color=colors)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.show();


def avg_feature_per_genre(df, genres_list, feature, title, xlabel, ylabel, ylmin=None, ylmax=None):
    avg_feature = {}

    # Вычисление среднего значения score для каждой категории
    for category in genres_list:
        avg = df[df[category] == category][feature].mean().round(1)
        avg_feature[category] = avg

    # Преобразование словаря в DataFrame для удобства
    avg_feature_per_genre = pd.DataFrame(list(avg_feature.items()), columns=['Category', 'Average Score'])

    # Определение индексов трёх наибольших значений
    top3_indices = avg_feature_per_genre['Average Score'].nlargest(3).index
    # Цвета для столбцов
    colors = ['skyblue' if genre not in top3_indices else 'orange' for genre in avg_feature_per_genre.index]

    # Построение столбчатой диаграммы среднего рейтинга по жанрам
    avg_feature_per_genre.plot(x='Category', y='Average Score', kind='bar', color=colors, legend=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.ylim(ylmin, ylmax)
    plt.show();


def genre_free_percent_per_genre(df, genres_list, feature, title, xlabel, ylabel):
    genre_free = {}

    # Вычисление среднего значения score для каждой категории
    for category in genres_list:
        free = round((df[df[feature] == True][category].count() / df[category].count() * 100), 1)
        genre_free[category] = free

    # Преобразование словаря в DataFrame для удобства
    free_per_genre = pd.DataFrame(list(genre_free.items()), columns=['Category', 'Percent'])

    # Определение индексов трёх наибольших значений
    top3_indices = free_per_genre['Percent'].nlargest(3).index
    # Цвета для столбцов
    colors = ['skyblue' if genre not in top3_indices else 'orange' for genre in free_per_genre.index]

    # Построение столбчатой диаграммы среднего рейтинга по жанрам
    fig, ax = plt.subplots()
    bars = ax.bar(free_per_genre['Category'], free_per_genre['Percent'], color=colors)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.ylim(0, 100)
    plt.show()


def sum_feature_per_genre(df, genres_list, feature, title, xlabel, ylabel):
    # Словарь для хранения средних значений
    sum_feature = {}

    # Вычисление среднего значения reviews для каждой категории
    for category in genres_list:
        category_sum = df[df[category] == category][feature].sum()
        sum_feature[category] = category_sum

    # Преобразование словаря в DataFrame для удобства
    sum_reviews_per_genre = pd.DataFrame(list(sum_feature.items()), columns=['Category', 'Average Score'])

    # Определение индексов трёх наибольших значений
    top3_indices = sum_reviews_per_genre['Average Score'].nlargest(3).index
    # Цвета для столбцов
    colors = ['skyblue' if genre not in top3_indices else 'orange' for genre in sum_reviews_per_genre.index]


    # Построение гистограммы количества отзывов по жанрам
    sum_reviews_per_genre.plot(x='Category', y='Average Score', kind='bar', color=colors, legend=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30)
    plt.show();


def age_group_distribution(df, genres_list, feature, title, xlabel, ylabel):
    result_df = pd.DataFrame(columns=["contentRating"] + genres_list)

    for genre in genres_list:
        genre_df = df[['contentRating', genre, feature]].dropna(subset=[genre])
        genre_grouped = genre_df.groupby('contentRating')[feature].sum().reset_index()
        genre_grouped = genre_grouped.rename(columns={feature: genre})
        if result_df.empty:
            result_df = genre_grouped
        else:
            result_df = result_df.merge(genre_grouped, on='contentRating', how='outer')

    result_df = result_df.fillna(0)

    result_df.plot(kind='bar', x='contentRating', figsize=(12, 5))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper right')
    plt.xticks(rotation=0)
    plt.show();


def free_paid_per_genre(df, genres_list, feature, title, xlabel, ylabel):
    # Создание пустого DataFrame для хранения результатов
    free_paid_counts = pd.DataFrame(columns=['Category', 'Free', 'Paid'])

    # Вычисление количества бесплатных и платных приложений для каждой категории
    for category in genres_list:
        counts = df.groupby([category, feature]).size().unstack().fillna(0)
        counts.reset_index(inplace=True)
        counts['Category'] = category
        counts.rename(columns={False: 'Paid', True: 'Free'}, inplace=True)
        free_paid_counts = pd.concat([free_paid_counts, counts[['Category', 'Free', 'Paid']]], ignore_index=True)

    # Вывод результата
    free_paid_counts

    # Построение гистограммы распределения бесплатных и платных игр по жанрам
    free_paid_counts.plot(x='Category', kind='bar', stacked=True, colormap='tab20', figsize=(12, 4))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30)
    plt.legend(labels=['Бесплатные', 'Платные'])
    plt.show();


def genre_group_distribution(df, title, xlabel, ylabel):
    collecion_genre = df[['collection', 'Action', 'Adventure', 'Casino', 
                                    'Casual', 'Family', 'Puzzle', 'Racing', 
                                    'Role Playing', 'Simulation', 'Sports', 'Strategy']].groupby('collection').count().T

    # Построение графика
    collecion_genre.plot(kind='bar', figsize=(12, 6))

    # Настройка графика
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title='Коллекции', loc='upper right')
    plt.xticks(rotation=0)
    # plt.grid(True)

    plt.show();


def count_collections_per_genre(df, genres_list, title, xlabel, ylabel):
    # Коллекции и их заголовки
    collections = ['NEW', 'NEW_FREE', 'NEW_PAID', 
                'TOP_FREE', 'TOP_PAID', 'TOP_GROSSING']
    collection_titles = {
        'NEW':          'Новые игры (iOS)',
        'NEW_FREE':     'Новые бесплатные игры (iOS)',
        'NEW_PAID':     'Новые платные игры (iOS)',
        'TOP_FREE':     'Топ бесплатных игр (iOS)',
        'TOP_PAID':     'Топ платных игр (iOS)',
        'TOP_GROSSING': 'Топ прибыльных игр (iOS)'
    }

    max_y = 1

    # Находим максимальное значение для y-шкалы
    for collection in collections:
        max_y = max(max_y, round((df[df['collection'] == collection][genres_list].count().max() * 1.02)))

    # Построение графиков
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    fig.tight_layout(pad=6.0)

    # Упрощаем итерацию, приводим к двумерному массиву
    axes = axes.flatten()

    for ax, collection in zip(axes, collections):
        # Подсчет количества игр в каждом жанре
        genre_counts = df[df['collection'] == collection][genres_list].count()

        # Определение индексов трёх наибольших значений
        top3_indices = genre_counts.nlargest(3).index
        # Цвета для столбцов
        colors = ['skyblue' if genre not in top3_indices else 'orange' for genre in genre_counts.index]

        # Построение гистограммы популярности жанров
        genre_counts.plot(kind='bar', ax=ax, color=colors)
            
        ax.set_title(collection_titles[collection])
        ax.set_xlabel(None)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=35)
        ax.set_ylim(0, max_y)

    # Удаляем пустые оси, если такие есть
    for ax in axes[len(collections):]:
        fig.delaxes(ax)

    # Добавляем общий заголовок
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Добавляем общие подписи осей
    fig.text(0.5, 0.33, xlabel, ha='center', va='center', fontsize=12)
    fig.text(0.03, 0.66, ylabel, ha='center', va='center', rotation='vertical', fontsize=12)

    plt.show();


def avg_collections_per_genre(df, genres_list, feature, title, xlabel, ylabel, ylmin=None):
    # Коллекции и их заголовки
    collections = ['NEW', 'NEW_FREE', 'NEW_PAID', 
                'TOP_FREE', 'TOP_PAID', 'TOP_GROSSING']
    collection_titles = {
        'NEW':          'Новые игры (iOS)',
        'NEW_FREE':     'Новые бесплатные игры (iOS)',
        'NEW_PAID':     'Новые платные игры (iOS)',
        'TOP_FREE':     'Топ бесплатных игр (iOS)',
        'TOP_PAID':     'Топ платных игр (iOS)',
        'TOP_GROSSING': 'Топ прибыльных игр (iOS)'
    }

    # Построение графиков
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    fig.tight_layout(pad=6.0)

    # Упрощаем итерацию, приводим к двумерному массиву
    axes = axes.flatten()
    
    max_y = 1

    # Словарь для хранения средних значений
    category_means = {}

    for collection in collections:
        # Вычисление среднего значения score для каждой категории
        for category in genres_list:
            category_mean = df[(df['collection'] == collection) & (df[category] == category)][feature].mean()
            category_means[category] = category_mean

        # Преобразование словаря в DataFrame для удобства
        avg_score_per_genre = pd.DataFrame(list(category_means.items()), columns=['Category', 'Average Score'])
        max_y = max(max_y, round((avg_score_per_genre['Average Score'].max() * 1.02)))

    for ax, collection in zip(axes, collections):
        # Словарь для хранения средних значений
        category_means = {}

        # Вычисление среднего значения score для каждой категории
        for category in genres_list:
            category_mean = df[(df['collection'] == collection) & (df[category] == category)][feature].mean()
            category_means[category] = category_mean

        # Преобразование словаря в DataFrame для удобства
        avg_score_per_genre = pd.DataFrame(list(category_means.items()), columns=['Category', 'Average Score'])

        # Определение индексов трёх наибольших значений
        top3_indices = avg_score_per_genre['Average Score'].nlargest(3).index
        # Цвета для столбцов
        colors = ['skyblue' if genre not in top3_indices else 'orange' for genre in avg_score_per_genre.index]

        # Построение столбчатой диаграммы среднего рейтинга по жанрам
        avg_score_per_genre.plot(x='Category', y='Average Score', kind='bar', color=colors, legend=False, ax=ax)
        ax.set_title(collection_titles[collection])
        ax.set_xlabel(None)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=35)
        ax.set_ylim(ylmin, max_y)

    # Удаляем пустые оси, если такие есть
    for ax in axes[len(collections):]:
        fig.delaxes(ax)

    # Добавляем общий заголовок
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Добавляем общие подписи осей
    fig.text(0.5, 0.33, xlabel, ha='center', va='center', fontsize=12)
    fig.text(0.03, 0.66, ylabel, ha='center', va='center', rotation='vertical', fontsize=12)

    plt.show();


def sum_collections_per_genre(df, genres_list, feature, title, xlabel, ylabel):
    # Коллекции и их заголовки
    collections = ['NEW', 'NEW_FREE', 'NEW_PAID', 
                'TOP_FREE', 'TOP_PAID', 'TOP_GROSSING']
    collection_titles = {
        'NEW':          'Новые игры (iOS)',
        'NEW_FREE':     'Новые бесплатные игры (iOS)',
        'NEW_PAID':     'Новые платные игры (iOS)',
        'TOP_FREE':     'Топ бесплатных игр (iOS)',
        'TOP_PAID':     'Топ платных игр (iOS)',
        'TOP_GROSSING': 'Топ прибыльных игр (iOS)'
    }

    # Построение графиков
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    fig.tight_layout(pad=6.0)

    # Упрощаем итерацию, приводим к двумерному массиву
    axes = axes.flatten()

    max_y = 1

    # Словарь для хранения средних значений
    reviews_sum = {}

    # Находим максимальное значение для y-шкалы
    for collection in collections:
        for category in genres_list:
            category_sum = df[(df['collection'] == collection) & (df[category] == category)][feature].sum()
            reviews_sum[category] = category_sum
        
        sum_reviews_per_genre = pd.DataFrame(list(reviews_sum.items()), columns=['Category', 'Average Score'])
        max_y = max(max_y, round((sum_reviews_per_genre['Average Score'].max() * 1.02)))
        
    for ax, collection in zip(axes, collections):
        
        # Словарь для хранения средних значений
        reviews_sum = {}

        # Вычисление среднего значения reviews для каждой категории
        for category in genres_list:
            category_sum = df[(df['collection'] == collection) & (df[category] == category)][feature].sum()
            reviews_sum[category] = category_sum

        # Преобразование словаря в DataFrame для удобства
        sum_reviews_per_genre = pd.DataFrame(list(reviews_sum.items()), columns=['Category', 'Average Score'])

        # Определение индексов трёх наибольших значений
        top3_indices = sum_reviews_per_genre['Average Score'].nlargest(3).index
        # Цвета для столбцов
        colors = ['skyblue' if genre not in top3_indices else 'orange' for genre in sum_reviews_per_genre.index]    

        # Построение столбчатой диаграммы среднего рейтинга по жанрам
        sum_reviews_per_genre.plot(x='Category', y='Average Score', kind='bar', color=colors, legend=False, ax=ax)
        ax.set_title(collection_titles[collection])
        ax.set_xlabel(None)
        # ax.set_ylabel('Количество отзывов')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=35)
        ax.set_ylim(0, max_y)  # Устанавливаем одинаковую шкалу y


    # Удаляем пустые оси, если такие есть
    for ax in axes[len(collections):]:
        fig.delaxes(ax)

    # Добавляем общий заголовок
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Добавляем общие подписи осей
    fig.text(0.5, 0.33, xlabel, ha='center', va='center', fontsize=12)
    fig.text(0.04, 0.66, ylabel, ha='center', va='center', rotation='vertical', fontsize=12)
    plt.show();