import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime, timedelta
import auth

DATA_FILE = 'data.json'

class InsuranceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система - Страховая фирма")
        self.root.geometry("1000x700")
        self.current_user = None

        # Загрузка данных
        self.load_data()

        # Показать окно входа
        self.show_login()
    
    def load_data(self):
        """Загрузка данных из файла"""
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден!")
            return False
        return True
    
    def save_data(self):
        """Сохранение данных в файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно входа в систему"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Страховая фирма", font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, font=('Arial', 12), width=25)
        username_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, font=('Arial', 12), width=25, show='*')
        password_entry.grid(row=2, column=1, pady=5)
        
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            user = auth.authenticate(username, password)
            if user:
                self.current_user = user
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login, font=('Arial', 12), width=20, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка
        hint_text = "Учетные записи по умолчанию:\nadmin/admin123\nmanager/manager123\nclient/client123"
        tk.Label(frame, text=hint_text, font=('Arial', 9), fg='gray', justify='left').grid(row=4, column=0, columnspan=2)
        
        password_entry.bind('<Return>', lambda e: login())
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли пользователя"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"Добро пожаловать, {self.current_user['full_name']}", 
                bg='#2196F3', fg='white', font=('Arial', 14)).pack(side='left', padx=20, pady=15)
        
        tk.Button(top_frame, text="Выход", command=self.show_login, bg='#f44336', fg='white', 
                 font=('Arial', 10)).pack(side='right', padx=20, pady=15)
        
        # Меню в зависимости от роли
        if self.current_user['role'] == 'administrator':
            self.show_admin_menu()
        elif self.current_user['role'] == 'manager':
            self.show_manager_menu()
        elif self.current_user['role'] == 'client':
            self.show_client_menu()
    
    def show_admin_menu(self):
        """Меню администратора"""
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=30)
        
        tk.Label(menu_frame, text="Панель администратора", font=('Arial', 18, 'bold')).pack(pady=20)
        
        buttons = [
            ("👥 Управление пользователями", self.manage_users),
            ("📋 Управление типами страхования", self.manage_insurance_types),
            ("📊 Просмотр всех данных", self.view_all_data),
            ("📈 Генерация отчетов", self.generate_reports),
            ("💾 Резервное копирование", self.backup_data)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, font=('Arial', 12), 
                     width=35, height=2, bg='#2196F3', fg='white').pack(pady=5)
    
    def show_manager_menu(self):
        """Меню менеджера"""
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=30)
        
        tk.Label(menu_frame, text="Панель менеджера", font=('Arial', 18, 'bold')).pack(pady=20)
        
        buttons = [
            ("👤 Регистрация клиентов", self.register_client),
            ("📄 Создание полисов", self.create_policy),
            ("✉️ Обработка заявок", self.process_claims),
            ("👥 Просмотр клиентов", self.view_clients),
            ("💰 Расчет стоимости страхования", self.calculate_insurance)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, font=('Arial', 12), 
                     width=35, height=2, bg='#4CAF50', fg='white').pack(pady=5)
    
    def show_client_menu(self):
        """Меню клиента"""
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=30)
        
        tk.Label(menu_frame, text="Личный кабинет", font=('Arial', 18, 'bold')).pack(pady=20)
        
        buttons = [
            ("📄 Мои полисы", self.view_my_policies),
            ("✉️ Подать заявку", self.submit_claim),
            ("📋 Статус заявок", self.check_claim_status),
            ("✏️ Обновить личные данные", self.update_profile)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command, font=('Arial', 12), 
                     width=35, height=2, bg='#FF9800', fg='white').pack(pady=5)
    
    # ФУНКЦИИ АДМИНИСТРАТОРА
    
    def manage_users(self):
        """Управление пользователями"""
        window = tk.Toplevel(self.root)
        window.title("Управление пользователями")
        window.geometry("900x500")
        
        # Таблица пользователей
        columns = ('ID', 'Логин', 'Роль', 'ФИО', 'Дата создания')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            users = auth.get_all_users()
            for user in users:
                tree.insert('', 'end', values=(user['id'], user['username'], user['role'], user['full_name'], user['created']))
        
        refresh_table()
        
        # Кнопки управления
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_user():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить пользователя")
            add_window.geometry("400x300")
            
            tk.Label(add_window, text="Логин:").grid(row=0, column=0, padx=10, pady=5)
            username_entry = tk.Entry(add_window, width=30)
            username_entry.grid(row=0, column=1, pady=5)
            
            tk.Label(add_window, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
            password_entry = tk.Entry(add_window, width=30, show='*')
            password_entry.grid(row=1, column=1, pady=5)
            
            tk.Label(add_window, text="ФИО:").grid(row=2, column=0, padx=10, pady=5)
            fullname_entry = tk.Entry(add_window, width=30)
            fullname_entry.grid(row=2, column=1, pady=5)
            
            tk.Label(add_window, text="Роль:").grid(row=3, column=0, padx=10, pady=5)
            role_var = tk.StringVar(value='manager')
            role_combo = ttk.Combobox(add_window, textvariable=role_var, values=['administrator', 'manager', 'client'], width=27)
            role_combo.grid(row=3, column=1, pady=5)
            
            def save():
                success, msg = auth.create_user(username_entry.get(), password_entry.get(), role_var.get(), fullname_entry.get())
                messagebox.showinfo("Результат", msg)
                if success:
                    refresh_table()
                    add_window.destroy()
            
            tk.Button(add_window, text="Создать", command=save, bg='#4CAF50', fg='white').grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            user_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить пользователя?"):
                auth.delete_user(user_id)
                refresh_table()
        
        tk.Button(btn_frame, text="➕ Добавить", command=add_user, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Удалить", command=delete_user, bg='#f44336', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Обновить", command=refresh_table, bg='#2196F3', fg='white').pack(side='left', padx=5)
    
    def manage_insurance_types(self):
        """Управление типами страхования"""
        window = tk.Toplevel(self.root)
        window.title("Типы страхования")
        window.geometry("900x500")
        
        columns = ('ID', 'Название', 'Описание', 'Базовая цена')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.pack(pady=10, padx=10)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            for itype in self.data['insurance_types']:
                tree.insert('', 'end', values=(itype['id'], itype['name'], itype['description'], itype['base_price']))
        
        refresh_table()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_type():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить тип страхования")
            add_window.geometry("400x250")
            
            tk.Label(add_window, text="Название:").grid(row=0, column=0, padx=10, pady=5)
            name_entry = tk.Entry(add_window, width=30)
            name_entry.grid(row=0, column=1, pady=5)
            
            tk.Label(add_window, text="Описание:").grid(row=1, column=0, padx=10, pady=5)
            desc_entry = tk.Entry(add_window, width=30)
            desc_entry.grid(row=1, column=1, pady=5)
            
            tk.Label(add_window, text="Базовая цена:").grid(row=2, column=0, padx=10, pady=5)
            price_entry = tk.Entry(add_window, width=30)
            price_entry.grid(row=2, column=1, pady=5)
            
            def save():
                new_id = max([t['id'] for t in self.data['insurance_types']], default=0) + 1
                self.data['insurance_types'].append({
                    'id': new_id,
                    'name': name_entry.get(),
                    'description': desc_entry.get(),
                    'base_price': int(price_entry.get())
                })
                self.save_data()
                refresh_table()
                add_window.destroy()
            
            tk.Button(add_window, text="Создать", command=save, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="➕ Добавить", command=add_type, bg='#4CAF50', fg='white').pack(side='left', padx=5)
    
    def view_all_data(self):
        """Просмотр всех данных системы"""
        window = tk.Toplevel(self.root)
        window.title("Все данные системы")
        window.geometry("1000x600")
        
        notebook = ttk.Notebook(window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка клиенты
        clients_frame = tk.Frame(notebook)
        notebook.add(clients_frame, text='Клиенты')
        
        columns = ('ID', 'ФИО', 'Паспорт', 'Телефон', 'Email')
        tree_clients = ttk.Treeview(clients_frame, columns=columns, show='headings')
        for col in columns:
            tree_clients.heading(col, text=col)
        tree_clients.pack(fill='both', expand=True)
        
        for client in self.data['clients']:
            tree_clients.insert('', 'end', values=(client['id'], client['full_name'], client['passport'], client['phone'], client['email']))
        
        # Вкладка полисы
        policies_frame = tk.Frame(notebook)
        notebook.add(policies_frame, text='Полисы')
        
        columns = ('ID', 'Номер полиса', 'Клиент', 'Тип', 'Начало', 'Конец', 'Цена', 'Статус')
        tree_policies = ttk.Treeview(policies_frame, columns=columns, show='headings')
        for col in columns:
            tree_policies.heading(col, text=col)
            tree_policies.column(col, width=100)
        tree_policies.pack(fill='both', expand=True)
        
        for policy in self.data['policies']:
            client = next((c for c in self.data['clients'] if c['id'] == policy['client_id']), None)
            itype = next((t for t in self.data['insurance_types'] if t['id'] == policy['insurance_type_id']), None)
            tree_policies.insert('', 'end', values=(
                policy['id'], policy['policy_number'], client['full_name'] if client else 'N/A',
                itype['name'] if itype else 'N/A', policy['start_date'], policy['end_date'],
                policy['price'], policy['status']
            ))
        
        # Вкладка заявки
        claims_frame = tk.Frame(notebook)
        notebook.add(claims_frame, text='Заявки')
        
        columns = ('ID', 'Клиент', 'Полис', 'Описание', 'Сумма', 'Статус', 'Дата')
        tree_claims = ttk.Treeview(claims_frame, columns=columns, show='headings')
        for col in columns:
            tree_claims.heading(col, text=col)
            tree_claims.column(col, width=120)
        tree_claims.pack(fill='both', expand=True)
        
        for claim in self.data['claims']:
            client = next((c for c in self.data['clients'] if c['id'] == claim['client_id']), None)
            policy = next((p for p in self.data['policies'] if p['id'] == claim['policy_id']), None)
            tree_claims.insert('', 'end', values=(
                claim['id'], client['full_name'] if client else 'N/A',
                policy['policy_number'] if policy else 'N/A', claim['description'][:30],
                claim['amount'], claim['status'], claim['created']
            ))
    
    def generate_reports(self):
        """Генерация отчетов"""
        total_clients = len(self.data['clients'])
        total_policies = len(self.data['policies'])
        active_policies = len([p for p in self.data['policies'] if p['status'] == 'active'])
        total_claims = len(self.data['claims'])
        pending_claims = len([c for c in self.data['claims'] if c['status'] == 'pending'])
        
        total_revenue = sum(p['price'] for p in self.data['policies'])
        
        report = f"""
