import json
from datetime import datetime

class AuthManager:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.current_user = None
        self.load_users()
    
    def load_users(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users_data = json.load(f)
        except FileNotFoundError:
            self.users_data = {"users": []}
            self.save_users()
    
    def save_users(self):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users_data, f, indent=2, ensure_ascii=False)
    
    
    def login(self, username, password):
        for user in self.users_data['users']:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                return True
        return False
    
    def logout(self):
        self.current_user = None
    
    def get_current_user(self):
        return self.current_user
    
    def get_role(self):
        if self.current_user:
            return self.current_user['role']
        return None
    
    def create_user(self, username, password, role, phone=""):
        if self.user_exists(username):
            return False

        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "phone": phone
        }

        self.users_data['users'].append(new_user)
        self.save_users()
        return True
    
    def user_exists(self, username):
        return any(user['username'] == username for user in self.users_data['users'])
    
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