from bs4 import BeautifulSoup
import pandas as pd

with open("патент.html", encoding="utf-8") as f:
    s = BeautifulSoup(f, "html.parser")

df = pd.DataFrame([[
    b.find("h1", id="title").get_text(" ", strip=True),
    b.find("div", id="doc-abstract-text").get_text(" ", strip=True)
] for b in s.find_all("div", class_="patent")], columns=["title", "abstract"])

df.to_csv("parsed.csv", index=False, encoding="utf-8-sig")
