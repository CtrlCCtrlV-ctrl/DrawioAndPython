import json

class AuthManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None
    
    def _load_users(self):
        """Загрузка пользователей из JSON"""
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_users(self, users_data):
        """Сохранение пользователей в JSON"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
    
    def login(self, username, password):
        """Проверка логина и пароля"""
        users_data = self._load_users()

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = {
                    'username': user['username'],
                    'role': user['role'],
                    'email': user.get('email', '')
                }
                return True
        return False
    
    def register(self, username, password, role, email):
        """Регистрация нового пользователя"""
        users_data = self._load_users()

        # Проверка существования пользователя
        if any(u['username'] == username for u in users_data['users']):
            return False, "Пользователь уже существует"

        # Добавление нового пользователя
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "created": "2024-01-01 10:00:00",
            "email": email
        }
        users_data['users'].append(new_user)
        self._save_users(users_data)
        return True, "Пользователь успешно создан"
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
    
    def get_all_users(self):
        """Получение списка всех пользователей (без паролей)"""
        users_data = self._load_users()
        return [{k: v for k, v in u.items() if k != 'password'} 
                for u in users_data['users']]
    
    def delete_user(self, username):
        """Удаление пользователя"""
        users_data = self._load_users()
        users_data['users'] = [u for u in users_data['users'] 
                               if u['username'] != username]
        self._save_users(users_data)
        return True