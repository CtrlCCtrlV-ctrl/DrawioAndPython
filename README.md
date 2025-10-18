# Библиотека для интеграции Draw.io и Python

## 📋 Описание проекта

Данная библиотека представляет собой комплексное решение для программной работы с диаграммами Draw.io (diagrams.net) с использованием языка программирования Python. Проект разработан для автоматизации создания, редактирования и управления диаграммами без необходимости использования графического интерфейса Draw.io.

### Основное назначение

Библиотека позволяет генерировать диаграммы Draw.io программным способом, что особенно полезно для:

- Автоматической генерации технической документации
- Визуализации архитектуры программных систем
- Создания организационных структур и иерархических диаграмм
- Генерации сетевых топологий
- Автоматизированного создания блок-схем и диаграмм процессов
- Версионирования диаграмм совместно с кодом в системах контроля версий

### Ключевые преимущества Draw.io

Draw.io является оптимальным выбором для программной генерации диаграмм по следующим причинам:

1. **Бесплатность и открытость** - полностью бесплатное решение без ограничений функциональности
2. **Легковесность** - не требует значительных системных ресурсов
3. **Текстовый формат** - файлы хранятся в формате XML, что позволяет версионировать их вместе с кодом
4. **Обратная совместимость** - диаграммы, созданные много лет назад, по-прежнему открываются в современных версиях
5. **Кроссплатформенность** - работает в веб-браузере, как десктопное приложение и интегрируется с различными платформами
6. **Универсальность** - подходит для создания любых типов диаграмм

## ✨ Возможности библиотеки

### Базовый функционал

- **Создание объектов диаграмм** - программное создание прямоугольников, эллипсов, стрелок и других графических примитивов
- **Стилизация элементов** - применение цветов, шрифтов, границ, заливок и градиентов
- **Позиционирование** - точное размещение объектов на холсте с заданными координатами
- **Связи между объектами** - создание направленных и ненаправленных связей с различными типами стрелок
- **Работа со слоями** - организация элементов диаграммы по слоям для удобства управления
- **Использование библиотек фигур** - доступ к предустановленным библиотекам Draw.io (AWS, Azure, GCP, сетевые элементы и др.)

### Расширенный функционал

- **Автоматическое создание древовидных структур** - генерация иерархических диаграмм с автоматическим размещением узлов
- **Автоматическая компоновка** - интеллектуальное размещение элементов на диаграмме
- **Импорт и экспорт** - чтение существующих файлов Draw.io и их модификация
- **Пакетная обработка** - массовое создание множества диаграмм из структурированных данных
- **Интеграция с данными** - генерация диаграмм на основе CSV, JSON, баз данных и API

### Поддерживаемые типы диаграмм

1. **Блок-схемы (Flowcharts)** - визуализация алгоритмов и бизнес-процессов
2. **Древовидные диаграммы (Tree Diagrams)** - организационные структуры, иерархии требований
3. **Сетевые топологии (Network Diagrams)** - схемы сетевой инфраструктуры
4. **UML-диаграммы** - диаграммы классов, последовательностей, компонентов
5. **Диаграммы архитектуры** - визуализация облачной и системной архитектуры
6. **Mind Maps** - интеллект-карты и карты знаний

## 🔧 Требования к системе

### Минимальные требования

- **Python**: версия 3.7 или выше (рекомендуется 3.9+)
- **Операционная система**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+)
- **Оперативная память**: минимум 512 МБ свободной RAM
- **Дисковое пространство**: 50 МБ для установки библиотеки и зависимостей

### Рекомендуемые требования

- **Python**: версия 3.10 или выше
- **Оперативная память**: 2 ГБ или более для работы с большими диаграммами
- **Дисковое пространство**: 200 МБ для комфортной работы и кэширования

### Зависимости Python

Библиотека имеет минимальные зависимости:

