import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

stop_words = {
    "и", "в", "на", "по", "с", "со", "от", "за", "для", "при", "о",
    "а", "но", "что", "как", "к", "из", "у", "не", "то", "это"
}

df = pd.read_csv("parsed.csv")

def clean_data(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

df["Текст"] = df["abstract"].fillna("").apply(clean_data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["Текст"])
df_vect = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

df_vect.to_csv("vectorized.csv", index=False, encoding="utf-8-sig")