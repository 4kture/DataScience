import os
import pandas as pd
import numpy as np
import json
import csv
import shutil
import matplotlib.pyplot as plt
import seaborn as sns
from cryptography.fernet import Fernet
from fpdf import FPDF


def find_usb():
    if os.name == "nt":
        possible_drives = [f"{chr(letter)}:\\" for letter in range(69, 91)]
        for drive in possible_drives:
            if os.path.exists(drive):
                return drive
    else:
        base_path = "/media" if os.name != "darwin" else "/Volumes"
        for root, dirs, files in os.walk(base_path):
            if "data" in dirs:
                return os.path.join(root, "data")
    return None

usb_path = find_usb()
if usb_path is None:
    raise FileNotFoundError("Флеш-накопитель не найден!")

print(f"✅ Флеш-накопитель найден: {usb_path}")


def find_file(extension):
    for file in os.listdir(usb_path):
        if file.endswith(extension):
            return os.path.join(usb_path, file)
    return None

data_file = find_file(".csv") or find_file(".xlsx") or find_file(".json")
key_file = find_file(".key")

if data_file:
    print(f"✅ Найден файл данных: {data_file}")
else:
    raise FileNotFoundError("Файл с данными не найден!")

if key_file:
    print(f"🔑 Найден ключ для расшифровки: {key_file}")


def load_data(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    elif file_path.endswith(".json"):
        return pd.read_json(file_path)
    else:
        raise ValueError("Неизвестный формат данных!")

df = load_data(data_file)
print("📊 Данные успешно загружены!")


def decrypt_data(df, key_file):
    with open(key_file, "rb") as f:
        key = f.read()
    cipher = Fernet(key)

    for col in df.select_dtypes(include="object"):
        try:
            df[col] = df[col].apply(lambda x: cipher.decrypt(x.encode()).decode() if isinstance(x, str) else x)
        except:
            pass
    print("🔓 Данные успешно расшифрованы!")

if key_file:
    decrypt_data(df, key_file)

print("🛠 Очистка данных...")

df = df.drop_duplicates()
df = df.fillna("Unknown")

for col in df.select_dtypes(include=[np.number]):
    df[col] = df[col].apply(lambda x: np.nan if str(x).strip().lower() in ["ошибка", "-999"] else x)
    df[col].fillna(df[col].median(), inplace=True)

print("✅ Данные очищены!")

print("📈 Создание отчёта...")

plt.figure(figsize=(10, 5))
sns.histplot(df.select_dtypes(include=np.number), bins=30, kde=True)
plt.title("Распределение числовых данных")
plt.grid(True)
plt.savefig("histogram.png")

plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Корреляция признаков")
plt.savefig("correlation.png")


class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, "📊 Аналитический отчёт по данным", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 7, body)
        self.ln(5)


pdf = PDFReport()
pdf.add_page()

pdf.chapter_title("1. Общая информация")
pdf.chapter_body(f"Количество строк: {df.shape[0]}\nКоличество столбцов: {df.shape[1]}")

pdf.chapter_title("2. Пропущенные значения")
missing_info = df.isnull().sum().sort_values(ascending=False).to_string()
pdf.chapter_body(missing_info)

pdf.chapter_title("3. Распределение числовых данных")
pdf.image("histogram.png", x=10, y=pdf.get_y(), w=180)
pdf.ln(55)

pdf.chapter_title("4. Корреляция признаков")
pdf.image("correlation.png", x=10, y=pdf.get_y(), w=180)
pdf.ln(55)

pdf.output("data_report.pdf")
print("📄 Отчёт data_report.pdf создан!")

output_file = "cleaned_data.csv"
df.to_csv(output_file, index=False)
print(f"✅ Очищенные данные сохранены в {output_file}")

shutil.move("data_report.pdf", os.path.join(usb_path, "data_report.pdf"))
shutil.move("cleaned_data.csv", os.path.join(usb_path, "cleaned_data.csv"))

print("📂 Файлы сохранены на флеш-накопитель!")