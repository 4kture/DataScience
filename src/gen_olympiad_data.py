import pandas as pd
import random

tatarstan_cities = [
    "Казань", "Набережные Челны", "Альметьевск", "Зеленодольск", "Бугульма",
    "Елабуга", "Лениногорск", "Чистополь", "Азнакаево", "Заинск", "Бавлы",
    "Менделеевск", "Мамадыш", "Арск", "Агрыз", "Буинск", "Апастово", "Кукмор",
    "Тетюши", "Балтаси"
]

stages = ["Школьный", "Муниципальный", "Региональный", "Заключительный"]

years = list(range(2015, 2025))

data = []

for _ in range(500):
    city = random.choice(tatarstan_cities)
    stage = random.choice(stages)
    year = random.choice(years)

    if stage == "Школьный":
        participants = random.randint(500, 5000)
    elif stage == "Муниципальный":
        participants = random.randint(100, 1000)
    elif stage == "Региональный":
        participants = random.randint(50, 500)
    else:
        participants = random.randint(10, 100)

    if random.random() < 0.05:
        participants = random.choice([1, 9999, 15000])

    if participants > 1:
        winners = random.randint(int(0.1 * participants), int(0.4 * participants))
    else:
        winners = 0

    if random.random() < 0.15:
        winners_percent = None
    else:
        winners_percent = round((winners / participants) * 100, 2)

    if random.random() < 0.1:
        avg_score = random.choice([0, 150])
    elif random.random() < 0.15:
        avg_score = None
    else:
        avg_score = round(random.uniform(50, 100), 2)

    data.append([city, stage, year, participants, winners, winners_percent, avg_score])

df_tatarstan_updated = pd.DataFrame(data, columns=[
    "Муниципалитет", "Этап олимпиады", "Год проведения", "Количество участников",
    "Количество призёров", "Процент призёров", "Средний балл по этапу"
])

file_path = "../data/olympiad_data.csv"
df_tatarstan_updated.to_csv(file_path, index=False)

print("Данные олимпиады по Республике Татарстан успешно создана!")