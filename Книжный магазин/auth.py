import json
import os

USERS_FILE = 'users.json'

def load_users():
    """Загрузка пользователей из файла"""
    if not os.path.exists(USERS_FILE):
        raise FileNotFoundError(f"Файл {USERS_FILE} не найден. Запустите программу с существующими тестовыми данными.")

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

def register_user(username, password, full_name, role='client'):
    """Регистрация нового пользователя"""
    users_data = load_users()

    # Проверка существования пользователя
    for user in users_data['users']:
        if user['username'] == username:
            return False, "Пользователь уже существует"

    # Создание нового пользователя
    new_id = max([u['id'] for u in users_data['users']]) + 1 if users_data['users'] else 1
    from datetime import datetime
    new_user = {
        "id": new_id,
        "username": username,
        "password": password,
        "role": role,
        "full_name": full_name,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Регистрация успешна"

def get_all_users():
    """Получить всех пользователей"""
    users_data = load_users()
    return users_data['users']

def delete_user(user_id):
    """Удалить пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['id'] != user_id]
    save_users(users_data)

def update_user(user_id, full_name=None, role=None, password=None):
    """Обновить данные пользователя"""
    users_data = load_users()
    for user in users_data['users']:
        if user['id'] == user_id:
            if full_name:
                user['full_name'] = full_name
            if role:
                user['role'] = role
            if password:
                user['password'] = password
            break
    save_users(users_data)