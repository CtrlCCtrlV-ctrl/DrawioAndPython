import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import authenticate, Session, create_user, delete_user, get_all_users

DATA_FILE = 'data.json'

class FlowerShopApp:
    """Главный класс приложения Цветочный магазин"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Цветочный магазин - Информационная система")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        try:
            self.load_data()
            self.show_login_window()
        except FileNotFoundError as e:
            messagebox.showerror("Ошибка", str(e))
            self.root.quit()
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if not os.path.exists(DATA_FILE):
            raise FileNotFoundError(f"Файл данных {DATA_FILE} не найден. Создайте файл с тестовыми данными.")

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="🌸 Цветочный магазин", font=('Arial', 20, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=10)
        self.login_entry = tk.Entry(frame, font=('Arial', 12), width=20)
        self.login_entry.grid(row=1, column=1, padx=5, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12), bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=10)
        self.password_entry = tk.Entry(frame, font=('Arial', 12), width=20, show='*')
        self.password_entry.grid(row=2, column=1, padx=5, pady=10)
        
        tk.Button(frame, text="Войти", font=('Arial', 12), width=15, command=self.login, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        info_text = "По умолчанию:\nadmin/admin123\nseller/seller123\nclient/client123"
        tk.Label(frame, text=info_text, font=('Arial', 9), bg='#f0f0f0', fg='#666').grid(row=4, column=0, columnspan=2, pady=10)
    
    def login(self):
        """Обработка входа"""
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        user = authenticate(username, password)
        if user:
            Session.login(user)
            self.show_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def logout(self):
        """Выход из системы"""
        Session.logout()
        self.show_login_window()
    
    def show_main_window(self):
        """Главное окно после входа"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"👤 {Session.current_user['full_name']}", font=('Arial', 12), bg='#2196F3', fg='white').pack(side='left', padx=20, pady=15)
        tk.Label(top_frame, text=f"Роль: {self.get_role_name()}", font=('Arial', 10), bg='#2196F3', fg='white').pack(side='left', pady=15)
        tk.Button(top_frame, text="Выход", command=self.logout, bg='#f44336', fg='white', font=('Arial', 10)).pack(side='right', padx=20, pady=15)
        
        # Основной контент
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        role = Session.get_role()
        
        if role == 'administrator':
            self.show_admin_panel(content_frame)
        elif role == 'manager':
            self.show_manager_panel(content_frame)
        elif role == 'client':
            self.show_client_panel(content_frame)
    
    def get_role_name(self):
        """Получение названия роли на русском"""
        roles = {
            'administrator': 'Администратор',
            'manager': 'Продавец',
            'client': 'Клиент'
        }
        return roles.get(Session.get_role(), 'Неизвестно')
    
    def show_admin_panel(self, parent):
        """Панель администратора"""
        tk.Label(parent, text="Панель администратора", font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Управление пользователями", width=25, height=2, command=self.manage_users).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Управление каталогом", width=25, height=2, command=self.manage_flowers).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Все заказы", width=25, height=2, command=self.view_all_orders).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Статистика", width=25, height=2, command=self.view_statistics).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Управление поставщиками", width=25, height=2, command=self.manage_suppliers).grid(row=2, column=0, padx=10, pady=10)
    
    def show_manager_panel(self, parent):
        """Панель продавца"""
        tk.Label(parent, text="Панель продавца", font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Каталог цветов", width=25, height=2, command=self.view_catalog).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Создать заказ", width=25, height=2, command=self.create_order).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Просмотр заказов", width=25, height=2, command=self.view_orders).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Управление клиентами", width=25, height=2, command=self.manage_clients).grid(row=1, column=1, padx=10, pady=10)
    
    def show_client_panel(self, parent):
        """Панель клиента"""
        tk.Label(parent, text="Панель клиента", font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Каталог цветов", width=25, height=2, command=self.view_catalog).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Поиск цветов", width=25, height=2, command=self.search_flowers).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Оформить заказ", width=25, height=2, command=self.place_order).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Мои заказы", width=25, height=2, command=self.view_my_orders).grid(row=1, column=1, padx=10, pady=10)
    
    # Функции для администратора
    def manage_users(self):
        """Управление пользователями"""
        window = tk.Toplevel(self.root)
        window.title("Управление пользователями")
        window.geometry("700x500")
        
        # Таблица пользователей
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('Логин', 'ФИО', 'Роль', 'Дата создания')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        def refresh_users():
            tree.delete(*tree.get_children())
            for user in get_all_users():
                tree.insert('', 'end', values=(user['username'], user['full_name'], user['role'], user['created']))
        
        refresh_users()
        
        # Кнопки
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_user_dialog():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить пользователя")
            add_win.geometry("400x300")
            
            tk.Label(add_win, text="Логин:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
            username_entry = tk.Entry(add_win, width=30)
            username_entry.grid(row=0, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Пароль:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
            password_entry = tk.Entry(add_win, width=30, show='*')
            password_entry.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="ФИО:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
            fullname_entry = tk.Entry(add_win, width=30)
            fullname_entry.grid(row=2, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Роль:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
            role_var = tk.StringVar(value="client")
            roles_combo = ttk.Combobox(add_win, textvariable=role_var, values=['administrator', 'manager', 'client'], width=28)
            roles_combo.grid(row=3, column=1, padx=10, pady=10)
            
            def save_user():
                success, message = create_user(username_entry.get(), password_entry.get(), role_var.get(), fullname_entry.get())
                if success:
                    messagebox.showinfo("Успех", message)
                    refresh_users()
                    add_win.destroy()
                else:
                    messagebox.showerror("Ошибка", message)
            
            tk.Button(add_win, text="Сохранить", command=save_user, width=15).grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_selected_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            username = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                delete_user(username)
                refresh_users()
                messagebox.showinfo("Успех", "Пользователь удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_user_dialog, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_selected_user, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Закрыть", command=window.destroy, width=15).pack(side='left', padx=5)
    
    def manage_flowers(self):
        """Управление каталогом цветов"""
        window = tk.Toplevel(self.root)
        window.title("Управление каталогом цветов")
        window.geometry("800x500")
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Цена', 'Количество', 'Поставщик')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Название', width=200)
        tree.column('Цена', width=100)
        tree.column('Количество', width=100)
        tree.column('Поставщик', width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        def refresh_flowers():
            tree.delete(*tree.get_children())
            for flower in self.data['flowers']:
                tree.insert('', 'end', values=(flower['id'], flower['name'], flower['price'], flower['quantity'], flower['supplier']))
        
        refresh_flowers()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_flower_dialog():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить цветок")
            add_win.geometry("400x300")
            
            tk.Label(add_win, text="Название:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Цена:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
            price_entry = tk.Entry(add_win, width=30)
            price_entry.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Количество:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
            quantity_entry = tk.Entry(add_win, width=30)
            quantity_entry.grid(row=2, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Поставщик:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
            supplier_entry = tk.Entry(add_win, width=30)
            supplier_entry.grid(row=3, column=1, padx=10, pady=10)
            
            def save_flower():
                try:
                    new_id = max([f['id'] for f in self.data['flowers']], default=0) + 1
                    new_flower = {
                        'id': new_id,
                        'name': name_entry.get(),
                        'price': int(price_entry.get()),
                        'quantity': int(quantity_entry.get()),
                        'supplier': supplier_entry.get()
                    }
                    self.data['flowers'].append(new_flower)
                    self.save_data()
                    refresh_flowers()
                    messagebox.showinfo("Успех", "Цветок добавлен")
                    add_win.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Проверьте правильность данных")
            
            tk.Button(add_win, text="Сохранить", command=save_flower, width=15).grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_flower():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите цветок")
                return
            
            flower_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить выбранный цветок?"):
                self.data['flowers'] = [f for f in self.data['flowers'] if f['id'] != flower_id]
                self.save_data()
                refresh_flowers()
                messagebox.showinfo("Успех", "Цветок удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_flower_dialog, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_flower, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Закрыть", command=window.destroy, width=15).pack(side='left', padx=5)
    
    def view_all_orders(self):
        """Просмотр всех заказов"""
        window = tk.Toplevel(self.root)
        window.title("Все заказы")
        window.geometry("900x500")
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Клиент', 'Цветы', 'Сумма', 'Статус', 'Дата', 'Создал')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Клиент', width=150)
        tree.column('Цветы', width=200)
        tree.column('Сумма', width=100)
        tree.column('Статус', width=120)
        tree.column('Дата', width=100)
        tree.column('Создал', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        for order in self.data['orders']:
            tree.insert('', 'end', values=(order['id'], order['client'], order['flowers'], order['total'], order['status'], order['date'], order['created_by']))
        
        tk.Button(window, text="Закрыть", command=window.destroy, width=15).pack(pady=10)
    
    def view_statistics(self):
        """Просмотр статистики"""
        window = tk.Toplevel(self.root)
        window.title("Статистика")
        window.geometry("500x400")
        
        frame = tk.Frame(window, padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        total_orders = len(self.data['orders'])
        total_revenue = sum(order['total'] for order in self.data['orders'])
        total_flowers = len(self.data['flowers'])
        total_clients = len(self.data['clients'])
        
        tk.Label(frame, text="📊 Общая статистика", font=('Arial', 16, 'bold')).pack(pady=20)
        
        stats_frame = tk.Frame(frame)
        stats_frame.pack(pady=10)
        
        tk.Label(stats_frame, text=f"Всего заказов: {total_orders}", font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Общая выручка: {total_revenue} руб.", font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Цветов в каталоге: {total_flowers}", font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Клиентов: {total_clients}", font=('Arial', 12)).pack(pady=5)
        
        tk.Button(window, text="Закрыть", command=window.destroy, width=15).pack(pady=20)
    
    def manage_suppliers(self):
        """Управление поставщиками"""
        window = tk.Toplevel(self.root)
        window.title("Управление поставщиками")
        window.geometry("800x500")
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Телефон', 'Адрес')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Название', width=200)
        tree.column('Телефон', width=150)
        tree.column('Адрес', width=300)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        def refresh_suppliers():
            tree.delete(*tree.get_children())
            for supplier in self.data['suppliers']:
                tree.insert('', 'end', values=(supplier['id'], supplier['name'], supplier['phone'], supplier['address']))
        
        refresh_suppliers()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_supplier_dialog():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить поставщика")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="Название:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Телефон:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
            phone_entry = tk.Entry(add_win, width=30)
            phone_entry.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Адрес:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
            address_entry = tk.Entry(add_win, width=30)
            address_entry.grid(row=2, column=1, padx=10, pady=10)
            
            def save_supplier():
                new_id = max([s['id'] for s in self.data['suppliers']], default=0) + 1
                new_supplier = {
                    'id': new_id,
                    'name': name_entry.get(),
                    'phone': phone_entry.get(),
                    'address': address_entry.get()
                }
                self.data['suppliers'].append(new_supplier)
                self.save_data()
                refresh_suppliers()
                messagebox.showinfo("Успех", "Поставщик добавлен")
                add_win.destroy()
            
            tk.Button(add_win, text="Сохранить", command=save_supplier, width=15).grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Добавить", command=add_supplier_dialog, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Закрыть", command=window.destroy, width=15).pack(side='left', padx=5)
    
    # Функции для продавца
    def view_catalog(self):
        """Просмотр каталога"""
        window = tk.Toplevel(self.root)
        window.title("Каталог цветов")
        window.geometry("700x500")
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Цена', 'Количество', 'Поставщик')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Название', width=200)
        tree.column('Цена', width=100)
        tree.column('Количество', width=100)
        tree.column('Поставщик', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        for flower in self.data['flowers']:
            tree.insert('', 'end', values=(flower['id'], flower['name'], f"{flower['price']} руб.", flower['quantity'], flower['supplier']))
        
        tk.Button(window, text="Закрыть", command=window.destroy, width=15).pack(pady=10)
    
    def create_order(self):
        """Создание заказа (продавец)"""
        window = tk.Toplevel(self.root)
        window.title("Создать заказ")
        window.geometry("500x400")
        
        frame = tk.Frame(window, padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Создание нового заказа", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(frame, text="Клиент:").pack(pady=5)
        client_var = tk.StringVar()
        client_combo = ttk.Combobox(frame, textvariable=client_var, values=[c['name'] for c in self.data['clients']], width=40)
        client_combo.pack(pady=5)
        
        tk.Label(frame, text="Цветы (описание):").pack(pady=5)
        flowers_entry = tk.Entry(frame, width=42)
        flowers_entry.pack(pady=5)
        
        tk.Label(frame, text="Сумма (руб.):").pack(pady=5)
        total_entry = tk.Entry(frame, width=42)
        total_entry.pack(pady=5)
        
        tk.Label(frame, text="Статус:").pack(pady=5)
        status_var = tk.StringVar(value="В обработке")
        status_combo = ttk.Combobox(frame, textvariable=status_var, values=['В обработке', 'Выполнен', 'Отменен'], width=40)
        status_combo.pack(pady=5)
        
        def save_order():
            try:
                new_id = max([o['id'] for o in self.data['orders']], default=0) + 1
                new_order = {
                    'id': new_id,
                    'client': client_var.get(),
                    'flowers': flowers_entry.get(),
                    'total': int(total_entry.get()),
                    'status': status_var.get(),
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'created_by': Session.current_user['username']
                }
                self.data['orders'].append(new_order)
                self.save_data()
                messagebox.showinfo("Успех", "Заказ создан")
                window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте правильность данных")
        
        tk.Button(frame, text="Сохранить заказ", command=save_order, width=20).pack(pady=20)
    
    def view_orders(self):
        """Просмотр заказов (продавец)"""
        window = tk.Toplevel(self.root)
        window.title("Заказы")
        window.geometry("900x500")
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Клиент', 'Цветы', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Клиент', width=150)
        tree.column('Цветы', width=250)
        tree.column('Сумма', width=100)
        tree.column('Статус', width=120)
        tree.column('Дата', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        def refresh_orders():
            tree.delete(*tree.get_children())
            for order in self.data['orders']:
                tree.insert('', 'end', values=(order['id'], order['client'], order['flowers'], order['total'], order['status'], order['date']))
        
        refresh_orders()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def update_status():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите заказ")
                return
            
            order_id = tree.item(selected[0])['values'][0]
            
            status_win = tk.Toplevel(window)
            status_win.title("Обновить статус")
            status_win.geometry("300x150")
            
            tk.Label(status_win, text="Новый статус:").pack(pady=10)
            status_var = tk.StringVar(value="В обработке")
            status_combo = ttk.Combobox(status_win, textvariable=status_var, values=['В обработке', 'Выполнен', 'Отменен'], width=30)
            status_combo.pack(pady=10)
            
            def save_status():
                for order in self.data['orders']:
                    if order['id'] == order_id:
                        order['status'] = status_var.get()
                        break
                self.save_data()
                refresh_orders()
                messagebox.showinfo("Успех", "Статус обновлен")
                status_win.destroy()
            
            tk.Button(status_win, text="Сохранить", command=save_status, width=15).pack(pady=10)
        
        tk.Button(btn_frame, text="Обновить статус", command=update_status, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Закрыть", command=window.destroy, width=15).pack(side='left', padx=5)
    
    def manage_clients(self):
        """Управление клиентами"""
        window = tk.Toplevel(self.root)
        window.title("Управление клиентами")
        window.geometry("700x500")
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'ФИО', 'Телефон', 'Email')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('ФИО', width=200)
        tree.column('Телефон', width=150)
        tree.column('Email', width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        def refresh_clients():
            tree.delete(*tree.get_children())
            for client in self.data['clients']:
                tree.insert('', 'end', values=(client['id'], client['name'], client['phone'], client['email']))
        
        refresh_clients()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_client_dialog():
            add_win = tk.Toplevel(window)
            add_win.title("Добавить клиента")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="ФИО:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Телефон:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
            phone_entry = tk.Entry(add_win, width=30)
            phone_entry.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(add_win, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
            email_entry = tk.Entry(add_win, width=30)
            email_entry.grid(row=2, column=1, padx=10, pady=10)
            
            def save_client():
                new_id = max([c['id'] for c in self.data['clients']], default=0) + 1
                new_client = {
                    'id': new_id,
                    'name': name_entry.get(),
                    'phone': phone_entry.get(),
                    'email': email_entry.get()
                }
                self.data['clients'].append(new_client)
                self.save_data()
                refresh_clients()
                messagebox.showinfo("Успех", "Клиент добавлен")
                add_win.destroy()
            
            tk.Button(add_win, text="Сохранить", command=save_client, width=15).grid(row=3, column=0, columnspan=2, pady=20)
        
        def delete_client():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите клиента")
                return
            
            client_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить выбранного клиента?"):
                self.data['clients'] = [c for c in self.data['clients'] if c['id'] != client_id]
                self.save_data()
                refresh_clients()
                messagebox.showinfo("Успех", "Клиент удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_client_dialog, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_client, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Закрыть", command=window.destroy, width=15).pack(side='left', padx=5)
    
    # Функции для клиента
    def search_flowers(self):
        """Поиск цветов"""
        window = tk.Toplevel(self.root)
        window.title("Поиск цветов")
        window.geometry("700x500")
        
        search_frame = tk.Frame(window)
        search_frame.pack(pady=10, padx=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=40)
        search_entry.pack(side='left', padx=5)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Цена', 'Доступно')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Название', width=300)
        tree.column('Цена', width=150)
        tree.column('Доступно', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        def do_search():
            tree.delete(*tree.get_children())
            search_term = search_entry.get().lower()
            for flower in self.data['flowers']:
                if search_term in flower['name'].lower():
                    available = "Да" if flower['quantity'] > 0 else "Нет"
                    tree.insert('', 'end', values=(flower['id'], flower['name'], f"{flower['price']} руб.", available))
        
        tk.Button(search_frame, text="Искать", command=do_search, width=10).pack(side='left', padx=5)
        
        do_search()
        
        tk.Button(window, text="Закрыть", command=window.destroy, width=15).pack(pady=10)
    
    def place_order(self):
        """Оформление заказа (клиент)"""
        window = tk.Toplevel(self.root)
        window.title("Оформить заказ")
        window.geometry("500x350")
        
        frame = tk.Frame(window, padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Оформление заказа", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(frame, text="Ваше имя:").pack(pady=5)
        name_entry = tk.Entry(frame, width=42)
        name_entry.insert(0, Session.current_user['full_name'])
        name_entry.pack(pady=5)
        
        tk.Label(frame, text="Цветы (название и количество):").pack(pady=5)
        flowers_entry = tk.Entry(frame, width=42)
        flowers_entry.pack(pady=5)
        
        tk.Label(frame, text="Сумма (руб.):").pack(pady=5)
        total_entry = tk.Entry(frame, width=42)
        total_entry.pack(pady=5)
        
        def save_order():
            try:
                new_id = max([o['id'] for o in self.data['orders']], default=0) + 1
                new_order = {
                    'id': new_id,
                    'client': name_entry.get(),
                    'flowers': flowers_entry.get(),
                    'total': int(total_entry.get()),
                    'status': 'В обработке',
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'created_by': Session.current_user['username']
                }
                self.data['orders'].append(new_order)
                self.save_data()
                messagebox.showinfo("Успех", "Ваш заказ принят!")
                window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте правильность данных")
        
        tk.Button(frame, text="Оформить заказ", command=save_order, width=20).pack(pady=20)
    
    def view_my_orders(self):
        """Просмотр своих заказов (клиент)"""
        window = tk.Toplevel(self.root)
        window.title("Мои заказы")
        window.geometry("800x500")
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Цветы', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Цветы', width=300)
        tree.column('Сумма', width=100)
        tree.column('Статус', width=150)
        tree.column('Дата', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)
        
        username = Session.current_user['username']
        for order in self.data['orders']:
            if order['created_by'] == username:
                tree.insert('', 'end', values=(order['id'], order['flowers'], order['total'], order['status'], order['date']))
        
        tk.Button(window, text="Закрыть", command=window.destroy, width=15).pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    app = FlowerShopApp(root)
    root.mainloop()