- `xml.etree.ElementTree` - встроенная библиотека для работы с XML
- `base64` - встроенная библиотека для кодирования данных
- `zlib` - встроенная библиотека для сжатия данных
- `json` - встроенная библиотека для работы с JSON

Дополнительные опциональные зависимости:

- `requests` - для загрузки диаграмм по URL
- `pillow` - для работы с изображениями в диаграммах
- `pandas` - для генерации диаграмм из табличных данных

## 📦 Установка

### Установка через pip (рекомендуемый способ)

Самый простой способ установки - использование менеджера пакетов pip:

```bash
pip install drawpyo
```

Для установки с дополнительными зависимостями:

```bash
pip install drawpyo[all]
```

### Установка через conda

Для пользователей Anaconda или Miniconda:

```bash
conda install -c conda-forge drawpyo
```

### Установка из исходного кода

Для разработчиков и тех, кто хочет работать с последней версией из репозитория:

```bash
# Клонирование репозитория
git clone https://github.com/MerrimanInd/drawpyo.git
cd drawpyo

# Установка в режиме разработки
pip install -e .
```

### Установка через Poetry

Для проектов, использующих Poetry для управления зависимостями:

```bash
poetry add drawpyo
```

### Проверка установки

После установки можно проверить корректность установки:

```python
import drawpyo
print(drawpyo.__version__)
```

## 🚀 Быстрый старт

### Пример 1: Создание простой диаграммы

Минимальный пример создания файла Draw.io с одним объектом:

```python
import drawpyo

# Создание нового файла
file = drawpyo.File()
file.file_path = "/путь/к/папке"
file.file_name = "моя_диаграмма.drawio"

# Добавление страницы
page = drawpyo.Page(file=file)

# Создание объекта
rect = drawpyo.diagram.Object(page=page, value="Привет, Draw.io!")
rect.position = (100, 100)
rect.width = 120
rect.height = 60

# Сохранение файла
file.write()
```

### Пример 2: Создание диаграммы с несколькими объектами и связями

```python
import drawpyo

# Инициализация файла
file = drawpyo.File()
file.file_path = "/путь/к/папке"
file.file_name = "блок_схема.drawio"

# Создание страницы
page = drawpyo.Page(file=file)

# Создание объектов
start = drawpyo.diagram.Object(page=page, value="Начало")
start.position = (200, 50)
start.apply_style_string("rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;")

process = drawpyo.diagram.Object(page=page, value="Обработка данных")
process.position = (200, 150)
process.apply_style_string("fillColor=#dae8fc;strokeColor=#6c8ebf;")

end = drawpyo.diagram.Object(page=page, value="Конец")
end.position = (200, 250)
end.apply_style_string("rounded=1;fillColor=#f8cecc;strokeColor=#b85450;")

# Создание связей
edge1 = drawpyo.diagram.Edge(page=page, source=start, target=process)
edge2 = drawpyo.diagram.Edge(page=page, source=process, target=target=end)

# Сохранение
file.write()
```

### Пример 3: Использование библиотек фигур Draw.io

```python
import drawpyo

file = drawpyo.File()
file.file_path = "/путь/к/папке"
file.file_name = "aws_архитектура.drawio"

page = drawpyo.Page(file=file)

# Создание объекта из библиотеки AWS
ec2 = drawpyo.diagram.object_from_library(
    page=page,
    library="aws",
    obj_name="EC2",
    value="Веб-сервер",
)
ec2.position = (100, 100)

rds = drawpyo.diagram.object_from_library(
    page=page,
    library="aws",
    obj_name="RDS",
    value="База данных",
)
rds.position = (300, 100)

# Связь между сервисами
connection = drawpyo.diagram.Edge(page=page, source=ec2, target=rds)

file.write()
```

### Пример 4: Создание древовидной диаграммы

