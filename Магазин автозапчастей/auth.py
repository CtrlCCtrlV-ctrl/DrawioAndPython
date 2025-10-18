import json
from datetime import datetime

class AuthManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None
    
    
    
    def _load_users(self):
        # Загрузка пользователей из файла
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_users(self, data):
        # Сохранение пользователей в файл
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def login(self, username, password):
        # Проверка логина и пароля
        users_data = self._load_users()

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, user['role'], user['full_name']

        return False, None, None
    
    def logout(self):
        # Выход из системы
        self.current_user = None
    
    def create_user(self, username, password, role, full_name):
        # Создание нового пользователя
        users_data = self._load_users()
        
        # Проверка существования пользователя
        for user in users_data['users']:
            if user['username'] == username:
                return False, "Пользователь уже существует"
        
        # Генерация ID
        new_id = max([u['id'] for u in users_data['users']]) + 1 if users_data['users'] else 1
        
        new_user = {
            "id": new_id,
            "username": username,
            "password": password,
            "role": role,
            "full_name": full_name,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users_data['users'].append(new_user)
        self._save_users(users_data)
        return True, "Пользователь создан успешно"
    
    def get_all_users(self):
        # Получение всех пользователей
        users_data = self._load_users()
        return users_data['users']
    
    def delete_user(self, user_id):
        # Удаление пользователя
        users_data = self._load_users()
        users_data['users'] = [u for u in users_data['users'] if u['id'] != user_id]
        self._save_users(users_data)
        return True
    
    def get_current_user(self):
        # Получение текущего пользователя
        return self.current_user