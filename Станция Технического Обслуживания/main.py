import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
from auth import AuthManager

class STOSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система СТО")
        self.root.geometry("1000x700")
        
        self.auth_manager = AuthManager()
        self.data_file = 'data.json'

        self.show_login_window()
    
    def _load_data(self):
        """Загрузка данных из JSON"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Сохранение данных в JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Вход в систему СТО", font=('Arial', 18, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
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
            
            if self.auth_manager.authenticate(username, password):
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login, width=20, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=15)
        
        # Подсказка
        info_text = "Тестовые учетные записи:\nadmin/admin123\nmechanic/mech123\nclient/client123"
        tk.Label(frame, text=info_text, bg='#f0f0f0', fg='gray', font=('Arial', 8)).grid(row=4, column=0, columnspan=2, pady=10)
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        user = self.auth_manager.current_user
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"СТО - {user['full_name']} ({user['role']})", 
                bg='#2c3e50', fg='white', font=('Arial', 14)).pack(side='left', padx=20, pady=15)
        
        tk.Button(top_frame, text="Выход", command=self.logout, bg='#e74c3c', fg='white').pack(side='right', padx=20)
        
        # Контентная область
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if user['role'] == 'administrator':
            self.show_admin_menu(content_frame)
        elif user['role'] == 'mechanic':
            self.show_mechanic_menu(content_frame)
        elif user['role'] == 'client':
            self.show_client_menu(content_frame)
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Управление пользователями", command=self.manage_users, 
                 width=25, height=2, bg='#3498db', fg='white').grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Управление услугами", command=self.manage_services, 
                 width=25, height=2, bg='#3498db', fg='white').grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="Управление запчастями", command=self.manage_parts, 
                 width=25, height=2, bg='#3498db', fg='white').grid(row=1, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Все заказы", command=self.view_all_orders, 
                 width=25, height=2, bg='#3498db', fg='white').grid(row=1, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="Отчеты", command=self.generate_reports, 
                 width=25, height=2, bg='#9b59b6', fg='white').grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    
    def show_mechanic_menu(self, parent):
        """Меню механика"""
        tk.Label(parent, text="Рабочее место механика", font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Мои заказы", command=self.view_mechanic_orders, 
                 width=25, height=2, bg='#27ae60', fg='white').grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Обновить статус заказа", command=self.update_order_status, 
                 width=25, height=2, bg='#27ae60', fg='white').grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="Просмотр запчастей", command=self.view_parts, 
                 width=25, height=2, bg='#27ae60', fg='white').grid(row=1, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Заказать запчасти", command=self.order_parts, 
                 width=25, height=2, bg='#f39c12', fg='white').grid(row=1, column=1, padx=10, pady=5)
    
    def show_client_menu(self, parent):
        """Меню клиента"""
        tk.Label(parent, text="Личный кабинет клиента", font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Мои заказы", command=self.view_my_orders, 
                 width=25, height=2, bg='#e67e22', fg='white').grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Создать заявку", command=self.create_order, 
                 width=25, height=2, bg='#e67e22', fg='white').grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="Просмотр услуг", command=self.view_services, 
                 width=25, height=2, bg='#e67e22', fg='white').grid(row=1, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Прайс-лист", command=self.view_price_list, 
                 width=25, height=2, bg='#16a085', fg='white').grid(row=1, column=1, padx=10, pady=5)
    
    # === ФУНКЦИИ АДМИНИСТРАТОРА ===
    
    def manage_users(self):
        """Управление пользователями"""
        win = tk.Toplevel(self.root)
        win.title("Управление пользователями")
        win.geometry("800x500")
        
        # Таблица пользователей
        columns = ('Логин', 'Роль', 'ФИО', 'Дата создания')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_users():
            tree.delete(*tree.get_children())
            users = self.auth_manager.get_all_users()
            for user in users:
                tree.insert('', 'end', values=(user['username'], user['role'], 
                                              user['full_name'], user['created']))
        
        def add_user():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить пользователя")
            add_win.geometry("400x300")
            
            tk.Label(add_win, text="Логин:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            username_entry = tk.Entry(add_win)
            username_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Пароль:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            password_entry = tk.Entry(add_win, show='*')
            password_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="ФИО:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            fullname_entry = tk.Entry(add_win)
            fullname_entry.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Роль:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
            role_var = tk.StringVar(value='client')
            roles = ['administrator', 'mechanic', 'client']
            role_combo = ttk.Combobox(add_win, textvariable=role_var, values=roles, state='readonly')
            role_combo.grid(row=3, column=1, padx=10, pady=5)
            
            def save_user():
                success, msg = self.auth_manager.register_user(
                    username_entry.get(),
                    password_entry.get(),
                    role_var.get(),
                    fullname_entry.get()
                )
                if success:
                    messagebox.showinfo("Успех", msg)
                    refresh_users()
                    add_win.destroy()
                else:
                    messagebox.showerror("Ошибка", msg)
            
            tk.Button(add_win, text="Сохранить", command=save_user, bg='#27ae60', fg='white').grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите пользователя")
                return
            
            item = tree.item(selected[0])
            username = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                self.auth_manager.delete_user(username)
                refresh_users()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_user, bg='#27ae60', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, bg='#e74c3c', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_users, bg='#3498db', fg='white', width=15).pack(side='left', padx=5)
        
        refresh_users()
    
    def manage_services(self):
        """Управление услугами"""
        win = tk.Toplevel(self.root)
        win.title("Управление услугами")
        win.geometry("700x500")
        
        columns = ('ID', 'Название', 'Цена', 'Длительность')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column('ID', width=50)
        tree.column('Название', width=300)
        tree.column('Цена', width=100)
        tree.column('Длительность', width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_services():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for service in data['services']:
                tree.insert('', 'end', values=(service['id'], service['name'], 
                                              service['price'], service['duration']))
        
        def add_service():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить услугу")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="Название:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Цена:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            price_entry = tk.Entry(add_win, width=30)
            price_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Длительность:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            duration_entry = tk.Entry(add_win, width=30)
            duration_entry.grid(row=2, column=1, padx=10, pady=5)
            
            def save_service():
                try:
                    data = self._load_data()
                    new_id = max([s['id'] for s in data['services']], default=0) + 1
                    
                    new_service = {
                        'id': new_id,
                        'name': name_entry.get(),
                        'price': int(price_entry.get()),
                        'duration': duration_entry.get()
                    }
                    
                    data['services'].append(new_service)
                    self._save_data(data)
                    
                    messagebox.showinfo("Успех", "Услуга добавлена")
                    refresh_services()
                    add_win.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Проверьте корректность данных")
            
            tk.Button(add_win, text="Сохранить", command=save_service, bg='#27ae60', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        def delete_service():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите услугу")
                return
            
            item = tree.item(selected[0])
            service_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить услугу?"):
                data = self._load_data()
                data['services'] = [s for s in data['services'] if s['id'] != service_id]
                self._save_data(data)
                refresh_services()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_service, bg='#27ae60', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_service, bg='#e74c3c', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_services, bg='#3498db', fg='white', width=15).pack(side='left', padx=5)
        
        refresh_services()
    
    def manage_parts(self):
        """Управление запчастями"""
        win = tk.Toplevel(self.root)
        win.title("Управление запчастями")
        win.geometry("700x500")
        
        columns = ('ID', 'Название', 'Цена', 'Количество')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh_parts():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for part in data['parts']:
                tree.insert('', 'end', values=(part['id'], part['name'], 
                                              part['price'], part['quantity']))
        
        def add_part():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить запчасть")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="Название:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Цена:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            price_entry = tk.Entry(add_win, width=30)
            price_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Количество:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            qty_entry = tk.Entry(add_win, width=30)
            qty_entry.grid(row=2, column=1, padx=10, pady=5)
            
            def save_part():
                try:
                    data = self._load_data()
                    new_id = max([p['id'] for p in data['parts']], default=0) + 1
                    
                    new_part = {
                        'id': new_id,
                        'name': name_entry.get(),
                        'price': int(price_entry.get()),
                        'quantity': int(qty_entry.get())
                    }
                    
                    data['parts'].append(new_part)
                    self._save_data(data)
                    
                    messagebox.showinfo("Успех", "Запчасть добавлена")
                    refresh_parts()
                    add_win.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Проверьте корректность данных")
            
            tk.Button(add_win, text="Сохранить", command=save_part, bg='#27ae60', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_part, bg='#27ae60', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_parts, bg='#3498db', fg='white', width=15).pack(side='left', padx=5)
        
        refresh_parts()
    
    def view_all_orders(self):
        """Просмотр всех заказов"""
        win = tk.Toplevel(self.root)
        win.title("Все заказы")
        win.geometry("900x500")
        
        columns = ('ID', 'Клиент', 'Автомобиль', 'Услуга', 'Статус', 'Механик', 'Дата', 'Сумма')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        for order in data['orders']:
            tree.insert('', 'end', values=(order['id'], order['client'], order['car'],
                                          order['service'], order['status'], order['mechanic'],
                                          order['date'], order['total']))
    
    def generate_reports(self):
        """Генерация отчетов"""
        win = tk.Toplevel(self.root)
        win.title("Отчеты")
        win.geometry("600x500")
        
        tk.Label(win, text="Статистика системы", font=('Arial', 14, 'bold')).pack(pady=10)
        
        report_text = scrolledtext.ScrolledText(win, width=70, height=25)
        report_text.pack(pady=10, padx=10)
        
        data = self._load_data()
        users = self.auth_manager.get_all_users()
        
        report = f"""
{'='*60}
                    ОТЧЕТ ПО СИСТЕМЕ СТО
{'='*60}