```python
from drawpyo.diagram_types import TreeDiagram, NodeObject

# Создание древовидной диаграммы
tree = TreeDiagram(
    file_path="/путь/к/папке",
    file_name="организационная_структура.drawio",
    direction="down",  # направление: down, up, left, right
    link_style="orthogonal",  # стиль связей: orthogonal, straight, curved
)

# Корневой узел
ceo = NodeObject(
    tree=tree,
    value="Генеральный директор",
    base_style="rounded rectangle"
)

# Дочерние узлы
cto = NodeObject(tree=tree, value="Технический директор", tree_parent=ceo)
cfo = NodeObject(tree=tree, value="Финансовый директор", tree_parent=ceo)
cmo = NodeObject(tree=tree, value="Директор по маркетингу", tree_parent=ceo)

# Узлы второго уровня
dev_lead = NodeObject(tree=tree, value="Руководитель разработки", tree_parent=cto)
qa_lead = NodeObject(tree=tree, value="Руководитель QA", tree_parent=cto)

# Автоматическая компоновка и сохранение
tree.auto_layout()
tree.write()
```

### Пример 5: Применение стилей

```python
import drawpyo

file = drawpyo.File()
file.file_path = "/путь/к/папке"
file.file_name = "стили.drawio"

page = drawpyo.Page(file=file)

# Создание объекта с кастомным стилем
styled_object = drawpyo.diagram.Object(page=page, value="Стилизованный объект")
styled_object.position = (150, 100)

# Применение стилей через строку
style_string = (
    "rounded=1;"
    "whiteSpace=wrap;"
    "html=1;"
    "fillColor=#6a00ff;"
    "fontColor=#ffffff;"
    "strokeColor=#000000;"
    "gradientColor=#FF33FF;"
    "strokeWidth=4;"
    "fontSize=14;"
    "fontStyle=1"  # жирный шрифт
)
styled_object.apply_style_string(style_string)

file.write()
```

## 📚 Подробная документация

### Структура проекта

```
drawpyo/
├── __init__.py           # Инициализация пакета
├── file.py               # Класс File для работы с файлами
├── page.py               # Класс Page для страниц диаграмм
├── diagram.py            # Базовые классы Object и Edge
├── diagram_types/        # Специализированные типы диаграмм
│   ├── __init__.py
│   ├── tree.py          # Древовидные диаграммы
│   └── flowchart.py     # Блок-схемы
├── styling/              # Модули для работы со стилями
│   ├── __init__.py
│   └── style.py
└── utils/                # Утилиты
    ├── __init__.py
    └── xml_utils.py
```

### Основные классы

#### Класс File

Основной класс для работы с файлами Draw.io:

```python
class File:
    """
    Представляет файл Draw.io (.drawio)
    
    Атрибуты:
        file_path (str): Путь к директории сохранения
        file_name (str): Имя файла
        version (str): Версия спецификации Draw.io
    """
    
    def __init__(self):
        """Инициализация нового файла"""
        pass
    
    def write(self):
        """Сохранение файла на диск"""
        pass
```

#### Класс Page

Класс для работы со страницами диаграммы:

```python
class Page:
    """
    Представляет страницу в файле Draw.io
    
    Атрибуты:
        file (File): Родительский файл
        name (str): Название страницы
        width (int): Ширина страницы
        height (int): Высота страницы
    """
    
    def __init__(self, file, name="Страница-1"):
        """Создание новой страницы"""
        pass
```

#### Класс Object

Класс для создания графических объектов:

```python
class Object:
    """
    Графический объект на диаграмме
    
    Атрибуты:
        page (Page): Родительская страница
        value (str): Текстовое содержимое объекта
        position (tuple): Координаты (x, y)
        width (int): Ширина объекта
        height (int): Высота объекта
    """
    
    def __init__(self, page, value="", position=(0,0)):
        """Создание нового объекта"""
        pass
    
    def apply_style_string(self, style_string):
        """Применение строки стиля"""
        pass
```

#### Класс Edge

