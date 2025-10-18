import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

DATA_FILE = 'data.json'

class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система - Аптека")
        self.root.geometry("900x600")
        
        # Файлы данных уже созданы с предустановленными данными
        
        # Показ окна входа
        self.show_login()
    
    
    def load_data(self):
        """Загрузка данных из JSON"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в JSON"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Вход в систему", font=('Arial', 16, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
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
                auth.set_current_user(user)
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login, width=20, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка
        hint_text = "admin/admin123 | pharmacist/pharm123 | client/client123"
        tk.Label(frame, text=hint_text, font=('Arial', 8), bg='#f0f0f0', fg='gray').grid(row=4, column=0, columnspan=2)
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        user = auth.get_current_user()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"Аптека | {user['role'].upper()}", 
                font=('Arial', 14, 'bold'), bg='#2196F3', fg='white').pack(side='left', padx=20, pady=15)
        
        tk.Label(top_frame, text=f"Пользователь: {user['username']}", 
                bg='#2196F3', fg='white').pack(side='right', padx=20)
        
        tk.Button(top_frame, text="Выход", command=self.show_login, 
                 bg='#f44336', fg='white').pack(side='right', padx=5)
        
        # Контент в зависимости от роли
        if user['role'] == 'administrator':
            self.show_admin_panel()
        elif user['role'] == 'pharmacist':
            self.show_pharmacist_panel()
        elif user['role'] == 'client':
            self.show_client_panel()
    
    def show_admin_panel(self):
        """Панель администратора"""
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Меню
        menu_frame = tk.Frame(container)
        menu_frame.pack(side='left', fill='y', padx=(0, 20))
        
        tk.Label(menu_frame, text="Управление", font=('Arial', 12, 'bold')).pack(pady=10)
        
        tk.Button(menu_frame, text="Пользователи", command=self.manage_users, width=20).pack(pady=5)
        tk.Button(menu_frame, text="Поставщики", command=self.manage_suppliers, width=20).pack(pady=5)
        tk.Button(menu_frame, text="Категории", command=self.manage_categories, width=20).pack(pady=5)
        tk.Button(menu_frame, text="Лекарства", command=self.manage_medicines, width=20).pack(pady=5)
        tk.Button(menu_frame, text="Отчеты", command=self.view_reports, width=20).pack(pady=5)
        
        # Рабочая область
        self.work_area = tk.Frame(container, relief='solid', borderwidth=1)
        self.work_area.pack(side='right', fill='both', expand=True)
        
        tk.Label(self.work_area, text="Выберите раздел для работы", 
                font=('Arial', 14)).pack(pady=100)
    
    def manage_users(self):
        """Управление пользователями"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Управление пользователями", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Таблица
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Логин', 'Роль', 'Дата создания')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Загрузка данных
        for user in auth.get_all_users():
            tree.insert('', 'end', values=(user['username'], user['role'], user['created']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки
        btn_frame = tk.Frame(self.work_area)
        btn_frame.pack(pady=10)
        
        def add_user():
            win = tk.Toplevel(self.root)
            win.title("Добавить пользователя")
            win.geometry("300x200")
            
            tk.Label(win, text="Логин:").pack(pady=5)
            username_entry = tk.Entry(win)
            username_entry.pack()
            
            tk.Label(win, text="Пароль:").pack(pady=5)
            password_entry = tk.Entry(win, show='*')
            password_entry.pack()
            
            tk.Label(win, text="Роль:").pack(pady=5)
            role_var = tk.StringVar(value='client')
            roles = ['administrator', 'pharmacist', 'client']
            role_menu = ttk.Combobox(win, textvariable=role_var, values=roles, state='readonly')
            role_menu.pack()
            
            def save():
                if auth.create_user(username_entry.get(), password_entry.get(), role_var.get()):
                    messagebox.showinfo("Успех", "Пользователь создан")
                    win.destroy()
                    self.manage_users()
                else:
                    messagebox.showerror("Ошибка", "Пользователь уже существует")
            
            tk.Button(win, text="Сохранить", command=save).pack(pady=10)
        
        def delete_user():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                username = item['values'][0]
                if username == 'admin':
                    messagebox.showerror("Ошибка", "Нельзя удалить администратора")
                    return
                if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                    auth.delete_user(username)
                    self.manage_users()
        
        tk.Button(btn_frame, text="Добавить", command=add_user, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, bg='#f44336', fg='white').pack(side='left', padx=5)
    
    def manage_suppliers(self):
        """Управление поставщиками"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Управление поставщиками", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Таблица
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Название', 'Контакт')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for supplier in data['suppliers']:
            tree.insert('', 'end', values=(supplier['id'], supplier['name'], supplier['contact']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки
        btn_frame = tk.Frame(self.work_area)
        btn_frame.pack(pady=10)
        
        def add_supplier():
            win = tk.Toplevel(self.root)
            win.title("Добавить поставщика")
            win.geometry("300x150")
            
            tk.Label(win, text="Название:").pack(pady=5)
            name_entry = tk.Entry(win, width=30)
            name_entry.pack()
            
            tk.Label(win, text="Контакт:").pack(pady=5)
            contact_entry = tk.Entry(win, width=30)
            contact_entry.pack()
            
            def save():
                data = self.load_data()
                new_id = max([s['id'] for s in data['suppliers']], default=0) + 1
                data['suppliers'].append({
                    'id': new_id,
                    'name': name_entry.get(),
                    'contact': contact_entry.get()
                })
                self.save_data(data)
                messagebox.showinfo("Успех", "Поставщик добавлен")
                win.destroy()
                self.manage_suppliers()
            
            tk.Button(win, text="Сохранить", command=save).pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_supplier, bg='#4CAF50', fg='white').pack(side='left', padx=5)
    
    def manage_categories(self):
        """Управление категориями"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Управление категориями", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Список
        listbox = tk.Listbox(self.work_area, height=15, width=50)
        listbox.pack(pady=10)
        
        for cat in data['categories']:
            listbox.insert('end', cat)
        
        # Кнопки
        btn_frame = tk.Frame(self.work_area)
        btn_frame.pack(pady=10)
        
        def add_category():
            win = tk.Toplevel(self.root)
            win.title("Добавить категорию")
            win.geometry("300x100")
            
            tk.Label(win, text="Название:").pack(pady=5)
            name_entry = tk.Entry(win, width=30)
            name_entry.pack()
            
            def save():
                data = self.load_data()
                if name_entry.get() not in data['categories']:
                    data['categories'].append(name_entry.get())
                    self.save_data(data)
                    messagebox.showinfo("Успех", "Категория добавлена")
                    win.destroy()
                    self.manage_categories()
            
            tk.Button(win, text="Сохранить", command=save).pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_category, bg='#4CAF50', fg='white').pack(side='left', padx=5)
    
    def manage_medicines(self):
        """Управление лекарствами (для админа)"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Управление лекарствами", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Таблица
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Название', 'Категория', 'Цена', 'Остаток', 'Поставщик')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for med in data['medicines']:
            tree.insert('', 'end', values=(med['id'], med['name'], med['category'], 
                                          med['price'], med['stock'], med['supplier']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки
        btn_frame = tk.Frame(self.work_area)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Обновить", command=self.manage_medicines, bg='#2196F3', fg='white').pack(side='left', padx=5)
    
    def view_reports(self):
        """Просмотр отчетов"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Отчеты и статистика", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Статистика
        total_medicines = len(data['medicines'])
        total_stock = sum([m['stock'] for m in data['medicines']])
        total_sales = len(data['sales'])
        total_revenue = sum([s['total'] for s in data['sales']])
        
        stats_frame = tk.Frame(self.work_area, relief='solid', borderwidth=1)
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        tk.Label(stats_frame, text=f"Всего лекарств: {total_medicines}", font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Общий остаток: {total_stock} шт", font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Продаж: {total_sales}", font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Выручка: {total_revenue:.2f} руб", font=('Arial', 12)).pack(pady=5)
        
        # История продаж
        tk.Label(self.work_area, text="Последние продажи", font=('Arial', 12, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Дата', 'Лекарство', 'Количество', 'Сумма')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for sale in data['sales'][-10:]:
            tree.insert('', 'end', values=(sale['date'], sale['medicine'], 
                                          sale['quantity'], sale['total']))
        
        tree.pack(fill='both', expand=True)
    
    def show_pharmacist_panel(self):
        """Панель фармацевта"""
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Меню
        menu_frame = tk.Frame(container)
        menu_frame.pack(side='left', fill='y', padx=(0, 20))
        
        tk.Label(menu_frame, text="Операции", font=('Arial', 12, 'bold')).pack(pady=10)
        
        tk.Button(menu_frame, text="Продажа лекарств", command=self.sell_medicine, width=20).pack(pady=5)
        tk.Button(menu_frame, text="Добавить лекарство", command=self.add_medicine, width=20).pack(pady=5)
        tk.Button(menu_frame, text="Обновить остатки", command=self.update_stock, width=20).pack(pady=5)
        tk.Button(menu_frame, text="Поиск лекарств", command=self.search_medicine, width=20).pack(pady=5)
        tk.Button(menu_frame, text="История продаж", command=self.sales_history, width=20).pack(pady=5)
        
        # Рабочая область
        self.work_area = tk.Frame(container, relief='solid', borderwidth=1)
        self.work_area.pack(side='right', fill='both', expand=True)
        
        tk.Label(self.work_area, text="Выберите операцию", font=('Arial', 14)).pack(pady=100)
    
    def sell_medicine(self):
        """Продажа лекарств"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Продажа лекарств", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Каталог
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Название', 'Цена', 'Остаток')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for med in data['medicines']:
            if med['stock'] > 0:
                tree.insert('', 'end', values=(med['id'], med['name'], med['price'], med['stock']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Форма продажи
        form_frame = tk.Frame(self.work_area)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Количество:").pack(side='left', padx=5)
        qty_entry = tk.Entry(form_frame, width=10)
        qty_entry.pack(side='left', padx=5)
        
        def process_sale():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Ошибка", "Выберите лекарство")
                return
            
            try:
                qty = int(qty_entry.get())
                if qty <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Ошибка", "Введите корректное количество")
                return
            
            item = tree.item(selected[0])
            med_id = item['values'][0]
            
            data = self.load_data()
            medicine = next((m for m in data['medicines'] if m['id'] == med_id), None)
            
            if medicine and medicine['stock'] >= qty:
                # Обновление остатка
                medicine['stock'] -= qty
                
                # Запись продажи
                sale = {
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'medicine': medicine['name'],
                    'quantity': qty,
                    'total': medicine['price'] * qty
                }
                data['sales'].append(sale)
                
                self.save_data(data)
                messagebox.showinfo("Успех", f"Продано: {medicine['name']}\nСумма: {sale['total']:.2f} руб")
                self.sell_medicine()
            else:
                messagebox.showerror("Ошибка", "Недостаточно товара на складе")
        
        tk.Button(form_frame, text="Продать", command=process_sale, bg='#4CAF50', fg='white').pack(side='left', padx=5)
    
    def add_medicine(self):
        """Добавление лекарства"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Добавление лекарства", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        form_frame = tk.Frame(self.work_area)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Категория:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        category_var = tk.StringVar()
        category_menu = ttk.Combobox(form_frame, textvariable=category_var, 
                                     values=data['categories'], width=28, state='readonly')
        category_menu.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Цена:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        price_entry = tk.Entry(form_frame, width=30)
        price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Количество:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        stock_entry = tk.Entry(form_frame, width=30)
        stock_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Поставщик:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        supplier_var = tk.StringVar()
        suppliers = [s['name'] for s in data['suppliers']]
        supplier_menu = ttk.Combobox(form_frame, textvariable=supplier_var, 
                                     values=suppliers, width=28, state='readonly')
        supplier_menu.grid(row=4, column=1, padx=5, pady=5)
        
        def save():
            try:
                name = name_entry.get()
                category = category_var.get()
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                supplier = supplier_var.get()
                
                if not all([name, category, supplier]) or price <= 0 or stock < 0:
                    raise ValueError
                
                data = self.load_data()
                new_id = max([m['id'] for m in data['medicines']], default=0) + 1
                
                data['medicines'].append({
                    'id': new_id,
                    'name': name,
                    'category': category,
                    'price': price,
                    'stock': stock,
                    'supplier': supplier
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Лекарство добавлено")
                self.add_medicine()
            except:
                messagebox.showerror("Ошибка", "Проверьте корректность данных")
        
        tk.Button(form_frame, text="Сохранить", command=save, bg='#4CAF50', fg='white', width=20).grid(row=5, column=0, columnspan=2, pady=20)
    
    def update_stock(self):
        """Обновление остатков"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Обновление остатков", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Таблица
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Название', 'Текущий остаток')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for med in data['medicines']:
            tree.insert('', 'end', values=(med['id'], med['name'], med['stock']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Форма обновления
        form_frame = tk.Frame(self.work_area)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Новый остаток:").pack(side='left', padx=5)
        stock_entry = tk.Entry(form_frame, width=10)
        stock_entry.pack(side='left', padx=5)
        
        def update():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Ошибка", "Выберите лекарство")
                return
            
            try:
                new_stock = int(stock_entry.get())
                if new_stock < 0:
                    raise ValueError
            except:
                messagebox.showerror("Ошибка", "Введите корректное количество")
                return
            
            item = tree.item(selected[0])
            med_id = item['values'][0]
            
            data = self.load_data()
            for med in data['medicines']:
                if med['id'] == med_id:
                    med['stock'] = new_stock
                    break
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Остаток обновлен")
            self.update_stock()
        
        tk.Button(form_frame, text="Обновить", command=update, bg='#2196F3', fg='white').pack(side='left', padx=5)
    
    def search_medicine(self):
        """Поиск лекарств"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Поиск лекарств", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Поиск
        search_frame = tk.Frame(self.work_area)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Результаты
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Название', 'Категория', 'Цена', 'Остаток')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        def search():
            tree.delete(*tree.get_children())
            query = search_entry.get().lower()
            data = self.load_data()
            
            for med in data['medicines']:
                if query in med['name'].lower() or query in med['category'].lower():
                    tree.insert('', 'end', values=(med['name'], med['category'], 
                                                  med['price'], med['stock']))
        
        tk.Button(search_frame, text="Найти", command=search, bg='#2196F3', fg='white').pack(side='left', padx=5)
    
    def sales_history(self):
        """История продаж"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="История продаж", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Таблица
        tree_frame = tk.Frame(self.work_area)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Дата', 'Лекарство', 'Количество', 'Сумма')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for sale in reversed(data['sales']):
            tree.insert('', 'end', values=(sale['date'], sale['medicine'], 
                                          sale['quantity'], f"{sale['total']:.2f}"))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
    
    def show_client_panel(self):
        """Панель клиента"""
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(container, text="Каталог лекарств", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Поиск
        search_frame = tk.Frame(container)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=40)
        search_entry.pack(side='left', padx=5)
        
        # Каталог
        tree_frame = tk.Frame(container)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Название', 'Категория', 'Цена', 'Наличие')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        def load_catalog():
            tree.delete(*tree.get_children())
            data = self.load_data()
            query = search_entry.get().lower()
            
            for med in data['medicines']:
                if not query or query in med['name'].lower() or query in med['category'].lower():
                    availability = "В наличии" if med['stock'] > 0 else "Нет в наличии"
                    tree.insert('', 'end', values=(med['name'], med['category'], 
                                                  f"{med['price']:.2f}", availability))
        
        load_catalog()
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        tk.Button(search_frame, text="Найти", command=load_catalog, bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        # Просмотр информации
        def view_info():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                info = f"Название: {item['values'][0]}\n"
                info += f"Категория: {item['values'][1]}\n"
                info += f"Цена: {item['values'][2]} руб\n"
                info += f"Статус: {item['values'][3]}"
                messagebox.showinfo("Информация о лекарстве", info)
        
        tk.Button(container, text="Подробная информация", command=view_info, 
                 bg='#4CAF50', fg='white', width=20).pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()