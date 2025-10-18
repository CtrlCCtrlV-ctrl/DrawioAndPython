import json
import os
from datetime import datetime

def load_users():
    """Загрузка пользователей из файла"""
    if not os.path.exists('users.json'):
        # Создание файла с дефолтными пользователями
        default_users = {
            "users": [
                {
                    "id": 1,
                    "username": "admin",
                    "password": "admin123",
                    "role": "administrator",
                    "name": "Администратор Системы",
                    "created": "2024-01-01"
                },
                {
                    "id": 2,
                    "username": "doctor1",
                    "password": "doctor123",
                    "role": "doctor",
                    "doctor_id": 1,
                    "name": "Иванов Иван Иванович",
                    "created": "2024-01-01"
                },
                {
                    "id": 3,
                    "username": "patient1",
                    "password": "patient123",
                    "role": "patient",
                    "patient_id": 1,
                    "name": "Петров Петр Петрович",
                    "created": "2024-01-01"
                }
            ]
        }
        save_users(default_users)
        return default_users
    
    with open('users.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users_data):
    """Сохранение пользователей в файл"""
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def authenticate(username, password):
    """Проверка логина и пароля"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def create_user(username, password, role, name, doctor_id=None, patient_id=None):
    """Создание нового пользователя"""
    users_data = load_users()
    
    # Проверка уникальности username
    for user in users_data['users']:
        if user['username'] == username:
            return False, "Пользователь с таким логином уже существует"
    
    new_user = {
        "id": max([u['id'] for u in users_data['users']]) + 1 if users_data['users'] else 1,
        "username": username,
        "password": password,
        "role": role,
        "name": name,
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    if doctor_id:
        new_user['doctor_id'] = doctor_id
    if patient_id:
        new_user['patient_id'] = patient_id
    
    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь успешно создан"

def get_user_by_id(user_id):
    """Получение пользователя по ID"""
    users_data = load_users()
    for user in users_data['users']:
        if user['id'] == user_id:
            return user
    return None

def delete_user(user_id):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['id'] != user_id]
    save_users(users_data)