import json
import os

current_user = None

def load_users():
    """Загрузка пользователей из файла"""
    with open('users.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users_data):
    """Сохранение пользователей в файл"""
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def verify_credentials(username, password):
    """Проверка логина и пароля"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def login(username, password):
    """Вход в систему"""
    global current_user
    user = verify_credentials(username, password)
    if user:
        current_user = {
            'username': user['username'],
            'role': user['role'],
            'full_name': user['full_name']
        }
        return True
    return False

def logout():
    """Выход из системы"""
    global current_user
    current_user = None

def get_current_user():
    """Получение текущего пользователя"""
    return current_user

def register_user(username, password, role, full_name):
    """Регистрация нового пользователя"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username:
            return False, "Пользователь уже существует"

    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "full_name": full_name,
        "created": "2024-01-01"
    }

    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь успешно создан"

def get_all_users():
    """Получение всех пользователей"""
    users_data = load_users()
    return users_data['users']

def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)