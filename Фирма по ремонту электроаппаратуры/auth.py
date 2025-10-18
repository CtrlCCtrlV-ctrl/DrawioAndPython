import json
import os
from datetime import datetime

class AuthManager:
    """Менеджер аутентификации и авторизации"""

    def __init__(self):
        self.users_file = 'users.json'
        self.current_user = None
    
    def authenticate(self, username, password):
        """Проверка учетных данных"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, user['role']

        return False, None
    
    def register_user(self, username, password, role, full_name):
        """Регистрация нового пользователя"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        # Проверка существования пользователя
        for user in users_data['users']:
            if user['username'] == username:
                return False, "Пользователь уже существует"

        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "full_name": full_name,
            "created": datetime.now().isoformat()
        }

        users_data['users'].append(new_user)

        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)

        return True, "Пользователь успешно зарегистрирован"
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
    
    def get_all_users(self):
        """Получение списка всех пользователей"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        return users_data['users']
    
    def delete_user(self, username):
        """Удаление пользователя"""
        if username == 'admin':
            return False, "Нельзя удалить администратора"
        
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        
        return True, "Пользователь удален"