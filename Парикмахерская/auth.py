import json
import os
from datetime import datetime

USERS_FILE = 'users.json'

def init_users_file():
    """Инициализация файла пользователей с данными по умолчанию"""
    if not os.path.exists(USERS_FILE):
        default_users = {
            "users": [
                {
                    "username": "admin",
                    "password": "admin123",
                    "role": "administrator",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "full_name": "Администратор Системы"
                },
                {
                    "username": "master1",
                    "password": "master123",
                    "role": "master",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "full_name": "Иванова Мария",
                    "master_id": 1
                },
                {
                    "username": "client1",
                    "password": "client123",
                    "role": "client",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "full_name": "Петров Иван",
                    "client_id": 1
                }
            ]
        }
        save_users(default_users)
        return default_users
    return load_users()

def load_users():
    """Загрузка пользователей из файла"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": []}

def save_users(data):
    """Сохранение пользователей в файл"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def authenticate(username, password):
    """Проверка логина и пароля"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def create_user(username, password, role, full_name, extra_data=None):
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
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "full_name": full_name
    }

    if extra_data:
        new_user.update(extra_data)

    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь создан"

def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)

def get_all_users():
    """Получение всех пользователей"""
    return load_users()['users']

class Session:
    """Класс для управления текущей сессией"""
    current_user = None
    
    @classmethod
    def login(cls, user):
        cls.current_user = user
    
    @classmethod
    def logout(cls):
        cls.current_user = None
    
    @classmethod
    def is_authenticated(cls):
        return cls.current_user is not None
    
    @classmethod
    def get_role(cls):
        if cls.current_user:
            return cls.current_user.get('role')
        return None