import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

class TouristAgencyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Туристическая фирма - Информационная система")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.init_data()
        self.show_login()
        
    def init_data(self):
        """Инициализация данных"""
        pass
    
    def load_data(self):
        """Загрузка данных из JSON"""
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в JSON"""
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно входа в систему"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Туристическая фирма", font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(frame, text="Информационная система", font=('Arial', 12)).grid(row=1, column=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="Логин:", font=('Arial', 11)).grid(row=2, column=0, sticky='e', padx=5, pady=10)
        username_entry = tk.Entry(frame, font=('Arial', 11), width=25)
        username_entry.grid(row=2, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 11)).grid(row=3, column=0, sticky='e', padx=5, pady=10)
        password_entry = tk.Entry(frame, show="*", font=('Arial', 11), width=25)
        password_entry.grid(row=3, column=1, pady=10)
        
        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            if auth.login(username, password):
                user = auth.get_current_user()
                self.show_main_menu(user)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", font=('Arial', 11), width=20, command=do_login).grid(row=4, column=0, columnspan=2, pady=20)
        
        info_text = "Тестовые учетные записи:\nadmin/admin123 (Администратор)\nmanager/manager123 (Менеджер)\nclient/client123 (Клиент)"
        tk.Label(frame, text=info_text, font=('Arial', 9), fg='gray', justify='left').grid(row=5, column=0, columnspan=2)
        
        password_entry.bind('<Return>', lambda e: do_login())
    
    def show_main_menu(self, user):
        """Главное меню (зависит от роли)"""
        self.clear_window()
        
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Добро пожаловать, {user['full_name']}", bg='#2c3e50', fg='white', font=('Arial', 14)).pack(side='left', padx=20, pady=15)
        tk.Label(header, text=f"Роль: {self.get_role_name(user['role'])}", bg='#2c3e50', fg='#ecf0f1', font=('Arial', 10)).pack(side='left', padx=10)
        
        tk.Button(header, text="Выход", command=self.show_login, bg='#e74c3c', fg='white', font=('Arial', 10)).pack(side='right', padx=20)
        
        if user['role'] == 'administrator':
            self.show_admin_panel()
        elif user['role'] == 'manager':
            self.show_manager_panel()
        elif user['role'] == 'client':
            self.show_client_panel()
    
    def get_role_name(self, role):
        """Получение названия роли на русском"""
        roles = {
            'administrator': 'Администратор',
            'manager': 'Менеджер',
            'client': 'Клиент'
        }
        return roles.get(role, role)
    
    # ПАНЕЛЬ АДМИНИСТРАТОРА
    def show_admin_panel(self):
        """Панель администратора"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        notebook.add(self.create_users_tab(), text="Пользователи")
        notebook.add(self.create_tours_tab(), text="Туры")
        notebook.add(self.create_clients_tab(), text="Клиенты")
        notebook.add(self.create_bookings_tab(), text="Бронирования")
        notebook.add(self.create_reports_tab(), text="Отчеты")
    
    def create_users_tab(self):
        """Вкладка управления пользователями"""
        frame = tk.Frame(self.root)
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text="Добавить пользователя", command=self.add_user).pack(side='left', padx=5)
        tk.Button(toolbar, text="Удалить пользователя", command=self.delete_user).pack(side='left', padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.refresh_users_table(tree)).pack(side='left', padx=5)
        
        columns = ('Логин', 'Роль', 'ФИО', 'Дата создания')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=5)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_users_table(tree)
        
        return frame
    
    def refresh_users_table(self, tree):
        """Обновление таблицы пользователей"""
        for item in tree.get_children():
            tree.delete(item)
        
        users = auth.get_all_users()
        for user in users:
            tree.insert('', 'end', values=(
                user['username'],
                self.get_role_name(user['role']),
                user['full_name'],
                user['created']
            ))
    
    def add_user(self):
        """Добавление нового пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый пользователь")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Логин:", font=('Arial', 10)).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        username_entry = tk.Entry(dialog, font=('Arial', 10), width=25)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Пароль:", font=('Arial', 10)).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        password_entry = tk.Entry(dialog, show="*", font=('Arial', 10), width=25)
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="ФИО:", font=('Arial', 10)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        fullname_entry = tk.Entry(dialog, font=('Arial', 10), width=25)
        fullname_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Роль:", font=('Arial', 10)).grid(row=3, column=0, sticky='e', padx=10, pady=10)
        role_var = tk.StringVar(value='client')
        roles_frame = tk.Frame(dialog)
        roles_frame.grid(row=3, column=1, sticky='w', padx=10, pady=10)
        
        tk.Radiobutton(roles_frame, text="Клиент", variable=role_var, value='client').pack(anchor='w')
        tk.Radiobutton(roles_frame, text="Менеджер", variable=role_var, value='manager').pack(anchor='w')
        tk.Radiobutton(roles_frame, text="Администратор", variable=role_var, value='administrator').pack(anchor='w')
        
        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            role = role_var.get()
            
            if not username or not password or not fullname:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = auth.register_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(dialog, text="Сохранить", command=save_user, width=15).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_user(self):
        """Удаление пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Удалить пользователя")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Выберите пользователя:", font=('Arial', 10)).pack(pady=10)
        
        users = auth.get_all_users()
        usernames = [u['username'] for u in users]
        
        selected = tk.StringVar()
        combo = ttk.Combobox(dialog, textvariable=selected, values=usernames, state='readonly', width=25)
        combo.pack(pady=10)
        
        def do_delete():
            username = selected.get()
            if not username:
                messagebox.showerror("Ошибка", "Выберите пользователя")
                return
            
            if username == auth.get_current_user()['username']:
                messagebox.showerror("Ошибка", "Нельзя удалить текущего пользователя")
                return
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                auth.delete_user(username)
                messagebox.showinfo("Успех", "Пользователь удален")
                dialog.destroy()
        
        tk.Button(dialog, text="Удалить", command=do_delete, width=15).pack(pady=10)
    
    # УПРАВЛЕНИЕ ТУРАМИ
    def create_tours_tab(self):
        """Вкладка управления турами"""
        frame = tk.Frame(self.root)
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text="Добавить тур", command=self.add_tour).pack(side='left', padx=5)
        tk.Button(toolbar, text="Редактировать", command=lambda: self.edit_tour(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Удалить", command=lambda: self.delete_tour(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.refresh_tours_table(tree)).pack(side='left', padx=5)
        
        columns = ('ID', 'Название', 'Страна', 'Дней', 'Цена', 'Доступен')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        widths = [50, 250, 150, 80, 100, 100]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=5)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_tours_table(tree)
        
        return frame
    
    def refresh_tours_table(self, tree):
        """Обновление таблицы туров"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        for tour in data['tours']:
            tree.insert('', 'end', values=(
                tour['id'],
                tour['name'],
                tour['country'],
                tour['duration'],
                f"{tour['price']:,} ₽",
                "Да" if tour['available'] else "Нет"
            ))
    
    def add_tour(self):
        """Добавление нового тура"""
        self.tour_dialog(None)
    
    def edit_tour(self, tree):
        """Редактирование тура"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите тур")
            return
        
        tour_id = int(tree.item(selected[0])['values'][0])
        data = self.load_data()
        tour = next((t for t in data['tours'] if t['id'] == tour_id), None)
        
        if tour:
            self.tour_dialog(tour)
    
    def delete_tour(self, tree):
        """Удаление тура"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите тур")
            return
        
        tour_id = int(tree.item(selected[0])['values'][0])
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный тур?"):
            data = self.load_data()
            data['tours'] = [t for t in data['tours'] if t['id'] != tour_id]
            self.save_data(data)
            self.refresh_tours_table(tree)
            messagebox.showinfo("Успех", "Тур удален")
    
    def tour_dialog(self, tour=None):
        """Диалог создания/редактирования тура"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование тура" if tour else "Новый тур")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Название:", font=('Arial', 10)).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        name_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Страна:", font=('Arial', 10)).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        country_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        country_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Длительность (дн):", font=('Arial', 10)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        duration_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        duration_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Цена (₽):", font=('Arial', 10)).grid(row=3, column=0, sticky='e', padx=10, pady=10)
        price_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        price_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Описание:", font=('Arial', 10)).grid(row=4, column=0, sticky='ne', padx=10, pady=10)
        desc_text = tk.Text(dialog, font=('Arial', 10), width=30, height=5)
        desc_text.grid(row=4, column=1, padx=10, pady=10)
        
        available_var = tk.BooleanVar(value=True)
        tk.Checkbutton(dialog, text="Доступен для бронирования", variable=available_var, font=('Arial', 10)).grid(row=5, column=0, columnspan=2, pady=10)
        
        if tour:
            name_entry.insert(0, tour['name'])
            country_entry.insert(0, tour['country'])
            duration_entry.insert(0, tour['duration'])
            price_entry.insert(0, tour['price'])
            desc_text.insert('1.0', tour['description'])
            available_var.set(tour['available'])
        
        def save_tour():
            name = name_entry.get().strip()
            country = country_entry.get().strip()
            duration = duration_entry.get().strip()
            price = price_entry.get().strip()
            description = desc_text.get('1.0', 'end').strip()
            
            if not all([name, country, duration, price, description]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                duration = int(duration)
                price = int(price)
            except ValueError:
                messagebox.showerror("Ошибка", "Длительность и цена должны быть числами")
                return
            
            data = self.load_data()
            
            if tour:
                for t in data['tours']:
                    if t['id'] == tour['id']:
                        t['name'] = name
                        t['country'] = country
                        t['duration'] = duration
                        t['price'] = price
                        t['description'] = description
                        t['available'] = available_var.get()
                        break
            else:
                new_id = max([t['id'] for t in data['tours']], default=0) + 1
                data['tours'].append({
                    'id': new_id,
                    'name': name,
                    'country': country,
                    'duration': duration,
                    'price': price,
                    'description': description,
                    'available': available_var.get()
                })
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Тур сохранен")
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_tour, width=15).grid(row=6, column=0, columnspan=2, pady=20)
    
    # УПРАВЛЕНИЕ КЛИЕНТАМИ
    def create_clients_tab(self):
        """Вкладка управления клиентами"""
        frame = tk.Frame(self.root)
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text="Добавить клиента", command=self.add_client).pack(side='left', padx=5)
        tk.Button(toolbar, text="Редактировать", command=lambda: self.edit_client(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Удалить", command=lambda: self.delete_client(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.refresh_clients_table(tree)).pack(side='left', padx=5)
        
        columns = ('ID', 'ФИО', 'Телефон', 'Email', 'Паспорт')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        widths = [50, 250, 150, 200, 150]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=5)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_clients_table(tree)
        
        return frame
    
    def refresh_clients_table(self, tree):
        """Обновление таблицы клиентов"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        for client in data['clients']:
            tree.insert('', 'end', values=(
                client['id'],
                client['full_name'],
                client['phone'],
                client['email'],
                client['passport']
            ))
    
    def add_client(self):
        """Добавление клиента"""
        self.client_dialog(None)
    
    def edit_client(self, tree):
        """Редактирование клиента"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите клиента")
            return
        
        client_id = int(tree.item(selected[0])['values'][0])
        data = self.load_data()
        client = next((c for c in data['clients'] if c['id'] == client_id), None)
        
        if client:
            self.client_dialog(client)
    
    def delete_client(self, tree):
        """Удаление клиента"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите клиента")
            return
        
        client_id = int(tree.item(selected[0])['values'][0])
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранного клиента?"):
            data = self.load_data()
            data['clients'] = [c for c in data['clients'] if c['id'] != client_id]
            self.save_data(data)
            self.refresh_clients_table(tree)
            messagebox.showinfo("Успех", "Клиент удален")
    
    def client_dialog(self, client=None):
        """Диалог создания/редактирования клиента"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование клиента" if client else "Новый клиент")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="ФИО:", font=('Arial', 10)).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        name_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Телефон:", font=('Arial', 10)).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        phone_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Email:", font=('Arial', 10)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        email_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Паспорт:", font=('Arial', 10)).grid(row=3, column=0, sticky='e', padx=10, pady=10)
        passport_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        passport_entry.grid(row=3, column=1, padx=10, pady=10)
        
        if client:
            name_entry.insert(0, client['full_name'])
            phone_entry.insert(0, client['phone'])
            email_entry.insert(0, client['email'])
            passport_entry.insert(0, client['passport'])
        
        def save_client():
            full_name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            passport = passport_entry.get().strip()
            
            if not all([full_name, phone, email, passport]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            data = self.load_data()
            
            if client:
                for c in data['clients']:
                    if c['id'] == client['id']:
                        c['full_name'] = full_name
                        c['phone'] = phone
                        c['email'] = email
                        c['passport'] = passport
                        break
            else:
                new_id = max([c['id'] for c in data['clients']], default=0) + 1
                data['clients'].append({
                    'id': new_id,
                    'full_name': full_name,
                    'phone': phone,
                    'email': email,
                    'passport': passport
                })
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Клиент сохранен")
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_client, width=15).grid(row=4, column=0, columnspan=2, pady=20)
    
    # УПРАВЛЕНИЕ БРОНИРОВАНИЯМИ
    def create_bookings_tab(self):
        """Вкладка управления бронированиями"""
        frame = tk.Frame(self.root)
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text="Новое бронирование", command=self.add_booking).pack(side='left', padx=5)
        tk.Button(toolbar, text="Изменить статус", command=lambda: self.change_booking_status(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Удалить", command=lambda: self.delete_booking(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.refresh_bookings_table(tree)).pack(side='left', padx=5)
        
        columns = ('ID', 'Тур', 'Клиент', 'Дата бронир.', 'Дата тура', 'Персон', 'Сумма', 'Статус')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        widths = [40, 150, 150, 100, 100, 60, 100, 100]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=5)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_bookings_table(tree)
        
        return frame
    
    def refresh_bookings_table(self, tree):
        """Обновление таблицы бронирований"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        for booking in data['bookings']:
            tour = next((t for t in data['tours'] if t['id'] == booking['tour_id']), None)
            client = next((c for c in data['clients'] if c['id'] == booking['client_id']), None)
            
            tree.insert('', 'end', values=(
                booking['id'],
                tour['name'] if tour else 'Не найден',
                client['full_name'] if client else 'Не найден',
                booking['booking_date'],
                booking['travel_date'],
                booking['persons'],
                f"{booking['total_price']:,} ₽",
                self.get_status_name(booking['status'])
            ))
    
    def get_status_name(self, status):
        """Получение названия статуса на русском"""
        statuses = {
            'pending': 'Ожидает',
            'confirmed': 'Подтвержден',
            'cancelled': 'Отменен',
            'completed': 'Завершен'
        }
        return statuses.get(status, status)
    
    def add_booking(self):
        """Добавление бронирования"""
        self.booking_dialog(None)
    
    def delete_booking(self, tree):
        """Удаление бронирования"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите бронирование")
            return
        
        booking_id = int(tree.item(selected[0])['values'][0])
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранное бронирование?"):
            data = self.load_data()
            data['bookings'] = [b for b in data['bookings'] if b['id'] != booking_id]
            self.save_data(data)
            self.refresh_bookings_table(tree)
            messagebox.showinfo("Успех", "Бронирование удалено")
    
    def change_booking_status(self, tree):
        """Изменение статуса бронирования"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите бронирование")
            return
        
        booking_id = int(tree.item(selected[0])['values'][0])
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменение статуса")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Выберите новый статус:", font=('Arial', 10)).pack(pady=10)
        
        status_var = tk.StringVar(value='pending')
        
        tk.Radiobutton(dialog, text="Ожидает подтверждения", variable=status_var, value='pending').pack(anchor='w', padx=50)
        tk.Radiobutton(dialog, text="Подтвержден", variable=status_var, value='confirmed').pack(anchor='w', padx=50)
        tk.Radiobutton(dialog, text="Отменен", variable=status_var, value='cancelled').pack(anchor='w', padx=50)
        tk.Radiobutton(dialog, text="Завершен", variable=status_var, value='completed').pack(anchor='w', padx=50)
        
        def save_status():
            data = self.load_data()
            for booking in data['bookings']:
                if booking['id'] == booking_id:
                    booking['status'] = status_var.get()
                    break
            
            self.save_data(data)
            self.refresh_bookings_table(tree)
            messagebox.showinfo("Успех", "Статус изменен")
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_status, width=15).pack(pady=20)
    
    def booking_dialog(self, booking=None):
        """Диалог создания бронирования"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новое бронирование")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        
        data = self.load_data()
        
        tk.Label(dialog, text="Тур:", font=('Arial', 10)).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        tour_var = tk.StringVar()
        tours_list = [f"{t['id']} - {t['name']}" for t in data['tours'] if t['available']]
        tour_combo = ttk.Combobox(dialog, textvariable=tour_var, values=tours_list, state='readonly', width=27)
        tour_combo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Клиент:", font=('Arial', 10)).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        client_var = tk.StringVar()
        clients_list = [f"{c['id']} - {c['full_name']}" for c in data['clients']]
        client_combo = ttk.Combobox(dialog, textvariable=client_var, values=clients_list, state='readonly', width=27)
        client_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Дата поездки:", font=('Arial', 10)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        date_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        date_entry.insert(0, "2024-03-01")
        date_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Кол-во персон:", font=('Arial', 10)).grid(row=3, column=0, sticky='e', padx=10, pady=10)
        persons_entry = tk.Entry(dialog, font=('Arial', 10), width=30)
        persons_entry.insert(0, "1")
        persons_entry.grid(row=3, column=1, padx=10, pady=10)
        
        total_label = tk.Label(dialog, text="Итого: 0 ₽", font=('Arial', 11, 'bold'))
        total_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        def calculate_total(*args):
            try:
                tour_id = int(tour_var.get().split(' - ')[0])
                persons = int(persons_entry.get())
                
                tour = next((t for t in data['tours'] if t['id'] == tour_id), None)
                if tour:
                    total = tour['price'] * persons
                    total_label.config(text=f"Итого: {total:,} ₽")
            except:
                pass
        
        tour_var.trace('w', calculate_total)
        persons_entry.bind('<KeyRelease>', calculate_total)
        
        def save_booking():
            if not tour_var.get() or not client_var.get():
                messagebox.showerror("Ошибка", "Выберите тур и клиента")
                return
            
            try:
                tour_id = int(tour_var.get().split(' - ')[0])
                client_id = int(client_var.get().split(' - ')[0])
                persons = int(persons_entry.get())
                travel_date = date_entry.get().strip()
                
                tour = next((t for t in data['tours'] if t['id'] == tour_id), None)
                total_price = tour['price'] * persons
                
                new_id = max([b['id'] for b in data['bookings']], default=0) + 1
                
                current_user = auth.get_current_user()
                
                data['bookings'].append({
                    'id': new_id,
                    'tour_id': tour_id,
                    'client_id': client_id,
                    'client_username': current_user['username'],
                    'booking_date': datetime.now().strftime("%Y-%m-%d"),
                    'travel_date': travel_date,
                    'persons': persons,
                    'total_price': total_price,
                    'status': 'pending'
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Бронирование создано")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при создании: {str(e)}")
        
        tk.Button(dialog, text="Создать бронирование", command=save_booking, width=20).grid(row=5, column=0, columnspan=2, pady=20)
    
    # ОТЧЕТЫ
    def create_reports_tab(self):
        """Вкладка отчетов"""
        frame = tk.Frame(self.root)
        
        tk.Label(frame, text="Статистика системы", font=('Arial', 16, 'bold')).pack(pady=20)
        
        stats_frame = tk.Frame(frame)
        stats_frame.pack(pady=20)
        
        data = self.load_data()
        users = auth.get_all_users()
        
        stats = [
            ("Всего пользователей:", len(users)),
            ("Всего туров:", len(data['tours'])),
            ("Доступных туров:", len([t for t in data['tours'] if t['available']])),
            ("Всего клиентов:", len(data['clients'])),
            ("Всего бронирований:", len(data['bookings'])),
            ("Подтвержденных бронирований:", len([b for b in data['bookings'] if b['status'] == 'confirmed'])),
            ("Общая сумма бронирований:", f"{sum([b['total_price'] for b in data['bookings']]):,} ₽"),
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 12), anchor='w', width=30).grid(row=i, column=0, sticky='w', padx=20, pady=5)
            tk.Label(stats_frame, text=str(value), font=('Arial', 12, 'bold'), anchor='e', width=20).grid(row=i, column=1, sticky='e', padx=20, pady=5)
        
        return frame
    
    # ПАНЕЛЬ МЕНЕДЖЕРА
    def show_manager_panel(self):
        """Панель менеджера"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        notebook.add(self.create_tours_tab(), text="Туры")
        notebook.add(self.create_clients_tab(), text="Клиенты")
        notebook.add(self.create_bookings_tab(), text="Бронирования")
    
    # ПАНЕЛЬ КЛИЕНТА
    def show_client_panel(self):
        """Панель клиента"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        notebook.add(self.create_client_tours_view(), text="Доступные туры")
        notebook.add(self.create_client_bookings_view(), text="Мои бронирования")
    
    def create_client_tours_view(self):
        """Просмотр туров для клиента"""
        frame = tk.Frame(self.root)
        
        tk.Label(frame, text="Доступные туры", font=('Arial', 14, 'bold')).pack(pady=10)
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text="Забронировать выбранный тур", command=lambda: self.client_book_tour(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.refresh_client_tours_table(tree)).pack(side='left', padx=5)
        
        columns = ('ID', 'Название', 'Страна', 'Дней', 'Цена', 'Описание')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=18)
        
        widths = [50, 200, 120, 80, 100, 300]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=5)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_client_tours_table(tree)
        
        return frame
    
    def refresh_client_tours_table(self, tree):
        """Обновление таблицы туров для клиента"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        for tour in data['tours']:
            if tour['available']:
                tree.insert('', 'end', values=(
                    tour['id'],
                    tour['name'],
                    tour['country'],
                    tour['duration'],
                    f"{tour['price']:,} ₽",
                    tour['description']
                ))
    
    def client_book_tour(self, tree):
        """Клиент бронирует тур"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите тур")
            return
        
        tour_id = int(tree.item(selected[0])['values'][0])
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Бронирование тура")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        data = self.load_data()
        tour = next((t for t in data['tours'] if t['id'] == tour_id), None)
        
        tk.Label(dialog, text=f"Тур: {tour['name']}", font=('Arial', 12, 'bold')).pack(pady=10)
        tk.Label(dialog, text=f"Цена: {tour['price']:,} ₽ за человека", font=('Arial', 10)).pack(pady=5)
        
        tk.Label(dialog, text="Дата поездки (ГГГГ-ММ-ДД):", font=('Arial', 10)).pack(pady=10)
        date_entry = tk.Entry(dialog, font=('Arial', 10), width=25)
        date_entry.insert(0, "2024-03-01")
        date_entry.pack()
        
        tk.Label(dialog, text="Количество персон:", font=('Arial', 10)).pack(pady=10)
        persons_entry = tk.Entry(dialog, font=('Arial', 10), width=25)
        persons_entry.insert(0, "1")
        persons_entry.pack()
        
        total_label = tk.Label(dialog, text=f"Итого: {tour['price']:,} ₽", font=('Arial', 12, 'bold'))
        total_label.pack(pady=15)
        
        def update_total(*args):
            try:
                persons = int(persons_entry.get())
                total = tour['price'] * persons
                total_label.config(text=f"Итого: {total:,} ₽")
            except:
                pass
        
        persons_entry.bind('<KeyRelease>', update_total)
        
        def create_booking():
            try:
                persons = int(persons_entry.get())
                travel_date = date_entry.get().strip()
                
                current_user = auth.get_current_user()
                
                # Найти клиента по username
                client = next((c for c in data['clients'] if c.get('username') == current_user['username']), None)
                
                if not client:
                    # Создать нового клиента
                    new_client_id = max([c['id'] for c in data['clients']], default=0) + 1
                    client = {
                        'id': new_client_id,
                        'full_name': current_user['full_name'],
                        'phone': '+7-000-000-00-00',
                        'email': 'client@example.com',
                        'passport': '0000 000000',
                        'username': current_user['username']
                    }
                    data['clients'].append(client)
                
                total_price = tour['price'] * persons
                new_id = max([b['id'] for b in data['bookings']], default=0) + 1
                
                data['bookings'].append({
                    'id': new_id,
                    'tour_id': tour_id,
                    'client_id': client['id'],
                    'client_username': current_user['username'],
                    'booking_date': datetime.now().strftime("%Y-%m-%d"),
                    'travel_date': travel_date,
                    'persons': persons,
                    'total_price': total_price,
                    'status': 'pending'
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Бронирование создано! Ожидайте подтверждения менеджера.")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при создании: {str(e)}")
        
        tk.Button(dialog, text="Забронировать", command=create_booking, width=20).pack(pady=10)
    
    def create_client_bookings_view(self):
        """Просмотр своих бронирований для клиента"""
        frame = tk.Frame(self.root)
        
        tk.Label(frame, text="Мои бронирования", font=('Arial', 14, 'bold')).pack(pady=10)
        
        toolbar = tk.Frame(frame)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        tk.Button(toolbar, text="Отменить бронирование", command=lambda: self.client_cancel_booking(tree)).pack(side='left', padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.refresh_client_bookings_table(tree)).pack(side='left', padx=5)
        
        columns = ('ID', 'Тур', 'Дата брониров.', 'Дата поездки', 'Персон', 'Сумма', 'Статус')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=18)
        
        widths = [50, 200, 120, 120, 80, 120, 120]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True, padx=5)
        scrollbar.pack(side='right', fill='y')
        
        self.refresh_client_bookings_table(tree)
        
        return frame
    
    def refresh_client_bookings_table(self, tree):
        """Обновление таблицы бронирований клиента"""
        for item in tree.get_children():
            tree.delete(item)
        
        current_user = auth.get_current_user()
        data = self.load_data()
        
        for booking in data['bookings']:
            if booking.get('client_username') == current_user['username']:
                tour = next((t for t in data['tours'] if t['id'] == booking['tour_id']), None)
                
                tree.insert('', 'end', values=(
                    booking['id'],
                    tour['name'] if tour else 'Не найден',
                    booking['booking_date'],
                    booking['travel_date'],
                    booking['persons'],
                    f"{booking['total_price']:,} ₽",
                    self.get_status_name(booking['status'])
                ))
    
    def client_cancel_booking(self, tree):
        """Клиент отменяет бронирование"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите бронирование")
            return
        
        booking_id = int(tree.item(selected[0])['values'][0])
        
        if messagebox.askyesno("Подтверждение", "Отменить выбранное бронирование?"):
            data = self.load_data()
            for booking in data['bookings']:
                if booking['id'] == booking_id:
                    booking['status'] = 'cancelled'
                    break
            
            self.save_data(data)
            self.refresh_client_bookings_table(tree)
            messagebox.showinfo("Успех", "Бронирование отменено")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TouristAgencyApp()
    app.run()