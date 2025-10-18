import json
import os
from datetime import datetime

# Глобальная переменная для текущего пользователя
current_user = None

class AuthManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.init_users()
    
    def init_users(self):
        """Инициализация файла пользователей"""
        # Файл пользователей уже создан с тестовыми данными
        pass
    
    
    def login(self, username, password):
        """Проверка логина и пароля"""
        global current_user

        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for user in data['users']:
            if user['username'] == username and user['password'] == password:
                current_user = {
                    'username': username,
                    'role': user['role'],
                    'login_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                return True
        return False
    
    def create_user(self, username, password, role):
        """Создание нового пользователя"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Проверка существования пользователя
        for user in data['users']:
            if user['username'] == username:
                return False, "Пользователь уже существует"
        
        # Добавление нового пользователя
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data['users'].append(new_user)
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True, "Пользователь создан"
    
    def change_password(self, username, old_password, new_password):
        """Смена пароля"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for user in data['users']:
            if user['username'] == username and user['password'] == old_password:
                user['password'] = new_password

                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                return True, "Пароль изменен"

        return False, "Неверный старый пароль"
    
    def get_all_users(self):
        """Получение списка всех пользователей"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [{'username': u['username'], 'role': u['role'], 'created': u['created']} 
                for u in data['users']]

def get_current_user():
    """Получение текущего пользователя"""
    global current_user
    return current_user

def logout_user():
    """Выход пользователя"""
    global current_user
    current_user = None

def is_admin():
    """Проверка является ли текущий пользователь администратором"""
    global current_user
    return current_user and current_user['role'] == 'admin'

def is_dispatcher():
    """Проверка является ли текущий пользователь диспетчером"""
    global current_user
    return current_user and current_user['role'] == 'dispatcher'

def is_passenger():
    """Проверка является ли текущий пользователь пассажиром"""
    global current_user
    return current_user and current_user['role'] == 'passenger'