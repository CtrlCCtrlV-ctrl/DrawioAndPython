import json
import os
from datetime import datetime

USERS_FILE = 'users.json'

def load_users():
    """Загрузка пользователей из файла"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": []}

def save_users(users_data):
    """Сохранение пользователей в файл"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def authenticate(username, password):
    """Проверка учетных данных пользователя"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return {
                'username': user['username'],
                'role': user['role'],
                'full_name': user['full_name'],
                'email': user.get('email', ''),
                'company': user.get('company', '')
            }
    return None

def register_user(username, password, role, full_name, email, company=''):
    """Регистрация нового пользователя"""
    users_data = load_users()

    # Проверка существования пользователя
    for user in users_data['users']:
        if user['username'] == username:
            return False, "Пользователь с таким именем уже существует"

    # Создание нового пользователя
    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "full_name": full_name,
        "email": email
    }

    if role == "employer" and company:
        new_user["company"] = company

    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь успешно зарегистрирован"

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

def update_user(username, **kwargs):
    """Обновление данных пользователя"""
    users_data = load_users()
    for user in users_data['users']:
        if user['username'] == username:
            for key, value in kwargs.items():
                user[key] = value
            save_users(users_data)
            return True
    return False