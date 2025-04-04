from bs4 import BeautifulSoup
import pandas as pd

with open("патент.html", encoding='utf-8') as fp:
    s = BeautifulSoup(fp, 'html.parser')

data = []

titles = s.find_all('h1', id='title')
texts = s.find_all('div', id='doc-abstract-text')

for a, b in zip(titles, texts):
    title = a.get_text(' ', strip=True)
    text = b.get_text(' ', strip=True)
    data.append([title, text])

df = pd.DataFrame(data, columns=['title', 'text'])
df.to_csv("parsed.csv", index=False)