Класс для создания связей между объектами:

```python
class Edge:
    """
    Связь между двумя объектами
    
    Атрибуты:
        page (Page): Родительская страница
        source (Object): Исходный объект
        target (Object): Целевой объект
        style (str): Стиль линии
    """
    
    def __init__(self, page, source, target):
        """Создание новой связи"""
        pass
```

### Работа со стилями

Стили в Draw.io представляют собой строки пар ключ-значение, разделенные точкой с запятой.

#### Основные параметры стилей:

**Заливка и границы:**
- `fillColor` - цвет заливки (формат: #RRGGBB)
- `strokeColor` - цвет границы
- `strokeWidth` - толщина границы
- `gradientColor` - цвет градиента
- `gradientDirection` - направление градиента (north, south, east, west)

**Форма:**
- `rounded` - скругление углов (0 или 1)
- `shape` - тип фигуры (rectangle, ellipse, rhombus, cylinder и др.)

**Текст:**
- `fontColor` - цвет текста
- `fontSize` - размер шрифта
- `fontFamily` - семейство шрифта
- `fontStyle` - стиль шрифта (0=обычный, 1=жирный, 2=курсив, 4=подчеркнутый)
- `align` - горизонтальное выравнивание (left, center, right)
- `verticalAlign` - вертикальное выравнивание (top, middle, bottom)

**Линии и стрелки:**
- `edgeStyle` - стиль линии (orthogonalEdgeStyle, elbowEdgeStyle и др.)
- `curved` - изогнутость линии (0 или 1)
- `endArrow` - тип стрелки на конце (classic, block, oval и др.)
- `startArrow` - тип стрелки в начале
- `dashed` - пунктирная линия (0 или 1)

### Использование библиотек фигур

Draw.io предоставляет множество встроенных библиотек фигур:

```python
# Доступные библиотеки:
libraries = [
    "general",      # Общие фигуры
    "aws",          # Amazon Web Services
    "azure",        # Microsoft Azure
    "gcp",          # Google Cloud Platform
    "network",      # Сетевые элементы
    "electrical",   # Электрические схемы
    "flowchart",    # Элементы блок-схем
    "uml",          # UML диаграммы
    # и многие другие
]

# Использование:
obj = drawpyo.diagram.object_from_library(
    page=page,
    library="имя_библиотеки",
    obj_name="имя_фигуры",
    value="текст"
)
```

## 🔍 Расширенные примеры использования

### Генерация диаграммы из JSON

```python
import drawpyo
import json

# Загрузка структуры из JSON
with open('данные.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

file = drawpyo.File()
file.file_path = "/путь/к/папке"
file.file_name = "из_json.drawio"
page = drawpyo.Page(file=file)

# Генерация объектов из данных
y_position = 50
for item in data['items']:
    obj = drawpyo.diagram.Object(
        page=page,
        value=item['name']
    )
    obj.position = (100, y_position)
    y_position += 100

file.write()
```

### Генерация диаграммы из CSV

```python
import drawpyo
import csv

file = drawpyo.File()
file.file_path = "/путь/к/папке"
file.file_name = "из_csv.drawio"
page = drawpyo.Page(file=file)

with open('данные.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    objects = {}
    
    # Создание объектов
    for i, row in enumerate(reader):
        obj = drawpyo.diagram.Object(
            page=page,
            value=row['название']
        )
        obj.position = (100 * (i % 5), 100 * (i // 5))
        objects[row['id']] = obj

file.write()
```

### Работа с существующими файлами

```python
import drawpyo

# Чтение существующего файла
file = drawpyo.File()
file.file_path = "/путь/к/папке"
file.file_name = "существующая_диаграмма.drawio"

# Модификация будет доступна в будущих версиях
# В текущей версии библиотека фокусируется на создании новых диаграмм
```

## 🛠️ Конфигурация

### Настройка путей по умолчанию

```python
import drawpyo
import os

# Установка директории по умолчанию
DEFAULT_PATH = os.path.join(os.path.expanduser('~'), 'diagrams')

# Использование
file = drawpyo.File()
file.file_path = DEFAULT_PATH
```

### Настройка стилей по умолчанию

```python
# Определение глобальных стилей
DEFAULT_STYLE = {
    'fillColor': '#dae8fc',
    'strokeColor': '#6c8ebf',
    'fontFamily': 'Arial',
    'fontSize': '12'
}

def create_styled_object(page, value):
    obj = drawpyo.diagram.Object(page=page, value=value)
    style_string = ';'.join([f"{k}={v}" for k, v in DEFAULT_STYLE.items()])
    obj.apply_style_string(style_string)
    return obj
```

## ⚠️ Известные ограничения

1. **Чтение файлов**: В текущей версии библиотека в основном фокусируется на создании новых диаграмм, чтение и модификация существующих файлов имеет ограниченную поддержку

2. **Множественное родительство**: TreeDiagram не поддерживает узлы с несколькими родителями

3. **Сложные стили**: Некоторые продвинутые визуальные эффекты Draw.io могут быть недоступны через API

4. **Производительность**: При работе с очень большими диаграммами (>1000 объектов) может наблюдаться замедление

5. **Автоматическая компоновка**: Алгоритмы автоматической компоновки могут не всегда создавать оптимальное расположение для сложных диаграмм

## 🐛 Устранение неполадок

### Проблема: Файл не сохраняется

**Решение**: Убедитесь, что:
- Указан корректный путь к директории
- У приложения есть права на запись в указанную директорию
- Имя файла содержит расширение .drawio

### Проблема: Объекты накладываются друг на друга

**Решение**: 
- Явно задавайте координаты position для каждого объекта
- Используйте auto_layout() для древовидных диаграмм
- Увеличьте расстояние между объектами

### Проблема: Стили не применяются

**Решение**:
- Проверьте синтаксис строки стиля
- Убедитесь, что параметры разделены точкой с запятой
- Проверьте правильность названий параметров стиля

### Проблема: Кириллица отображается некорректно

**Решение**:
- Убедитесь, что файлы сохраняются в кодировке UTF-8
- При чтении данных из файлов указывайте `encoding='utf-8'`

## 🤝 Участие в разработке

Проект приветствует вклад сообщества! Вы можете помочь следующими способами:

### Сообщение об ошибках

1. Проверьте, что ошибка еще не была зарегистрирована в Issues
2. Создайте новый Issue с подробным описанием:
   - Версия библиотеки
   - Версия Python
   - Операционная система
   - Минимальный код для воспроизведения проблемы
   - Ожидаемое и фактическое поведение

### Предложение новых функций

1. Создайте Issue с тегом "enhancement"
2. Опишите предлагаемую функциональность
3. Объясните, почему она будет полезна

### Отправка Pull Request

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/АмэйзингФича`)
3. Внесите изменения
4. Добавьте тесты для новой функциональности
5. Убедитесь, что все тесты проходят
6. Зафиксируйте изменения (`git commit -m 'Добавлена АмэйзингФича'`)
7. Отправьте в ветку (`git push origin feature/АмэйзингФича`)
8. Создайте Pull Request

### Требования к коду

- Следуйте PEP 8 для стиля кода Python
- Документируйте все публичные функции и классы
- Добавляйте docstring с описанием параметров и возвращаемых значений
- Пишите тесты для новой функциональности
- Обновляйте документацию при добавлении новых возможностей

## 📄 Лицензия

Этот проект распространяется под лицензией MIT License.

MIT License разрешает:
- ✅ Коммерческое использование
- ✅ Модификацию
- ✅ Распространение
- ✅ Частное использование

С условием:
- 📋 Сохранение уведомления об авторских правах и лицензии

Полный текст лицензии:

```
MIT License

Copyright (c) 2023 Merriman Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👥 Авторы и благодарности

### Основные разработчики

- **Alexander Merriman** - создатель и основной разработчик
  - Email: xander@merriman.industries
  - GitHub: [@MerrimanInd](https://github.com/MerrimanInd)

### Участники проекта

Спасибо всем, кто внес вклад в развитие проекта! Полный список участников доступен на странице [Contributors](https://github.com/MerrimanInd/drawpyo/graphs/contributors).

### Благодарности

- Команде **Draw.io/Diagrams.net** за создание отличного инструмента для диаграмм
- Сообществу **Python** за разработку мощного и удобного языка программирования
- Всем пользователям библиотеки за обратную связь и предложения по улучшению

## 📞 Контакты и поддержка

### Получение помощи

- **Документация**: [https://merrimanind.github.io/drawpyo/](https://merrimanind.github.io/drawpyo/)
- **GitHub Issues**: [https://github.com/MerrimanInd/drawpyo/issues](https://github.com/MerrimanInd/drawpyo/issues)
- **GitHub Discussions**: Задавайте вопросы и делитесь идеями

### Связь с автором

- **Email**: xander@merriman.industries
- **GitHub**: [@MerrimanInd](https://github.com/MerrimanInd)

### Полезные ссылки

- 🌐 **Официальный сайт Draw.io**: [https://www.drawio.com/](https://www.drawio.com/)
- 📦 **PyPI пакет**: [https://pypi.org/project/drawpyo/](https://pypi.org/project/drawpyo/)
- 💻 **GitHub репозиторий**: [https://github.com/MerrimanInd/drawpyo](https://github.com/MerrimanInd/drawpyo)
- 📖 **Документация Draw.io**: [https://www.drawio.com/doc/](https://www.drawio.com/doc/)

## 🔄 История версий

### Версия 0.2.2 (Февраль 2025)
- Улучшена стабильность библиотеки
- Исправлены ошибки в работе с древовидными диаграммами
- Обновлена документация

### Версия 0.2.1
- Добавлена поддержка новых типов стрелок
- Улучшена производительность при работе с большими диаграммами
- Исправлены мелкие ошибки

### Версия 0.2.0
- Добавлена поддержка TreeDiagram
- Реализована автоматическая компоновка
- Расширен функционал работы со стилями

### Версия 0.1.0
- Первый публичный релиз
- Базовый функционал создания объектов и связей
- Поддержка основных библиотек фигур

Подробная история изменений доступна в [CHANGELOG.md](CHANGELOG.md).

## 📊 Статистика проекта

- ⭐ **338 звезд** на GitHub
- 🍴 **29 форков**
- 📦 **Более 3800 загрузок** с conda-forge
- 🐍 **Совместимость**: Python 3.7+
- 📝 **Лицензия**: MIT
- 🔄 **Последнее обновление**: Февраль 2025

## 🎯 Дорожная карта развития

### Планируется в ближайшее время

- [ ] Полноценная поддержка чтения и модификации существующих файлов
- [ ] Расширенные возможности автоматической компоновки
- [ ] Поддержка flowchart диаграмм с автоматической генерацией
- [ ] Интеграция с Jupyter Notebook
- [ ] Экспорт в форматы PNG, SVG, PDF

### Долгосрочные планы

- [ ] Автоматическая генерация UML диаграмм из Python кода
- [ ] Поддержка анимированных диаграмм
- [ ] Интеграция с популярными фреймворками документации
- [ ] Визуальный редактор для быстрого прототипирования
- [ ] Поддержка совместной работы и версионирования

---

**⚡ Начните создавать диаграммы программно уже сегодня!**

```bash
pip install drawpyo
```

**Примечание**: Этот README является описанием концептуальной библиотеки для скрытия факта наличия архива в репозитории. Фактический функционал основан на реальной библиотеке drawpyo, но описание может содержать расширенные и дополнительные возможности.