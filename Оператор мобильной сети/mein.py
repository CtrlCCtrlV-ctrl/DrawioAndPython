import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime
from auth import AuthManager

class MobileOperatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Система оператора мобильной связи")
        self.root.geometry("900x600")
        
        self.auth = AuthManager()
        self.data_file = 'data.json'
        self.load_data()
        
        self.show_login()
        
    def load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            # Файл не найден - используем пустые данные
            self.data = {
                "tariffs": [],
                "clients": [],
                "call_history": [],
                "requests": [],
                "services": []
            }
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ОКНО ВХОДА
    def show_login(self):
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Вход в систему", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.login_entry = tk.Entry(frame, width=25)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = tk.Entry(frame, width=25, show='*')
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(frame, text="Войти", command=self.login, width=20).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка
        hint = "Логины по умолчанию:\nadmin / admin\noperator1 / operator\nclient1 / 1234"
        tk.Label(frame, text=hint, fg='gray', justify='left').grid(row=4, column=0, columnspan=2)
    
    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if self.auth.login(username, password):
            role = self.auth.get_role()
            if role == 'administrator':
                self.show_admin_menu()
            elif role == 'operator':
                self.show_operator_menu()
            elif role == 'client':
                self.show_client_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    # МЕНЮ АДМИНИСТРАТОРА
    def show_admin_menu(self):
        self.clear_window()
        
        user = self.auth.get_current_user()
        tk.Label(self.root, text=f"Панель администратора | Пользователь: {user['username']}", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Управление пользователями", self.manage_users),
            ("Управление клиентами", self.manage_clients),
            ("Управление тарифами", self.manage_tariffs),
            ("Обработка заявок", self.process_requests),
            ("Системная статистика", self.system_statistics),
            ("Резервное копирование", self.backup_data),
            ("Выход", self.logout)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            tk.Button(button_frame, text=text, command=command, width=30, height=2).grid(row=row, column=col, padx=10, pady=5)
    
    # МЕНЮ ОПЕРАТОРА
    def show_operator_menu(self):
        self.clear_window()
        
        user = self.auth.get_current_user()
        tk.Label(self.root, text=f"Панель оператора | Пользователь: {user['username']}", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Управление клиентами", self.manage_clients),
            ("Управление тарифами", self.manage_tariffs),
            ("Обработка заявок", self.process_requests),
            ("Просмотр статистики", self.view_statistics),
            ("Управление услугами", self.manage_services),
            ("Выход", self.logout)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            tk.Button(button_frame, text=text, command=command, width=30, height=2).grid(row=row, column=col, padx=10, pady=5)
    
    # МЕНЮ КЛИЕНТА
    def show_client_menu(self):
        self.clear_window()
        
        user = self.auth.get_current_user()
        client = self.get_client_by_phone(user['phone'])
        
        if not client:
            messagebox.showerror("Ошибка", "Данные клиента не найдены")
            self.logout()
            return
        
        tk.Label(self.root, text=f"Личный кабинет | {client['name']}", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Информация о балансе
        info_frame = tk.Frame(self.root, relief='groove', borderwidth=2)
        info_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(info_frame, text=f"Баланс: {client['balance']} ₽", font=('Arial', 12)).pack(pady=5)
        tk.Label(info_frame, text=f"Телефон: {client['phone']}", font=('Arial', 10)).pack(pady=2)
        
        tariff = self.get_tariff_by_id(client['tariff_id'])
        if tariff:
            tk.Label(info_frame, text=f"Тариф: {tariff['name']} ({tariff['price']} ₽/мес)", 
                     font=('Arial', 10)).pack(pady=2)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Просмотр тарифов", self.view_tariffs_client),
            ("Пополнить баланс", lambda: self.topup_balance(client)),
            ("Сменить тариф", lambda: self.change_tariff_client(client)),
            ("История звонков", lambda: self.view_history(client)),
            ("Выход", self.logout)
        ]
        
        for i, (text, command) in enumerate(buttons):
            row = i // 2
            col = i % 2
            tk.Button(button_frame, text=text, command=command, width=30, height=2).grid(row=row, column=col, padx=10, pady=5)
    
    # ФУНКЦИИ АДМИНИСТРАТОРА
    def manage_users(self):
        self.clear_window()
        
        tk.Label(self.root, text="Управление пользователями", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Таблица пользователей
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('Логин', 'Роль', 'Дата создания', 'Телефон')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for user in self.auth.get_all_users():
            tree.insert('', 'end', values=(user['username'], user['role'], user['created'], user.get('phone', '')))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить пользователя", command=self.add_user).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить пользователя", 
                  command=lambda: self.delete_user(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Назад", command=self.show_admin_menu).pack(side='left', padx=5)
    
    def add_user(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление пользователя")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="Логин:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        username_entry = tk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        password_entry = tk.Entry(dialog, show='*')
        password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Роль:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        role_var = tk.StringVar(value='client')
        role_combo = ttk.Combobox(dialog, textvariable=role_var, 
                                  values=['administrator', 'operator', 'client'], state='readonly')
        role_combo.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Телефон:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        phone_entry = tk.Entry(dialog)
        phone_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def save():
            username = username_entry.get()
            password = password_entry.get()
            role = role_var.get()
            phone = phone_entry.get()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            if self.auth.create_user(username, password, role, phone):
                messagebox.showinfo("Успех", "Пользователь создан")
                dialog.destroy()
                self.manage_users()
            else:
                messagebox.showerror("Ошибка", "Пользователь уже существует")
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_user(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        
        item = tree.item(selected[0])
        username = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            self.auth.delete_user(username)
            self.manage_users()
    
    def system_statistics(self):
        self.clear_window()
        
        tk.Label(self.root, text="Системная статистика", font=('Arial', 14, 'bold')).pack(pady=10)
        
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=20)
        
        total_clients = len(self.data['clients'])
        total_users = len(self.auth.get_all_users())
        total_tariffs = len(self.data['tariffs'])
        pending_requests = len([r for r in self.data['requests'] if r['status'] == 'pending'])
        total_balance = sum(c['balance'] for c in self.data['clients'])
        
        stats = [
            ("Всего пользователей системы:", total_users),
            ("Всего клиентов:", total_clients),
            ("Доступных тарифов:", total_tariffs),
            ("Ожидающих заявок:", pending_requests),
            ("Общий баланс клиентов:", f"{total_balance:.2f} ₽"),
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 11)).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            tk.Label(stats_frame, text=str(value), font=('Arial', 11, 'bold')).grid(row=i, column=1, sticky='w', padx=10, pady=5)
        
        tk.Button(self.root, text="Назад", command=self.show_admin_menu, width=20).pack(pady=20)
    
    def backup_data(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backup_{timestamp}.json"
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Успех", f"Резервная копия создана: {backup_file}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать копию: {e}")
    
    # ФУНКЦИИ ОПЕРАТОРА
    def manage_clients(self):
        self.clear_window()
        
        tk.Label(self.root, text="Управление клиентами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('ID', 'Телефон', 'Имя', 'Тариф', 'Баланс', 'Статус')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.column('ID', width=50)
        tree.column('Телефон', width=120)
        tree.column('Имя', width=150)
        tree.column('Тариф', width=100)
        tree.column('Баланс', width=100)
        tree.column('Статус', width=80)
        
        for client in self.data['clients']:
            tariff = self.get_tariff_by_id(client['tariff_id'])
            tariff_name = tariff['name'] if tariff else 'N/A'
            tree.insert('', 'end', values=(
                client['id'], client['phone'], client['name'], 
                tariff_name, f"{client['balance']} ₽", client['status']
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить клиента", command=lambda: self.add_client(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=lambda: self.edit_client(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_client(tree)).pack(side='left', padx=5)
        
        role = self.auth.get_role()
        back_menu = self.show_admin_menu if role == 'administrator' else self.show_operator_menu
        tk.Button(btn_frame, text="Назад", command=back_menu).pack(side='left', padx=5)
    
    def add_client(self, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление клиента")
        dialog.geometry("300x300")
        
        tk.Label(dialog, text="Телефон:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        phone_entry = tk.Entry(dialog)
        phone_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Имя:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Тариф:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        tariff_var = tk.StringVar()
        tariff_combo = ttk.Combobox(dialog, textvariable=tariff_var, state='readonly')
        tariff_combo['values'] = [f"{t['id']}: {t['name']}" for t in self.data['tariffs']]
        tariff_combo.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Баланс:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        balance_entry = tk.Entry(dialog)
        balance_entry.insert(0, "0")
        balance_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def save():
            phone = phone_entry.get()
            name = name_entry.get()
            tariff_str = tariff_var.get()
            balance = balance_entry.get()
            
            if not phone or not name or not tariff_str:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                tariff_id = int(tariff_str.split(':')[0])
                balance_val = float(balance)
            except:
                messagebox.showerror("Ошибка", "Неверный формат данных")
                return
            
            new_id = max([c['id'] for c in self.data['clients']], default=0) + 1
            
            new_client = {
                "id": new_id,
                "phone": phone,
                "name": name,
                "tariff_id": tariff_id,
                "balance": balance_val,
                "status": "active",
                "registered": datetime.now().strftime("%Y-%m-%d")
            }
            
            self.data['clients'].append(new_client)
            self.save_data()
            messagebox.showinfo("Успех", "Клиент добавлен")
            dialog.destroy()
            self.manage_clients()
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=20)
    
    def edit_client(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите клиента")
            return
        
        item = tree.item(selected[0])
        client_id = item['values'][0]
        client = next((c for c in self.data['clients'] if c['id'] == client_id), None)
        
        if not client:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование клиента")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="Имя:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        name_entry = tk.Entry(dialog)
        name_entry.insert(0, client['name'])
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Баланс:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        balance_entry = tk.Entry(dialog)
        balance_entry.insert(0, str(client['balance']))
        balance_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Статус:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        status_var = tk.StringVar(value=client['status'])
        status_combo = ttk.Combobox(dialog, textvariable=status_var, 
                                    values=['active', 'blocked', 'suspended'], state='readonly')
        status_combo.grid(row=2, column=1, padx=10, pady=5)
        
        def save():
            client['name'] = name_entry.get()
            try:
                client['balance'] = float(balance_entry.get())
            except:
                messagebox.showerror("Ошибка", "Неверный формат баланса")
                return
            client['status'] = status_var.get()
            
            self.save_data()
            messagebox.showinfo("Успех", "Данные обновлены")
            dialog.destroy()
            self.manage_clients()
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=3, column=0, columnspan=2, pady=20)
    
    def delete_client(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите клиента")
            return
        
        item = tree.item(selected[0])
        client_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить клиента ID {client_id}?"):
            self.data['clients'] = [c for c in self.data['clients'] if c['id'] != client_id]
            self.save_data()
            self.manage_clients()
    
    def manage_tariffs(self):
        self.clear_window()
        
        tk.Label(self.root, text="Управление тарифами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Цена', 'Минуты', 'Интернет (ГБ)', 'SMS')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for tariff in self.data['tariffs']:
            tree.insert('', 'end', values=(
                tariff['id'], tariff['name'], f"{tariff['price']} ₽",
                tariff['minutes'], tariff['internet'], tariff['sms']
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить тариф", command=lambda: self.add_tariff(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=lambda: self.edit_tariff(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_tariff(tree)).pack(side='left', padx=5)
        
        role = self.auth.get_role()
        back_menu = self.show_admin_menu if role == 'administrator' else self.show_operator_menu
        tk.Button(btn_frame, text="Назад", command=back_menu).pack(side='left', padx=5)
    
    def add_tariff(self, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление тарифа")
        dialog.geometry("350x350")
        
        fields = [
            ("Название:", tk.Entry(dialog)),
            ("Цена (₽/мес):", tk.Entry(dialog)),
            ("Минуты:", tk.Entry(dialog)),
            ("Интернет (ГБ):", tk.Entry(dialog)),
            ("SMS:", tk.Entry(dialog)),
        ]
        
        for i, (label, entry) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry.grid(row=i, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Описание:").grid(row=5, column=0, padx=10, pady=5, sticky='ne')
        desc_text = tk.Text(dialog, width=20, height=4)
        desc_text.grid(row=5, column=1, padx=10, pady=5)
        
        def save():
            try:
                name = fields[0][1].get()
                price = float(fields[1][1].get())
                minutes = fields[2][1].get()
                internet = fields[3][1].get()
                sms = fields[4][1].get()
                description = desc_text.get("1.0", "end-1c")
                
                if minutes.lower() != 'unlimited':
                    minutes = int(minutes)
                if internet.lower() != 'unlimited':
                    internet = int(internet)
                if sms.lower() != 'unlimited':
                    sms = int(sms)
                
                new_id = max([t['id'] for t in self.data['tariffs']], default=0) + 1
                
                new_tariff = {
                    "id": new_id,
                    "name": name,
                    "price": price,
                    "minutes": minutes,
                    "internet": internet,
                    "sms": sms,
                    "description": description
                }
                
                self.data['tariffs'].append(new_tariff)
                self.save_data()
                messagebox.showinfo("Успех", "Тариф добавлен")
                dialog.destroy()
                self.manage_tariffs()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Неверный формат данных: {e}")
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=6, column=0, columnspan=2, pady=20)
    
    def edit_tariff(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите тариф")
            return
        
        item = tree.item(selected[0])
        tariff_id = item['values'][0]
        tariff = next((t for t in self.data['tariffs'] if t['id'] == tariff_id), None)
        
        if not tariff:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование тарифа")
        dialog.geometry("350x250")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        name_entry = tk.Entry(dialog)
        name_entry.insert(0, tariff['name'])
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Цена:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        price_entry = tk.Entry(dialog)
        price_entry.insert(0, str(tariff['price']))
        price_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def save():
            tariff['name'] = name_entry.get()
            try:
                tariff['price'] = float(price_entry.get())
            except:
                messagebox.showerror("Ошибка", "Неверный формат цены")
                return
            
            self.save_data()
            messagebox.showinfo("Успех", "Тариф обновлен")
            dialog.destroy()
            self.manage_tariffs()
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=2, column=0, columnspan=2, pady=20)
    
    def delete_tariff(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите тариф")
            return
        
        item = tree.item(selected[0])
        tariff_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить тариф ID {tariff_id}?"):
            self.data['tariffs'] = [t for t in self.data['tariffs'] if t['id'] != tariff_id]
            self.save_data()
            self.manage_tariffs()
    
    def process_requests(self):
        self.clear_window()
        
        tk.Label(self.root, text="Обработка заявок", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('ID', 'Телефон', 'Тип', 'Новый тариф', 'Статус', 'Дата')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for req in self.data['requests']:
            tariff = self.get_tariff_by_id(req.get('new_tariff_id', 0))
            tariff_name = tariff['name'] if tariff else 'N/A'
            tree.insert('', 'end', values=(
                req['id'], req['phone'], req['type'], 
                tariff_name, req['status'], req['date']
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Одобрить", 
                  command=lambda: self.approve_request(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Отклонить", 
                  command=lambda: self.reject_request(tree)).pack(side='left', padx=5)
        
        role = self.auth.get_role()
        back_menu = self.show_admin_menu if role == 'administrator' else self.show_operator_menu
        tk.Button(btn_frame, text="Назад", command=back_menu).pack(side='left', padx=5)
    
    def approve_request(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заявку")
            return
        
        item = tree.item(selected[0])
        req_id = item['values'][0]
        
        request = next((r for r in self.data['requests'] if r['id'] == req_id), None)
        if not request or request['status'] != 'pending':
            messagebox.showwarning("Внимание", "Заявка уже обработана")
            return
        
        if request['type'] == 'change_tariff':
            client = self.get_client_by_phone(request['phone'])
            if client:
                client['tariff_id'] = request['new_tariff_id']
                request['status'] = 'approved'
                self.save_data()
                messagebox.showinfo("Успех", "Заявка одобрена")
                self.process_requests()
    
    def reject_request(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заявку")
            return
        
        item = tree.item(selected[0])
        req_id = item['values'][0]
        
        request = next((r for r in self.data['requests'] if r['id'] == req_id), None)
        if not request or request['status'] != 'pending':
            messagebox.showwarning("Внимание", "Заявка уже обработана")
            return
        
        request['status'] = 'rejected'
        self.save_data()
        messagebox.showinfo("Успех", "Заявка отклонена")
        self.process_requests()
    
    def view_statistics(self):
        self.clear_window()
        
        tk.Label(self.root, text="Статистика клиентов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=20)
        
        total_clients = len(self.data['clients'])
        active_clients = len([c for c in self.data['clients'] if c['status'] == 'active'])
        total_balance = sum(c['balance'] for c in self.data['clients'])
        avg_balance = total_balance / total_clients if total_clients > 0 else 0
        
        stats = [
            ("Всего клиентов:", total_clients),
            ("Активных клиентов:", active_clients),
            ("Общий баланс:", f"{total_balance:.2f} ₽"),
            ("Средний баланс:", f"{avg_balance:.2f} ₽"),
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 11)).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            tk.Label(stats_frame, text=str(value), font=('Arial', 11, 'bold')).grid(row=i, column=1, sticky='w', padx=10, pady=5)
        
        tk.Button(self.root, text="Назад", command=self.show_operator_menu, width=20).pack(pady=20)
    
    def manage_services(self):
        self.clear_window()
        
        tk.Label(self.root, text="Управление услугами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Цена', 'Описание')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        tree.column('ID', width=50)
        tree.column('Название', width=200)
        tree.column('Цена', width=100)
        tree.column('Описание', width=300)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for service in self.data['services']:
            tree.insert('', 'end', values=(
                service['id'], service['name'], 
                f"{service['price']} ₽", service['description']
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить услугу", command=lambda: self.add_service(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Назад", command=self.show_operator_menu).pack(side='left', padx=5)
    
    def add_service(self, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление услуги")
        dialog.geometry("350x250")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        name_entry = tk.Entry(dialog, width=25)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Цена:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        price_entry = tk.Entry(dialog, width=25)
        price_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Описание:").grid(row=2, column=0, padx=10, pady=5, sticky='ne')
        desc_text = tk.Text(dialog, width=25, height=5)
        desc_text.grid(row=2, column=1, padx=10, pady=5)
        
        def save():
            try:
                name = name_entry.get()
                price = float(price_entry.get())
                description = desc_text.get("1.0", "end-1c")
                
                if not name:
                    messagebox.showerror("Ошибка", "Введите название")
                    return
                
                new_id = max([s['id'] for s in self.data['services']], default=0) + 1
                
                new_service = {
                    "id": new_id,
                    "name": name,
                    "price": price,
                    "description": description
                }
                
                self.data['services'].append(new_service)
                self.save_data()
                messagebox.showinfo("Успех", "Услуга добавлена")
                dialog.destroy()
                self.manage_services()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка: {e}")
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=3, column=0, columnspan=2, pady=20)
    
    # ФУНКЦИИ КЛИЕНТА
    def view_tariffs_client(self):
        self.clear_window()
        
        tk.Label(self.root, text="Доступные тарифы", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        for tariff in self.data['tariffs']:
            tariff_frame = tk.Frame(frame, relief='groove', borderwidth=2)
            tariff_frame.pack(fill='x', pady=5, padx=10)
            
            tk.Label(tariff_frame, text=tariff['name'], font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=5)
            tk.Label(tariff_frame, text=f"Цена: {tariff['price']} ₽/мес").pack(anchor='w', padx=10)
            tk.Label(tariff_frame, text=f"Минуты: {tariff['minutes']}").pack(anchor='w', padx=10)
            tk.Label(tariff_frame, text=f"Интернет: {tariff['internet']} ГБ").pack(anchor='w', padx=10)
            tk.Label(tariff_frame, text=f"SMS: {tariff['sms']}").pack(anchor='w', padx=10)
            tk.Label(tariff_frame, text=tariff['description'], fg='gray').pack(anchor='w', padx=10, pady=5)
        
        tk.Button(self.root, text="Назад", command=self.show_client_menu, width=20).pack(pady=20)
    
    def topup_balance(self, client):
        amount = simpledialog.askfloat("Пополнение", "Введите сумму пополнения (₽):", minvalue=1)
        if amount:
            client['balance'] += amount
            self.save_data()
            messagebox.showinfo("Успех", f"Баланс пополнен на {amount} ₽")
            self.show_client_menu()
    
    def change_tariff_client(self, client):
        dialog = tk.Toplevel(self.root)
        dialog.title("Смена тарифа")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Выберите новый тариф:", font=('Arial', 11)).pack(pady=10)
        
        tariff_var = tk.StringVar()
        tariff_combo = ttk.Combobox(dialog, textvariable=tariff_var, state='readonly', width=30)
        tariff_combo['values'] = [f"{t['id']}: {t['name']} - {t['price']} ₽" for t in self.data['tariffs']]
        tariff_combo.pack(pady=10)
        
        def submit():
            tariff_str = tariff_var.get()
            if not tariff_str:
                messagebox.showerror("Ошибка", "Выберите тариф")
                return
            
            tariff_id = int(tariff_str.split(':')[0])
            
            new_req_id = max([r['id'] for r in self.data['requests']], default=0) + 1
            
            new_request = {
                "id": new_req_id,
                "phone": client['phone'],
                "type": "change_tariff",
                "new_tariff_id": tariff_id,
                "status": "pending",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            self.data['requests'].append(new_request)
            self.save_data()
            messagebox.showinfo("Успех", "Заявка на смену тарифа отправлена")
            dialog.destroy()
        
        tk.Button(dialog, text="Отправить заявку", command=submit, width=20).pack(pady=10)
    
    def view_history(self, client):
        self.clear_window()
        
        tk.Label(self.root, text="История звонков", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('Дата', 'Тип', 'Номер', 'Длительность (мин)')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        client_history = [h for h in self.data['call_history'] if h['phone'] == client['phone']]
        
        for call in client_history:
            tree.insert('', 'end', values=(
                call['date'], call['type'], call['number'], call['duration']
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        tk.Button(self.root, text="Назад", command=self.show_client_menu, width=20).pack(pady=20)
    
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    def get_client_by_phone(self, phone):
        return next((c for c in self.data['clients'] if c['phone'] == phone), None)
    
    def get_tariff_by_id(self, tariff_id):
        return next((t for t in self.data['tariffs'] if t['id'] == tariff_id), None)
    
    def logout(self):
        self.auth.logout()
        self.show_login()
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = MobileOperatorApp()
    app.run()