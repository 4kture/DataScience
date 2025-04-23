import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Анализ данных о недвижимости")

plt.style.use("dark_background")
sns.set_style("darkgrid")

sns.set_palette("mako")

@st.cache_data
def load_data():
    return pd.read_csv("../data/AmesHousing_Cleaned.csv")

df = load_data()

st.sidebar.header("🔍 Фильтры")

year_range = st.sidebar.slider("Выберите диапазон года постройки", int(df["Year Built"].min()), int(df["Year Built"].max()), (2000, 2010))

garage_filter = st.sidebar.selectbox("Выберите количество мест в гараже", sorted(df["Garage Cars"].dropna().unique()))

qual_filter = st.sidebar.slider("Выберите уровень качества", int(df["Overall Qual"].min()), int(df["Overall Qual"].max()), (5, 10))

filtered_df = df[(df["Year Built"].between(year_range[0], year_range[1])) &
                 (df["Garage Cars"] == garage_filter) &
                 (df["Overall Qual"].between(qual_filter[0], qual_filter[1]))]

st.subheader("📈 Корреляционная матрица")
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(filtered_df[["SalePrice", "Overall Qual", "Gr Liv Area", "Garage Cars", "Total Bsmt SF"]].corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.subheader("📊 Гистограмма цен")
fig, ax = plt.subplots()
sns.histplot(filtered_df["SalePrice"], bins=30, kde=True, color="blue", ax=ax)
st.pyplot(fig)

st.subheader("📌 График зависимости цены от жилой площади")
fig, ax = plt.subplots()
sns.scatterplot(x=filtered_df["Gr Liv Area"], y=filtered_df["SalePrice"], alpha=0.6, ax=ax)
ax.set_xlabel("Жилая площадь (Gr Liv Area)")
ax.set_ylabel("Цена продажи (SalePrice)")
st.pyplot(fig)

st.subheader("🏠 Средняя цена по годам постройки")
avg_price_by_year = filtered_df.groupby("Year Built")["SalePrice"].mean()
fig, ax = plt.subplots()
avg_price_by_year.plot(kind="bar", ax=ax, color="purple")
ax.set_xlabel("Год постройки")
ax.set_ylabel("Средняя цена")
st.pyplot(fig)

st.subheader("📊 Распределение гаражных мест")
fig, ax = plt.subplots()
sns.countplot(x=filtered_df["Garage Cars"], ax=ax, palette="mako")
st.pyplot(fig)

st.success("✅ Дашборд готов! Можно менять фильтры и анализировать данные.")