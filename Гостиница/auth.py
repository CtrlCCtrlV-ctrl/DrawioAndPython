import json
from datetime import datetime
from pathlib import Path

# Путь к файлу пользователей
USERS_FILE = Path(__file__).parent / 'users.json'

# Текущий авторизованный пользователь
current_user = None


def load_users():
    """Загрузка пользователей из JSON файла"""
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_users(users_data):
    """Сохранение пользователей в JSON файл"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)


def authenticate(username, password):
    """Проверка логина и пароля"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None


def create_user(username, password, role, full_name):
    """Создание нового пользователя"""
    users_data = load_users()

    # Проверка на существование пользователя
    for user in users_data['users']:
        if user['username'] == username:
            return False, "Пользователь уже существует"

    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "full_name": full_name
    }

    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь создан успешно"


def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)
    return True


def get_all_users():
    """Получение всех пользователей"""
    return load_users()['users']


def set_current_user(user):
    """Установка текущего пользователя"""
    global current_user
    current_user = user


def get_current_user():
    """Получение текущего пользователя"""
    return current_user


def logout():
    """Выход из системы"""
    global current_user
    current_user = None