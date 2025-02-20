import pandas as pd
import numpy as np
import random

# Список городов Татарстана и этапов олимпиады
tatarstan_cities = [
    "Казань", "Набережные Челны", "Альметьевск", "Зеленодольск", "Бугульма",
    "Елабуга", "Лениногорск", "Чистополь", "Азнакаево", "Заинск", "Бавлы",
    "Менделеевск", "Мамадыш", "Арск", "Агрыз", "Буинск", "Апастово", "Кукмор",
    "Тетюши", "Балтаси"
]

stages = ["Школьный", "Муниципальный", "Региональный", "Заключительный"]

# Количество записей
num_records = 2000
data = []

for _ in range(num_records):
    city = random.choice(tatarstan_cities)
    stage = random.choice(stages)

    # Внесение ошибок в формат года
    year = random.choice([
        random.randint(2015, 2024),
        float(random.randint(2015, 2024)) if random.random() < 0.2 else random.randint(2015, 2024),
        str(random.randint(2015, 2024)) if random.random() < 0.15 else random.randint(2015, 2024)
    ])

    # Пропуски и ошибки в числовых данных
    participants = random.choice([
        max(10, random.randint(5, 200)),
        np.nan if random.random() < 0.3 else max(10, random.randint(5, 200)),
        "ошибка" if random.random() < 0.1 else max(10, random.randint(5, 200))
    ])

    # Исправление NaN перед int()
    participants_cleaned = int(participants) if isinstance(participants, (int, float)) and not np.isnan(participants) else 0

    winners = random.choice([
        max(0, min(participants_cleaned, random.randint(0, max(1, participants_cleaned // 2)))),
        np.nan if random.random() < 0.25 else max(0, min(participants_cleaned, random.randint(0, max(1, participants_cleaned // 2)))),
        "ошибка" if random.random() < 0.08 else max(0, min(participants_cleaned, random.randint(0, max(1, participants_cleaned // 2))))
    ])

    percent_winners = round((winners / participants_cleaned) * 100, 2) if participants_cleaned > 0 and isinstance(winners, (int, float)) and winners > 0 else np.nan
    if random.random() < 0.2:
        percent_winners = "ошибка"

    avg_score = random.choice([
        round(random.uniform(40, 100), 2),
        np.nan if random.random() < 0.2 else round(random.uniform(40, 100), 2),
        -1 if random.random() < 0.1 else round(random.uniform(40, 100), 2),
        "ошибка" if random.random() < 0.1 else round(random.uniform(40, 100), 2)
    ])

    data.append([city, stage, year, participants, winners, percent_winners, avg_score])

# Создание DataFrame
columns = [
    "Муниципалитет", "Этап олимпиады", "Год проведения", "Количество участников",
    "Количество призёров", "Процент призёров", "Средний балл по этапу"
]
df = pd.DataFrame(data, columns=columns)

df.to_csv('../data/olympiad_data.csv', index=False)

# Проверка количества пропусков
print(df.isnull().sum().sort_values(ascending=False))
print("\n✅ Данные олимпиады по Республике Татарстан успешно обновлены!")
