import json

class AuthSystem:
    def __init__(self):
        self.users_file = 'users.json'
        self.current_user = None
    
    def load_users(self):
        # Загрузка пользователей из файла
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_users(self, data):
        # Сохранение пользователей в файл
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def authenticate(self, username, password):
        # Проверка логина и пароля
        users_data = self.load_users()

        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, user
        return False, None
    
    def register_user(self, username, password, role, full_name, phone):
        # Регистрация нового пользователя
        users_data = self.load_users()
        
        # Проверка существования пользователя
        for user in users_data['users']:
            if user['username'] == username:
                return False, "Пользователь уже существует"
        
        # Создание нового пользователя
        new_id = max([u['id'] for u in users_data['users']]) + 1 if users_data['users'] else 1
        new_user = {
            "id": new_id,
            "username": username,
            "password": password,
            "role": role,
            "full_name": full_name,
            "phone": phone,
            "created": "2024-01-15 10:00:00"
        }
        
        users_data['users'].append(new_user)
        self.save_users(users_data)
        return True, "Регистрация успешна"
    
    def get_all_users(self):
        # Получение всех пользователей
        users_data = self.load_users()
        return users_data['users']
    
    def delete_user(self, user_id):
        # Удаление пользователя
        users_data = self.load_users()
        users_data['users'] = [u for u in users_data['users'] if u['id'] != user_id]
        self.save_users(users_data)
        return True
    
    def update_user(self, user_id, **kwargs):
        # Обновление данных пользователя
        users_data = self.load_users()
        for user in users_data['users']:
            if user['id'] == user_id:
                for key, value in kwargs.items():
                    user[key] = value
                break
        self.save_users(users_data)
        return True
    
    def logout(self):
        # Выход из системы
        self.current_user = None