import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from auth import AuthManager, get_current_user, logout

class GIBDDSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Информационная система ГИБДД")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        self.auth_manager = AuthManager()
        self.current_frame = None
        self.show_login_window()
        
    def show_login_window(self):
        # Окно авторизации
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(expand=True)
        
        tk.Label(self.current_frame, text="СИСТЕМА ГИБДД", font=("Arial", 20, "bold")).pack(pady=20)
        
        tk.Label(self.current_frame, text="Логин:").pack(pady=5)
        self.login_entry = tk.Entry(self.current_frame, width=30)
        self.login_entry.pack(pady=5)
        
        tk.Label(self.current_frame, text="Пароль:").pack(pady=5)
        self.password_entry = tk.Entry(self.current_frame, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.current_frame, text="Войти", command=self.login, 
                 width=20, height=2, bg="#4CAF50", fg="white").pack(pady=20)
        
    def login(self):
        # Процесс авторизации
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
            
        if self.auth_manager.authenticate(username, password):
            user = get_current_user()
            self.show_main_window(user['role'])
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            
    def show_main_window(self, role):
        # Главное окно в зависимости от роли
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель
        top_frame = tk.Frame(self.current_frame, bg="#2196F3", height=50)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        user = get_current_user()
        tk.Label(top_frame, text=f"Пользователь: {user['username']} | Роль: {user['role']}", 
                bg="#2196F3", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Button(top_frame, text="Выход", command=self.logout_user,
                 bg="#f44336", fg="white").pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Главная область
        if role == 'inspector':
            self.show_inspector_interface()
        elif role == 'admin':
            self.show_admin_interface()
        elif role == 'driver':
            self.show_driver_interface()
            
    def show_inspector_interface(self):
        # Интерфейс инспектора
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка регистрации нарушения
        violation_tab = ttk.Frame(notebook)
        notebook.add(violation_tab, text="Регистрация нарушения")
        
        tk.Label(violation_tab, text="Регистрация нарушения", font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = tk.Frame(violation_tab)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Номер автомобиля:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.car_number_entry = tk.Entry(form_frame, width=30)
        self.car_number_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Тип нарушения:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.violation_type = ttk.Combobox(form_frame, width=28, values=[
            "Превышение скорости", "Проезд на красный", "Неправильная парковка",
            "Езда без ремня", "Использование телефона"
        ])
        self.violation_type.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Место нарушения:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.location_entry = tk.Entry(form_frame, width=30)
        self.location_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Описание:").grid(row=3, column=0, padx=10, pady=5, sticky='ne')
        self.description_text = tk.Text(form_frame, width=30, height=5)
        self.description_text.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Button(form_frame, text="Зарегистрировать", command=self.register_violation,
                 bg="#4CAF50", fg="white", width=20).grid(row=4, column=1, pady=20)
        
        # Вкладка выписки штрафов
        fine_tab = ttk.Frame(notebook)
        notebook.add(fine_tab, text="Выписка штрафов")
        
        tk.Label(fine_tab, text="Выписка штрафа", font=("Arial", 14, "bold")).pack(pady=10)
        
        fine_form = tk.Frame(fine_tab)
        fine_form.pack(pady=20)
        
        tk.Label(fine_form, text="Номер водительского удостоверения:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.license_entry = tk.Entry(fine_form, width=30)
        self.license_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(fine_form, text="Сумма штрафа:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.fine_amount_entry = tk.Entry(fine_form, width=30)
        self.fine_amount_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(fine_form, text="Статья КоАП:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.article_entry = tk.Entry(fine_form, width=30)
        self.article_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Button(fine_form, text="Выписать штраф", command=self.issue_fine,
                 bg="#FF9800", fg="white", width=20).grid(row=3, column=1, pady=20)
        
        # Вкладка проверки водителя
        check_tab = ttk.Frame(notebook)
        notebook.add(check_tab, text="Проверка водителя")
        
        tk.Label(check_tab, text="Проверка водителя", font=("Arial", 14, "bold")).pack(pady=10)
        
        check_frame = tk.Frame(check_tab)
        check_frame.pack(pady=20)
        
        tk.Label(check_frame, text="Номер удостоверения:").pack(side=tk.LEFT, padx=5)
        self.check_license_entry = tk.Entry(check_frame, width=30)
        self.check_license_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(check_frame, text="Проверить", command=self.check_driver,
                 bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Таблица результатов
        self.check_tree = ttk.Treeview(check_tab, columns=("Date", "Type", "Fine", "Status"), height=10)
        self.check_tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        self.check_tree.heading("#0", text="ID")
        self.check_tree.heading("Date", text="Дата")
        self.check_tree.heading("Type", text="Нарушение")
        self.check_tree.heading("Fine", text="Штраф")
        self.check_tree.heading("Status", text="Статус")
        
        self.check_tree.column("#0", width=50)
        self.check_tree.column("Date", width=150)
        self.check_tree.column("Type", width=200)
        self.check_tree.column("Fine", width=100)
        self.check_tree.column("Status", width=100)
        
    def show_admin_interface(self):
        # Интерфейс администратора
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка управления пользователями
        users_tab = ttk.Frame(notebook)
        notebook.add(users_tab, text="Управление пользователями")
        
        tk.Label(users_tab, text="Управление пользователями", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Форма добавления пользователя
        user_form = tk.Frame(users_tab)
        user_form.pack(pady=10)
        
        tk.Label(user_form, text="Имя пользователя:").grid(row=0, column=0, padx=5, pady=5)
        self.new_username_entry = tk.Entry(user_form, width=20)
        self.new_username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(user_form, text="Пароль:").grid(row=0, column=2, padx=5, pady=5)
        self.new_password_entry = tk.Entry(user_form, width=20)
        self.new_password_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(user_form, text="Роль:").grid(row=0, column=4, padx=5, pady=5)
        self.new_role_combo = ttk.Combobox(user_form, width=15, values=["inspector", "admin", "driver"])
        self.new_role_combo.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(user_form, text="Добавить", command=self.add_user,
                 bg="#4CAF50", fg="white").grid(row=0, column=6, padx=10, pady=5)
        
        # Таблица пользователей
        self.users_tree = ttk.Treeview(users_tab, columns=("Username", "Role", "Created"), height=10)
        self.users_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.users_tree.heading("#0", text="ID")
        self.users_tree.heading("Username", text="Имя пользователя")
        self.users_tree.heading("Role", text="Роль")
        self.users_tree.heading("Created", text="Дата создания")
        
        self.users_tree.column("#0", width=50)
        
        self.load_users_list()
        
        # Кнопка удаления
        tk.Button(users_tab, text="Удалить выбранного", command=self.delete_user,
                 bg="#f44336", fg="white").pack(pady=10)
        
        # Вкладка статистики
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="Статистика системы")
        
        tk.Label(stats_tab, text="Статистика системы", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.stats_text = tk.Text(stats_tab, width=80, height=20)
        self.stats_text.pack(pady=20, padx=20)
        
        tk.Button(stats_tab, text="Обновить статистику", command=self.update_statistics,
                 bg="#2196F3", fg="white").pack(pady=10)
        
        self.update_statistics()
        
        # Вкладка резервного копирования
        backup_tab = ttk.Frame(notebook)
        notebook.add(backup_tab, text="Резервное копирование")
        
        tk.Label(backup_tab, text="Резервное копирование", font=("Arial", 14, "bold")).pack(pady=20)
        
        tk.Button(backup_tab, text="Создать резервную копию", command=self.create_backup,
                 bg="#4CAF50", fg="white", width=30, height=2).pack(pady=10)
        
        tk.Button(backup_tab, text="Восстановить из резервной копии", command=self.restore_backup,
                 bg="#FF9800", fg="white", width=30, height=2).pack(pady=10)
        
        self.backup_status = tk.Label(backup_tab, text="", font=("Arial", 10))
        self.backup_status.pack(pady=20)
        
    def show_driver_interface(self):
        # Интерфейс водителя
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка просмотра штрафов
        fines_tab = ttk.Frame(notebook)
        notebook.add(fines_tab, text="Мои штрафы")
        
        tk.Label(fines_tab, text="Мои штрафы", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Поиск по номеру удостоверения
        search_frame = tk.Frame(fines_tab)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Номер удостоверения:").pack(side=tk.LEFT, padx=5)
        self.driver_license_entry = tk.Entry(search_frame, width=30)
        self.driver_license_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame, text="Найти", command=self.search_my_fines,
                 bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)
        
        # Таблица штрафов
        self.driver_fines_tree = ttk.Treeview(fines_tab, columns=("Date", "Article", "Amount", "Status"), height=10)
        self.driver_fines_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.driver_fines_tree.heading("#0", text="ID")
        self.driver_fines_tree.heading("Date", text="Дата")
        self.driver_fines_tree.heading("Article", text="Статья")
        self.driver_fines_tree.heading("Amount", text="Сумма")
        self.driver_fines_tree.heading("Status", text="Статус")
        
        self.driver_fines_tree.column("#0", width=50)
        
        # Кнопка оплаты
        tk.Button(fines_tab, text="Оплатить выбранный штраф", command=self.pay_fine,
                 bg="#4CAF50", fg="white", width=25).pack(pady=10)
        
        # Вкладка истории
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text="История нарушений")
        
        tk.Label(history_tab, text="История нарушений", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.history_tree = ttk.Treeview(history_tab, columns=("Date", "Type", "Location", "Description"), height=15)
        self.history_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.history_tree.heading("#0", text="ID")
        self.history_tree.heading("Date", text="Дата")
        self.history_tree.heading("Type", text="Тип")
        self.history_tree.heading("Location", text="Место")
        self.history_tree.heading("Description", text="Описание")
        
        self.history_tree.column("#0", width=50)
        self.history_tree.column("Description", width=250)
        
    def register_violation(self):
        # Регистрация нарушения
        car_number = self.car_number_entry.get()
        violation_type = self.violation_type.get()
        location = self.location_entry.get()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not all([car_number, violation_type, location]):
            messagebox.showerror("Ошибка", "Заполните все обязательные поля")
            return
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        violation = {
            'id': len(data['violations']) + 1,
            'car_number': car_number,
            'type': violation_type,
            'location': location,
            'description': description,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'inspector': get_current_user()['username']
        }
        
        data['violations'].append(violation)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Успех", "Нарушение зарегистрировано")
        
        # Очистка полей
        self.car_number_entry.delete(0, tk.END)
        self.violation_type.set('')
        self.location_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        
    def issue_fine(self):
        # Выписка штрафа
        license_number = self.license_entry.get()
        amount = self.fine_amount_entry.get()
        article = self.article_entry.get()
        
        if not all([license_number, amount, article]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректная сумма штрафа")
            return
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fine = {
            'id': len(data['fines']) + 1,
            'license_number': license_number,
            'amount': amount,
            'article': article,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Не оплачен',
            'inspector': get_current_user()['username']
        }
        
        data['fines'].append(fine)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Успех", f"Штраф на сумму {amount} руб. выписан")
        
        # Очистка полей
        self.license_entry.delete(0, tk.END)
        self.fine_amount_entry.delete(0, tk.END)
        self.article_entry.delete(0, tk.END)
        
    def check_driver(self):
        # Проверка водителя
        license_number = self.check_license_entry.get()
        
        if not license_number:
            messagebox.showerror("Ошибка", "Введите номер удостоверения")
            return
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Очистка таблицы
        for item in self.check_tree.get_children():
            self.check_tree.delete(item)
        
        # Поиск штрафов
        found = False
        for fine in data['fines']:
            if fine['license_number'] == license_number:
                self.check_tree.insert('', 'end', text=fine['id'],
                                      values=(fine['date'], fine['article'], 
                                            f"{fine['amount']} руб.", fine['status']))
                found = True
        
        if not found:
            messagebox.showinfo("Результат", "Штрафов не найдено")
            
    def add_user(self):
        # Добавление пользователя
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.new_role_combo.get()
        
        if not all([username, password, role]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if self.auth_manager.create_user(username, password, role):
            messagebox.showinfo("Успех", "Пользователь создан")
            self.new_username_entry.delete(0, tk.END)
            self.new_password_entry.delete(0, tk.END)
            self.new_role_combo.set('')
            self.load_users_list()
        else:
            messagebox.showerror("Ошибка", "Пользователь уже существует")
            
    def load_users_list(self):
        # Загрузка списка пользователей
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        for i, user in enumerate(users_data['users'], 1):
            self.users_tree.insert('', 'end', text=i,
                                  values=(user['username'], user['role'], user['created']))
            
    def delete_user(self):
        # Удаление пользователя
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите пользователя")
            return
        
        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        
        if username == get_current_user()['username']:
            messagebox.showerror("Ошибка", "Нельзя удалить текущего пользователя")
            return
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            with open('users.json', 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
            
            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
            
            self.load_users_list()
            messagebox.showinfo("Успех", "Пользователь удален")
            
    def update_statistics(self):
        # Обновление статистики
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        stats = f"""
        === СТАТИСТИКА СИСТЕМЫ ===
        
        Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        ПОЛЬЗОВАТЕЛИ:
        - Всего пользователей: {len(users_data['users'])}
        - Инспекторов: {len([u for u in users_data['users'] if u['role'] == 'inspector'])}
        - Администраторов: {len([u for u in users_data['users'] if u['role'] == 'admin'])}
        - Водителей: {len([u for u in users_data['users'] if u['role'] == 'driver'])}
        
        НАРУШЕНИЯ:
        - Всего зарегистрировано: {len(data['violations'])}
        
        ШТРАФЫ:
        - Всего выписано: {len(data['fines'])}
        - Оплачено: {len([f for f in data['fines'] if f['status'] == 'Оплачен'])}
        - Не оплачено: {len([f for f in data['fines'] if f['status'] == 'Не оплачен'])}
        - Общая сумма: {sum([f['amount'] for f in data['fines']])} руб.
        - Оплачено на сумму: {sum([f['amount'] for f in data['fines'] if f['status'] == 'Оплачен'])} руб.
        """
        
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats)
        
    def create_backup(self):
        # Создание резервной копии
        backup_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data': {},
            'users': {}
        }
        
        with open('data.json', 'r', encoding='utf-8') as f:
            backup_data['data'] = json.load(f)
        
        with open('users.json', 'r', encoding='utf-8') as f:
            backup_data['users'] = json.load(f)
        
        backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        self.backup_status.config(text=f"Резервная копия создана: {backup_filename}")
        messagebox.showinfo("Успех", f"Резервная копия создана: {backup_filename}")
        
    def restore_backup(self):
        # Восстановление из резервной копии (заглушка)
        messagebox.showinfo("Информация", "Функция восстановления будет доступна в следующей версии")
        
    def search_my_fines(self):
        # Поиск штрафов водителя
        license_number = self.driver_license_entry.get()
        
        if not license_number:
            messagebox.showerror("Ошибка", "Введите номер удостоверения")
            return
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Очистка таблицы
        for item in self.driver_fines_tree.get_children():
            self.driver_fines_tree.delete(item)
        
        # Заполнение таблицы
        for fine in data['fines']:
            if fine['license_number'] == license_number:
                self.driver_fines_tree.insert('', 'end', text=fine['id'],
                                             values=(fine['date'], fine['article'],
                                                   f"{fine['amount']} руб.", fine['status']))
        
        # Загрузка истории нарушений
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Добавление примерных данных для демонстрации
        for violation in data['violations']:
            self.history_tree.insert('', 'end', text=violation['id'],
                                    values=(violation['date'], violation['type'],
                                          violation['location'], violation['description']))
                                          
    def pay_fine(self):
        # Оплата штрафа
        selected = self.driver_fines_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите штраф для оплаты")
            return
        
        item = self.driver_fines_tree.item(selected[0])
        fine_id = int(item['text'])
        
        if messagebox.askyesno("Подтверждение", "Оплатить выбранный штраф?"):
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for fine in data['fines']:
                if fine['id'] == fine_id:
                    fine['status'] = 'Оплачен'
                    break
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", "Штраф оплачен")
            self.search_my_fines()
            
    def logout_user(self):
        # Выход из системы
        logout()
        self.show_login_window()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GIBDDSystem()
    app.run()