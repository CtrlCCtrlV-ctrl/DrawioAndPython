import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import AuthManager

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система Ресторан")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.auth = AuthManager()
        self.data_file = 'data.json'

        self.show_login_screen()
    
    def _load_data(self):
        # Загрузка данных из файла
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data):
        # Сохранение данных в файл
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        # Экран авторизации
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="🍽️ Система Ресторан", font=('Arial', 20, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, font=('Arial', 12), width=20)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12), bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, font=('Arial', 12), width=20, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            if self.auth.login(username, password):
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", font=('Arial', 12), command=do_login, width=15, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказки
        hints = tk.Label(frame, text="Подсказки:\nadmin/admin123 - Администратор\nwaiter1/waiter123 - Официант\nclient1/client123 - Клиент", 
                        font=('Arial', 9), bg='#f0f0f0', fg='#666', justify='left')
        hints.grid(row=4, column=0, columnspan=2, pady=10)
        
        password_entry.bind('<Return>', lambda e: do_login())
    
    def show_main_menu(self):
        # Главное меню в зависимости от роли
        self.clear_window()
        
        user = self.auth.get_current_user()
        role = user['role']
        username = user['username']
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text=f"🍽️ Система Ресторан | {username} ({self._get_role_name(role)})", 
                font=('Arial', 14, 'bold'), bg='#2196F3', fg='white').pack(side='left', padx=20, pady=15)
        
        tk.Button(top_frame, text="Выход", command=self.logout, bg='#f44336', fg='white', font=('Arial', 10)).pack(side='right', padx=20)
        
        # Контент
        content = tk.Frame(self.root, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        if role == 'administrator':
            self._show_admin_menu(content)
        elif role == 'waiter':
            self._show_waiter_menu(content)
        else:  # client
            self._show_client_menu(content)
    
    def _get_role_name(self, role):
        roles = {
            'administrator': 'Администратор',
            'waiter': 'Официант',
            'client': 'Клиент'
        }
        return roles.get(role, role)
    
    def _show_admin_menu(self, parent):
        # Меню администратора
        tk.Label(parent, text="Панель администратора", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(pady=20)
        
        buttons = [
            ("👥 Управление пользователями", self.show_users_management),
            ("📋 Управление меню", self.show_menu_management),
            ("🪑 Управление столиками", self.show_tables_management),
            ("📊 Просмотр заказов", self.show_all_orders),
            ("📈 Статистика", self.show_statistics)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=('Arial', 12), width=30, height=2, 
                     command=command, bg='#2196F3', fg='white').grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def _show_waiter_menu(self, parent):
        # Меню официанта
        tk.Label(parent, text="Панель официанта", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(pady=20)
        
        buttons = [
            ("📋 Просмотр меню", self.show_menu_view),
            ("➕ Создать заказ", self.show_create_order),
            ("📊 Мои заказы", self.show_my_orders),
            ("🪑 Столики", self.show_tables_view),
            ("✏️ Изменить статус заказа", self.show_change_order_status)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=('Arial', 12), width=30, height=2, 
                     command=command, bg='#4CAF50', fg='white').grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def _show_client_menu(self, parent):
        # Меню клиента
        tk.Label(parent, text="Панель клиента", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(pady=20)
        
        buttons = [
            ("📋 Просмотр меню", self.show_menu_view),
            ("➕ Создать заказ", self.show_create_order),
            ("📊 Мои заказы", self.show_my_orders)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=('Arial', 12), width=30, height=2, 
                     command=command, bg='#FF9800', fg='white').pack(pady=10)
    
    def logout(self):
        # Выход из системы
        self.auth.logout()
        self.show_login_screen()
    
    # УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ
    def show_users_management(self):
        self.clear_window()
        self._create_header("Управление пользователями")
        
        # Таблица пользователей
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('username', 'role', 'created')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('username', text='Логин')
        tree.heading('role', text='Роль')
        tree.heading('created', text='Дата создания')
        
        tree.column('username', width=200)
        tree.column('role', width=200)
        tree.column('created', width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_users():
            tree.delete(*tree.get_children())
            users = self.auth.get_all_users()
            for user in users:
                tree.insert('', 'end', values=(user['username'], self._get_role_name(user['role']), user['created']))
        
        refresh_users()
        
        # Кнопки действий
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def add_user_dialog():
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить пользователя")
            dialog.geometry("300x250")
            dialog.resizable(False, False)
            
            tk.Label(dialog, text="Логин:", font=('Arial', 10)).pack(pady=5)
            username_entry = tk.Entry(dialog, font=('Arial', 10))
            username_entry.pack(pady=5)
            
            tk.Label(dialog, text="Пароль:", font=('Arial', 10)).pack(pady=5)
            password_entry = tk.Entry(dialog, font=('Arial', 10), show='*')
            password_entry.pack(pady=5)
            
            tk.Label(dialog, text="Роль:", font=('Arial', 10)).pack(pady=5)
            role_var = tk.StringVar(value='client')
            roles = [('Администратор', 'administrator'), ('Официант', 'waiter'), ('Клиент', 'client')]
            for text, value in roles:
                tk.Radiobutton(dialog, text=text, variable=role_var, value=value).pack()
            
            def save_user():
                username = username_entry.get()
                password = password_entry.get()
                role = role_var.get()
                
                if not username or not password:
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                if self.auth.add_user(username, password, role):
                    messagebox.showinfo("Успех", "Пользователь добавлен")
                    dialog.destroy()
                    refresh_users()
                else:
                    messagebox.showerror("Ошибка", "Пользователь уже существует")
            
            tk.Button(dialog, text="Сохранить", command=save_user, bg='#4CAF50', fg='white').pack(pady=10)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            username = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                self.auth.delete_user(username)
                refresh_users()
        
        tk.Button(btn_frame, text="➕ Добавить", command=add_user_dialog, bg='#4CAF50', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Удалить", command=delete_user, bg='#f44336', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Обновить", command=refresh_users, bg='#2196F3', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="← Назад", command=self.show_main_menu, width=15).pack(side='left', padx=5)
    
    # УПРАВЛЕНИЕ МЕНЮ
    def show_menu_management(self):
        self.clear_window()
        self._create_header("Управление меню")
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('id', 'name', 'category', 'price', 'available')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='ID')
        tree.heading('name', text='Название')
        tree.heading('category', text='Категория')
        tree.heading('price', text='Цена')
        tree.heading('available', text='Доступно')
        
        tree.column('id', width=50)
        tree.column('name', width=200)
        tree.column('category', width=150)
        tree.column('price', width=100)
        tree.column('available', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_menu():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for item in data['menu']:
                tree.insert('', 'end', values=(
                    item['id'], 
                    item['name'], 
                    item['category'], 
                    f"{item['price']} ₽",
                    "Да" if item['available'] else "Нет"
                ))
        
        refresh_menu()
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def add_dish_dialog():
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить блюдо")
            dialog.geometry("300x300")
            
            tk.Label(dialog, text="Название:", font=('Arial', 10)).pack(pady=5)
            name_entry = tk.Entry(dialog, font=('Arial', 10))
            name_entry.pack(pady=5)
            
            tk.Label(dialog, text="Категория:", font=('Arial', 10)).pack(pady=5)
            category_entry = tk.Entry(dialog, font=('Arial', 10))
            category_entry.pack(pady=5)
            
            tk.Label(dialog, text="Цена:", font=('Arial', 10)).pack(pady=5)
            price_entry = tk.Entry(dialog, font=('Arial', 10))
            price_entry.pack(pady=5)
            
            available_var = tk.BooleanVar(value=True)
            tk.Checkbutton(dialog, text="Доступно", variable=available_var).pack(pady=5)
            
            def save_dish():
                name = name_entry.get()
                category = category_entry.get()
                try:
                    price = float(price_entry.get())
                except:
                    messagebox.showerror("Ошибка", "Неверный формат цены")
                    return
                
                if not name or not category:
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                data = self._load_data()
                new_dish = {
                    "id": data['next_menu_id'],
                    "name": name,
                    "category": category,
                    "price": price,
                    "available": available_var.get()
                }
                data['menu'].append(new_dish)
                data['next_menu_id'] += 1
                self._save_data(data)
                
                messagebox.showinfo("Успех", "Блюдо добавлено")
                dialog.destroy()
                refresh_menu()
            
            tk.Button(dialog, text="Сохранить", command=save_dish, bg='#4CAF50', fg='white').pack(pady=10)
        
        def delete_dish():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите блюдо")
                return
            
            dish_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить блюдо?"):
                data = self._load_data()
                data['menu'] = [d for d in data['menu'] if d['id'] != dish_id]
                self._save_data(data)
                refresh_menu()
        
        tk.Button(btn_frame, text="➕ Добавить", command=add_dish_dialog, bg='#4CAF50', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Удалить", command=delete_dish, bg='#f44336', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Обновить", command=refresh_menu, bg='#2196F3', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="← Назад", command=self.show_main_menu, width=15).pack(side='left', padx=5)
    
    # УПРАВЛЕНИЕ СТОЛИКАМИ
    def show_tables_management(self):
        self.clear_window()
        self._create_header("Управление столиками")
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('id', 'number', 'seats', 'status')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='ID')
        tree.heading('number', text='Номер')
        tree.heading('seats', text='Мест')
        tree.heading('status', text='Статус')
        
        tree.column('id', width=50)
        tree.column('number', width=150)
        tree.column('seats', width=150)
        tree.column('status', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_tables():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for table in data['tables']:
                status_text = "Свободен" if table['status'] == 'free' else "Занят"
                tree.insert('', 'end', values=(table['id'], table['number'], table['seats'], status_text))
        
        refresh_tables()
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def add_table_dialog():
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить столик")
            dialog.geometry("300x200")
            
            tk.Label(dialog, text="Номер столика:", font=('Arial', 10)).pack(pady=5)
            number_entry = tk.Entry(dialog, font=('Arial', 10))
            number_entry.pack(pady=5)
            
            tk.Label(dialog, text="Количество мест:", font=('Arial', 10)).pack(pady=5)
            seats_entry = tk.Entry(dialog, font=('Arial', 10))
            seats_entry.pack(pady=5)
            
            def save_table():
                try:
                    number = int(number_entry.get())
                    seats = int(seats_entry.get())
                except:
                    messagebox.showerror("Ошибка", "Неверный формат данных")
                    return
                
                data = self._load_data()
                new_table = {
                    "id": data['next_table_id'],
                    "number": number,
                    "seats": seats,
                    "status": "free"
                }
                data['tables'].append(new_table)
                data['next_table_id'] += 1
                self._save_data(data)
                
                messagebox.showinfo("Успех", "Столик добавлен")
                dialog.destroy()
                refresh_tables()
            
            tk.Button(dialog, text="Сохранить", command=save_table, bg='#4CAF50', fg='white').pack(pady=10)
        
        def delete_table():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите столик")
                return
            
            table_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить столик?"):
                data = self._load_data()
                data['tables'] = [t for t in data['tables'] if t['id'] != table_id]
                self._save_data(data)
                refresh_tables()
        
        tk.Button(btn_frame, text="➕ Добавить", command=add_table_dialog, bg='#4CAF50', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Удалить", command=delete_table, bg='#f44336', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Обновить", command=refresh_tables, bg='#2196F3', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="← Назад", command=self.show_main_menu, width=15).pack(side='left', padx=5)
    
    # ПРОСМОТР МЕНЮ
    def show_menu_view(self):
        self.clear_window()
        self._create_header("Меню ресторана")
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('name', 'category', 'price', 'available')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('name', text='Название')
        tree.heading('category', text='Категория')
        tree.heading('price', text='Цена')
        tree.heading('available', text='Доступно')
        
        tree.column('name', width=250)
        tree.column('category', width=150)
        tree.column('price', width=100)
        tree.column('available', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self._load_data()
        for item in data['menu']:
            if item['available']:
                tree.insert('', 'end', values=(item['name'], item['category'], f"{item['price']} ₽", "Да"))
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu, width=15).pack(pady=10)
    
    # СОЗДАНИЕ ЗАКАЗА
    def show_create_order(self):
        self.clear_window()
        self._create_header("Создание заказа")
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Левая часть - меню
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(left_frame, text="Меню:", font=('Arial', 12, 'bold')).pack()
        
        menu_tree = ttk.Treeview(left_frame, columns=('name', 'price'), show='headings', height=15)
        menu_tree.heading('name', text='Блюдо')
        menu_tree.heading('price', text='Цена')
        menu_tree.column('name', width=200)
        menu_tree.column('price', width=100)
        menu_tree.pack(pady=5)
        
        data = self._load_data()
        menu_items = {item['id']: item for item in data['menu'] if item['available']}
        
        for item_id, item in menu_items.items():
            menu_tree.insert('', 'end', values=(item['name'], f"{item['price']} ₽"), tags=(item_id,))
        
        # Правая часть - корзина
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(right_frame, text="Корзина:", font=('Arial', 12, 'bold')).pack()
        
        cart_tree = ttk.Treeview(right_frame, columns=('name', 'qty', 'price'), show='headings', height=10)
        cart_tree.heading('name', text='Блюдо')
        cart_tree.heading('qty', text='Кол-во')
        cart_tree.heading('price', text='Сумма')
        cart_tree.column('name', width=150)
        cart_tree.column('qty', width=60)
        cart_tree.column('price', width=90)
        cart_tree.pack(pady=5)
        
        cart_items = {}
        total_label = tk.Label(right_frame, text="Итого: 0 ₽", font=('Arial', 14, 'bold'))
        total_label.pack(pady=10)
        
        def update_total():
            total = sum(item['price'] * item['qty'] for item in cart_items.values())
            total_label.config(text=f"Итого: {total} ₽")
        
        def add_to_cart():
            selected = menu_tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите блюдо")
                return
            
            item_id = int(menu_tree.item(selected[0])['tags'][0])
            item = menu_items[item_id]
            
            if item_id in cart_items:
                cart_items[item_id]['qty'] += 1
            else:
                cart_items[item_id] = {
                    'name': item['name'],
                    'price': item['price'],
                    'qty': 1
                }
            
            refresh_cart()
        
        def remove_from_cart():
            selected = cart_tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите позицию")
                return
            
            item_id = int(cart_tree.item(selected[0])['tags'][0])
            if cart_items[item_id]['qty'] > 1:
                cart_items[item_id]['qty'] -= 1
            else:
                del cart_items[item_id]
            
            refresh_cart()
        
        def refresh_cart():
            cart_tree.delete(*cart_tree.get_children())
            for item_id, item in cart_items.items():
                cart_tree.insert('', 'end', values=(
                    item['name'],
                    item['qty'],
                    f"{item['price'] * item['qty']} ₽"
                ), tags=(item_id,))
            update_total()
        
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="➕ Добавить", command=add_to_cart, bg='#4CAF50', fg='white', width=12).pack(side='left', padx=2)
        tk.Button(btn_frame, text="➖ Убрать", command=remove_from_cart, bg='#f44336', fg='white', width=12).pack(side='left', padx=2)
        
        tk.Label(right_frame, text="Номер столика:", font=('Arial', 10)).pack(pady=5)
        table_var = tk.StringVar()
        table_combo = ttk.Combobox(right_frame, textvariable=table_var, state='readonly', width=20)
        table_combo['values'] = [f"Столик {t['number']}" for t in data['tables'] if t['status'] == 'free']
        if table_combo['values']:
            table_combo.current(0)
        table_combo.pack()
        
        def create_order():
            if not cart_items:
                messagebox.showwarning("Предупреждение", "Корзина пуста")
                return
            
            if not table_var.get():
                messagebox.showwarning("Предупреждение", "Выберите столик")
                return
            
            table_number = int(table_var.get().split()[1])
            
            data = self._load_data()
            new_order = {
                "id": data['next_order_id'],
                "waiter": self.auth.get_current_user()['username'],
                "table": table_number,
                "items": [{"name": item['name'], "qty": item['qty'], "price": item['price']} 
                         for item in cart_items.values()],
                "total": sum(item['price'] * item['qty'] for item in cart_items.values()),
                "status": "new",
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            data['orders'].append(new_order)
            data['next_order_id'] += 1
            
            # Обновление статуса столика
            for table in data['tables']:
                if table['number'] == table_number:
                    table['status'] = 'occupied'
            
            self._save_data(data)
            
            messagebox.showinfo("Успех", f"Заказ №{new_order['id']} создан")
            self.show_main_menu()
        
        tk.Button(right_frame, text="✅ Оформить заказ", command=create_order, bg='#2196F3', fg='white', font=('Arial', 12), width=20).pack(pady=10)
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu, width=15).pack(pady=10)
    
    # ПРОСМОТР ЗАКАЗОВ
    def show_my_orders(self):
        self.clear_window()
        self._create_header("Мои заказы")
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('id', 'table', 'total', 'status', 'created')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='№')
        tree.heading('table', text='Столик')
        tree.heading('total', text='Сумма')
        tree.heading('status', text='Статус')
        tree.heading('created', text='Дата')
        
        tree.column('id', width=50)
        tree.column('table', width=100)
        tree.column('total', width=100)
        tree.column('status', width=150)
        tree.column('created', width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self._load_data()
        username = self.auth.get_current_user()['username']
        
        for order in data['orders']:
            if order['waiter'] == username:
                status_text = {
                    'new': 'Новый',
                    'cooking': 'Готовится',
                    'ready': 'Готов',
                    'completed': 'Завершен'
                }.get(order['status'], order['status'])
                
                tree.insert('', 'end', values=(
                    order['id'],
                    f"Столик {order['table']}",
                    f"{order['total']} ₽",
                    status_text,
                    order['created']
                ))
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu, width=15).pack(pady=10)
    
    # ПРОСМОТР ВСЕХ ЗАКАЗОВ
    def show_all_orders(self):
        self.clear_window()
        self._create_header("Все заказы")
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('id', 'waiter', 'table', 'total', 'status', 'created')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='№')
        tree.heading('waiter', text='Официант')
        tree.heading('table', text='Столик')
        tree.heading('total', text='Сумма')
        tree.heading('status', text='Статус')
        tree.heading('created', text='Дата')
        
        tree.column('id', width=50)
        tree.column('waiter', width=120)
        tree.column('table', width=80)
        tree.column('total', width=100)
        tree.column('status', width=120)
        tree.column('created', width=180)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self._load_data()
        
        for order in data['orders']:
            status_text = {
                'new': 'Новый',
                'cooking': 'Готовится',
                'ready': 'Готов',
                'completed': 'Завершен'
            }.get(order['status'], order['status'])
            
            tree.insert('', 'end', values=(
                order['id'],
                order['waiter'],
                f"Столик {order['table']}",
                f"{order['total']} ₽",
                status_text,
                order['created']
            ))
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu, width=15).pack(pady=10)
    
    # ИЗМЕНЕНИЕ СТАТУСА ЗАКАЗА
    def show_change_order_status(self):
        self.clear_window()
        self._create_header("Изменение статуса заказа")
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('id', 'table', 'total', 'status')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='№')
        tree.heading('table', text='Столик')
        tree.heading('total', text='Сумма')
        tree.heading('status', text='Статус')
        
        tree.column('id', width=100)
        tree.column('table', width=150)
        tree.column('total', width=150)
        tree.column('status', width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_orders():
            tree.delete(*tree.get_children())
            data = self._load_data()
            username = self.auth.get_current_user()['username']
            
            for order in data['orders']:
                if order['waiter'] == username and order['status'] != 'completed':
                    status_text = {
                        'new': 'Новый',
                        'cooking': 'Готовится',
                        'ready': 'Готов'
                    }.get(order['status'], order['status'])
                    
                    tree.insert('', 'end', values=(
                        order['id'],
                        f"Столик {order['table']}",
                        f"{order['total']} ₽",
                        status_text
                    ), tags=(order['id'],))
        
        refresh_orders()
        
        def change_status(new_status):
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите заказ")
                return
            
            order_id = int(tree.item(selected[0])['tags'][0])
            data = self._load_data()
            
            for order in data['orders']:
                if order['id'] == order_id:
                    order['status'] = new_status
                    
                    # Если завершен - освобождаем столик
                    if new_status == 'completed':
                        for table in data['tables']:
                            if table['number'] == order['table']:
                                table['status'] = 'free'
                    break
            
            self._save_data(data)
            refresh_orders()
            messagebox.showinfo("Успех", "Статус обновлен")
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🍳 Готовится", command=lambda: change_status('cooking'), bg='#FF9800', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="✅ Готов", command=lambda: change_status('ready'), bg='#4CAF50', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🏁 Завершен", command=lambda: change_status('completed'), bg='#2196F3', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="← Назад", command=self.show_main_menu, width=15).pack(side='left', padx=5)
    
    # ПРОСМОТР СТОЛИКОВ
    def show_tables_view(self):
        self.clear_window()
        self._create_header("Столики")
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('number', 'seats', 'status')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('number', text='Номер')
        tree.heading('seats', text='Количество мест')
        tree.heading('status', text='Статус')
        
        tree.column('number', width=200)
        tree.column('seats', width=200)
        tree.column('status', width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self._load_data()
        for table in data['tables']:
            status_text = "Свободен" if table['status'] == 'free' else "Занят"
            tree.insert('', 'end', values=(table['number'], table['seats'], status_text))
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu, width=15).pack(pady=10)
    
    # СТАТИСТИКА
    def show_statistics(self):
        self.clear_window()
        self._create_header("Статистика")
        
        data = self._load_data()
        
        # Подсчет статистики
        total_orders = len(data['orders'])
        total_revenue = sum(order['total'] for order in data['orders'])
        completed_orders = len([o for o in data['orders'] if o['status'] == 'completed'])
        active_orders = len([o for o in data['orders'] if o['status'] != 'completed'])
        
        stats_frame = tk.Frame(self.root, bg='white')
        stats_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        stats = [
            ("📊 Всего заказов:", total_orders),
            ("💰 Общая выручка:", f"{total_revenue} ₽"),
            ("✅ Завершено заказов:", completed_orders),
            ("🔄 Активных заказов:", active_orders),
            ("📋 Позиций в меню:", len(data['menu'])),
            ("🪑 Всего столиков:", len(data['tables'])),
            ("🆓 Свободных столиков:", len([t for t in data['tables'] if t['status'] == 'free']))
        ]
        
        for i, (label, value) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg='#f5f5f5', relief='ridge', borderwidth=2)
            frame.pack(pady=10, padx=50, fill='x')
            
            tk.Label(frame, text=label, font=('Arial', 14), bg='#f5f5f5', anchor='w').pack(side='left', padx=20, pady=15)
            tk.Label(frame, text=str(value), font=('Arial', 14, 'bold'), bg='#f5f5f5', anchor='e').pack(side='right', padx=20, pady=15)
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu, width=15).pack(pady=10)
    
    def _create_header(self, title):
        # Создание заголовка страницы
        header = tk.Frame(self.root, bg='#2196F3', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text=title, font=('Arial', 16, 'bold'), bg='#2196F3', fg='white').pack(pady=12)

if __name__ == '__main__':
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()