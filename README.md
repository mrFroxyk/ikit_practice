# Приложение для работы с изображениями
Простой графический редактор изображений (убийца фотошопа) с возможностью редактирования изображений, полученных с камеры
или загруженных с диска
 
## 👀 Функционал
 - Загрузка изображений
 - Захват изображения с веб-камеры 
 - Отображение изображений
 - Показ цветовых каналов (красный, зеленый, синий) 
 - Размытие изображения по Гауссу
 - Получить изображение в оттенках серого
 - Нарисовать линию на изображении зеленым цветом
   
## 🔧 Запуск проекта

#### 1. Клонирование репозитория
```
git clone https://github.com/SeCrey36/finalprac
```

#### 2. Создание и активация виртуального окружения
- **С помощью Anaconda Navigator**: Создайте виртуальное окружение с версией Python 3.7.
- **С помощью Conda**:
`conda create --name image_editor python=3.7` 

#### 3. Активация виртуального окружения
-   **Anaconda**: Откройте Anaconda Prompt и активируйте окружение:
    `conda activate image_editor` 
-   **Conda**:
    `conda activate image_editor`

#### 4. Установка зависимостей
```
pip install -r requirements.txt
```

#### 5. Запуск приложения
```
python main.py
```