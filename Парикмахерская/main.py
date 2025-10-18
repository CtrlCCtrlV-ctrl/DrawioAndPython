import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

DATA_FILE = 'data.json'

class HairdresserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система - Парикмахерская")
        self.root.geometry("900x600")
        
        # Инициализация данных
        # Файлы уже созданы с тестовыми данными
        
        # Показываем окно входа
        self.show_login()
    
    
    def load_data(self):
        """Загрузка данных из файла"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно входа в систему"""
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Информационная система", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(frame, text="ПАРИКМАХЕРСКАЯ", font=('Arial', 14)).grid(row=1, column=0, columnspan=2, pady=5)
        
        tk.Label(frame, text="Логин:", font=('Arial', 11)).grid(row=2, column=0, sticky='e', padx=5, pady=10)
        login_entry = tk.Entry(frame, font=('Arial', 11), width=20)
        login_entry.grid(row=2, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 11)).grid(row=3, column=0, sticky='e', padx=5, pady=10)
        password_entry = tk.Entry(frame, show="*", font=('Arial', 11), width=20)
        password_entry.grid(row=3, column=1, pady=10)
        
        def do_login():
            username = login_entry.get()
            password = password_entry.get()
            
            user = auth.authenticate(username, password)
            if user:
                auth.Session.login(user)
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=do_login, font=('Arial', 11), width=15, bg='#4CAF50', fg='white').grid(row=4, column=0, columnspan=2, pady=20)
        
        # Подсказка
        hint_text = "Подсказка:\nadmin/admin123\nmaster1/master123\nclient1/client123"
        tk.Label(frame, text=hint_text, font=('Arial', 9), fg='gray', justify='left').grid(row=5, column=0, columnspan=2)
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        role = auth.Session.get_role()
        user_name = auth.Session.current_user.get('full_name', 'Пользователь')
        
        # Шапка
        header = tk.Frame(self.root, bg='#2196F3', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Парикмахерская | {user_name} ({role})", 
                bg='#2196F3', fg='white', font=('Arial', 14, 'bold')).pack(side='left', padx=20, pady=15)
        
        tk.Button(header, text="Выход", command=self.logout, 
                 bg='#f44336', fg='white', font=('Arial', 10)).pack(side='right', padx=20)
        
        # Контейнер для меню
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if role == 'administrator':
            self.show_admin_menu(menu_frame)
        elif role == 'master':
            self.show_master_menu(menu_frame)
        elif role == 'client':
            self.show_client_menu(menu_frame)
    
    def logout(self):
        """Выход из системы"""
        auth.Session.logout()
        self.show_login()
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons = [
            ("Управление пользователями", self.manage_users),
            ("Управление мастерами", self.manage_masters),
            ("Управление услугами", self.manage_services),
            ("Просмотр всех записей", self.view_all_appointments),
            ("Просмотр отчетов", self.view_reports)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, command=command, 
                     font=('Arial', 12), width=30, height=2, bg='#e3f2fd').pack(pady=5)
    
    def show_master_menu(self, parent):
        """Меню мастера"""
        tk.Label(parent, text="Панель мастера", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons = [
            ("Мое расписание", self.view_my_schedule),
            ("Управление записями", self.manage_appointments),
            ("Просмотр клиентов", self.view_clients),
            ("Отметить выполненные услуги", self.mark_completed)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, command=command, 
                     font=('Arial', 12), width=30, height=2, bg='#c8e6c9').pack(pady=5)
    
    def show_client_menu(self, parent):
        """Меню клиента"""
        tk.Label(parent, text="Личный кабинет клиента", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons = [
            ("Просмотр услуг", self.view_services),
            ("Записаться на прием", self.create_appointment),
            ("Мои записи", self.view_my_appointments),
            ("Отменить запись", self.cancel_appointment)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, command=command, 
                     font=('Arial', 12), width=30, height=2, bg='#fff9c4').pack(pady=5)
    
    # ========== ФУНКЦИИ АДМИНИСТРАТОРА ==========
    
    def manage_users(self):
        """Управление пользователями"""
        win = tk.Toplevel(self.root)
        win.title("Управление пользователями")
        win.geometry("800x500")
        
        # Таблица пользователей
        columns = ('username', 'role', 'full_name', 'created')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        tree.heading('username', text='Логин')
        tree.heading('role', text='Роль')
        tree.heading('full_name', text='ФИО')
        tree.heading('created', text='Дата создания')
        
        tree.column('username', width=150)
        tree.column('role', width=120)
        tree.column('full_name', width=200)
        tree.column('created', width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            for user in auth.get_all_users():
                tree.insert('', 'end', values=(
                    user['username'],
                    user['role'],
                    user.get('full_name', ''),
                    user.get('created', '')
                ))
        
        def add_user():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить пользователя")
            add_win.geometry("400x300")
            
            tk.Label(add_win, text="Логин:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            username_entry = tk.Entry(add_win, width=25)
            username_entry.grid(row=0, column=1, pady=5)
            
            tk.Label(add_win, text="Пароль:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            password_entry = tk.Entry(add_win, show="*", width=25)
            password_entry.grid(row=1, column=1, pady=5)
            
            tk.Label(add_win, text="ФИО:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            fullname_entry = tk.Entry(add_win, width=25)
            fullname_entry.grid(row=2, column=1, pady=5)
            
            tk.Label(add_win, text="Роль:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
            role_var = tk.StringVar(value="client")
            roles = [("Администратор", "administrator"), ("Мастер", "master"), ("Клиент", "client")]
            for i, (text, value) in enumerate(roles):
                tk.Radiobutton(add_win, text=text, variable=role_var, value=value).grid(row=4+i, column=1, sticky='w')
            
            def save():
                success, msg = auth.create_user(
                    username_entry.get(),
                    password_entry.get(),
                    role_var.get(),
                    fullname_entry.get()
                )
                if success:
                    messagebox.showinfo("Успех", msg)
                    add_win.destroy()
                    refresh()
                else:
                    messagebox.showerror("Ошибка", msg)
            
            tk.Button(add_win, text="Сохранить", command=save, bg='#4CAF50', fg='white').grid(row=7, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            item = tree.item(selected[0])
            username = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                auth.delete_user(username)
                refresh()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_user, width=15, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, width=15, bg='#f44336', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh, width=15, bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        refresh()
    
    def manage_masters(self):
        """Управление мастерами"""
        win = tk.Toplevel(self.root)
        win.title("Управление мастерами")
        win.geometry("700x500")
        
        columns = ('id', 'name', 'specialization', 'phone')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='ID')
        tree.heading('name', text='ФИО')
        tree.heading('specialization', text='Специализация')
        tree.heading('phone', text='Телефон')
        
        tree.column('id', width=50)
        tree.column('name', width=200)
        tree.column('specialization', width=150)
        tree.column('phone', width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            data = self.load_data()
            for master in data['masters']:
                tree.insert('', 'end', values=(
                    master['id'],
                    master['name'],
                    master['specialization'],
                    master['phone']
                ))
        
        def add_master():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить мастера")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="ФИО:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
            name_entry = tk.Entry(add_win, width=25)
            name_entry.grid(row=0, column=1, pady=10)
            
            tk.Label(add_win, text="Специализация:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
            spec_entry = tk.Entry(add_win, width=25)
            spec_entry.grid(row=1, column=1, pady=10)
            
            tk.Label(add_win, text="Телефон:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
            phone_entry = tk.Entry(add_win, width=25)
            phone_entry.grid(row=2, column=1, pady=10)
            
            def save():
                data = self.load_data()
                new_id = max([m['id'] for m in data['masters']], default=0) + 1
                data['masters'].append({
                    'id': new_id,
                    'name': name_entry.get(),
                    'specialization': spec_entry.get(),
                    'phone': phone_entry.get()
                })
                self.save_data(data)
                messagebox.showinfo("Успех", "Мастер добавлен")
                add_win.destroy()
                refresh()
            
            tk.Button(add_win, text="Сохранить", command=save, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        def delete_master():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите мастера")
                return
            
            item = tree.item(selected[0])
            master_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить мастера?"):
                data = self.load_data()
                data['masters'] = [m for m in data['masters'] if m['id'] != master_id]
                self.save_data(data)
                refresh()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_master, width=15, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_master, width=15, bg='#f44336', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh, width=15, bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        refresh()
    
    def manage_services(self):
        """Управление услугами"""
        win = tk.Toplevel(self.root)
        win.title("Управление услугами")
        win.geometry("800x500")
        
        columns = ('id', 'name', 'description', 'price', 'duration')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='ID')
        tree.heading('name', text='Название')
        tree.heading('description', text='Описание')
        tree.heading('price', text='Цена')
        tree.heading('duration', text='Длительность (мин)')
        
        tree.column('id', width=50)
        tree.column('name', width=150)
        tree.column('description', width=250)
        tree.column('price', width=100)
        tree.column('duration', width=120)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            data = self.load_data()
            for service in data['services']:
                tree.insert('', 'end', values=(
                    service['id'],
                    service['name'],
                    service['description'],
                    service['price'],
                    service['duration']
                ))
        
        def add_service():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить услугу")
            add_win.geometry("400x300")
            
            tk.Label(add_win, text="Название:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
            name_entry = tk.Entry(add_win, width=25)
            name_entry.grid(row=0, column=1, pady=10)
            
            tk.Label(add_win, text="Описание:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
            desc_entry = tk.Entry(add_win, width=25)
            desc_entry.grid(row=1, column=1, pady=10)
            
            tk.Label(add_win, text="Цена:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
            price_entry = tk.Entry(add_win, width=25)
            price_entry.grid(row=2, column=1, pady=10)
            
            tk.Label(add_win, text="Длительность (мин):").grid(row=3, column=0, padx=10, pady=10, sticky='e')
            duration_entry = tk.Entry(add_win, width=25)
            duration_entry.grid(row=3, column=1, pady=10)
            
            def save():
                data = self.load_data()
                new_id = max([s['id'] for s in data['services']], default=0) + 1
                data['services'].append({
                    'id': new_id,
                    'name': name_entry.get(),
                    'description': desc_entry.get(),
                    'price': int(price_entry.get()),
                    'duration': int(duration_entry.get())
                })
                self.save_data(data)
                messagebox.showinfo("Успех", "Услуга добавлена")
                add_win.destroy()
                refresh()
            
            tk.Button(add_win, text="Сохранить", command=save, bg='#4CAF50', fg='white').grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_service():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите услугу")
                return
            
            item = tree.item(selected[0])
            service_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить услугу?"):
                data = self.load_data()
                data['services'] = [s for s in data['services'] if s['id'] != service_id]
                self.save_data(data)
                refresh()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_service, width=15, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_service, width=15, bg='#f44336', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh, width=15, bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        refresh()
    
    def view_all_appointments(self):
        """Просмотр всех записей"""
        win = tk.Toplevel(self.root)
        win.title("Все записи")
        win.geometry("900x500")
        
        columns = ('id', 'client', 'master', 'service', 'date', 'time', 'status')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        tree.heading('id', text='ID')
        tree.heading('client', text='Клиент')
        tree.heading('master', text='Мастер')
        tree.heading('service', text='Услуга')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('status', text='Статус')
        
        for col in columns:
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self.load_data()
        for appt in data['appointments']:
            client = next((c['name'] for c in data['clients'] if c['id'] == appt['client_id']), 'N/A')
            master = next((m['name'] for m in data['masters'] if m['id'] == appt['master_id']), 'N/A')
            service = next((s['name'] for s in data['services'] if s['id'] == appt['service_id']), 'N/A')
            
            tree.insert('', 'end', values=(
                appt['id'],
                client,
                master,
                service,
                appt['date'],
                appt['time'],
                appt['status']
            ))
    
    def view_reports(self):
        """Просмотр отчетов"""
        win = tk.Toplevel(self.root)
        win.title("Отчеты")
        win.geometry("600x400")
        
        data = self.load_data()
        
        # Статистика
        total_appointments = len(data['appointments'])
        total_masters = len(data['masters'])
        total_clients = len(data['clients'])
        total_services = len(data['services'])
        
        completed = len([a for a in data['appointments'] if a['status'] == 'Выполнена'])
        planned = len([a for a in data['appointments'] if a['status'] == 'Запланирована'])
        
        report_text = f"""
        ОТЧЕТ ПО СИСТЕМЕ
        =====================================
        
        Общая статистика:
        - Всего записей: {total_appointments}
        - Выполнено: {completed}
        - Запланировано: {planned}
        
        Ресурсы:
        - Мастеров: {total_masters}
        - Клиентов: {total_clients}
        - Услуг: {total_services}
        
        =====================================
        Дата формирования: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        text_widget = tk.Text(win, font=('Courier', 11), wrap='word')
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)
        text_widget.insert('1.0', report_text)
        text_widget.config(state='disabled')
    
    # ========== ФУНКЦИИ МАСТЕРА ==========
    
    def view_my_schedule(self):
        """Расписание мастера"""
        win = tk.Toplevel(self.root)
        win.title("Мое расписание")
        win.geometry("800x500")
        
        master_id = auth.Session.current_user.get('master_id')
        
        columns = ('id', 'client', 'service', 'date', 'time', 'status')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        tree.heading('id', text='ID')
        tree.heading('client', text='Клиент')
        tree.heading('service', text='Услуга')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('status', text='Статус')
        
        for col in columns:
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self.load_data()
        for appt in data['appointments']:
            if appt['master_id'] == master_id:
                client = next((c['name'] for c in data['clients'] if c['id'] == appt['client_id']), 'N/A')
                service = next((s['name'] for s in data['services'] if s['id'] == appt['service_id']), 'N/A')
                
                tree.insert('', 'end', values=(
                    appt['id'],
                    client,
                    service,
                    appt['date'],
                    appt['time'],
                    appt['status']
                ))
    
    def manage_appointments(self):
        """Управление записями (для мастера)"""
        self.view_my_schedule()
    
    def view_clients(self):
        """Просмотр клиентов"""
        win = tk.Toplevel(self.root)
        win.title("Клиенты")
        win.geometry("700x500")
        
        columns = ('id', 'name', 'phone', 'email')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        tree.heading('id', text='ID')
        tree.heading('name', text='ФИО')
        tree.heading('phone', text='Телефон')
        tree.heading('email', text='Email')
        
        tree.column('id', width=50)
        tree.column('name', width=200)
        tree.column('phone', width=150)
        tree.column('email', width=200)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self.load_data()
        for client in data['clients']:
            tree.insert('', 'end', values=(
                client['id'],
                client['name'],
                client['phone'],
                client['email']
            ))
    
    def mark_completed(self):
        """Отметить выполненные услуги"""
        win = tk.Toplevel(self.root)
        win.title("Отметить выполненные")
        win.geometry("800x500")
        
        master_id = auth.Session.current_user.get('master_id')
        
        columns = ('id', 'client', 'service', 'date', 'time', 'status')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='ID')
        tree.heading('client', text='Клиент')
        tree.heading('service', text='Услуга')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('status', text='Статус')
        
        for col in columns:
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            
            data = self.load_data()
            for appt in data['appointments']:
                if appt['master_id'] == master_id and appt['status'] == 'Запланирована':
                    client = next((c['name'] for c in data['clients'] if c['id'] == appt['client_id']), 'N/A')
                    service = next((s['name'] for s in data['services'] if s['id'] == appt['service_id']), 'N/A')
                    
                    tree.insert('', 'end', values=(
                        appt['id'],
                        client,
                        service,
                        appt['date'],
                        appt['time'],
                        appt['status']
                    ))
        
        def mark_done():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите запись")
                return
            
            item = tree.item(selected[0])
            appt_id = item['values'][0]
            
            data = self.load_data()
            for appt in data['appointments']:
                if appt['id'] == appt_id:
                    appt['status'] = 'Выполнена'
                    break
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Запись отмечена как выполненная")
            refresh()
        
        tk.Button(win, text="Отметить выполненной", command=mark_done, 
                 width=25, bg='#4CAF50', fg='white').pack(pady=10)
        
        refresh()
    
    # ========== ФУНКЦИИ КЛИЕНТА ==========
    
    def view_services(self):
        """Просмотр услуг"""
        win = tk.Toplevel(self.root)
        win.title("Доступные услуги")
        win.geometry("700x500")
        
        columns = ('name', 'description', 'price', 'duration')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        tree.heading('name', text='Название')
        tree.heading('description', text='Описание')
        tree.heading('price', text='Цена (руб)')
        tree.heading('duration', text='Длительность (мин)')
        
        tree.column('name', width=150)
        tree.column('description', width=250)
        tree.column('price', width=100)
        tree.column('duration', width=120)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self.load_data()
        for service in data['services']:
            tree.insert('', 'end', values=(
                service['name'],
                service['description'],
                service['price'],
                service['duration']
            ))
    
    def create_appointment(self):
        """Создание записи на прием"""
        win = tk.Toplevel(self.root)
        win.title("Записаться на прием")
        win.geometry("450x400")
        
        data = self.load_data()
        client_id = auth.Session.current_user.get('client_id')
        
        tk.Label(win, text="Выберите услугу:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        service_var = tk.StringVar()
        service_combo = ttk.Combobox(win, textvariable=service_var, width=30, state='readonly')
        service_combo['values'] = [f"{s['id']} - {s['name']} ({s['price']} руб)" for s in data['services']]
        service_combo.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(win, text="Выберите мастера:", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        master_var = tk.StringVar()
        master_combo = ttk.Combobox(win, textvariable=master_var, width=30, state='readonly')
        master_combo['values'] = [f"{m['id']} - {m['name']} ({m['specialization']})" for m in data['masters']]
        master_combo.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(win, text="Дата (ГГГГ-ММ-ДД):", font=('Arial', 11)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        date_entry = tk.Entry(win, width=32)
        date_entry.grid(row=2, column=1, pady=10, padx=10)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Label(win, text="Время (ЧЧ:ММ):", font=('Arial', 11)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        time_entry = tk.Entry(win, width=32)
        time_entry.grid(row=3, column=1, pady=10, padx=10)
        time_entry.insert(0, "10:00")
        
        def save_appointment():
            if not service_var.get() or not master_var.get():
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            
            service_id = int(service_var.get().split(' - ')[0])
            master_id = int(master_var.get().split(' - ')[0])
            
            data = self.load_data()
            new_id = max([a['id'] for a in data['appointments']], default=0) + 1
            
            data['appointments'].append({
                'id': new_id,
                'client_id': client_id,
                'master_id': master_id,
                'service_id': service_id,
                'date': date_entry.get(),
                'time': time_entry.get(),
                'status': 'Запланирована'
            })
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Вы успешно записаны!")
            win.destroy()
        
        tk.Button(win, text="Записаться", command=save_appointment, 
                 width=20, bg='#4CAF50', fg='white', font=('Arial', 11)).grid(row=4, column=0, columnspan=2, pady=30)
    
    def view_my_appointments(self):
        """Просмотр своих записей"""
        win = tk.Toplevel(self.root)
        win.title("Мои записи")
        win.geometry("800x500")
        
        client_id = auth.Session.current_user.get('client_id')
        
        columns = ('id', 'master', 'service', 'date', 'time', 'status')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        
        tree.heading('id', text='ID')
        tree.heading('master', text='Мастер')
        tree.heading('service', text='Услуга')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('status', text='Статус')
        
        for col in columns:
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self.load_data()
        for appt in data['appointments']:
            if appt['client_id'] == client_id:
                master = next((m['name'] for m in data['masters'] if m['id'] == appt['master_id']), 'N/A')
                service = next((s['name'] for s in data['services'] if s['id'] == appt['service_id']), 'N/A')
                
                tree.insert('', 'end', values=(
                    appt['id'],
                    master,
                    service,
                    appt['date'],
                    appt['time'],
                    appt['status']
                ))
    
    def cancel_appointment(self):
        """Отмена записи"""
        win = tk.Toplevel(self.root)
        win.title("Отменить запись")
        win.geometry("800x500")
        
        client_id = auth.Session.current_user.get('client_id')
        
        columns = ('id', 'master', 'service', 'date', 'time', 'status')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        tree.heading('id', text='ID')
        tree.heading('master', text='Мастер')
        tree.heading('service', text='Услуга')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('status', text='Статус')
        
        for col in columns:
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            
            data = self.load_data()
            for appt in data['appointments']:
                if appt['client_id'] == client_id and appt['status'] == 'Запланирована':
                    master = next((m['name'] for m in data['masters'] if m['id'] == appt['master_id']), 'N/A')
                    service = next((s['name'] for s in data['services'] if s['id'] == appt['service_id']), 'N/A')
                    
                    tree.insert('', 'end', values=(
                        appt['id'],
                        master,
                        service,
                        appt['date'],
                        appt['time'],
                        appt['status']
                    ))
        
        def cancel():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите запись")
                return
            
            item = tree.item(selected[0])
            appt_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Отменить запись?"):
                data = self.load_data()
                data['appointments'] = [a for a in data['appointments'] if a['id'] != appt_id]
                self.save_data(data)
                messagebox.showinfo("Успех", "Запись отменена")
                refresh()
        
        tk.Button(win, text="Отменить выбранную запись", command=cancel, 
                 width=25, bg='#f44336', fg='white').pack(pady=10)
        
        refresh()


if __name__ == '__main__':
    root = tk.Tk()
    app = HairdresserApp(root)
    root.mainloop()