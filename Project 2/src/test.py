import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import shapiro

df = pd.read_csv('../data/cleaned_olympiad_data.csvS')


#гистограммы циклом
numeric_columns = df.select_dtypes(include=['number']).columns

plt.figure(figsize=(15, 12))
for i, col in enumerate(numeric_columns):
    plt.subplot(5, 5, i+1)
    sns.histplot(df[col], bins=20, kde=True)
    plt.title(col)
plt.tight_layout()
plt.show()


#5 важных признаков
df.corr(numeric_only=True)['Количество участников'].sort_values(ascending=False)[1:6]


#построение матрицы
columns = [
    'text 1',
    'text 2',
    'text 3',
    'text 4',
    'text 5',
    'text 6',
]

plt.figure(figsize=(10, 6))
sns.heatmap(df[columns].corr(), annot=True, cmap="coolwarm", fmt=".2f")

plt.title("Корреляционная матрица важных признаков")
plt.show()


#зависимости
sns.pairplot(df[columns])
plt.show()


#оценка распределения
for col in columns:
    stat, p = shapiro(df[col])
    print(f"{col}: Stat={stat:.3f}, p={p:.3f}")
    if p > 0.05:
        print(" ✅ Распределение похоже на нормальное (не отвергаем H0)")
    else:
        print(" ❌ Распределение НЕ нормальное (отвергаем H0)")
    print("-" * 50)


#построение Q-Q
plt.figure(figsize=(12, 8))

for i, col in enumerate(columns, 1):
    plt.subplot(2, 3, i)
    stats.probplot(df[col], dist="norm", plot=plt)
    plt.title(f"Q-Q plot для {col}")

plt.tight_layout()
plt.show()