from bs4 import BeautifulSoup
import pandas as pd

with open("патент.html", "r", encoding="utf-8") as f:
    s = BeautifulSoup(f, "html.parser")

title = s.find("h1", id="title").get_text(" ", strip=True)
abstract = s.find("div", id="doc-abstract-text").get_text(" ", strip=True)
date = s.find("div", class_="patent_value").get_text(strip=True)

df = pd.DataFrame([[title, abstract, date]], columns=["title", "abstract", "date"])
df.to_csv("parsed.csv", index=False)
