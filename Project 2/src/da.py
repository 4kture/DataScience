import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

df = pd.read_csv('../data/text_data.csv')

stop_words = {'Текст1', 'Текст2'}

df = df.dropna(subset=['Текст обращения']).copy()
df['Тематика'] = df['Тематика'].fillna('Не указано')
df_unique_texts = pd.DataFrame(df["Текст обращения"].dropna().unique(), columns=["Уникальные тексты"])

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)
df["Текст обращения"] = df["Текст обращения"].apply(clean_text)

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["Текст обращения"])

num_clusters = 10
kmeans = KMeans(n_clusters=num_clusters, random_state=143, n_init=10)
df["Кластер"] = kmeans.fit_predict(X)

for cluster_num in range(num_clusters):
    print(f"\nКластер {cluster_num}:")
    print(df[df["Кластер"] == cluster_num]["Текст обращения"].head(5).tolist())

cluster_names = {0: "Текст1", 1: "Текст2"}

df["Тематика"] = df["Кластер"].map(cluster_names)
df.drop(columns=["Кластер"], inplace=True)

print("Статистика по кластерам:")
print(df["Тематика"].value_counts())

df.to_csv("../data/cleaned_text_data.csv", index=False)

# Макет
print(df["Кластер"].value_counts())