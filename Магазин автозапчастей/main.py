import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import AuthManager

class AutoPartsShop:
    def __init__(self, root):
        self.root = root
        self.root.title("Магазин автозапчастей")
        self.root.geometry("900x600")
        
        self.auth = AuthManager()
        self.data_file = 'data.json'

        # Показ окна авторизации
        self.show_login_screen()
    
    
    def _load_data(self):
        # Загрузка данных
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data):
        # Сохранение данных
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        # Окно авторизации
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Магазин автозапчастей", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=("Arial", 12)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 12)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, font=("Arial", 12), width=25, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, role, full_name = self.auth.login(username, password)
            
            if success:
                messagebox.showinfo("Успех", f"Добро пожаловать, {full_name}!")
                self.show_main_menu(role)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", font=("Arial", 12), width=20, command=do_login).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка
        hint = tk.Label(frame, text="admin/admin123 | seller/seller123 | client/client123", 
                       font=("Arial", 9), fg="gray")
        hint.grid(row=4, column=0, columnspan=2)
    
    def show_main_menu(self, role):
        # Главное меню в зависимости от роли
        self.clear_window()
        
        user = self.auth.get_current_user()
        
        # Шапка
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text="Магазин автозапчастей", bg='#2c3e50', fg='white', 
                font=("Arial", 16, "bold")).pack(side='left', padx=20, pady=15)
        
        tk.Label(header, text=f"{user['full_name']} ({role})", bg='#2c3e50', fg='white',
                font=("Arial", 10)).pack(side='right', padx=20)
        
        # Меню
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if role == 'admin':
            self.show_admin_menu(menu_frame)
        elif role == 'seller':
            self.show_seller_menu(menu_frame)
        elif role == 'client':
            self.show_client_menu(menu_frame)
        
        # Кнопка выхода
        tk.Button(self.root, text="Выйти из системы", command=self.logout).pack(pady=10)
    
    def logout(self):
        # Выход
        self.auth.logout()
        self.show_login_screen()
    
    def show_admin_menu(self, parent):
        # Меню администратора
        tk.Label(parent, text="Панель администратора", font=("Arial", 14, "bold")).pack(pady=10)
        
        buttons = [
            ("Управление пользователями", self.manage_users),
            ("Управление товарами", self.manage_parts),
            ("Управление поставщиками", self.manage_suppliers),
            ("Просмотр всех заказов", self.view_all_orders),
            ("Отчеты", self.view_reports),
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, font=("Arial", 12), width=30, 
                     command=command).pack(pady=5)
    
    def show_seller_menu(self, parent):
        # Меню продавца
        tk.Label(parent, text="Панель продавца", font=("Arial", 14, "bold")).pack(pady=10)
        
        buttons = [
            ("Каталог товаров", self.view_catalog),
            ("Оформить заказ", self.create_order),
            ("Управление клиентами", self.manage_clients),
            ("Просмотр заказов", self.view_orders),
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, font=("Arial", 12), width=30,
                     command=command).pack(pady=5)
    
    def show_client_menu(self, parent):
        # Меню клиента
        tk.Label(parent, text="Личный кабинет", font=("Arial", 14, "bold")).pack(pady=10)
        
        buttons = [
            ("Каталог товаров", self.view_catalog),
            ("Мои заказы", self.my_orders),
            ("Оформить заказ", self.client_create_order),
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, font=("Arial", 12), width=30,
                     command=command).pack(pady=5)
    
    # === УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ===
    def manage_users(self):
        window = tk.Toplevel(self.root)
        window.title("Управление пользователями")
        window.geometry("800x500")
        
        # Таблица пользователей
        columns = ('ID', 'Логин', 'Роль', 'ФИО', 'Дата создания')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            users = self.auth.get_all_users()
            for user in users:
                tree.insert('', 'end', values=(user['id'], user['username'], 
                                               user['role'], user['full_name'], user['created']))
        
        refresh_table()
        
        # Кнопки
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_user():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить пользователя")
            add_win.geometry("400x300")
            
            tk.Label(add_win, text="Логин:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            username_entry = tk.Entry(add_win, width=30)
            username_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Пароль:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            password_entry = tk.Entry(add_win, width=30, show='*')
            password_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="ФИО:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            fullname_entry = tk.Entry(add_win, width=30)
            fullname_entry.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Роль:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
            role_var = tk.StringVar(value='client')
            ttk.Combobox(add_win, textvariable=role_var, values=['admin', 'seller', 'client'],
                        width=27, state='readonly').grid(row=3, column=1, padx=10, pady=5)
            
            def save_user():
                username = username_entry.get().strip()
                password = password_entry.get().strip()
                fullname = fullname_entry.get().strip()
                role = role_var.get()
                
                if not all([username, password, fullname]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                success, msg = self.auth.create_user(username, password, role, fullname)
                if success:
                    messagebox.showinfo("Успех", msg)
                    refresh_table()
                    add_win.destroy()
                else:
                    messagebox.showerror("Ошибка", msg)
            
            tk.Button(add_win, text="Сохранить", command=save_user).grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            item = tree.item(selected[0])
            user_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить пользователя?"):
                self.auth.delete_user(user_id)
                refresh_table()
        
        tk.Button(btn_frame, text="Добавить", command=add_user).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_table).pack(side='left', padx=5)
    
    # === УПРАВЛЕНИЕ ТОВАРАМИ ===
    def manage_parts(self):
        window = tk.Toplevel(self.root)
        window.title("Управление товарами")
        window.geometry("900x500")
        
        columns = ('ID', 'Название', 'Артикул', 'Производитель', 'Категория', 'Цена', 'Количество')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for part in data['parts']:
                tree.insert('', 'end', values=(part['id'], part['name'], part['article'],
                                              part['manufacturer'], part['category'], 
                                              f"{part['price']:.2f}", part['quantity']))
        
        refresh_table()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_part():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить товар")
            add_win.geometry("400x400")
            
            fields = [
                ("Название:", tk.Entry(add_win, width=30)),
                ("Артикул:", tk.Entry(add_win, width=30)),
                ("Производитель:", tk.Entry(add_win, width=30)),
                ("Категория:", tk.Entry(add_win, width=30)),
                ("Цена:", tk.Entry(add_win, width=30)),
                ("Количество:", tk.Entry(add_win, width=30)),
            ]
            
            for i, (label, entry) in enumerate(fields):
                tk.Label(add_win, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
                entry.grid(row=i, column=1, padx=10, pady=5)
            
            def save_part():
                try:
                    name = fields[0][1].get().strip()
                    article = fields[1][1].get().strip()
                    manufacturer = fields[2][1].get().strip()
                    category = fields[3][1].get().strip()
                    price = float(fields[4][1].get().strip())
                    quantity = int(fields[5][1].get().strip())
                    
                    if not all([name, article, manufacturer, category]):
                        messagebox.showerror("Ошибка", "Заполните все поля")
                        return
                    
                    data = self._load_data()
                    new_id = max([p['id'] for p in data['parts']]) + 1 if data['parts'] else 1
                    
                    new_part = {
                        "id": new_id,
                        "name": name,
                        "article": article,
                        "manufacturer": manufacturer,
                        "category": category,
                        "price": price,
                        "quantity": quantity,
                        "supplier_id": 1
                    }
                    
                    data['parts'].append(new_part)
                    self._save_data(data)
                    
                    messagebox.showinfo("Успех", "Товар добавлен")
                    refresh_table()
                    add_win.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Проверьте правильность ввода цены и количества")
            
            tk.Button(add_win, text="Сохранить", command=save_part).grid(row=6, column=0, columnspan=2, pady=20)
        
        def delete_part():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите товар")
                return
            
            item = tree.item(selected[0])
            part_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить товар?"):
                data = self._load_data()
                data['parts'] = [p for p in data['parts'] if p['id'] != part_id]
                self._save_data(data)
                refresh_table()
        
        tk.Button(btn_frame, text="Добавить", command=add_part).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_part).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_table).pack(side='left', padx=5)
    
    # === УПРАВЛЕНИЕ ПОСТАВЩИКАМИ ===
    def manage_suppliers(self):
        window = tk.Toplevel(self.root)
        window.title("Управление поставщиками")
        window.geometry("700x400")
        
        columns = ('ID', 'Название', 'Контакт', 'Адрес')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for supplier in data['suppliers']:
                tree.insert('', 'end', values=(supplier['id'], supplier['name'],
                                              supplier['contact'], supplier['address']))
        
        refresh_table()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_supplier():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить поставщика")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="Название:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Контакт:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            contact_entry = tk.Entry(add_win, width=30)
            contact_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Адрес:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            address_entry = tk.Entry(add_win, width=30)
            address_entry.grid(row=2, column=1, padx=10, pady=5)
            
            def save_supplier():
                name = name_entry.get().strip()
                contact = contact_entry.get().strip()
                address = address_entry.get().strip()
                
                if not all([name, contact, address]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                data = self._load_data()
                new_id = max([s['id'] for s in data['suppliers']]) + 1 if data['suppliers'] else 1
                
                new_supplier = {
                    "id": new_id,
                    "name": name,
                    "contact": contact,
                    "address": address
                }
                
                data['suppliers'].append(new_supplier)
                self._save_data(data)
                
                messagebox.showinfo("Успех", "Поставщик добавлен")
                refresh_table()
                add_win.destroy()
            
            tk.Button(add_win, text="Сохранить", command=save_supplier).grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Добавить", command=add_supplier).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_table).pack(side='left', padx=5)
    
    # === КАТАЛОГ ТОВАРОВ ===
    def view_catalog(self):
        window = tk.Toplevel(self.root)
        window.title("Каталог товаров")
        window.geometry("900x500")
        
        # Поиск
        search_frame = tk.Frame(window)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        columns = ('ID', 'Название', 'Артикул', 'Производитель', 'Категория', 'Цена', 'В наличии')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=18)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_table(search_text=''):
            tree.delete(*tree.get_children())
            data = self._load_data()
            for part in data['parts']:
                if search_text.lower() in part['name'].lower() or \
                   search_text.lower() in part['article'].lower() or \
                   search_text.lower() in part['manufacturer'].lower():
                    tree.insert('', 'end', values=(part['id'], part['name'], part['article'],
                                                  part['manufacturer'], part['category'],
                                                  f"{part['price']:.2f} руб", part['quantity']))
        
        refresh_table()
        
        def do_search():
            refresh_table(search_entry.get().strip())
        
        tk.Button(search_frame, text="Найти", command=do_search).pack(side='left', padx=5)
        tk.Button(search_frame, text="Сбросить", command=lambda: (search_entry.delete(0, 'end'), refresh_table())).pack(side='left', padx=5)
    
    # === ОФОРМЛЕНИЕ ЗАКАЗА (ПРОДАВЕЦ) ===
    def create_order(self):
        window = tk.Toplevel(self.root)
        window.title("Оформление заказа")
        window.geometry("800x600")
        
        # Выбор клиента
        tk.Label(window, text="Клиент:", font=("Arial", 10)).pack(pady=5)
        
        data = self._load_data()
        clients = data.get('clients', [])
        
        client_var = tk.StringVar()
        client_combo = ttk.Combobox(window, textvariable=client_var, width=40, state='readonly')
        client_combo['values'] = [f"{c['id']} - {c['name']} ({c['phone']})" for c in clients]
        client_combo.pack(pady=5)
        
        # Корзина
        tk.Label(window, text="Корзина:", font=("Arial", 10)).pack(pady=10)
        
        cart_columns = ('ID', 'Название', 'Цена', 'Количество', 'Сумма')
        cart_tree = ttk.Treeview(window, columns=cart_columns, show='headings', height=8)
        
        for col in cart_columns:
            cart_tree.heading(col, text=col)
            cart_tree.column(col, width=150)
        
        cart_tree.pack(pady=5, padx=10, fill='both', expand=True)
        
        cart_items = []
        
        def add_to_cart():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить товар")
            add_win.geometry("600x400")
            
            columns = ('ID', 'Название', 'Цена', 'В наличии')
            parts_tree = ttk.Treeview(add_win, columns=columns, show='headings', height=12)
            
            for col in columns:
                parts_tree.heading(col, text=col)
                parts_tree.column(col, width=140)
            
            parts_tree.pack(pady=10, padx=10, fill='both', expand=True)
            
            for part in data['parts']:
                parts_tree.insert('', 'end', values=(part['id'], part['name'],
                                                    f"{part['price']:.2f}", part['quantity']))
            
            tk.Label(add_win, text="Количество:").pack()
            qty_entry = tk.Entry(add_win, width=10)
            qty_entry.pack()
            
            def select_part():
                selected = parts_tree.selection()
                if not selected:
                    messagebox.showwarning("Предупреждение", "Выберите товар")
                    return
                
                try:
                    qty = int(qty_entry.get().strip())
                    if qty <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректное количество")
                    return
                
                item = parts_tree.item(selected[0])
                part_id = item['values'][0]
                part_name = item['values'][1]
                part_price = float(item['values'][2])
                available = item['values'][3]
                
                if qty > available:
                    messagebox.showerror("Ошибка", f"Недостаточно товара (доступно: {available})")
                    return
                
                total = part_price * qty
                cart_items.append({
                    'id': part_id,
                    'name': part_name,
                    'price': part_price,
                    'quantity': qty,
                    'total': total
                })
                
                cart_tree.insert('', 'end', values=(part_id, part_name, f"{part_price:.2f}",
                                                   qty, f"{total:.2f}"))
                update_total()
                add_win.destroy()
            
            tk.Button(add_win, text="Добавить", command=select_part).pack(pady=10)
        
        def update_total():
            total = sum(item['total'] for item in cart_items)
            total_label.config(text=f"Итого: {total:.2f} руб")
        
        total_label = tk.Label(window, text="Итого: 0.00 руб", font=("Arial", 12, "bold"))
        total_label.pack(pady=10)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def save_order():
            if not client_var.get():
                messagebox.showerror("Ошибка", "Выберите клиента")
                return
            
            if not cart_items:
                messagebox.showerror("Ошибка", "Добавьте товары в корзину")
                return
            
            client_id = int(client_var.get().split(' - ')[0])
            
            data = self._load_data()
            new_id = max([o['id'] for o in data['orders']]) + 1 if data['orders'] else 1
            
            order = {
                'id': new_id,
                'client_id': client_id,
                'items': cart_items,
                'total': sum(item['total'] for item in cart_items),
                'status': 'Новый',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'seller_id': self.auth.current_user['id']
            }
            
            data['orders'].append(order)
            
            # Обновление остатков
            for item in cart_items:
                for part in data['parts']:
                    if part['id'] == item['id']:
                        part['quantity'] -= item['quantity']
            
            self._save_data(data)
            
            messagebox.showinfo("Успех", f"Заказ №{new_id} оформлен")
            window.destroy()
        
        tk.Button(btn_frame, text="Добавить товар", command=add_to_cart).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Сохранить заказ", command=save_order).pack(side='left', padx=5)
    
    # === УПРАВЛЕНИЕ КЛИЕНТАМИ ===
    def manage_clients(self):
        window = tk.Toplevel(self.root)
        window.title("Управление клиентами")
        window.geometry("700x400")
        
        columns = ('ID', 'ФИО', 'Телефон', 'Email')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for client in data.get('clients', []):
                tree.insert('', 'end', values=(client['id'], client['name'],
                                              client['phone'], client.get('email', '')))
        
        refresh_table()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_client():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить клиента")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="ФИО:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Телефон:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            phone_entry = tk.Entry(add_win, width=30)
            phone_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            email_entry = tk.Entry(add_win, width=30)
            email_entry.grid(row=2, column=1, padx=10, pady=5)
            
            def save_client():
                name = name_entry.get().strip()
                phone = phone_entry.get().strip()
                email = email_entry.get().strip()
                
                if not all([name, phone]):
                    messagebox.showerror("Ошибка", "Заполните обязательные поля")
                    return
                
                data = self._load_data()
                if 'clients' not in data:
                    data['clients'] = []
                
                new_id = max([c['id'] for c in data['clients']]) + 1 if data['clients'] else 1
                
                new_client = {
                    "id": new_id,
                    "name": name,
                    "phone": phone,
                    "email": email
                }
                
                data['clients'].append(new_client)
                self._save_data(data)
                
                messagebox.showinfo("Успех", "Клиент добавлен")
                refresh_table()
                add_win.destroy()
            
            tk.Button(add_win, text="Сохранить", command=save_client).grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Добавить", command=add_client).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_table).pack(side='left', padx=5)
    
    # === ПРОСМОТР ЗАКАЗОВ ===
    def view_orders(self):
        window = tk.Toplevel(self.root)
        window.title("Просмотр заказов")
        window.geometry("800x500")
        
        columns = ('№', 'Клиент', 'Дата', 'Сумма', 'Статус')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            data = self._load_data()
            
            for order in data.get('orders', []):
                client_name = "Неизвестный"
                for client in data.get('clients', []):
                    if client['id'] == order['client_id']:
                        client_name = client['name']
                        break
                
                tree.insert('', 'end', values=(order['id'], client_name, order['created'],
                                              f"{order['total']:.2f} руб", order['status']))
        
        refresh_table()
        
        tk.Button(window, text="Обновить", command=refresh_table).pack(pady=10)
    
    # === ПРОСМОТР ВСЕХ ЗАКАЗОВ (ADMIN) ===
    def view_all_orders(self):
        self.view_orders()
    
    # === МОИ ЗАКАЗЫ (CLIENT) ===
    def my_orders(self):
        window = tk.Toplevel(self.root)
        window.title("Мои заказы")
        window.geometry("800x500")
        
        columns = ('№', 'Дата', 'Товары', 'Сумма', 'Статус')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        user_id = self.auth.current_user['id']
        
        for order in data.get('orders', []):
            if order['client_id'] == user_id:
                items_str = ', '.join([f"{item['name']} x{item['quantity']}" for item in order['items']])
                tree.insert('', 'end', values=(order['id'], order['created'], items_str,
                                              f"{order['total']:.2f} руб", order['status']))
    
    # === ОФОРМЛЕНИЕ ЗАКАЗА (CLIENT) ===
    def client_create_order(self):
        window = tk.Toplevel(self.root)
        window.title("Оформление заказа")
        window.geometry("800x600")
        
        tk.Label(window, text="Корзина:", font=("Arial", 10)).pack(pady=10)
        
        cart_columns = ('ID', 'Название', 'Цена', 'Количество', 'Сумма')
        cart_tree = ttk.Treeview(window, columns=cart_columns, show='headings', height=8)
        
        for col in cart_columns:
            cart_tree.heading(col, text=col)
            cart_tree.column(col, width=150)
        
        cart_tree.pack(pady=5, padx=10, fill='both', expand=True)
        
        cart_items = []
        data = self._load_data()
        
        def add_to_cart():
            add_win = tk.Toplevel(window)
            add_win.title("Выбрать товар")
            add_win.geometry("600x400")
            
            columns = ('ID', 'Название', 'Цена', 'В наличии')
            parts_tree = ttk.Treeview(add_win, columns=columns, show='headings', height=12)
            
            for col in columns:
                parts_tree.heading(col, text=col)
                parts_tree.column(col, width=140)
            
            parts_tree.pack(pady=10, padx=10, fill='both', expand=True)
            
            for part in data['parts']:
                if part['quantity'] > 0:
                    parts_tree.insert('', 'end', values=(part['id'], part['name'],
                                                        f"{part['price']:.2f}", part['quantity']))
            
            tk.Label(add_win, text="Количество:").pack()
            qty_entry = tk.Entry(add_win, width=10)
            qty_entry.pack()
            
            def select_part():
                selected = parts_tree.selection()
                if not selected:
                    messagebox.showwarning("Предупреждение", "Выберите товар")
                    return
                
                try:
                    qty = int(qty_entry.get().strip())
                    if qty <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректное количество")
                    return
                
                item = parts_tree.item(selected[0])
                part_id = item['values'][0]
                part_name = item['values'][1]
                part_price = float(item['values'][2])
                available = item['values'][3]
                
                if qty > available:
                    messagebox.showerror("Ошибка", f"Недостаточно товара (доступно: {available})")
                    return
                
                total = part_price * qty
                cart_items.append({
                    'id': part_id,
                    'name': part_name,
                    'price': part_price,
                    'quantity': qty,
                    'total': total
                })
                
                cart_tree.insert('', 'end', values=(part_id, part_name, f"{part_price:.2f}",
                                                   qty, f"{total:.2f}"))
                update_total()
                add_win.destroy()
            
            tk.Button(add_win, text="Добавить", command=select_part).pack(pady=10)
        
        def update_total():
            total = sum(item['total'] for item in cart_items)
            total_label.config(text=f"Итого: {total:.2f} руб")
        
        total_label = tk.Label(window, text="Итого: 0.00 руб", font=("Arial", 12, "bold"))
        total_label.pack(pady=10)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def save_order():
            if not cart_items:
                messagebox.showerror("Ошибка", "Добавьте товары в корзину")
                return
            
            data = self._load_data()
            
            # Проверка или создание клиента
            user_id = self.auth.current_user['id']
            client_exists = False
            
            for client in data.get('clients', []):
                if client['id'] == user_id:
                    client_exists = True
                    break
            
            if not client_exists:
                if 'clients' not in data:
                    data['clients'] = []
                data['clients'].append({
                    'id': user_id,
                    'name': self.auth.current_user['full_name'],
                    'phone': 'Не указан',
                    'email': ''
                })
            
            new_id = max([o['id'] for o in data['orders']]) + 1 if data['orders'] else 1
            
            order = {
                'id': new_id,
                'client_id': user_id,
                'items': cart_items,
                'total': sum(item['total'] for item in cart_items),
                'status': 'Новый',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'seller_id': None
            }
            
            data['orders'].append(order)
            
            # Обновление остатков
            for item in cart_items:
                for part in data['parts']:
                    if part['id'] == item['id']:
                        part['quantity'] -= item['quantity']
            
            self._save_data(data)
            
            messagebox.showinfo("Успех", f"Заказ №{new_id} оформлен! Ожидайте обработки.")
            window.destroy()
        
        tk.Button(btn_frame, text="Добавить товар", command=add_to_cart).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Оформить заказ", command=save_order).pack(side='left', padx=5)
    
    # === ОТЧЕТЫ ===
    def view_reports(self):
        window = tk.Toplevel(self.root)
        window.title("Отчеты")
        window.geometry("600x400")
        
        data = self._load_data()
        
        # Статистика
        total_parts = len(data['parts'])
        total_orders = len(data.get('orders', []))
        total_revenue = sum(o['total'] for o in data.get('orders', []))
        total_clients = len(data.get('clients', []))
        
        stats_frame = tk.Frame(window)
        stats_frame.pack(pady=20)
        
        tk.Label(stats_frame, text="Статистика системы", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(stats_frame, text="Всего товаров:", font=("Arial", 11)).grid(row=1, column=0, sticky='e', padx=10, pady=5)
        tk.Label(stats_frame, text=str(total_parts), font=("Arial", 11, "bold")).grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        tk.Label(stats_frame, text="Всего заказов:", font=("Arial", 11)).grid(row=2, column=0, sticky='e', padx=10, pady=5)
        tk.Label(stats_frame, text=str(total_orders), font=("Arial", 11, "bold")).grid(row=2, column=1, sticky='w', padx=10, pady=5)
        
        tk.Label(stats_frame, text="Общая выручка:", font=("Arial", 11)).grid(row=3, column=0, sticky='e', padx=10, pady=5)
        tk.Label(stats_frame, text=f"{total_revenue:.2f} руб", font=("Arial", 11, "bold")).grid(row=3, column=1, sticky='w', padx=10, pady=5)
        
        tk.Label(stats_frame, text="Всего клиентов:", font=("Arial", 11)).grid(row=4, column=0, sticky='e', padx=10, pady=5)
        tk.Label(stats_frame, text=str(total_clients), font=("Arial", 11, "bold")).grid(row=4, column=1, sticky='w', padx=10, pady=5)

if __name__ == '__main__':
    root = tk.Tk()
    app = AutoPartsShop(root)
    root.mainloop()