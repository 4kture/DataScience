import pandas as pd
import os

input_folder = 'pages_data'
output_file = 'books_dataset.csv'

total_rows = 0

dfs = []

for i in range(1, 51):
    path = f'pages_data/books_page_{i}.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f'{path}: {len(df)} строк')
        total_rows += len(df)

print(f'\n🧾 Суммарно строк: {total_rows}')

for i in range(1, 51):
    filename = os.path.join(input_folder, f'books_page_{i}.csv')
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        if not df.empty:
            dfs.append(df)
            print(f'✅ Загружен: {filename}')
        else:
            print(f'⚠️ Пропущен пустой файл: {filename}')
    else:
        print(f'🚫 Файл не найден: {filename}')

if dfs:
    full_df = pd.concat(dfs, ignore_index=True)
    full_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f'\n🎉 Финальный файл сохранён: {output_file}')
    print(f'📦 Всего строк: {len(full_df)}')
else:
    print('❌ Нет данных для объединения.')
