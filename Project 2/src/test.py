import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 🔹 1. Загружаем данные модуля А (замени путь на свой файл)
file_path = "data_module_A.xlsx"  # Укажи свой файл
df = pd.read_excel(file_path)

# 🔹 2. Выбираем нужные столбцы
columns = [
    "Анализ информационных моделей", "Поиск информации в реляционных базах данных",
    "Кодирование и декодирование информации", "Определение результатов работы алгоритмов",
    "Работа с таблицами", "Поиск символов в текстовом редакторе",
    "Организация компьютерных сетей. Адресация", "Программирование", "Безопасность данных"
]

df_selected = df[columns]

# 🔹 3. Определяем зависимости между заданиями
edges = [
    ("Анализ информационных моделей", "Поиск информации в реляционных базах данных"),
    ("Поиск информации в реляционных базах данных", "Работа с таблицами"),
    ("Работа с таблицами", "Поиск символов в текстовом редакторе"),
    ("Определение результатов работы алгоритмов", "Программирование"),
    ("Программирование", "Безопасность данных"),
    ("Кодирование и декодирование информации", "Организация компьютерных сетей. Адресация"),
    ("Организация компьютерных сетей. Адресация", "Безопасность данных")
]

# 🔹 4. Создаём направленный граф
G = nx.DiGraph()
G.add_edges_from(edges)

# 🔹 5. Визуализируем граф зависимостей
plt.figure(figsize=(10, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
plt.title("Граф зависимостей заданий")
plt.show()

# 🔹 6. Анализ ключевых заданий
pagerank = nx.pagerank(G)
sorted_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)

print("\n🔹 Ключевые задания (по важности):")
for topic, score in sorted_pagerank[:3]:
    print(f"{topic}: {score:.4f}")

# 🔹 7. Определение оптимального порядка выполнения
if nx.is_directed_acyclic_graph(G):
    optimal_order = list(nx.topological_sort(G))
    print("\n🔹 Оптимальный порядок выполнения заданий:")
    print(" → ".join(optimal_order))
else:
    print("\n⚠️ Граф содержит циклы, сортировка невозможна.")

# 🔹 8. Оценка сложности выполнения (самый длинный путь)
if nx.is_directed_acyclic_graph(G):
    longest_path = nx.dag_longest_path(G)
    print(f"\n🔹 Самая сложная цепочка заданий: {len(longest_path)} шагов")
    print(" → ".join(longest_path))