import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Анализ данных по олимпиаде")

@st.cache_data
def load_data():
    return pd.read_csv("../data/cleaned_olympiad_data.csv")

df = load_data()

st.sidebar.header("🔍 Фильтрация данных")
selected_city = st.sidebar.multiselect("Выберите город:", df["Город"].unique())
year_range = st.sidebar.slider("Выберите год участия:", int(df["Год участия"].min()), int(df["Год участия"].max()), (2018, 2024))
participants_range = st.sidebar.slider("Фильтр по количеству участников", int(df["Количество участников"].min()), int(df["Количество участников"].max()), (1, df["Количество участников"].max()))

filtered_df = df[
    (df["Город"].isin(selected_city) if selected_city else df["Город"].notnull()) &
    (df["Год участия"].between(year_range[0], year_range[1])) &
    (df["Количество участников"].between(participants_range[0], participants_range[1]))
]

st.subheader("📈 Корреляционная матрица")
columns = [
    'Количество участников',
    'Количество победителей',
    'Количество призеров',
    'Теоретическое тестирование',
    'Кодирование и декодирование информации',
    'Организация компьютерных сетей. Адресация'
]
numeric_cols = filtered_df[columns].select_dtypes(include=['number'])
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
st.pyplot(fig)

st.subheader("📊 Количество участников")
fig, ax = plt.subplots()
sns.histplot(filtered_df["Количество участников"], bins=10, kde=True, color="blue", ax=ax)
st.pyplot(fig)

st.subheader("📈 Динамика количества участников по годам")
fig, ax = plt.subplots()
sns.lineplot(x=filtered_df["Год участия"], y=filtered_df["Количество участников"], marker="o", ax=ax)
ax.set_xlabel("Год участия")
ax.set_ylabel("Количество участников")
st.pyplot(fig)

st.subheader("📊 Распределение баллов по годам")
fig, ax = plt.subplots()
sns.boxplot(x=filtered_df["Год участия"], y=filtered_df["Программирование"], ax=ax)
st.pyplot(fig)

st.subheader("🏆 Средние баллы по учебным заведениям")
top_institutions = filtered_df.groupby("Учебное заведение")["Программирование"].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=top_institutions.values, y=top_institutions.index, palette="mako", ax=ax)
ax.set_xlabel("Средний балл")
ax.set_ylabel("Учебное заведение")
st.pyplot(fig)