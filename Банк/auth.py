import json
import os
from datetime import datetime

# Путь к файлу с пользователями
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
            return user
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
        "full_name": full_name,
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь успешно создан"

def change_password(username, old_password, new_password):
    """Изменение пароля пользователя"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username:
            if user['password'] == old_password:
                user['password'] = new_password
                save_users(users_data)
                return True, "Пароль успешно изменен"
            else:
                return False, "Неверный старый пароль"

    return False, "Пользователь не найден"

def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)
    return True

def get_all_users():
    """Получение списка всех пользователей"""
    return load_users()['users']