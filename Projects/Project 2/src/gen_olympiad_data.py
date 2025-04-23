import pandas as pd
import random
import numpy as np

educational_institutions = {
    "Казань": [
        "Казанский авиационно-технический колледж",
        "Казанский медицинский колледж",
        "Казанский педагогический колледж",
        "Казанский строительный колледж",
        "Казанский колледж технологий и дизайна",
        "Казанский энергетический колледж",
        "Казанский автотранспортный техникум",
        "Казанский колледж информационных технологий",
        "Казанский аграрный колледж"
    ],
    "Набережные Челны": [
        "Набережночелнинский педагогический колледж",
        "Набережночелнинский политехнический колледж",
        "Набережночелнинский медицинский колледж",
        "Набережночелнинский машиностроительный техникум",
        "Набережночелнинский строительный колледж"
    ],
    "Альметьевск": [
        "Альметьевский политехнический колледж",
        "Альметьевский медицинский колледж",
        "Альметьевский государственный нефтяной институт"
    ],
    "Чистополь": [
        "Чистопольский сельскохозяйственный техникум",
        "Чистопольский механический колледж"
    ]
}

num_rows = 200
data = []

for _ in range(num_rows):
    city = random.choice(list(educational_institutions.keys()))
    institution = random.choice(educational_institutions[city])
    year = random.choice(range(2018, 2025))
    max_score_all = random.choice([100, 80, 60])
    max_score_theoretical = random.choice([50, 40, 30])
    max_score_practical = random.choice([50, 40, 30])
    participants = random.randint(0, 5)
    gender = random.choice(["м", "ж"]) if participants > 0 else np.nan
    winners = random.randint(0, participants) if participants > 0 else np.nan
    prizery = random.randint(0, winners) if winners > 0 else np.nan
    max_score_participant = random.uniform(30, max_score_all) if participants > 0 else np.nan
    theoretical_test = random.uniform(10, max_score_theoretical) if participants > 0 else np.nan
    max_practical_score = random.uniform(10, max_score_practical) if participants > 0 else np.nan

    analysis_models = random.uniform(2, 10) if participants > 0 else np.nan
    database_search = random.uniform(2, 10) if participants > 0 else np.nan
    encoding_decoding = random.uniform(2, 10) if participants > 0 else np.nan
    algorithm_results = random.uniform(2, 10) if participants > 0 else np.nan
    table_work = random.uniform(2, 10) if participants > 0 else np.nan
    text_search = random.uniform(2, 10) if participants > 0 else np.nan
    network_organization = random.uniform(2, 10) if participants > 0 else np.nan
    programming = random.uniform(2, 10) if participants > 0 else np.nan
    data_security = random.uniform(2, 10) if participants > 0 else np.nan

    data.append([
        institution, city, year, max_score_all, max_score_theoretical, max_score_practical,
        participants, gender, winners, prizery, max_score_participant, theoretical_test,
        max_practical_score, analysis_models, database_search, encoding_decoding,
        algorithm_results, table_work, text_search, network_organization, programming, data_security
    ])

# Названия столбцов
columns = [
    "Учебное заведение", "Город", "Год участия", "Максимальный балл за все задания",
    "Максимальный балл за теоретическое задание", "Максимальный балл за практическое задание",
    "Количество участников", "Пол", "Количество победителей", "Количество призеров",
    "Максимальный балл участника за оба задания", "Теоретическое тестирование",
    "Максимальный балл участника за практическое задание", "Анализ информационных моделей",
    "Поиск информации в реляционных базах данных", "Кодирование и декодирование информации",
    "Определение результатов работы алгоритмов", "Работа с таблицами",
    "Поиск символов в текстовом редакторе", "Организация компьютерных сетей. Адресация",
    "Программирование", "Безопасность данных"
]

df = pd.DataFrame(data, columns=columns)

file_path = "../data/olympiad_data.csv"
df.to_csv(file_path, index=False)

print("\n✅ Данные олимпиады по Республике Татарстан!")