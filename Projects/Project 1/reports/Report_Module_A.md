## **📝 Отчёт по модулю А: Предобработка количественных данных**  

### **1. Введение**  
В рамках модуля А проведена предобработка количественных данных для последующего анализа. Мы очистили данные, обработали пропущенные значения, выявили выбросы и привели датасет к удобному формату.

---

### **2. Загрузка и изучение данных**  
📌 Данные загружены из файла `AmesHousing.txt`.  
📌 Использовались библиотеки `pandas`, `numpy`, `matplotlib`, `seaborn`.  
📌 Первичный анализ (`df.info()`, `df.describe()`) показал:  
- 2930 строк, 80 столбцов.  
- Наличие пропущенных значений в 27 столбцах.  
- Некоторые числовые признаки хранились в `float64`, а должны быть `int64`.  

---

### **3. Предобработка данных**  
✅ **Обнаружение и обработка пропусков:**  
- Полностью удалены столбцы с более чем **50% пропусков**:  
  - `Pool QC`, `Misc Feature`, `Alley`, `Fence`, `Mas Vnr Type`, `Fireplace Qu`.  
- **Числовые пропуски** заменены на **медиану** (`fillna(median)`):  
  - Например, `Lot Frontage` → заполнен медианой.  
- **Категориальные пропуски** заменены на `"None"`.  

✅ **Проверка дубликатов**  
- Дубликаты отсутствуют (`df.duplicated().sum() == 0`).  

---

### **4. Анализ выбросов**  
📌 Построены **боксплоты (boxplot)** и **гистограммы (histplot)** для ключевых признаков.  
📌 Наибольшее внимание уделено **SalePrice**, так как это целевая переменная.  
📌 Найдены **аномально дешёвые дома** (`SalePrice < 40,000`).  
- **Удалены** дома по строкам **181, 709** (12,789 и 37,900 долларов) как **подозрительно дешёвые**.  
📌 Дома с ценой **> 700,000** проверены вручную, оставлены как **действительные значения**.  

---

### **5. Обработка типов данных**  
✅ `Garage Yr Blt` (год постройки гаража) был `float64`, **преобразован в `int64`**.  
✅ `Year Built` и `Yr Sold` оставлены без изменений (`int64`).  

---

### **6. Сохранение результатов**  
📌 Итоговый датасет сохранён в **`AmesHousing_Cleaned.csv`** для дальнейшего анализа.  

```python
df.to_csv("AmesHousing_Cleaned.csv", index=False)
```

---

### **7. Вывод**  
📌 Датасет очищен и готов к дальнейшему анализу.  
📌 Удалены ненужные и проблемные данные.  
📌 Исправлены пропуски, выбросы, типы данных.  
📌 Итоговый файл **готов для использования в модуле Б**.  

---
