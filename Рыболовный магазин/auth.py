import json

class AuthManager:
    def __init__(self):
        self.current_user = None
        # Тестовые пользователи (без шифрования и файлов)
        self.users_data = {
            "users": [
                {
                    "username": "admin",
                    "password": "admin123",
                    "role": "administrator",
                    "created": "2024-01-01 00:00:00"
                },
                {
                    "username": "seller",
                    "password": "seller123",
                    "role": "seller",
                    "created": "2024-01-01 00:00:00"
                },
                {
                    "username": "client",
                    "password": "client123",
                    "role": "client",
                    "created": "2024-01-01 00:00:00"
                }
            ]
        }

    def login(self, username, password):
        # Проверка логина и пароля
        for user in self.users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, user['role']
        return False, None

    def register(self, username, password, role="client"):
        # Проверка существования пользователя
        for user in self.users_data['users']:
            if user['username'] == username:
                return False, "Пользователь уже существует"

        # Создание нового пользователя
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "created": "2024-01-01 00:00:00"
        }
        self.users_data['users'].append(new_user)
        return True, "Пользователь создан"

    def logout(self):
        # Выход из системы
        self.current_user = None

    def get_all_users(self):
        # Получение всех пользователей (без паролей)
        result = []
        for user in self.users_data['users']:
            result.append({
                'username': user['username'],
                'role': user['role'],
                'created': user['created']
            })
        return result

    def delete_user(self, username):
        # Удаление пользователя
        self.users_data['users'] = [u for u in self.users_data['users'] if u['username'] != username]
        return True