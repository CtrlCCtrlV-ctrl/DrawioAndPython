import json
from datetime import datetime

class AuthManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None
        self.load_users()

    def load_users(self):
        with open(self.users_file, 'r', encoding='utf-8') as f:
            self.users_data = json.load(f)

    def login(self, username, password):
        for user in self.users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True, user['role']
        return False, None

    def logout(self):
        self.current_user = None

    def create_user(self, username, password, role, full_name):
        if any(u['username'] == username for u in self.users_data['users']):
            return False, "Пользователь уже существует"

        new_user = {
            'username': username,
            'password': password,
            'role': role,
            'full_name': full_name,
            'created': datetime.now().strftime('%Y-%m-%d')
        }
        self.users_data['users'].append(new_user)
        self.save_users()
        return True, "Пользователь создан"

    def save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users_data, f, ensure_ascii=False, indent=2)

    def get_all_users(self):
        return self.users_data['users']

    def delete_user(self, username):
        self.users_data['users'] = [u for u in self.users_data['users'] if u['username'] != username]
        self.save_users()

    def update_user(self, username, **kwargs):
        for user in self.users_data['users']:
            if user['username'] == username:
                for key, value in kwargs.items():
                    user[key] = value
                self.save_users()
                return True
        return False