ПОЛЬЗОВАТЕЛИ:
Всего пользователей: {len(users)}
Администраторов: {len([u for u in users if u['role'] == 'administrator'])}
Механиков: {len([u for u in users if u['role'] == 'mechanic'])}
Клиентов: {len([u for u in users if u['role'] == 'client'])}

УСЛУГИ:
Всего услуг: {len(data['services'])}
Средняя стоимость: {sum([s['price'] for s in data['services']])/len(data['services']) if data['services'] else 0:.2f} руб.

ЗАПЧАСТИ:
Всего наименований: {len(data['parts'])}
Общее количество: {sum([p['quantity'] for p in data['parts']])} шт.
Стоимость склада: {sum([p['price']*p['quantity'] for p in data['parts']])} руб.

ЗАКАЗЫ:
Всего заказов: {len(data['orders'])}
Выполнено: {len([o for o in data['orders'] if o['status'] == 'Выполнено'])}
В работе: {len([o for o in data['orders'] if o['status'] == 'В работе'])}
Новых: {len([o for o in data['orders'] if o['status'] == 'Новый'])}
Общая сумма: {sum([o['total'] for o in data['orders']])} руб.

{'='*60}
Дата формирования: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'='*60}
        """
        
        report_text.insert('1.0', report)
        report_text.config(state='disabled')
    
    # === ФУНКЦИИ МЕХАНИКА ===
    
    def view_mechanic_orders(self):
        """Просмотр заказов механика"""
        win = tk.Toplevel(self.root)
        win.title("Мои заказы")
        win.geometry("900x500")
        
        columns = ('ID', 'Клиент', 'Автомобиль', 'Услуга', 'Статус', 'Дата', 'Сумма')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        current_mechanic = self.auth_manager.current_user['username']
        
        for order in data['orders']:
            if order['mechanic'] == current_mechanic:
                tree.insert('', 'end', values=(order['id'], order['client'], order['car'],
                                              order['service'], order['status'],
                                              order['date'], order['total']))
    
    def update_order_status(self):
        """Обновление статуса заказа"""
        win = tk.Toplevel(self.root)
        win.title("Обновить статус заказа")
        win.geometry("500x300")
        
        tk.Label(win, text="ID заказа:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        order_id_entry = tk.Entry(win)
        order_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(win, text="Новый статус:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        status_var = tk.StringVar(value='В работе')
        statuses = ['Новый', 'В работе', 'Выполнено', 'Отменен']
        status_combo = ttk.Combobox(win, textvariable=status_var, values=statuses, state='readonly')
        status_combo.grid(row=1, column=1, padx=10, pady=10)
        
        def update_status():
            try:
                order_id = int(order_id_entry.get())
                data = self._load_data()
                
                for order in data['orders']:
                    if order['id'] == order_id:
                        order['status'] = status_var.get()
                        self._save_data(data)
                        messagebox.showinfo("Успех", "Статус обновлен")
                        win.destroy()
                        return
                
                messagebox.showerror("Ошибка", "Заказ не найден")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректный ID")
        
        tk.Button(win, text="Обновить", command=update_status, bg='#27ae60', fg='white', width=20).grid(row=2, column=0, columnspan=2, pady=30)
    
    def view_parts(self):
        """Просмотр запчастей"""
        win = tk.Toplevel(self.root)
        win.title("Запчасти на складе")
        win.geometry("700x500")
        
        columns = ('ID', 'Название', 'Цена', 'Количество')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        for part in data['parts']:
            tree.insert('', 'end', values=(part['id'], part['name'], 
                                          part['price'], part['quantity']))
    
    def order_parts(self):
        """Заказ запчастей"""
        win = tk.Toplevel(self.root)
        win.title("Заказать запчасти")
        win.geometry("400x200")
        
        tk.Label(win, text="ID запчасти:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        part_id_entry = tk.Entry(win)
        part_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(win, text="Количество:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        qty_entry = tk.Entry(win)
        qty_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def place_order():
            try:
                part_id = int(part_id_entry.get())
                qty = int(qty_entry.get())
                
                data = self._load_data()
                for part in data['parts']:
                    if part['id'] == part_id:
                        part['quantity'] += qty
                        self._save_data(data)
                        messagebox.showinfo("Успех", f"Заказано {qty} шт. {part['name']}")
                        win.destroy()
                        return
                
                messagebox.showerror("Ошибка", "Запчасть не найдена")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные данные")
        
        tk.Button(win, text="Заказать", command=place_order, bg='#f39c12', fg='white', width=20).grid(row=2, column=0, columnspan=2, pady=20)
    
    # === ФУНКЦИИ КЛИЕНТА ===
    
    def view_my_orders(self):
        """Просмотр заказов клиента"""
        win = tk.Toplevel(self.root)
        win.title("Мои заказы")
        win.geometry("800x500")
        
        columns = ('ID', 'Автомобиль', 'Услуга', 'Статус', 'Механик', 'Дата', 'Сумма')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        current_client = self.auth_manager.current_user['username']
        
        for order in data['orders']:
            if order['client'] == current_client:
                tree.insert('', 'end', values=(order['id'], order['car'],
                                              order['service'], order['status'],
                                              order['mechanic'], order['date'], order['total']))
    
    def create_order(self):
        """Создание новой заявки"""
        win = tk.Toplevel(self.root)
        win.title("Создать заявку")
        win.geometry("500x350")
        
        tk.Label(win, text="Автомобиль:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        car_entry = tk.Entry(win, width=30)
        car_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(win, text="Услуга:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        data = self._load_data()
        services = [s['name'] for s in data['services']]
        service_var = tk.StringVar(value=services[0] if services else '')
        service_combo = ttk.Combobox(win, textvariable=service_var, values=services, state='readonly', width=28)
        service_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(win, text="Описание проблемы:").grid(row=2, column=0, padx=10, pady=10, sticky='ne')
        description_text = tk.Text(win, width=30, height=5)
        description_text.grid(row=2, column=1, padx=10, pady=10)
        
        def submit_order():
            if not car_entry.get() or not service_var.get():
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            data = self._load_data()
            new_id = max([o['id'] for o in data['orders']], default=0) + 1
            
            # Найти цену услуги
            service_price = 0
            for service in data['services']:
                if service['name'] == service_var.get():
                    service_price = service['price']
                    break
            
            new_order = {
                'id': new_id,
                'client': self.auth_manager.current_user['username'],
                'car': car_entry.get(),
                'service': service_var.get(),
                'status': 'Новый',
                'mechanic': 'mechanic',
                'date': datetime.now().strftime("%Y-%m-%d"),
                'total': service_price
            }
            
            data['orders'].append(new_order)
            self._save_data(data)
            
            messagebox.showinfo("Успех", f"Заявка №{new_id} создана")
            win.destroy()
        
        tk.Button(win, text="Создать заявку", command=submit_order, bg='#e67e22', fg='white', width=20).grid(row=3, column=0, columnspan=2, pady=20)
    
    def view_services(self):
        """Просмотр услуг"""
        win = tk.Toplevel(self.root)
        win.title("Наши услуги")
        win.geometry("700x500")
        
        columns = ('Название', 'Цена', 'Длительность')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column('Название', width=350)
        tree.column('Цена', width=150)
        tree.column('Длительность', width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        for service in data['services']:
            tree.insert('', 'end', values=(service['name'], f"{service['price']} руб.", 
                                          service['duration']))
    
    def view_price_list(self):
        """Прайс-лист"""
        win = tk.Toplevel(self.root)
        win.title("Прайс-лист")
        win.geometry("600x500")
        
        tk.Label(win, text="ПРАЙС-ЛИСТ СТО", font=('Arial', 14, 'bold')).pack(pady=10)
        
        price_text = scrolledtext.ScrolledText(win, width=70, height=25)
        price_text.pack(pady=10, padx=10)
        
        data = self._load_data()
        
        price_list = f"""
{'='*60}
                        УСЛУГИ
{'='*60}

"""
        for service in data['services']:
            price_list += f"{service['name']:<40} {service['price']:>8} руб.\n"
            price_list += f"  Время выполнения: {service['duration']}\n\n"
        
        price_list += f"\n{'='*60}\n                       ЗАПЧАСТИ\n{'='*60}\n\n"
        
        for part in data['parts']:
            price_list += f"{part['name']:<40} {part['price']:>8} руб.\n"
        
        price_list += f"\n{'='*60}\n"
        
        price_text.insert('1.0', price_list)
        price_text.config(state='disabled')
    
    def logout(self):
        """Выход из системы"""
        self.auth_manager.logout()
        self.show_login_window()

def main():
    root = tk.Tk()
    app = STOSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()