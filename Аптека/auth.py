import json
from datetime import datetime

USERS_FILE = 'users.json'

def load_users():
    """Загрузка пользователей из JSON"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": []}

def save_users(data):
    """Сохранение пользователей в JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def authenticate(username, password):
    """Проверка логина и пароля"""
    users_data = load_users()

    for user in users_data['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def create_user(username, password, role):
    """Создание нового пользователя"""
    users_data = load_users()
    
    # Проверка существования пользователя
    for user in users_data['users']:
        if user['username'] == username:
            return False
    
    # Добавление нового пользователя
    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    users_data['users'].append(new_user)
    save_users(users_data)
    return True

def delete_user(username):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
    save_users(users_data)

def get_all_users():
    """Получение списка всех пользователей"""
    return load_users()['users']

# Глобальная переменная для текущего пользователя
current_user = None

def set_current_user(user):
    """Установка текущего пользователя"""
    global current_user
    current_user = user

def get_current_user():
    """Получение текущего пользователя"""
    return current_user