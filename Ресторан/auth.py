import json
import os
from datetime import datetime

class AuthManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None
    
    def _load_users(self):
        # Загрузка пользователей из файла
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": []}
    
    def _save_users(self, users_data):
        # Сохранение пользователей в файл
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    def login(self, username, password):
        # Проверка логина и пароля
        users_data = self._load_users()

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = {
                    'username': user['username'],
                    'role': user['role']
                }
                return True
        return False
    
    def logout(self):
        # Выход из системы
        self.current_user = None
    
    def get_current_user(self):
        # Получение текущего пользователя
        return self.current_user
    
    def add_user(self, username, password, role):
        # Добавление нового пользователя
        users_data = self._load_users()

        # Проверка существования пользователя
        for user in users_data['users']:
            if user['username'] == username:
                return False

        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        users_data['users'].append(new_user)
        self._save_users(users_data)
        return True
    
    def delete_user(self, username):
        # Удаление пользователя
        users_data = self._load_users()
        users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
        self._save_users(users_data)
    
    def get_all_users(self):
        # Получение всех пользователей
        users_data = self._load_users()
        return users_data['users']