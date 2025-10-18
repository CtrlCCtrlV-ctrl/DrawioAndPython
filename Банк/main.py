import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

# Путь к файлу с данными
DATA_FILE = 'data.json'

class BankSystem:
    def __init__(self):
        self.current_user = None
        self.root = tk.Tk()
        self.root.title("Банковская Информационная Система")
        self.root.geometry("900x600")
        
        # Инициализация данных
        self.init_data()
        
        # Показ окна входа
        self.show_login()
        
    def init_data(self):
        """Инициализация данных - файлы уже созданы"""
        pass
    
    def load_data(self):
        """Загрузка данных из файла"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно входа в систему"""
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Вход в систему", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, width=25, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            user = auth.authenticate(username, password)
            if user:
                self.current_user = user
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login, width=20).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Информация для тестирования
        info_text = "Тестовые аккаунты:\nadmin/admin123\nmanager/manager123\nclient1/client123"
        tk.Label(frame, text=info_text, font=('Arial', 8), fg='gray').grid(row=4, column=0, columnspan=2)
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_frame.pack(fill='x')
        
        user_info = f"Пользователь: {self.current_user['full_name']} ({self.current_user['role']})"
        tk.Label(top_frame, text=user_info, bg='#2c3e50', fg='white', font=('Arial', 10)).pack(side='left', padx=10, pady=10)
        
        tk.Button(top_frame, text="Выход", command=self.show_login, bg='#e74c3c', fg='white').pack(side='right', padx=10, pady=10)
        
        # Боковое меню
        menu_frame = tk.Frame(self.root, bg='#34495e', width=200)
        menu_frame.pack(side='left', fill='y')
        
        # Рабочая область
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Меню в зависимости от роли
        if self.current_user['role'] == 'administrator':
            self.show_admin_menu(menu_frame)
        elif self.current_user['role'] == 'manager':
            self.show_manager_menu(menu_frame)
        else:
            self.show_client_menu(menu_frame)
    
    def show_admin_menu(self, menu_frame):
        """Меню администратора"""
        tk.Label(menu_frame, text="Администратор", bg='#34495e', fg='white', font=('Arial', 12, 'bold')).pack(pady=10)
        
        buttons = [
            ("Управление пользователями", self.admin_manage_users),
            ("Все операции", self.admin_view_transactions),
            ("Управление счетами", self.admin_manage_accounts),
            ("Отчеты", self.admin_reports),
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, width=20, bg='#3498db', fg='white').pack(pady=5, padx=10)
        
        self.admin_manage_users()
    
    def show_manager_menu(self, menu_frame):
        """Меню менеджера"""
        tk.Label(menu_frame, text="Менеджер", bg='#34495e', fg='white', font=('Arial', 12, 'bold')).pack(pady=10)
        
        buttons = [
            ("Создать счет", self.manager_create_account),
            ("Операции со счетами", self.manager_account_operations),
            ("Просмотр клиентов", self.manager_view_clients),
            ("История операций", self.manager_view_history),
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, width=20, bg='#2ecc71', fg='white').pack(pady=5, padx=10)
        
        self.manager_view_clients()
    
    def show_client_menu(self, menu_frame):
        """Меню клиента"""
        tk.Label(menu_frame, text="Клиент", bg='#34495e', fg='white', font=('Arial', 12, 'bold')).pack(pady=10)
        
        buttons = [
            ("Мои счета", self.client_view_accounts),
            ("Перевод", self.client_transfer),
            ("История операций", self.client_view_history),
            ("Изменить пароль", self.client_change_password),
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, width=20, bg='#f39c12', fg='white').pack(pady=5, padx=10)
        
        self.client_view_accounts()
    
    # ФУНКЦИИ АДМИНИСТРАТОРА
    
    def admin_manage_users(self):
        """Управление пользователями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление пользователями", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Таблица пользователей
        columns = ('Логин', 'Имя', 'Роль', 'Дата создания')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        users = auth.get_all_users()
        for user in users:
            tree.insert('', 'end', values=(
                user['username'],
                user['full_name'],
                user['role'],
                user['created']
            ))
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        def add_user():
            window = tk.Toplevel(self.root)
            window.title("Добавить пользователя")
            window.geometry("400x300")
            
            tk.Label(window, text="Логин:").grid(row=0, column=0, padx=10, pady=5)
            username_entry = tk.Entry(window)
            username_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(window, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
            password_entry = tk.Entry(window, show='*')
            password_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(window, text="ФИО:").grid(row=2, column=0, padx=10, pady=5)
            fullname_entry = tk.Entry(window)
            fullname_entry.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(window, text="Роль:").grid(row=3, column=0, padx=10, pady=5)
            role_var = tk.StringVar(value="client")
            role_combo = ttk.Combobox(window, textvariable=role_var, values=['administrator', 'manager', 'client'])
            role_combo.grid(row=3, column=1, padx=10, pady=5)
            
            def save():
                success, msg = auth.create_user(
                    username_entry.get(),
                    password_entry.get(),
                    role_var.get(),
                    fullname_entry.get()
                )
                if success:
                    messagebox.showinfo("Успех", msg)
                    window.destroy()
                    self.admin_manage_users()
                else:
                    messagebox.showerror("Ошибка", msg)
            
            tk.Button(window, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            item = tree.item(selected[0])
            username = item['values'][0]
            
            if username == self.current_user['username']:
                messagebox.showerror("Ошибка", "Нельзя удалить текущего пользователя")
                return
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                auth.delete_user(username)
                self.admin_manage_users()
        
        tk.Button(btn_frame, text="Добавить", command=add_user, bg='#2ecc71', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, bg='#e74c3c', fg='white').pack(side='left', padx=5)
    
    def admin_view_transactions(self):
        """Просмотр всех операций"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Все операции системы", font=('Arial', 16, 'bold')).pack(pady=10)
        
        columns = ('ID', 'От', 'Кому', 'Сумма', 'Тип', 'Дата')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column('ID', width=80)
        tree.column('От', width=100)
        tree.column('Кому', width=100)
        tree.column('Сумма', width=100)
        tree.column('Тип', width=100)
        tree.column('Дата', width=150)
        
        data = self.load_data()
        for trans in reversed(data['transactions']):
            tree.insert('', 'end', values=(
                trans['transaction_id'],
                trans['from_account'],
                trans['to_account'],
                f"{trans['amount']:.2f} ₽",
                trans['type'],
                trans['date']
            ))
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
    
    def admin_manage_accounts(self):
        """Управление всеми счетами"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление счетами", font=('Arial', 16, 'bold')).pack(pady=10)
        
        columns = ('ID счета', 'Владелец', 'Баланс', 'Статус', 'Дата создания')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        data = self.load_data()
        for acc in data['accounts']:
            tree.insert('', 'end', values=(
                acc['account_id'],
                acc['owner'],
                f"{acc['balance']:.2f} ₽",
                acc['status'],
                acc['created']
            ))
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
    
    def admin_reports(self):
        """Генерация отчетов"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Отчеты системы", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Статистика
        total_accounts = len(data['accounts'])
        total_balance = sum(acc['balance'] for acc in data['accounts'])
        total_transactions = len(data['transactions'])
        
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        stats = [
            ("Всего счетов:", total_accounts),
            ("Общий баланс:", f"{total_balance:.2f} ₽"),
            ("Всего операций:", total_transactions),
            ("Активных пользователей:", len(auth.get_all_users())),
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 12, 'bold')).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            tk.Label(stats_frame, text=str(value), font=('Arial', 12)).grid(row=i, column=1, sticky='w', padx=10, pady=5)
    
    # ФУНКЦИИ МЕНЕДЖЕРА
    
    def manager_create_account(self):
        """Создание нового счета"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Создание нового счета", font=('Arial', 16, 'bold')).pack(pady=20)
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Владелец (логин):").grid(row=0, column=0, padx=10, pady=5)
        owner_entry = tk.Entry(form_frame)
        owner_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Начальный баланс:").grid(row=1, column=0, padx=10, pady=5)
        balance_entry = tk.Entry(form_frame)
        balance_entry.insert(0, "0")
        balance_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def create():
            owner = owner_entry.get()
            try:
                balance = float(balance_entry.get())
            except:
                messagebox.showerror("Ошибка", "Неверный формат суммы")
                return
            
            if balance < 0:
                messagebox.showerror("Ошибка", "Баланс не может быть отрицательным")
                return
            
            data = self.load_data()
            
            # Генерация ID счета
            account_id = f"ACC{len(data['accounts']) + 1:03d}"
            
            new_account = {
                "account_id": account_id,
                "owner": owner,
                "balance": balance,
                "status": "active",
                "created": datetime.now().strftime("%Y-%m-%d")
            }
            
            data['accounts'].append(new_account)
            
            # Добавление транзакции
            if balance > 0:
                trans = {
                    "transaction_id": f"TRX{len(data['transactions']) + 1:03d}",
                    "from_account": "SYSTEM",
                    "to_account": account_id,
                    "amount": balance,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "deposit",
                    "description": "Начальный депозит"
                }
                data['transactions'].append(trans)
            
            self.save_data(data)
            messagebox.showinfo("Успех", f"Счет {account_id} успешно создан")
            owner_entry.delete(0, 'end')
            balance_entry.delete(0, 'end')
            balance_entry.insert(0, "0")
    
        tk.Button(form_frame, text="Создать счет", command=create, bg='#2ecc71', fg='white').grid(row=2, column=0, columnspan=2, pady=20)
    
    def manager_account_operations(self):
        """Операции со счетами (пополнение/снятие)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Операции со счетами", font=('Arial', 16, 'bold')).pack(pady=20)
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="ID счета:").grid(row=0, column=0, padx=10, pady=5)
        account_entry = tk.Entry(form_frame)
        account_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Сумма:").grid(row=1, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(form_frame)
        amount_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Операция:").grid(row=2, column=0, padx=10, pady=5)
        operation_var = tk.StringVar(value="deposit")
        tk.Radiobutton(form_frame, text="Пополнение", variable=operation_var, value="deposit").grid(row=2, column=1, sticky='w')
        tk.Radiobutton(form_frame, text="Снятие", variable=operation_var, value="withdraw").grid(row=3, column=1, sticky='w')
        
        def execute():
            account_id = account_entry.get()
            try:
                amount = float(amount_entry.get())
            except:
                messagebox.showerror("Ошибка", "Неверный формат суммы")
                return
            
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительной")
                return
            
            data = self.load_data()
            
            # Поиск счета
            account = None
            for acc in data['accounts']:
                if acc['account_id'] == account_id:
                    account = acc
                    break
            
            if not account:
                messagebox.showerror("Ошибка", "Счет не найден")
                return
            
            if account['status'] != 'active':
                messagebox.showerror("Ошибка", "Счет заблокирован")
                return
            
            operation = operation_var.get()
            
            if operation == "withdraw" and account['balance'] < amount:
                messagebox.showerror("Ошибка", "Недостаточно средств")
                return
            
            # Выполнение операции
            if operation == "deposit":
                account['balance'] += amount
                from_acc = "SYSTEM"
                to_acc = account_id
            else:
                account['balance'] -= amount
                from_acc = account_id
                to_acc = "SYSTEM"
            
            # Добавление транзакции
            trans = {
                "transaction_id": f"TRX{len(data['transactions']) + 1:03d}",
                "from_account": from_acc,
                "to_account": to_acc,
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": operation,
                "description": f"{'Пополнение' if operation == 'deposit' else 'Снятие'} менеджером"
            }
            data['transactions'].append(trans)
            
            self.save_data(data)
            messagebox.showinfo("Успех", f"Операция выполнена. Новый баланс: {account['balance']:.2f} ₽")
            amount_entry.delete(0, 'end')
        
        tk.Button(form_frame, text="Выполнить", command=execute, bg='#3498db', fg='white').grid(row=4, column=0, columnspan=2, pady=20)
    
    def manager_view_clients(self):
        """Просмотр клиентов и их счетов"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Клиенты и их счета", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        users = auth.get_all_users()
        
        # Группировка счетов по владельцам
        clients_data = {}
        for acc in data['accounts']:
            if acc['owner'] not in clients_data:
                clients_data[acc['owner']] = []
            clients_data[acc['owner']].append(acc)
        
        for username, accounts in clients_data.items():
            user_info = next((u for u in users if u['username'] == username), None)
            full_name = user_info['full_name'] if user_info else username
            
            frame = tk.LabelFrame(self.content_frame, text=f"{full_name} ({username})", font=('Arial', 12, 'bold'))
            frame.pack(pady=5, padx=10, fill='x')
            
            for acc in accounts:
                acc_text = f"Счет: {acc['account_id']} | Баланс: {acc['balance']:.2f} ₽ | Статус: {acc['status']}"
                tk.Label(frame, text=acc_text).pack(anchor='w', padx=10, pady=2)
    
    def manager_view_history(self):
        """Просмотр истории операций"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="История операций", font=('Arial', 16, 'bold')).pack(pady=10)
        
        columns = ('ID', 'От', 'Кому', 'Сумма', 'Тип', 'Дата')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column('ID', width=80)
        tree.column('От', width=100)
        tree.column('Кому', width=100)
        tree.column('Сумма', width=100)
        tree.column('Тип', width=100)
        tree.column('Дата', width=150)
        
        data = self.load_data()
        for trans in reversed(data['transactions']):
            tree.insert('', 'end', values=(
                trans['transaction_id'],
                trans['from_account'],
                trans['to_account'],
                f"{trans['amount']:.2f} ₽",
                trans['type'],
                trans['date']
            ))
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
    
    # ФУНКЦИИ КЛИЕНТА
    
    def client_view_accounts(self):
        """Просмотр счетов клиента"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои счета", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        my_accounts = [acc for acc in data['accounts'] if acc['owner'] == self.current_user['username']]
        
        if not my_accounts:
            tk.Label(self.content_frame, text="У вас пока нет счетов", font=('Arial', 12)).pack(pady=20)
            return
        
        for acc in my_accounts:
            frame = tk.LabelFrame(self.content_frame, text=f"Счет {acc['account_id']}", font=('Arial', 12, 'bold'))
            frame.pack(pady=10, padx=20, fill='x')
            
            tk.Label(frame, text=f"Баланс: {acc['balance']:.2f} ₽", font=('Arial', 14)).pack(anchor='w', padx=10, pady=5)
            tk.Label(frame, text=f"Статус: {acc['status']}").pack(anchor='w', padx=10, pady=2)
            tk.Label(frame, text=f"Создан: {acc['created']}").pack(anchor='w', padx=10, pady=2)
    
    def client_transfer(self):
        """Перевод средств"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Перевод средств", font=('Arial', 16, 'bold')).pack(pady=20)
        
        data = self.load_data()
        my_accounts = [acc for acc in data['accounts'] if acc['owner'] == self.current_user['username']]
        
        if not my_accounts:
            tk.Label(self.content_frame, text="У вас нет счетов для перевода", font=('Arial', 12)).pack(pady=20)
            return
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Со счета:").grid(row=0, column=0, padx=10, pady=5)
        from_var = tk.StringVar()
        from_combo = ttk.Combobox(form_frame, textvariable=from_var, values=[acc['account_id'] for acc in my_accounts])
        from_combo.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="На счет:").grid(row=1, column=0, padx=10, pady=5)
        to_entry = tk.Entry(form_frame)
        to_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Сумма:").grid(row=2, column=0, padx=10, pady=5)
        amount_entry = tk.Entry(form_frame)
        amount_entry.grid(row=2, column=1, padx=10, pady=5)
        
        def transfer():
            from_account_id = from_var.get()
            to_account_id = to_entry.get()
            
            try:
                amount = float(amount_entry.get())
            except:
                messagebox.showerror("Ошибка", "Неверный формат суммы")
                return
            
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительной")
                return
            
            if not from_account_id or not to_account_id:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            data = self.load_data()
            
            # Поиск счетов
            from_acc = None
            to_acc = None
            
            for acc in data['accounts']:
                if acc['account_id'] == from_account_id:
                    from_acc = acc
                if acc['account_id'] == to_account_id:
                    to_acc = acc
            
            if not from_acc:
                messagebox.showerror("Ошибка", "Счет отправителя не найден")
                return
            
            if not to_acc:
                messagebox.showerror("Ошибка", "Счет получателя не найден")
                return
            
            if from_acc['status'] != 'active' or to_acc['status'] != 'active':
                messagebox.showerror("Ошибка", "Один из счетов заблокирован")
                return
            
            if from_acc['balance'] < amount:
                messagebox.showerror("Ошибка", "Недостаточно средств")
                return
            
            # Выполнение перевода
            from_acc['balance'] -= amount
            to_acc['balance'] += amount
            
            # Добавление транзакции
            trans = {
                "transaction_id": f"TRX{len(data['transactions']) + 1:03d}",
                "from_account": from_account_id,
                "to_account": to_account_id,
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "transfer",
                "description": f"Перевод с {from_account_id} на {to_account_id}"
            }
            data['transactions'].append(trans)
            
            self.save_data(data)
            messagebox.showinfo("Успех", f"Перевод выполнен успешно!\nНовый баланс: {from_acc['balance']:.2f} ₽")
            amount_entry.delete(0, 'end')
            to_entry.delete(0, 'end')
        
        tk.Button(form_frame, text="Выполнить перевод", command=transfer, bg='#3498db', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
    
    def client_view_history(self):
        """Просмотр истории операций клиента"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Моя история операций", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        my_accounts = [acc['account_id'] for acc in data['accounts'] if acc['owner'] == self.current_user['username']]
        
        # Фильтрация транзакций
        my_transactions = [t for t in data['transactions'] if t['from_account'] in my_accounts or t['to_account'] in my_accounts]
        
        columns = ('ID', 'От', 'Кому', 'Сумма', 'Тип', 'Дата')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column('ID', width=80)
        tree.column('От', width=100)
        tree.column('Кому', width=100)
        tree.column('Сумма', width=100)
        tree.column('Тип', width=100)
        tree.column('Дата', width=150)
        
        for trans in reversed(my_transactions):
            tree.insert('', 'end', values=(
                trans['transaction_id'],
                trans['from_account'],
                trans['to_account'],
                f"{trans['amount']:.2f} ₽",
                trans['type'],
                trans['date']
            ))
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
    
    def client_change_password(self):
        """Изменение пароля"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Изменение пароля", font=('Arial', 16, 'bold')).pack(pady=20)
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Старый пароль:").grid(row=0, column=0, padx=10, pady=5)
        old_pass_entry = tk.Entry(form_frame, show='*')
        old_pass_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Новый пароль:").grid(row=1, column=0, padx=10, pady=5)
        new_pass_entry = tk.Entry(form_frame, show='*')
        new_pass_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Подтверждение:").grid(row=2, column=0, padx=10, pady=5)
        confirm_pass_entry = tk.Entry(form_frame, show='*')
        confirm_pass_entry.grid(row=2, column=1, padx=10, pady=5)
        
        def change():
            old_pass = old_pass_entry.get()
            new_pass = new_pass_entry.get()
            confirm_pass = confirm_pass_entry.get()
            
            if not old_pass or not new_pass or not confirm_pass:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            if new_pass != confirm_pass:
                messagebox.showerror("Ошибка", "Пароли не совпадают")
                return
            
            if len(new_pass) < 6:
                messagebox.showerror("Ошибка", "Пароль должен быть не менее 6 символов")
                return
            
            success, msg = auth.change_password(self.current_user['username'], old_pass, new_pass)
            
            if success:
                messagebox.showinfo("Успех", msg)
                old_pass_entry.delete(0, 'end')
                new_pass_entry.delete(0, 'end')
                confirm_pass_entry.delete(0, 'end')
            else:
                messagebox.showerror("Ошибка", msg)
        
        tk.Button(form_frame, text="Изменить пароль", command=change, bg='#3498db', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == '__main__':
    app = BankSystem()
    app.run()