╔══════════════════════════════════════════╗
║       ОТЧЕТ ПО СТРАХОВОЙ КОМПАНИИ        ║
╠══════════════════════════════════════════╣
║ Клиенты:                                 ║
║   Всего зарегистрировано: {total_clients:<14} ║
║                                          ║
║ Полисы:                                  ║
║   Всего полисов: {total_policies:<23} ║
║   Активных: {active_policies:<28} ║
║                                          ║
║ Заявки:                                  ║
║   Всего заявок: {total_claims:<24} ║
║   На рассмотрении: {pending_claims:<19} ║
║                                          ║
║ Финансы:                                 ║
║   Общая сумма полисов: {total_revenue:<15} ₽ ║
║                                          ║
║ Дата отчета: {datetime.now().strftime('%d.%m.%Y %H:%M'):<23} ║
╚══════════════════════════════════════════╝
        """
        
        messagebox.showinfo("Отчет", report)
    
    def backup_data(self):
        """Резервное копирование"""
        import shutil
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            shutil.copy(DATA_FILE, f'data_backup_{timestamp}.json')
            shutil.copy(auth.USERS_FILE, f'users_backup_{timestamp}.json')
            messagebox.showinfo("Успех", f"Резервные копии созданы:\ndata_backup_{timestamp}.json\nusers_backup_{timestamp}.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка создания резервной копии: {str(e)}")
    
    # ФУНКЦИИ МЕНЕДЖЕРА
    
    def register_client(self):
        """Регистрация нового клиента"""
        window = tk.Toplevel(self.root)
        window.title("Регистрация клиента")
        window.geometry("500x400")
        
        tk.Label(window, text="ФИО:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
        fullname_entry = tk.Entry(window, width=35, font=('Arial', 10))
        fullname_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(window, text="Паспорт:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        passport_entry = tk.Entry(window, width=35, font=('Arial', 10))
        passport_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(window, text="Телефон:", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
        phone_entry = tk.Entry(window, width=35, font=('Arial', 10))
        phone_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(window, text="Email:", font=('Arial', 10)).grid(row=3, column=0, padx=10, pady=5, sticky='e')
        email_entry = tk.Entry(window, width=35, font=('Arial', 10))
        email_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(window, text="Адрес:", font=('Arial', 10)).grid(row=4, column=0, padx=10, pady=5, sticky='e')
        address_entry = tk.Entry(window, width=35, font=('Arial', 10))
        address_entry.grid(row=4, column=1, pady=5)
        
        tk.Label(window, text="Логин:", font=('Arial', 10)).grid(row=5, column=0, padx=10, pady=5, sticky='e')
        username_entry = tk.Entry(window, width=35, font=('Arial', 10))
        username_entry.grid(row=5, column=1, pady=5)
        
        tk.Label(window, text="Пароль:", font=('Arial', 10)).grid(row=6, column=0, padx=10, pady=5, sticky='e')
        password_entry = tk.Entry(window, width=35, font=('Arial', 10), show='*')
        password_entry.grid(row=6, column=1, pady=5)
        
        def save_client():
            # Создать пользователя
            success, msg = auth.create_user(username_entry.get(), password_entry.get(), 'client', fullname_entry.get())
            
            if not success:
                messagebox.showerror("Ошибка", msg)
                return
            
            # Получить ID созданного пользователя
            users = auth.get_all_users()
            user_id = next(u['id'] for u in users if u['username'] == username_entry.get())
            
            # Создать клиента
            new_id = max([c['id'] for c in self.data['clients']], default=0) + 1
            new_client = {
                'id': new_id,
                'full_name': fullname_entry.get(),
                'passport': passport_entry.get(),
                'phone': phone_entry.get(),
                'email': email_entry.get(),
                'address': address_entry.get(),
                'user_id': user_id,
                'created': datetime.now().strftime('%Y-%m-%d')
            }
            
            self.data['clients'].append(new_client)
            self.save_data()
            messagebox.showinfo("Успех", "Клиент зарегистрирован")
            window.destroy()
        
        tk.Button(window, text="Зарегистрировать", command=save_client, bg='#4CAF50', fg='white', font=('Arial', 12)).grid(row=7, column=0, columnspan=2, pady=20)
    
    def create_policy(self):
        """Создание полиса"""
        window = tk.Toplevel(self.root)
        window.title("Создание полиса")
        window.geometry("500x400")
        
        tk.Label(window, text="Клиент:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
        client_var = tk.StringVar()
        client_combo = ttk.Combobox(window, textvariable=client_var, width=33, font=('Arial', 10))
        client_combo['values'] = [f"{c['id']} - {c['full_name']}" for c in self.data['clients']]
        client_combo.grid(row=0, column=1, pady=5)
        
        tk.Label(window, text="Тип страхования:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(window, textvariable=type_var, width=33, font=('Arial', 10))
        type_combo['values'] = [f"{t['id']} - {t['name']}" for t in self.data['insurance_types']]
        type_combo.grid(row=1, column=1, pady=5)
        
        tk.Label(window, text="Дата начала:", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
        start_entry = tk.Entry(window, width=35, font=('Arial', 10))
        start_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        start_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(window, text="Срок (месяцев):", font=('Arial', 10)).grid(row=3, column=0, padx=10, pady=5, sticky='e')
        duration_entry = tk.Entry(window, width=35, font=('Arial', 10))
        duration_entry.insert(0, '12')
        duration_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(window, text="Цена:", font=('Arial', 10)).grid(row=4, column=0, padx=10, pady=5, sticky='e')
        price_entry = tk.Entry(window, width=35, font=('Arial', 10))
        price_entry.grid(row=4, column=1, pady=5)
        
        def calculate_price():
            if type_var.get():
                type_id = int(type_var.get().split(' - ')[0])
                itype = next((t for t in self.data['insurance_types'] if t['id'] == type_id), None)
                if itype:
                    price_entry.delete(0, 'end')
                    price_entry.insert(0, str(itype['base_price']))
        
        tk.Button(window, text="Рассчитать цену", command=calculate_price, bg='#2196F3', fg='white').grid(row=5, column=1, pady=5)
        
        def save_policy():
            if not client_var.get() or not type_var.get():
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            client_id = int(client_var.get().split(' - ')[0])
            type_id = int(type_var.get().split(' - ')[0])
            
            start_date = datetime.strptime(start_entry.get(), '%Y-%m-%d')
            duration_months = int(duration_entry.get())
            end_date = start_date + timedelta(days=duration_months * 30)
            
            new_id = max([p['id'] for p in self.data['policies']], default=0) + 1
            policy_number = f"POL-{datetime.now().year}-{new_id:04d}"
            
            new_policy = {
                'id': new_id,
                'client_id': client_id,
                'insurance_type_id': type_id,
                'policy_number': policy_number,
                'start_date': start_entry.get(),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'price': int(price_entry.get()),
                'status': 'active',
                'created_by': self.current_user['id']
            }
            
            self.data['policies'].append(new_policy)
            self.save_data()
            messagebox.showinfo("Успех", f"Полис создан\nНомер: {policy_number}")
            window.destroy()
        
        tk.Button(window, text="Создать полис", command=save_policy, bg='#4CAF50', fg='white', font=('Arial', 12)).grid(row=6, column=0, columnspan=2, pady=20)
    
    def process_claims(self):
        """Обработка заявок"""
        window = tk.Toplevel(self.root)
        window.title("Обработка заявок")
        window.geometry("1000x500")
        
        columns = ('ID', 'Клиент', 'Полис', 'Описание', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=10)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            for claim in self.data['claims']:
                client = next((c for c in self.data['clients'] if c['id'] == claim['client_id']), None)
                policy = next((p for p in self.data['policies'] if p['id'] == claim['policy_id']), None)
                tree.insert('', 'end', values=(
                    claim['id'], client['full_name'] if client else 'N/A',
                    policy['policy_number'] if policy else 'N/A',
                    claim['description'][:30], claim['amount'], claim['status'], claim['created']
                ))
        
        refresh_table()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def approve_claim():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите заявку")
                return
            
            claim_id = tree.item(selected[0])['values'][0]
            claim = next((c for c in self.data['claims'] if c['id'] == claim_id), None)
            if claim:
                claim['status'] = 'approved'
                claim['processed_by'] = self.current_user['id']
                self.save_data()
                refresh_table()
                messagebox.showinfo("Успех", "Заявка одобрена")
        
        def reject_claim():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите заявку")
                return
            
            claim_id = tree.item(selected[0])['values'][0]
            claim = next((c for c in self.data['claims'] if c['id'] == claim_id), None)
            if claim:
                claim['status'] = 'rejected'
                claim['processed_by'] = self.current_user['id']
                self.save_data()
                refresh_table()
                messagebox.showinfo("Успех", "Заявка отклонена")
        
        tk.Button(btn_frame, text="✅ Одобрить", command=approve_claim, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Отклонить", command=reject_claim, bg='#f44336', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🔄 Обновить", command=refresh_table, bg='#2196F3', fg='white').pack(side='left', padx=5)
    
    def view_clients(self):
        """Просмотр клиентов"""
        window = tk.Toplevel(self.root)
        window.title("Клиенты")
        window.geometry("1000x500")
        
        columns = ('ID', 'ФИО', 'Паспорт', 'Телефон', 'Email', 'Адрес')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        for client in self.data['clients']:
            tree.insert('', 'end', values=(client['id'], client['full_name'], client['passport'], client['phone'], client['email'], client['address']))
    
    def calculate_insurance(self):
        """Калькулятор стоимости страхования"""
        window = tk.Toplevel(self.root)
        window.title("Калькулятор страхования")
        window.geometry("450x350")
        
        tk.Label(window, text="Тип страхования:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(window, textvariable=type_var, width=30, font=('Arial', 10))
        type_combo['values'] = [f"{t['name']} - {t['base_price']} ₽" for t in self.data['insurance_types']]
        type_combo.grid(row=0, column=1, pady=10)
        
        tk.Label(window, text="Срок (месяцев):", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        duration_var = tk.IntVar(value=12)
        duration_spin = tk.Spinbox(window, from_=1, to=60, textvariable=duration_var, width=30, font=('Arial', 10))
        duration_spin.grid(row=1, column=1, pady=10)
        
        tk.Label(window, text="Коэффициент риска:", font=('Arial', 11)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        risk_var = tk.DoubleVar(value=1.0)
        risk_spin = tk.Spinbox(window, from_=0.5, to=3.0, increment=0.1, textvariable=risk_var, width=30, font=('Arial', 10))
        risk_spin.grid(row=2, column=1, pady=10)
        
        result_label = tk.Label(window, text="", font=('Arial', 14, 'bold'), fg='green')
        result_label.grid(row=4, column=0, columnspan=2, pady=20)
        
        def calculate():
            if not type_var.get():
                messagebox.showerror("Ошибка", "Выберите тип страхования")
                return
            
            type_name = type_var.get().split(' - ')[0]
            itype = next((t for t in self.data['insurance_types'] if t['name'] == type_name), None)
            
            if itype:
                base_price = itype['base_price']
                duration = duration_var.get()
                risk = risk_var.get()
                
                total = base_price * (duration / 12) * risk
                result_label.config(text=f"Итоговая стоимость: {total:.2f} ₽")
        
        tk.Button(window, text="Рассчитать", command=calculate, bg='#4CAF50', fg='white', font=('Arial', 12), width=20).grid(row=3, column=0, columnspan=2, pady=10)
    
    # ФУНКЦИИ КЛИЕНТА
    
    def view_my_policies(self):
        """Просмотр полисов клиента"""
        # Найти клиента по user_id
        client = next((c for c in self.data['clients'] if c['user_id'] == self.current_user['id']), None)
        
        if not client:
            messagebox.showwarning("Предупреждение", "Профиль клиента не найден")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Мои полисы")
        window.geometry("900x400")
        
        columns = ('Номер полиса', 'Тип', 'Дата начала', 'Дата окончания', 'Цена', 'Статус')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(pady=10, padx=10)
        
        my_policies = [p for p in self.data['policies'] if p['client_id'] == client['id']]
        
        for policy in my_policies:
            itype = next((t for t in self.data['insurance_types'] if t['id'] == policy['insurance_type_id']), None)
            tree.insert('', 'end', values=(
                policy['policy_number'], itype['name'] if itype else 'N/A',
                policy['start_date'], policy['end_date'], policy['price'], policy['status']
            ))
    
    def submit_claim(self):
        """Подача заявки на страхование"""
        client = next((c for c in self.data['clients'] if c['user_id'] == self.current_user['id']), None)
        
        if not client:
            messagebox.showwarning("Предупреждение", "Профиль клиента не найден")
            return
        
        my_policies = [p for p in self.data['policies'] if p['client_id'] == client['id'] and p['status'] == 'active']
        
        if not my_policies:
            messagebox.showwarning("Предупреждение", "У вас нет активных полисов")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Подача заявки")
        window.geometry("500x300")
        
        tk.Label(window, text="Выберите полис:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        policy_var = tk.StringVar()
        policy_combo = ttk.Combobox(window, textvariable=policy_var, width=35, font=('Arial', 10))
        policy_combo['values'] = [f"{p['policy_number']}" for p in my_policies]
        policy_combo.grid(row=0, column=1, pady=10)
        
        tk.Label(window, text="Описание:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=10, sticky='ne')
        desc_text = tk.Text(window, width=28, height=5, font=('Arial', 10))
        desc_text.grid(row=1, column=1, pady=10)
        
        tk.Label(window, text="Сумма ущерба:", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        amount_entry = tk.Entry(window, width=37, font=('Arial', 10))
        amount_entry.grid(row=2, column=1, pady=10)
        
        def save_claim():
            if not policy_var.get():
                messagebox.showerror("Ошибка", "Выберите полис")
                return
            
            policy = next((p for p in my_policies if p['policy_number'] == policy_var.get()), None)
            
            new_id = max([c['id'] for c in self.data['claims']], default=0) + 1
            new_claim = {
                'id': new_id,
                'client_id': client['id'],
                'policy_id': policy['id'],
                'description': desc_text.get('1.0', 'end-1c'),
                'amount': int(amount_entry.get()),
                'status': 'pending',
                'created': datetime.now().strftime('%Y-%m-%d'),
                'processed_by': None
            }
            
            self.data['claims'].append(new_claim)
            self.save_data()
            messagebox.showinfo("Успех", "Заявка подана на рассмотрение")
            window.destroy()
        
        tk.Button(window, text="Подать заявку", command=save_claim, bg='#4CAF50', fg='white', font=('Arial', 12)).grid(row=3, column=0, columnspan=2, pady=20)
    
    def check_claim_status(self):
        """Просмотр статуса заявок"""
        client = next((c for c in self.data['clients'] if c['user_id'] == self.current_user['id']), None)
        
        if not client:
            messagebox.showwarning("Предупреждение", "Профиль клиента не найден")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Статус заявок")
        window.geometry("900x400")
        
        columns = ('ID', 'Полис', 'Описание', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(pady=10, padx=10)
        
        my_claims = [c for c in self.data['claims'] if c['client_id'] == client['id']]
        
        for claim in my_claims:
            policy = next((p for p in self.data['policies'] if p['id'] == claim['policy_id']), None)
            tree.insert('', 'end', values=(
                claim['id'], policy['policy_number'] if policy else 'N/A',
                claim['description'][:30], claim['amount'], claim['status'], claim['created']
            ))
    
    def update_profile(self):
        """Обновление личных данных"""
        client = next((c for c in self.data['clients'] if c['user_id'] == self.current_user['id']), None)
        
        if not client:
            messagebox.showwarning("Предупреждение", "Профиль клиента не найден")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Обновление данных")
        window.geometry("500x350")
        
        tk.Label(window, text="Телефон:", font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        phone_entry = tk.Entry(window, width=35, font=('Arial', 10))
        phone_entry.insert(0, client['phone'])
        phone_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(window, text="Email:", font=('Arial', 10)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        email_entry = tk.Entry(window, width=35, font=('Arial', 10))
        email_entry.insert(0, client['email'])
        email_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(window, text="Адрес:", font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        address_entry = tk.Entry(window, width=35, font=('Arial', 10))
        address_entry.insert(0, client['address'])
        address_entry.grid(row=2, column=1, pady=10)
        
        def save_changes():
            client['phone'] = phone_entry.get()
            client['email'] = email_entry.get()
            client['address'] = address_entry.get()
            self.save_data()
            messagebox.showinfo("Успех", "Данные обновлены")
            window.destroy()
        
        tk.Button(window, text="Сохранить изменения", command=save_changes, bg='#4CAF50', fg='white', font=('Arial', 12)).grid(row=3, column=0, columnspan=2, pady=30)

if __name__ == '__main__':
    root = tk.Tk()
    app = InsuranceSystem(root)
    root.mainloop()