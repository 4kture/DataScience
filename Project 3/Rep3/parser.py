import os
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Папка с HTML-файлами
HTML_FOLDER = 'path/to/your/html/files'  # замени на путь к своей папкеresponse = requests.get("https://searchplatform.rospatent.gov.ru/")
# Результирующий список данных
patents = []

# Обход всех файлов
for filename in os.listdir(HTML_FOLDER):
    if filename.endswith('.html') or filename.endswith('.htm'):
        file_path = os.path.join(HTML_FOLDER, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Получение заголовка
            title = soup.find('h1', id='title')
            title_text = title.get_text(strip=True) if title else None

            # Получение реферата
            abstract = soup.find('div', class_='patent_caption')
            abstract_text = abstract.get_text(strip=True) if abstract else None

            # Попытка найти "дату публикации" по контексту
            date_text = None
            all_labels = soup.find_all('div', class_='patent_label')
            for label in all_labels:
                if 'Дата публикации' in label.get_text():
                    value_div = label.find_next_sibling('div', class_='patent_value')
                    date_text = value_div.get_text(strip=True) if value_div else None
                    break

            patents.append({
                'filename': filename,
                'title': title_text,
                'abstract': abstract_text,
                'date': date_text
            })

# Сохраняем в CSV
df = pd.DataFrame(patents)
df.to_csv('parsed_patents.csv', index=False, encoding='utf-8-sig')
