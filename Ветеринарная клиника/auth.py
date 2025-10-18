import json
from pathlib import Path

USERS_FILE = "users.json"

def load_users():
    """Загрузка пользователей из файла"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"users": []}

def authenticate(username, password):
    """Проверка логина и пароля"""
    users_data = load_users()

    for user in users_data.get("users", []):
        if user["username"] == username and user["password"] == password:
            return user
    return None

def create_user(username, password, role, full_name):
    """Создание нового пользователя"""
    users_data = load_users()

    # Проверка на существование
    for user in users_data["users"]:
        if user["username"] == username:
            return False, "Пользователь уже существует"

    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "full_name": full_name,
        "created": "2025-10-17 10:00:00"
    }

    users_data["users"].append(new_user)
    save_users(users_data)
    return True, "Пользователь создан успешно"

def save_users(users_data):
    """Сохранение пользователей в файл"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def get_all_users():
    """Получить всех пользователей"""
    users_data = load_users()
    return users_data.get("users", [])

def delete_user(username):
    """Удалить пользователя"""
    users_data = load_users()
    users_data["users"] = [u for u in users_data["users"] if u["username"] != username]
    save_users(users_data)
    return True