import json
import os

class AuthManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.current_user = None
    
    def authenticate(self, username, password):
        """Аутентификация пользователя"""
        if not os.path.exists(self.users_file):
            return None

        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return user

        return None
    
    def create_user(self, username, password, role='reader'):
        """Создание нового пользователя"""
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
            "created": datetime.now().strftime("%Y-%m-%d")
        }
        
        users_data['users'].append(new_user)
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        
        return True, "Пользователь создан"
    
    def change_password(self, username, old_password, new_password):
        """Смена пароля пользователя"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for user in users_data['users']:
            if user['username'] == username and user['password'] == old_password:
                user['password'] = new_password
                
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump(users_data, f, ensure_ascii=False, indent=2)
                
                return True, "Пароль изменен"
        
        return False, "Неверный старый пароль"
    
    def get_user_role(self, username):
        """Получение роли пользователя"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for user in users_data['users']:
            if user['username'] == username:
                return user['role']
        
        return None
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        return True

from datetime import datetime