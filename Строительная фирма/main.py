import tkinter as tk
from tkinter import ttk, messagebox
import json
from auth import AuthManager
from datetime import datetime

class ConstructionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система - Строительная фирма")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.auth = AuthManager()
        self.data_file = 'data.json'
        self.load_data()
        
        self.show_login_screen()
    
    def load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # Экран входа
    def show_login_screen(self):
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Строительная фирма", font=('Arial', 20, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.login_entry = tk.Entry(frame, width=25)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)
        self.login_entry.insert(0, "admin")
        
        tk.Label(frame, text="Пароль:", bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = tk.Entry(frame, show='*', width=25)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        self.password_entry.insert(0, "admin")
        
        tk.Button(frame, text="Войти", command=self.login, width=20, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        info_frame = tk.Frame(self.root, bg='#fff9e6', bd=1, relief='solid')
        info_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        tk.Label(info_frame, text="Тестовые данные: admin/admin, manager/manager, client/client", 
                bg='#fff9e6', font=('Arial', 9)).pack(pady=5)
    
    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        success, role = self.auth.login(username, password)
        
        if success:
            if role == 'administrator':
                self.show_admin_panel()
            elif role == 'manager':
                self.show_manager_panel()
            elif role == 'client':
                self.show_client_panel()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    # Панель администратора
    def show_admin_panel(self):
        self.clear_window()
        
        header = tk.Frame(self.root, bg='#2196F3', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Администратор: {self.auth.current_user['full_name']}", 
                bg='#2196F3', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=20, pady=15)
        
        tk.Button(header, text="Выход", command=self.logout, bg='#f44336', fg='white').pack(side='right', padx=20, pady=15)
        
        menu_frame = tk.Frame(self.root, bg='#e3f2fd', width=200)
        menu_frame.pack(side='left', fill='y')
        
        buttons = [
            ("Управление пользователями", self.show_users_management),
            ("Просмотр проектов", self.show_projects),
            ("Просмотр сотрудников", self.show_employees),
            ("Просмотр материалов", self.show_materials),
            ("Просмотр заявок", self.show_requests),
            ("Отчеты", self.show_reports),
            ("Резервное копирование", self.backup_data)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, width=25, bg='white', 
                     anchor='w', padx=10, pady=10).pack(pady=2, padx=5)
        
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        tk.Label(self.content_frame, text="Добро пожаловать в систему управления!", 
                font=('Arial', 16), bg='white').pack(pady=50)
    
    # Панель менеджера
    def show_manager_panel(self):
        self.clear_window()
        
        header = tk.Frame(self.root, bg='#FF9800', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Менеджер: {self.auth.current_user['full_name']}", 
                bg='#FF9800', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=20, pady=15)
        
        tk.Button(header, text="Выход", command=self.logout, bg='#f44336', fg='white').pack(side='right', padx=20, pady=15)
        
        menu_frame = tk.Frame(self.root, bg='#fff3e0', width=200)
        menu_frame.pack(side='left', fill='y')
        
        buttons = [
            ("Управление проектами", self.manage_projects),
            ("Управление сотрудниками", self.manage_employees),
            ("Управление материалами", self.manage_materials),
            ("Назначение работников", self.assign_workers),
            ("Отслеживание прогресса", self.track_progress),
            ("Отчеты", self.show_reports)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, width=25, bg='white', 
                     anchor='w', padx=10, pady=10).pack(pady=2, padx=5)
        
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        tk.Label(self.content_frame, text="Панель управления проектами", 
                font=('Arial', 16), bg='white').pack(pady=50)
    
    # Панель клиента
    def show_client_panel(self):
        self.clear_window()
        
        header = tk.Frame(self.root, bg='#4CAF50', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Клиент: {self.auth.current_user['full_name']}", 
                bg='#4CAF50', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=20, pady=15)
        
        tk.Button(header, text="Выход", command=self.logout, bg='#f44336', fg='white').pack(side='right', padx=20, pady=15)
        
        menu_frame = tk.Frame(self.root, bg='#e8f5e9', width=200)
        menu_frame.pack(side='left', fill='y')
        
        buttons = [
            ("Мои проекты", self.show_my_projects),
            ("Создать заявку", self.create_request),
            ("Мои заявки", self.show_my_requests),
            ("Просмотр смет", self.show_estimates),
            ("Связь с менеджером", self.contact_manager)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, width=25, bg='white', 
                     anchor='w', padx=10, pady=10).pack(pady=2, padx=5)
        
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        tk.Label(self.content_frame, text="Личный кабинет клиента", 
                font=('Arial', 16), bg='white').pack(pady=50)
    
    def logout(self):
        self.auth.logout()
        self.show_login_screen()
    
    # Управление пользователями (Администратор)
    def show_users_management(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление пользователями", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить пользователя", command=self.add_user, 
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_user, 
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.users_tree = ttk.Treeview(tree_frame, columns=('Username', 'Role', 'Full Name', 'Created'), 
                                       show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.users_tree.yview)
        
        self.users_tree.heading('Username', text='Логин')
        self.users_tree.heading('Role', text='Роль')
        self.users_tree.heading('Full Name', text='Полное имя')
        self.users_tree.heading('Created', text='Дата создания')
        
        self.users_tree.column('Username', width=150)
        self.users_tree.column('Role', width=150)
        self.users_tree.column('Full Name', width=200)
        self.users_tree.column('Created', width=150)
        
        self.users_tree.pack(fill='both', expand=True)
        
        self.refresh_users_tree()
    
    def refresh_users_tree(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        for user in self.auth.get_all_users():
            role_name = {'administrator': 'Администратор', 'manager': 'Менеджер', 'client': 'Клиент'}.get(user['role'], user['role'])
            self.users_tree.insert('', 'end', values=(user['username'], role_name, user['full_name'], user['created']))
    
    def add_user(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить пользователя")
        add_window.geometry("400x300")
        
        tk.Label(add_window, text="Логин:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        username_entry = tk.Entry(add_window, width=25)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Пароль:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        password_entry = tk.Entry(add_window, show='*', width=25)
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Полное имя:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        fullname_entry = tk.Entry(add_window, width=25)
        fullname_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(add_window, text="Роль:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        role_var = tk.StringVar(value='client')
        role_combo = ttk.Combobox(add_window, textvariable=role_var, width=22, 
                                 values=['administrator', 'manager', 'client'], state='readonly')
        role_combo.grid(row=3, column=1, padx=10, pady=10)
        
        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get()
            fullname = fullname_entry.get().strip()
            role = role_var.get()
            
            if not username or not password or not fullname:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = self.auth.create_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Успех", message)
                add_window.destroy()
                self.refresh_users_tree()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(add_window, text="Сохранить", command=save_user, bg='#4CAF50', fg='white').grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        username = self.users_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            self.auth.delete_user(username)
            self.refresh_users_tree()
    
    # Просмотр проектов
    def show_projects(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Все проекты", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Client', 'Status', 'Budget', 'Progress'), 
                           show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Название')
        tree.heading('Client', text='Клиент')
        tree.heading('Status', text='Статус')
        tree.heading('Budget', text='Бюджет')
        tree.heading('Progress', text='Прогресс %')
        
        tree.column('ID', width=50)
        tree.column('Name', width=250)
        tree.column('Client', width=150)
        tree.column('Status', width=100)
        tree.column('Budget', width=100)
        tree.column('Progress', width=80)
        
        for project in self.data['projects']:
            tree.insert('', 'end', values=(project['id'], project['name'], project['client'], 
                                          project['status'], project['budget'], project['progress']))
        
        tree.pack(fill='both', expand=True)
    
    # Просмотр сотрудников
    def show_employees(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Все сотрудники", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Position', 'Phone', 'Salary', 'Status'), 
                           show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='ФИО')
        tree.heading('Position', text='Должность')
        tree.heading('Phone', text='Телефон')
        tree.heading('Salary', text='Зарплата')
        tree.heading('Status', text='Статус')
        
        tree.column('ID', width=50)
        tree.column('Name', width=200)
        tree.column('Position', width=150)
        tree.column('Phone', width=120)
        tree.column('Salary', width=100)
        tree.column('Status', width=100)
        
        for emp in self.data['employees']:
            tree.insert('', 'end', values=(emp['id'], emp['name'], emp['position'], 
                                          emp['phone'], emp['salary'], emp['status']))
        
        tree.pack(fill='both', expand=True)
    
    # Просмотр материалов
    def show_materials(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Все материалы", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Quantity', 'Unit', 'Price', 'Supplier'), 
                           show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Название')
        tree.heading('Quantity', text='Количество')
        tree.heading('Unit', text='Ед. изм.')
        tree.heading('Price', text='Цена')
        tree.heading('Supplier', text='Поставщик')
        
        tree.column('ID', width=50)
        tree.column('Name', width=200)
        tree.column('Quantity', width=100)
        tree.column('Unit', width=80)
        tree.column('Price', width=80)
        tree.column('Supplier', width=150)
        
        for material in self.data['materials']:
            tree.insert('', 'end', values=(material['id'], material['name'], material['quantity'], 
                                          material['unit'], material['price'], material['supplier']))
        
        tree.pack(fill='both', expand=True)
    
    # Просмотр заявок
    def show_requests(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Все заявки", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(tree_frame, columns=('ID', 'Client', 'Description', 'Date', 'Status', 'Cost'), 
                           show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Client', text='Клиент')
        tree.heading('Description', text='Описание')
        tree.heading('Date', text='Дата')
        tree.heading('Status', text='Статус')
        tree.heading('Cost', text='Смета')
        
        tree.column('ID', width=50)
        tree.column('Client', width=150)
        tree.column('Description', width=250)
        tree.column('Date', width=100)
        tree.column('Status', width=120)
        tree.column('Cost', width=100)
        
        for req in self.data['requests']:
            tree.insert('', 'end', values=(req['id'], req['client'], req['description'], 
                                          req['date'], req['status'], req['estimated_cost']))
        
        tree.pack(fill='both', expand=True)
    
    # Отчеты
    def show_reports(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Отчеты и статистика", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=20)
        
        total_projects = len(self.data['projects'])
        total_employees = len(self.data['employees'])
        total_materials = len(self.data['materials'])
        total_requests = len(self.data['requests'])
        
        active_projects = sum(1 for p in self.data['projects'] if p['status'] == 'В процессе')
        total_budget = sum(int(p['budget']) for p in self.data['projects'])
        
        stats = [
            ("Всего проектов:", total_projects),
            ("Активных проектов:", active_projects),
            ("Сотрудников:", total_employees),
            ("Материалов в базе:", total_materials),
            ("Заявок:", total_requests),
            ("Общий бюджет проектов:", f"{total_budget:,} руб.")
        ]
        
        for i, (label, value) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg='#e3f2fd', bd=1, relief='solid')
            frame.grid(row=i//2, column=i%2, padx=20, pady=10, sticky='ew')
            
            tk.Label(frame, text=label, font=('Arial', 11), bg='#e3f2fd', anchor='w').pack(fill='x', padx=10, pady=5)
            tk.Label(frame, text=str(value), font=('Arial', 14, 'bold'), bg='#e3f2fd', anchor='w').pack(fill='x', padx=10, pady=5)
    
    # Резервное копирование
    def backup_data(self):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = f'backup_data_{timestamp}.json'
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", f"Резервная копия создана: {backup_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать резервную копию: {str(e)}")
    
    # Управление проектами (Менеджер)
    def manage_projects(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление проектами", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить проект", command=self.add_project, 
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_project, 
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_project, 
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.projects_tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Client', 'Status', 'Budget', 'Progress'), 
                                         show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.projects_tree.yview)
        
        self.projects_tree.heading('ID', text='ID')
        self.projects_tree.heading('Name', text='Название')
        self.projects_tree.heading('Client', text='Клиент')
        self.projects_tree.heading('Status', text='Статус')
        self.projects_tree.heading('Budget', text='Бюджет')
        self.projects_tree.heading('Progress', text='Прогресс %')
        
        self.projects_tree.column('ID', width=50)
        self.projects_tree.column('Name', width=250)
        self.projects_tree.column('Client', width=150)
        self.projects_tree.column('Status', width=100)
        self.projects_tree.column('Budget', width=100)
        self.projects_tree.column('Progress', width=80)
        
        self.projects_tree.pack(fill='both', expand=True)
        self.refresh_projects_tree()
    
    def refresh_projects_tree(self):
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
        
        for project in self.data['projects']:
            self.projects_tree.insert('', 'end', values=(project['id'], project['name'], project['client'], 
                                                        project['status'], project['budget'], project['progress']))
    
    def add_project(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить проект")
        add_window.geometry("450x400")
        
        fields = [
            ("Название:", 'name'),
            ("Клиент:", 'client'),
            ("Бюджет (руб):", 'budget'),
            ("Дата начала (ГГГГ-ММ-ДД):", 'start_date'),
            ("Дата окончания (ГГГГ-ММ-ДД):", 'end_date'),
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=10, sticky='e')
            entry = tk.Entry(add_window, width=25)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        tk.Label(add_window, text="Статус:").grid(row=len(fields), column=0, padx=10, pady=10, sticky='e')
        status_var = tk.StringVar(value='Планирование')
        status_combo = ttk.Combobox(add_window, textvariable=status_var, width=22, 
                                   values=['Планирование', 'В процессе', 'Завершен', 'Приостановлен'], state='readonly')
        status_combo.grid(row=len(fields), column=1, padx=10, pady=10)
        
        def save_project():
            try:
                new_id = max([p['id'] for p in self.data['projects']], default=0) + 1
                
                new_project = {
                    'id': new_id,
                    'name': entries['name'].get(),
                    'client': entries['client'].get(),
                    'status': status_var.get(),
                    'start_date': entries['start_date'].get(),
                    'end_date': entries['end_date'].get(),
                    'budget': entries['budget'].get(),
                    'progress': '0'
                }
                
                if not all([new_project['name'], new_project['client'], new_project['budget']]):
                    messagebox.showerror("Ошибка", "Заполните обязательные поля")
                    return
                
                self.data['projects'].append(new_project)
                self.save_data()
                messagebox.showinfo("Успех", "Проект добавлен")
                add_window.destroy()
                self.refresh_projects_tree()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        tk.Button(add_window, text="Сохранить", command=save_project, bg='#4CAF50', fg='white').grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
    
    def edit_project(self):
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите проект")
            return
        
        project_id = self.projects_tree.item(selected[0])['values'][0]
        project = next((p for p in self.data['projects'] if p['id'] == project_id), None)
        
        if not project:
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать проект")
        edit_window.geometry("450x400")
        
        fields = [
            ("Название:", 'name'),
            ("Клиент:", 'client'),
            ("Бюджет (руб):", 'budget'),
            ("Дата начала:", 'start_date'),
            ("Дата окончания:", 'end_date'),
            ("Прогресс %:", 'progress')
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(edit_window, text=label).grid(row=i, column=0, padx=10, pady=10, sticky='e')
            entry = tk.Entry(edit_window, width=25)
            entry.insert(0, project.get(key, ''))
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        tk.Label(edit_window, text="Статус:").grid(row=len(fields), column=0, padx=10, pady=10, sticky='e')
        status_var = tk.StringVar(value=project['status'])
        status_combo = ttk.Combobox(edit_window, textvariable=status_var, width=22, 
                                   values=['Планирование', 'В процессе', 'Завершен', 'Приостановлен'], state='readonly')
        status_combo.grid(row=len(fields), column=1, padx=10, pady=10)
        
        def save_changes():
            project['name'] = entries['name'].get()
            project['client'] = entries['client'].get()
            project['budget'] = entries['budget'].get()
            project['start_date'] = entries['start_date'].get()
            project['end_date'] = entries['end_date'].get()
            project['progress'] = entries['progress'].get()
            project['status'] = status_var.get()
            
            self.save_data()
            messagebox.showinfo("Успех", "Проект обновлен")
            edit_window.destroy()
            self.refresh_projects_tree()
        
        tk.Button(edit_window, text="Сохранить", command=save_changes, bg='#4CAF50', fg='white').grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
    
    def delete_project(self):
        selected = self.projects_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите проект")
            return
        
        project_id = self.projects_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный проект?"):
            self.data['projects'] = [p for p in self.data['projects'] if p['id'] != project_id]
            self.save_data()
            self.refresh_projects_tree()
    
    # Управление сотрудниками (Менеджер)
    def manage_employees(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление сотрудниками", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить сотрудника", command=self.add_employee, 
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_employee, 
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_employee, 
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.employees_tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Position', 'Phone', 'Salary', 'Status'), 
                                          show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.employees_tree.yview)
        
        self.employees_tree.heading('ID', text='ID')
        self.employees_tree.heading('Name', text='ФИО')
        self.employees_tree.heading('Position', text='Должность')
        self.employees_tree.heading('Phone', text='Телефон')
        self.employees_tree.heading('Salary', text='Зарплата')
        self.employees_tree.heading('Status', text='Статус')
        
        self.employees_tree.column('ID', width=50)
        self.employees_tree.column('Name', width=200)
        self.employees_tree.column('Position', width=150)
        self.employees_tree.column('Phone', width=120)
        self.employees_tree.column('Salary', width=100)
        self.employees_tree.column('Status', width=100)
        
        self.employees_tree.pack(fill='both', expand=True)
        self.refresh_employees_tree()
    
    def refresh_employees_tree(self):
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        
        for emp in self.data['employees']:
            self.employees_tree.insert('', 'end', values=(emp['id'], emp['name'], emp['position'], 
                                                         emp['phone'], emp['salary'], emp['status']))
    
    def add_employee(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить сотрудника")
        add_window.geometry("400x350")
        
        fields = [
            ("ФИО:", 'name'),
            ("Должность:", 'position'),
            ("Телефон:", 'phone'),
            ("Зарплата:", 'salary'),
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=10, sticky='e')
            entry = tk.Entry(add_window, width=25)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        tk.Label(add_window, text="Статус:").grid(row=len(fields), column=0, padx=10, pady=10, sticky='e')
        status_var = tk.StringVar(value='Активен')
        status_combo = ttk.Combobox(add_window, textvariable=status_var, width=22, 
                                   values=['Активен', 'В отпуске', 'Уволен'], state='readonly')
        status_combo.grid(row=len(fields), column=1, padx=10, pady=10)
        
        def save_employee():
            new_id = max([e['id'] for e in self.data['employees']], default=0) + 1
            
            new_employee = {
                'id': new_id,
                'name': entries['name'].get(),
                'position': entries['position'].get(),
                'phone': entries['phone'].get(),
                'salary': entries['salary'].get(),
                'status': status_var.get()
            }
            
            if not all([new_employee['name'], new_employee['position']]):
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            self.data['employees'].append(new_employee)
            self.save_data()
            messagebox.showinfo("Успех", "Сотрудник добавлен")
            add_window.destroy()
            self.refresh_employees_tree()
        
        tk.Button(add_window, text="Сохранить", command=save_employee, bg='#4CAF50', fg='white').grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
    
    def edit_employee(self):
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сотрудника")
            return
        
        emp_id = self.employees_tree.item(selected[0])['values'][0]
        employee = next((e for e in self.data['employees'] if e['id'] == emp_id), None)
        
        if not employee:
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать сотрудника")
        edit_window.geometry("400x350")
        
        fields = [
            ("ФИО:", 'name'),
            ("Должность:", 'position'),
            ("Телефон:", 'phone'),
            ("Зарплата:", 'salary'),
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(edit_window, text=label).grid(row=i, column=0, padx=10, pady=10, sticky='e')
            entry = tk.Entry(edit_window, width=25)
            entry.insert(0, employee.get(key, ''))
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        tk.Label(edit_window, text="Статус:").grid(row=len(fields), column=0, padx=10, pady=10, sticky='e')
        status_var = tk.StringVar(value=employee['status'])
        status_combo = ttk.Combobox(edit_window, textvariable=status_var, width=22, 
                                   values=['Активен', 'В отпуске', 'Уволен'], state='readonly')
        status_combo.grid(row=len(fields), column=1, padx=10, pady=10)
        
        def save_changes():
            employee['name'] = entries['name'].get()
            employee['position'] = entries['position'].get()
            employee['phone'] = entries['phone'].get()
            employee['salary'] = entries['salary'].get()
            employee['status'] = status_var.get()
            
            self.save_data()
            messagebox.showinfo("Успех", "Сотрудник обновлен")
            edit_window.destroy()
            self.refresh_employees_tree()
        
        tk.Button(edit_window, text="Сохранить", command=save_changes, bg='#4CAF50', fg='white').grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
    
    def delete_employee(self):
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сотрудника")
            return
        
        emp_id = self.employees_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранного сотрудника?"):
            self.data['employees'] = [e for e in self.data['employees'] if e['id'] != emp_id]
            self.save_data()
            self.refresh_employees_tree()
    
    # Управление материалами (Менеджер)
    def manage_materials(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление материалами", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить материал", command=self.add_material, 
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_material, 
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_material, 
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.materials_tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Quantity', 'Unit', 'Price', 'Supplier'), 
                                          show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.materials_tree.yview)
        
        self.materials_tree.heading('ID', text='ID')
        self.materials_tree.heading('Name', text='Название')
        self.materials_tree.heading('Quantity', text='Количество')
        self.materials_tree.heading('Unit', text='Ед. изм.')
        self.materials_tree.heading('Price', text='Цена')
        self.materials_tree.heading('Supplier', text='Поставщик')
        
        self.materials_tree.column('ID', width=50)
        self.materials_tree.column('Name', width=200)
        self.materials_tree.column('Quantity', width=100)
        self.materials_tree.column('Unit', width=80)
        self.materials_tree.column('Price', width=80)
        self.materials_tree.column('Supplier', width=150)
        
        self.materials_tree.pack(fill='both', expand=True)
        self.refresh_materials_tree()
    
    def refresh_materials_tree(self):
        for item in self.materials_tree.get_children():
            self.materials_tree.delete(item)
        
        for mat in self.data['materials']:
            self.materials_tree.insert('', 'end', values=(mat['id'], mat['name'], mat['quantity'], 
                                                         mat['unit'], mat['price'], mat['supplier']))
    
    def add_material(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить материал")
        add_window.geometry("400x350")
        
        fields = [
            ("Название:", 'name'),
            ("Количество:", 'quantity'),
            ("Единица измерения:", 'unit'),
            ("Цена за ед.:", 'price'),
            ("Поставщик:", 'supplier')
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=10, sticky='e')
            entry = tk.Entry(add_window, width=25)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        def save_material():
            new_id = max([m['id'] for m in self.data['materials']], default=0) + 1
            
            new_material = {
                'id': new_id,
                'name': entries['name'].get(),
                'quantity': entries['quantity'].get(),
                'unit': entries['unit'].get(),
                'price': entries['price'].get(),
                'supplier': entries['supplier'].get()
            }
            
            if not all([new_material['name'], new_material['quantity']]):
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            self.data['materials'].append(new_material)
            self.save_data()
            messagebox.showinfo("Успех", "Материал добавлен")
            add_window.destroy()
            self.refresh_materials_tree()
        
        tk.Button(add_window, text="Сохранить", command=save_material, bg='#4CAF50', fg='white').grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    def edit_material(self):
        selected = self.materials_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите материал")
            return
        
        mat_id = self.materials_tree.item(selected[0])['values'][0]
        material = next((m for m in self.data['materials'] if m['id'] == mat_id), None)
        
        if not material:
            return
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать материал")
        edit_window.geometry("400x350")
        
        fields = [
            ("Название:", 'name'),
            ("Количество:", 'quantity'),
            ("Единица измерения:", 'unit'),
            ("Цена за ед.:", 'price'),
            ("Поставщик:", 'supplier')
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(edit_window, text=label).grid(row=i, column=0, padx=10, pady=10, sticky='e')
            entry = tk.Entry(edit_window, width=25)
            entry.insert(0, material.get(key, ''))
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        def save_changes():
            material['name'] = entries['name'].get()
            material['quantity'] = entries['quantity'].get()
            material['unit'] = entries['unit'].get()
            material['price'] = entries['price'].get()
            material['supplier'] = entries['supplier'].get()
            
            self.save_data()
            messagebox.showinfo("Успех", "Материал обновлен")
            edit_window.destroy()
            self.refresh_materials_tree()
        
        tk.Button(edit_window, text="Сохранить", command=save_changes, bg='#4CAF50', fg='white').grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    def delete_material(self):
        selected = self.materials_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите материал")
            return
        
        mat_id = self.materials_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный материал?"):
            self.data['materials'] = [m for m in self.data['materials'] if m['id'] != mat_id]
            self.save_data()
            self.refresh_materials_tree()
    
    # Назначение работников
    def assign_workers(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Назначение работников на проект", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(pady=20)
        
        tk.Label(frame, text="Выберите проект:", bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        project_var = tk.StringVar()
        project_combo = ttk.Combobox(frame, textvariable=project_var, width=30, state='readonly')
        project_combo['values'] = [f"{p['id']} - {p['name']}" for p in self.data['projects']]
        project_combo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Выберите сотрудника:", bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        employee_var = tk.StringVar()
        employee_combo = ttk.Combobox(frame, textvariable=employee_var, width=30, state='readonly')
        employee_combo['values'] = [f"{e['id']} - {e['name']} ({e['position']})" for e in self.data['employees']]
        employee_combo.grid(row=1, column=1, padx=10, pady=10)
        
        def assign():
            if not project_var.get() or not employee_var.get():
                messagebox.showwarning("Предупреждение", "Выберите проект и сотрудника")
                return
            
            messagebox.showinfo("Успех", f"Сотрудник назначен на проект\n{project_var.get()}\n{employee_var.get()}")
        
        tk.Button(frame, text="Назначить", command=assign, bg='#4CAF50', fg='white', width=20).grid(row=2, column=0, columnspan=2, pady=20)
    
    # Отслеживание прогресса
    def track_progress(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Отслеживание прогресса проектов", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        for project in self.data['projects']:
            frame = tk.Frame(self.content_frame, bg='#f5f5f5', bd=1, relief='solid')
            frame.pack(fill='x', padx=20, pady=10)
            
            tk.Label(frame, text=project['name'], font=('Arial', 12, 'bold'), bg='#f5f5f5').pack(anchor='w', padx=10, pady=5)
            tk.Label(frame, text=f"Клиент: {project['client']} | Статус: {project['status']}", bg='#f5f5f5').pack(anchor='w', padx=10)
            
            progress_frame = tk.Frame(frame, bg='#f5f5f5')
            progress_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(progress_frame, text=f"Прогресс: {project['progress']}%", bg='#f5f5f5').pack(side='left')
            
            progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
            progress_bar['value'] = int(project['progress'])
            progress_bar.pack(side='left', padx=10)
    
    # Клиентские функции
    def show_my_projects(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои проекты", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        client_name = self.auth.current_user['full_name']
        client_projects = [p for p in self.data['projects'] if p['client'] == client_name]
        
        if not client_projects:
            tk.Label(self.content_frame, text="У вас пока нет проектов", 
                    font=('Arial', 12), bg='white').pack(pady=50)
            return
        
        for project in client_projects:
            frame = tk.Frame(self.content_frame, bg='#e8f5e9', bd=1, relief='solid')
            frame.pack(fill='x', padx=20, pady=10)
            
            tk.Label(frame, text=project['name'], font=('Arial', 12, 'bold'), bg='#e8f5e9').pack(anchor='w', padx=10, pady=5)
            tk.Label(frame, text=f"Статус: {project['status']}", bg='#e8f5e9').pack(anchor='w', padx=10)
            tk.Label(frame, text=f"Бюджет: {project['budget']} руб.", bg='#e8f5e9').pack(anchor='w', padx=10)
            tk.Label(frame, text=f"Период: {project['start_date']} - {project['end_date']}", bg='#e8f5e9').pack(anchor='w', padx=10)
            tk.Label(frame, text=f"Прогресс: {project['progress']}%", bg='#e8f5e9').pack(anchor='w', padx=10, pady=5)
    
    def create_request(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Создание новой заявки", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(pady=20)
        
        tk.Label(frame, text="Описание проекта:", bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='ne')
        description_text = tk.Text(frame, width=40, height=10)
        description_text.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Примерный бюджет:", bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        budget_entry = tk.Entry(frame, width=30)
        budget_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def submit_request():
            description = description_text.get('1.0', 'end-1c')
            budget = budget_entry.get()
            
            if not description or not budget:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            new_id = max([r['id'] for r in self.data['requests']], default=0) + 1
            
            new_request = {
                'id': new_id,
                'client': self.auth.current_user['full_name'],
                'description': description,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'На рассмотрении',
                'estimated_cost': budget
            }
            
            self.data['requests'].append(new_request)
            self.save_data()
            
            messagebox.showinfo("Успех", "Заявка отправлена на рассмотрение")
            description_text.delete('1.0', 'end')
            budget_entry.delete(0, 'end')
        
        tk.Button(frame, text="Отправить заявку", command=submit_request, 
                 bg='#4CAF50', fg='white', width=20).grid(row=2, column=0, columnspan=2, pady=20)
    
    def show_my_requests(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои заявки", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        client_name = self.auth.current_user['full_name']
        client_requests = [r for r in self.data['requests'] if r['client'] == client_name]
        
        if not client_requests:
            tk.Label(self.content_frame, text="У вас пока нет заявок", 
                    font=('Arial', 12), bg='white').pack(pady=50)
            return
        
        for request in client_requests:
            frame = tk.Frame(self.content_frame, bg='#fff9e6', bd=1, relief='solid')
            frame.pack(fill='x', padx=20, pady=10)
            
            tk.Label(frame, text=f"Заявка #{request['id']}", font=('Arial', 11, 'bold'), bg='#fff9e6').pack(anchor='w', padx=10, pady=5)
            tk.Label(frame, text=f"Дата: {request['date']}", bg='#fff9e6').pack(anchor='w', padx=10)
            tk.Label(frame, text=f"Статус: {request['status']}", bg='#fff9e6').pack(anchor='w', padx=10)
            tk.Label(frame, text=f"Описание: {request['description'][:100]}...", bg='#fff9e6').pack(anchor='w', padx=10)
            tk.Label(frame, text=f"Смета: {request['estimated_cost']} руб.", bg='#fff9e6').pack(anchor='w', padx=10, pady=5)
    
    def show_estimates(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Сметы проектов", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        client_name = self.auth.current_user['full_name']
        client_projects = [p for p in self.data['projects'] if p['client'] == client_name]
        
        if not client_projects:
            tk.Label(self.content_frame, text="Нет доступных смет", 
                    font=('Arial', 12), bg='white').pack(pady=50)
            return
        
        for project in client_projects:
            frame = tk.Frame(self.content_frame, bg='#e3f2fd', bd=1, relief='solid')
            frame.pack(fill='x', padx=20, pady=10)
            
            tk.Label(frame, text=f"Проект: {project['name']}", font=('Arial', 11, 'bold'), bg='#e3f2fd').pack(anchor='w', padx=10, pady=5)
            tk.Label(frame, text=f"Общий бюджет: {project['budget']} руб.", font=('Arial', 10), bg='#e3f2fd').pack(anchor='w', padx=10)
            tk.Label(frame, text=f"Период выполнения: {project['start_date']} - {project['end_date']}", bg='#e3f2fd').pack(anchor='w', padx=10, pady=5)
    
    def contact_manager(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Связь с менеджером", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=20)
        
        info_frame = tk.Frame(self.content_frame, bg='#e8f5e9', bd=1, relief='solid')
        info_frame.pack(padx=40, pady=20, fill='x')
        
        tk.Label(info_frame, text="Контактная информация", font=('Arial', 12, 'bold'), bg='#e8f5e9').pack(pady=10)
        tk.Label(info_frame, text="Менеджер: Иван Петров", bg='#e8f5e9').pack(anchor='w', padx=20)
        tk.Label(info_frame, text="Телефон: +7 (495) 123-45-67", bg='#e8f5e9').pack(anchor='w', padx=20)
        tk.Label(info_frame, text="Email: manager@construction.ru", bg='#e8f5e9').pack(anchor='w', padx=20, pady=10)
        
        frame = tk.Frame(self.content_frame, bg='white')
        frame.pack(pady=20)
        
        tk.Label(frame, text="Ваше сообщение:", bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='ne')
        message_text = tk.Text(frame, width=50, height=10)
        message_text.grid(row=0, column=1, padx=10, pady=10)
        
        def send_message():
            message = message_text.get('1.0', 'end-1c')
            if message:
                messagebox.showinfo("Успех", "Сообщение отправлено менеджеру")
                message_text.delete('1.0', 'end')
            else:
                messagebox.showwarning("Предупреждение", "Введите сообщение")
        
        tk.Button(frame, text="Отправить", command=send_message, 
                 bg='#4CAF50', fg='white', width=20).grid(row=1, column=0, columnspan=2, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    app = ConstructionApp(root)
    root.mainloop()