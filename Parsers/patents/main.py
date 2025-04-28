from bs4 import BeautifulSoup
import pandas as pd
import os

all_patents = []

folder_path = 'grabbed'

max_files = 10000
count = 0

for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        filepath = os.path.join(folder_path, filename)

        with open(filepath, 'r', encoding='windows-1251') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')

        data = {
            'registration_number': None,
            'registration_date': None,
            'application_number_and_date': None,
            'publication_date': None,
            'authors': None,
            'holder': None,
            'database_title': None,
            'abstract': None,
            'computer_type': None,
            'dbms_type': None,
            'os_type': None,
            'database_size': None
        }

        bib_table = soup.find('table', {'id': 'bib'})
        if bib_table:
            paragraphs = bib_table.find_all('p')
            for p in paragraphs:
                text = p.get_text(separator=' ', strip=True)

                if 'Номер регистрации' in text:
                    data['registration_number'] = text.split(':')[-1].strip()
                elif 'Дата регистрации' in text:
                    data['registration_date'] = text.split(':')[-1].strip()
                elif 'Номер и дата поступления заявки' in text:
                    data['application_number_and_date'] = text.split(':')[-1].strip()
                elif 'Дата публикации' in text:
                    data['publication_date'] = text.split(':')[-1].strip()
                elif 'Автор' in text or 'Авторы' in text:
                    data['authors'] = text.replace('Автор:', '').replace('Авторы:', '').strip()
                elif 'Правообладатель' in text or 'Правообладатели' in text:
                    data['holder'] = text.replace('Правообладатель:', '').replace('Правообладатели:', '').strip()

        titabs_paragraphs = soup.find_all('p', {'class': 'TitAbs'})
        for p in titabs_paragraphs:
            text = p.get_text(separator=' ', strip=True)

            if 'Название базы данных' in text:
                data['database_title'] = text.replace('Название базы данных:', '').strip()
            elif 'Реферат' in text:
                data['abstract'] = text.replace('Реферат:', '').strip()
            elif 'Тип реализующей ЭВМ' in text:
                data['computer_type'] = text.replace('Тип реализующей ЭВМ:', '').strip()
            elif 'Вид и версия системы управления базой данных' in text:
                data['dbms_type'] = text.replace('Вид и версия системы управления базой данных:', '').strip()
            elif 'Вид и версия операционной системы' in text:
                data['os_type'] = text.replace('Вид и версия операционной системы:', '').strip()
            elif 'Объем базы данных' in text or 'Объём базы данных' in text:
                data['database_size'] = text.replace('Объем базы данных:', '').replace('Объём базы данных:', '').strip()

        all_patents.append(data)
        count += 1

        if count >= max_files:
            break

df = pd.DataFrame(all_patents)

df.to_csv('parsed_patents_all.csv', index=False, encoding='utf-8-sig')
