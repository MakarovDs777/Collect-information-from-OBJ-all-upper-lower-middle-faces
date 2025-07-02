import os
import tkinter as tk
from tkinter import filedialog

# Функция для сохранения текста на рабочем столе
def save_to_file(text):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "output.txt")
    with open(desktop_path, 'w') as file:
        file.write(text)
    print(f"Сохранено в {desktop_path}")

# Функция для получения граней из OBJ файла
def obj_to_faces_groups(obj_file):
    faces = []
    with open(obj_file, 'r') as file:
        for line in file:
            if line.startswith('f '):
                face = [int(idx.split('/')[0]) - 1 for idx in line.strip().split()[1:]]
                faces.append(face)
    return faces

# Основная функция для классификации граней
def categorize_faces(faces):
    global vertices
    bottom_faces = []
    top_faces = []
    vertical_faces = []

    # Находим глобальные min_y и max_y
    all_y = [v[1] for v in vertices]
    global_min_y = min(all_y)
    global_max_y = max(all_y)

    threshold = 1e-3  # порог для определения "близко" к вершине или низу

    for i, face in enumerate(faces):
        v_coords = [vertices[idx] for idx in face]
        y_coords = [v[1] for v in v_coords]
        min_y = min(y_coords)
        max_y = max(y_coords)

        # Проверка на горизонтальную грань
        if abs(max_y - min_y) < 1e-5:
            # Горизонтальная грань
            if abs(min_y - global_min_y) < threshold:
                bottom_faces.append(i)
            elif abs(max_y - global_max_y) < threshold:
                top_faces.append(i)
            else:
                vertical_faces.append(i)
        else:
            # Наклонные или вертикальные грани
            vertical_faces.append(i)

    return bottom_faces, top_faces, vertical_faces

# Основная функция выбора файла
def select_obj_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Выберите файл OBJ", filetypes=[("OBJ files", "*.obj")])
    if file_path:
        global vertices
        vertices = []
        # Читаем вершины
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertex = list(map(float, line.strip().split()[1:]))
                    vertices.append(vertex)
        # Получаем грани
        faces = obj_to_faces_groups(file_path)
        # Категоризируем грани
        bottom_faces, top_faces, vertical_faces = categorize_faces(faces)
        # Формируем текст
        text = (
            f"Все нижние горизонтальные faces: {bottom_faces}\n"
            f"Все верхние горизонтальные faces: {top_faces}\n"
            f"Все средние вертикальные faces: {vertical_faces}\n"
        )
        print(text)
        save_to_file(text)
    else:
        print("Файл не выбран.")

# Запуск диалогового окна
select_obj_file()
