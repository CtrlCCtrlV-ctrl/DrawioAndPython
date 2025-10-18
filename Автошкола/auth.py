import json

class AuthManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None

    def authenticate(self, username, password):
        """Проверка логина и пароля"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for user in data['users']:
                if user['username'] == username and user['password'] == password:
                    self.current_user = user
                    return True
        except FileNotFoundError:
            return False
        return False
    
    def create_user(self, username, password, role, full_name):
        """Создание нового пользователя"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for user in data['users']:
                if user['username'] == username:
                    return False

            from datetime import datetime
            new_user = {
                "username": username,
                "password": password,
                "role": role,
                "full_name": full_name,
                "created": datetime.now().strftime("%Y-%m-%d")
            }

            data['users'].append(new_user)

            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except FileNotFoundError:
            return False
    
    def get_all_users(self):
        """Получение всех пользователей"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data['users']
        except FileNotFoundError:
            return []

    def delete_user(self, username):
        """Удаление пользователя"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data['users'] = [u for u in data['users'] if u['username'] != username]

            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except FileNotFoundError:
            pass

    def logout(self):
        """Выход из системы"""
        self.current_user = None