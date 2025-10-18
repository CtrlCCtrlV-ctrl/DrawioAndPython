import json
import os
from datetime import datetime

USERS_FILE = 'users.json'

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
            return {
                'username': user['username'],
                'role': user['role'],
                'full_name': user['full_name']
            }
    return None

def create_user(username, password, role, full_name):
    """Создание нового пользователя"""
    users_data = load_users()

    # Проверка существования пользователя
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
    return True, "Пользователь успешно создан"

def get_all_users():
    """Получение списка всех пользователей"""
    users_data = load_users()
    return users_data['users']

def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)
    return True

class Session:
    """Класс для управления сессией пользователя"""
    def __init__(self):
        self.current_user = None
        self.is_authenticated = False
    
    def login(self, user_data):
        self.current_user = user_data
        self.is_authenticated = True
    
    def logout(self):
        self.current_user = None
        self.is_authenticated = False
    
    def get_role(self):
        return self.current_user['role'] if self.current_user else None

# Глобальная сессия
session = Session()