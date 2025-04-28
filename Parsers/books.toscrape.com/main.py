import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

base_url = 'https://books.toscrape.com/catalogue/category/books_1/'

os.makedirs('pages_data', exist_ok=True)

for count in range(25, 26):
    url = f'{base_url}page-{count}.html'
    print(f'🛠️ Обработка страницы {url}..')
    print('-' * 80 + '\n')

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    if response.status_code != 200:
        print('⛔ Больше страниц не найдено. Остановка.')
        break

    books = soup.find_all('article', class_='product_pod')
    all_books = []

    for book in books:
        try:
            relative_link = book.find('h3').find('a')['href']
            detail_url = 'https://books.toscrape.com/catalogue/' + relative_link.replace('../../', '')

            detail_response = requests.get(detail_url, headers=headers)
            detail_response.encoding = 'utf-8'
            detail_soup = BeautifulSoup(detail_response.text, 'lxml')

            category = None
            breadcrumb = detail_soup.select('ul.breadcrumb li')
            if len(breadcrumb) >= 3:
                category = breadcrumb[2].text.strip()

            table = {}
            for row in detail_soup.select('table.table-striped tr'):
                key = row.find('th').text.strip()
                value = row.find('td').text.strip()
                table[key] = value

            description_header = detail_soup.find('div', id='product_description')
            if description_header:
                description_tag = description_header.find_next_sibling('p')
                description = description_tag.text.strip()
            else:
                description = None

            rating_tag = detail_soup.find('p', class_='star-rating')
            rating = None
            if rating_tag:
                classes = rating_tag.get('class', [])
                for cls in classes:
                    if cls in ['One', 'Two', 'Three', 'Four', 'Five']:
                        rating_map = {
                            'One': 1,
                            'Two': 2,
                            'Three': 3,
                            'Four': 4,
                            'Five': 5
                        }
                        rating = rating_map.get(cls)
                        break

            name = detail_soup.find('h1').text
            upc = table.get('UPC')
            product_type = table.get('Product Type')
            price_excl_tax = table.get('Price (excl. tax)')
            price_incl_tax = table.get('Price (incl. tax)')
            tax = table.get('Tax')
            availability = table.get('Availability')
            reviews = table.get('Number of reviews')
            image_url = 'https://books.toscrape.com/' + detail_soup.find('img')['src'].replace('../../', '')

            print(f'📖 Название: {name}')
            print(f'📂 Категория: {category}')
            print(f'🆔 UPC (Айди): {upc}')
            print(f'📝 Описание: {description}')
            print(f'⭐ Рейтинг: {rating}')
            print(f'📚 Тип продукта: {product_type}')
            print(f'💵 Цена без налога: {price_excl_tax}')
            print(f'💰 Цена с налогом: {price_incl_tax}')
            print(f'📊 Налог: {tax}')
            print(f'📦 Наличие: {availability}')
            print(f'🗳️ Кол-во отзывов: {reviews}')
            print(f'🖼️ Картинка: {image_url}')
            print(f'🔗 Ссылка: {detail_url}')
            print('-' * 80 + '\n')

            all_books.append({
                'Название': name,
                'Категория': category,
                'UPC (Айди)': upc,
                'Описание': description,
                'Рейтинг': rating,
                'Тип продукта': product_type,
                'Цена без налога': price_excl_tax,
                'Цена с налогом:': price_incl_tax,
                'Налог': tax,
                'Наличие': availability,
                'Кол-во отзывов': reviews,
                'Картинка': image_url,
                'Ссылка': detail_url
            })

        except Exception as e:
            print(f'❌ Ошибка при обработке книги: {e}')
            continue

    page_filename = f'pages_data/books_page_{count}.csv'
    pd.DataFrame(all_books).to_csv(page_filename, index=False, encoding='utf-8-sig')
    print(f'✅ Страница {count} сохранена в файл: {page_filename}\n')

print('✅ Данные успешно обработаны!')
