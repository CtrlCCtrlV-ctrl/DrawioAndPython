import json
import os
from datetime import datetime

# Путь к файлу пользователей
USERS_FILE = 'users.json'

def load_users():
    """Загрузка пользователей из JSON файла"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файл не существует, возвращаем пустую структуру
        return {"users": []}
    except json.JSONDecodeError:
        # Если файл поврежден, возвращаем пустую структуру
        return {"users": []}

def save_users(users_data):
    """Сохранение пользователей в JSON файл"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def authenticate(username, password):
    """Проверка логина и пароля"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return {
                'username': user['username'],
                'role': user['role'],
                'full_name': user['full_name']
            }
    return None

def register_user(username, password, role, full_name):
    """Регистрация нового пользователя"""
    users_data = load_users()

    # Проверка существования пользователя
    for user in users_data['users']:
        if user['username'] == username:
            return False, "Пользователь уже существует"

    # Добавление нового пользователя
    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "full_name": full_name
    }

    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь успешно зарегистрирован"

def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)

def get_all_users():
    """Получение списка всех пользователей"""
    users_data = load_users()
    return users_data['users']

class Session:
    """Простое управление сессией"""
    current_user = None
    
    @classmethod
    def login(cls, user_data):
        cls.current_user = user_data
    
    @classmethod
    def logout(cls):
        cls.current_user = None
    
    @classmethod
    def is_authenticated(cls):
        return cls.current_user is not None
    
    @classmethod
    def get_role(cls):
        return cls.current_user['role'] if cls.current_user else None