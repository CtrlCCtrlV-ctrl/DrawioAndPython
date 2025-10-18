import json
import os
from datetime import datetime

class Auth:
    """Модуль аутентификации и управления пользователями"""

    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None
    
    def load_users(self):
        """Загрузка пользователей из JSON файла"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": []}
    
    def save_users(self, data):
        """Сохранение пользователей в JSON файл"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def login(self, username, password):
        """Проверка логина и пароля"""
        users_data = self.load_users()

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, user['role'], user['name']

        return False, None, None
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
    
    def register(self, username, password, role, name):
        """Регистрация нового пользователя"""
        users_data = self.load_users()

        # Проверка существования пользователя
        for user in users_data['users']:
            if user['username'] == username:
                return False, "Пользователь уже существует"

        # Добавление нового пользователя
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "name": name,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        users_data['users'].append(new_user)
        self.save_users(users_data)

        return True, "Пользователь успешно создан"
    
    def get_all_users(self):
        """Получение всех пользователей"""
        users_data = self.load_users()
        return users_data['users']
    
    def delete_user(self, username):
        """Удаление пользователя"""
        users_data = self.load_users()
        users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
        self.save_users(users_data)
        return True