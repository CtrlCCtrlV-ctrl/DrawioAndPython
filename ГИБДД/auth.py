import json
import os

# Глобальная переменная для текущего пользователя
current_user = None

class AuthManager:
    def __init__(self):
        self.users_file = 'users.json'
    
    def authenticate(self, username, password):
        # Проверка логина и пароля
        global current_user

        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                current_user = {
                    'username': user['username'],
                    'role': user['role']
                }
                return True

        return False
    
    def create_user(self, username, password, role):
        # Создание нового пользователя
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        # Проверка существования пользователя
        for user in users_data['users']:
            if user['username'] == username:
                return False

        # Добавление нового пользователя
        new_user = {
            'username': username,
            'password': password,
            'role': role,
            'created': datetime.now().strftime('%Y-%m-%d')
        }

        users_data['users'].append(new_user)

        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)

        return True
    
    def change_password(self, username, old_password, new_password):
        # Смена пароля пользователя
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        for user in users_data['users']:
            if user['username'] == username and user['password'] == old_password:
                user['password'] = new_password

                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump(users_data, f, ensure_ascii=False, indent=2)

                return True

        return False
    
    def get_user_role(self, username):
        # Получение роли пользователя
        with open(self.users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for user in users_data['users']:
            if user['username'] == username:
                return user['role']
        
        return None

def get_current_user():
    # Получение текущего пользователя
    global current_user
    return current_user

def logout():
    # Выход из системы
    global current_user
    current_user = None

def is_authenticated():
    # Проверка авторизации
    global current_user
    return current_user is not None