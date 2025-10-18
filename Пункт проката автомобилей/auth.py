import json
from datetime import datetime
import os

class AuthManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.current_user = None
        self.init_users_db()
    
    def init_users_db(self):
        """Инициализация базы пользователей"""
        if not os.path.exists(self.users_file):
            default_users = {
                "users": [
                    {
                        "username": "admin",
                        "password": "admin123",
                        "role": "administrator",
                        "full_name": "Администратор системы",
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    },
                    {
                        "username": "manager",
                        "password": "manager123",
                        "role": "manager",
                        "full_name": "Менеджер проката",
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    },
                    {
                        "username": "client",
                        "password": "client123",
                        "role": "client",
                        "full_name": "Иванов Иван",
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ]
            }
            self.save_users(default_users)
    
    
    def load_users(self):
        """Загрузка пользователей из файла"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"users": []}
    
    def save_users(self, data):
        """Сохранение пользователей в файл"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def authenticate(self, username, password):
        """Аутентификация пользователя"""
        users_data = self.load_users()

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, user['role']
        return False, None
    
    def register_user(self, username, password, role, full_name):
        """Регистрация нового пользователя"""
        users_data = self.load_users()
        
        # Проверка существования пользователя
        for user in users_data['users']:
            if user['username'] == username:
                return False, "Пользователь уже существует"
        
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "full_name": full_name,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users_data['users'].append(new_user)
        self.save_users(users_data)
        return True, "Пользователь успешно создан"
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
    
    def get_current_user(self):
        """Получение текущего пользователя"""
        return self.current_user