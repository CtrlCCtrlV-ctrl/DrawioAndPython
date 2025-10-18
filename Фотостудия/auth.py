import json
import os

USERS_FILE = 'users.json'

def load_users():
    """Загрузка пользователей из файла"""
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users_data):
    """Сохранение пользователей в файл"""
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

    for user in users_data['users']:
        if user['username'] == username:
            return False

    new_user = {
        'username': username,
        'password': password,
        'role': role,
        'full_name': full_name,
        'created': '2024-01-01'
    }

    users_data['users'].append(new_user)
    save_users(users_data)
    return True

def get_all_users():
    """Получение всех пользователей"""
    users_data = load_users()
    return users_data['users']

def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)

current_user = None