import json

class AuthManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None
    
    def login(self, username, password):
        """Проверка логина и пароля"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for user in data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = {
                    'username': user['username'],
                    'role': user['role']
                }
                return True
        return False
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
    
    def get_current_user(self):
        """Получение текущего пользователя"""
        return self.current_user
    
    def create_user(self, username, password, role):
        """Создание нового пользователя"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Проверка существования пользователя
        for user in data['users']:
            if user['username'] == username:
                return False

        from datetime import datetime
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data['users'].append(new_user)

        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return True
    
    def get_all_users(self):
        """Получение всех пользователей"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['users']
    
    def delete_user(self, username):
        """Удаление пользователя"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data['users'] = [u for u in data['users'] if u['username'] != username]
        
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)