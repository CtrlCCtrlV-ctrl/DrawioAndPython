import json
from datetime import datetime

USERS_FILE = 'users.json'

def load_users():
    """Загрузка пользователей из файла"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

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
    
    # Генерация нового ID
    new_id = max([u['id'] for u in users_data['users']], default=0) + 1
    
    new_user = {
        'id': new_id,
        'username': username,
        'password': password,
        'role': role,
        'full_name': full_name,
        'created': datetime.now().strftime('%Y-%m-%d')
    }
    
    users_data['users'].append(new_user)
    save_users(users_data)
    return True, "Пользователь создан успешно"

def get_all_users():
    """Получение всех пользователей"""
    users_data = load_users()
    return users_data['users']

def delete_user(user_id):
    """Удаление пользователя"""
    users_data = load_users()
    users_data['users'] = [u for u in users_data['users'] if u['id'] != user_id]
    save_users(users_data)

def init_default_users():
    """Инициализация пользователей по умолчанию"""
    users_data = load_users()
    
    if not users_data['users']:
        default_users = [
            {
                'id': 1,
                'username': 'admin',
                'password': 'admin123',
                'role': 'administrator',
                'full_name': 'Администратор Системы',
                'created': '2024-01-01'
            },
            {
                'id': 2,
                'username': 'manager',
                'password': 'manager123',
                'role': 'manager',
                'full_name': 'Менеджер Петров П.П.',
                'created': '2024-01-01'
            },
            {
                'id': 3,
                'username': 'client',
                'password': 'client123',
                'role': 'client',
                'full_name': 'Иванов Иван Иванович',
                'created': '2024-01-01'
            }
        ]
        
        users_data['users'] = default_users
        save_users(users_data)