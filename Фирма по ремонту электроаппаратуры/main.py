import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from auth import AuthManager

class RepairServiceApp:
    """Главное приложение системы ремонтной мастерской"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Система управления ремонтной мастерской")
        self.root.geometry("1200x700")
        
        self.auth_manager = AuthManager()
        self.data_file = 'data.json'

        self.current_frame = None
        self.show_login_window()
        
    
    def load_data(self):
        """Загрузка данных из файла"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_frame(self):
        """Очистка текущего фрейма"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login_window(self):
        """Окно входа в систему"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(expand=True)
        
        # Заголовок
        tk.Label(self.current_frame, text="Вход в систему", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Поля ввода
        tk.Label(self.current_frame, text="Имя пользователя:").pack(pady=5)
        self.username_entry = tk.Entry(self.current_frame, width=30)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.current_frame, text="Пароль:").pack(pady=5)
        self.password_entry = tk.Entry(self.current_frame, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        # Кнопка входа
        tk.Button(self.current_frame, text="Войти", 
                 command=self.login, width=20).pack(pady=20)
        
        # Информация о тестовых учетных записях
        info_frame = tk.Frame(self.current_frame)
        info_frame.pack(pady=20)
        
        tk.Label(info_frame, text="Тестовые учетные записи:", 
                font=("Arial", 10, "italic")).pack()
        tk.Label(info_frame, text="Администратор: admin / admin123", 
                font=("Arial", 9)).pack()
        tk.Label(info_frame, text="Мастер: master / master123", 
                font=("Arial", 9)).pack()
        tk.Label(info_frame, text="Клиент: client / client123", 
                font=("Arial", 9)).pack()
    
    def login(self):
        """Обработка входа"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        success, role = self.auth_manager.authenticate(username, password)
        
        if success:
            if role == "administrator":
                self.show_admin_panel()
            elif role == "master":
                self.show_master_panel()
            elif role == "client":
                self.show_client_panel()
        else:
            messagebox.showerror("Ошибка", "Неверные учетные данные")
    
    def show_admin_panel(self):
        """Панель администратора"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        
        # Заголовок
        header_frame = tk.Frame(self.current_frame, bg="#2c3e50")
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=f"Панель администратора - {self.auth_manager.current_user['full_name']}", 
                font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(side="left", padx=20, pady=10)
        
        tk.Button(header_frame, text="Выход", command=self.logout).pack(side="right", padx=20, pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка управления пользователями
        users_tab = tk.Frame(notebook)
        notebook.add(users_tab, text="Пользователи")
        self.create_users_management(users_tab)
        
        # Вкладка статистики
        stats_tab = tk.Frame(notebook)
        notebook.add(stats_tab, text="Статистика")
        self.create_statistics_view(stats_tab)
        
        # Вкладка справочников
        catalog_tab = tk.Frame(notebook)
        notebook.add(catalog_tab, text="Справочники")
        self.create_catalog_management(catalog_tab)
        
        # Вкладка заказов
        orders_tab = tk.Frame(notebook)
        notebook.add(orders_tab, text="Все заказы")
        self.create_orders_view(orders_tab, is_admin=True)
    
    def create_users_management(self, parent):
        """Создание интерфейса управления пользователями"""
        # Кнопки управления
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="Добавить пользователя", 
                 command=self.add_user_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить пользователя", 
                 command=self.delete_user).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", 
                 command=lambda: self.refresh_users_list()).pack(side="left", padx=5)
        
        # Таблица пользователей
        columns = ("Имя пользователя", "ФИО", "Роль", "Дата создания")
        self.users_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=200)
        
        self.users_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.users_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_users_list()
    
    def refresh_users_list(self):
        """Обновление списка пользователей"""
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        users = self.auth_manager.get_all_users()
        for user in users:
            role_display = {
                "administrator": "Администратор",
                "master": "Мастер",
                "client": "Клиент"
            }.get(user['role'], user['role'])
            
            self.users_tree.insert("", "end", values=(
                user['username'],
                user['full_name'],
                role_display,
                user['created'][:10]
            ))
    
    def add_user_dialog(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Имя пользователя:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        username_entry = tk.Entry(dialog, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        password_entry = tk.Entry(dialog, width=30, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="ФИО:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        fullname_entry = tk.Entry(dialog, width=30)
        fullname_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Роль:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        role_var = tk.StringVar(value="client")
        role_combo = ttk.Combobox(dialog, textvariable=role_var, width=28, state="readonly")
        role_combo['values'] = ("administrator", "master", "client")
        role_combo.grid(row=3, column=1, padx=10, pady=10)
        
        def save_user():
            success, message = self.auth_manager.register_user(
                username_entry.get(),
                password_entry.get(),
                role_var.get(),
                fullname_entry.get()
            )
            if success:
                messagebox.showinfo("Успех", message)
                self.refresh_users_list()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(dialog, text="Сохранить", command=save_user).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_user(self):
        """Удаление выбранного пользователя"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            success, message = self.auth_manager.delete_user(username)
            if success:
                messagebox.showinfo("Успех", message)
                self.refresh_users_list()
            else:
                messagebox.showerror("Ошибка", message)
    
    def create_statistics_view(self, parent):
        """Создание представления статистики"""
        data = self.load_data()
        stats = data.get('statistics', {})
        
        # Основная статистика
        stats_frame = tk.Frame(parent)
        stats_frame.pack(pady=20)
        
        tk.Label(stats_frame, text="Общая статистика", 
                font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(stats_frame, text="Всего заказов:").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        tk.Label(stats_frame, text=str(stats.get('total_orders', 0))).grid(row=1, column=1, padx=20, pady=5)
        
        tk.Label(stats_frame, text="Завершенных заказов:").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        tk.Label(stats_frame, text=str(stats.get('completed_orders', 0))).grid(row=2, column=1, padx=20, pady=5)
        
        tk.Label(stats_frame, text="Общая выручка:").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        tk.Label(stats_frame, text=f"{stats.get('total_revenue', 0)} руб.").grid(row=3, column=1, padx=20, pady=5)
        
        # График статистики по месяцам (упрощенный)
        chart_frame = tk.Frame(parent)
        chart_frame.pack(pady=20)
        
        tk.Label(chart_frame, text="Статистика по статусам заказов", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        orders = data.get('orders', [])
        status_counts = {}
        for order in orders:
            status = order.get('status', 'Неизвестно')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in status_counts.items():
            row_frame = tk.Frame(chart_frame)
            row_frame.pack(fill="x", padx=20, pady=2)
            tk.Label(row_frame, text=f"{status}:", width=20, anchor="w").pack(side="left")
            tk.Label(row_frame, text="█" * min(count * 5, 50), fg="blue").pack(side="left")
            tk.Label(row_frame, text=f" {count}").pack(side="left")
    
    def create_catalog_management(self, parent):
        """Управление справочником деталей"""
        # Кнопки управления
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="Добавить деталь", 
                 command=self.add_part_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Изменить количество", 
                 command=self.edit_part_quantity).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", 
                 command=lambda: self.refresh_parts_list()).pack(side="left", padx=5)
        
        # Таблица деталей
        columns = ("ID", "Название", "Количество", "Цена")
        self.parts_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.parts_tree.heading(col, text=col)
            self.parts_tree.column(col, width=200)
        
        self.parts_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_parts_list()
    
    def refresh_parts_list(self):
        """Обновление списка деталей"""
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        data = self.load_data()
        parts = data.get('parts', [])
        
        for part in parts:
            self.parts_tree.insert("", "end", values=(
                part['id'],
                part['name'],
                part['quantity'],
                f"{part['price']} руб."
            ))
    
    def add_part_dialog(self):
        """Диалог добавления детали"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить деталь")
        dialog.geometry("400x250")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Количество:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        quantity_entry = tk.Entry(dialog, width=30)
        quantity_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Цена:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        price_entry = tk.Entry(dialog, width=30)
        price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save_part():
            try:
                data = self.load_data()
                parts = data.get('parts', [])
                
                new_id = max([p['id'] for p in parts], default=0) + 1
                new_part = {
                    'id': new_id,
                    'name': name_entry.get(),
                    'quantity': int(quantity_entry.get()),
                    'price': float(price_entry.get())
                }
                
                parts.append(new_part)
                data['parts'] = parts
                self.save_data(data)
                
                messagebox.showinfo("Успех", "Деталь добавлена")
                self.refresh_parts_list()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте правильность введенных данных")
        
        tk.Button(dialog, text="Сохранить", command=save_part).grid(row=3, column=0, columnspan=2, pady=20)
    
    def edit_part_quantity(self):
        """Изменение количества детали"""
        selected = self.parts_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите деталь")
            return
        
        item = self.parts_tree.item(selected[0])
        part_id = item['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменить количество")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Новое количество:").pack(pady=10)
        quantity_entry = tk.Entry(dialog, width=20)
        quantity_entry.pack(pady=10)
        
        def update_quantity():
            try:
                new_quantity = int(quantity_entry.get())
                data = self.load_data()
                parts = data.get('parts', [])
                
                for part in parts:
                    if part['id'] == part_id:
                        part['quantity'] = new_quantity
                        break
                
                data['parts'] = parts
                self.save_data(data)
                
                messagebox.showinfo("Успех", "Количество обновлено")
                self.refresh_parts_list()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное число")
        
        tk.Button(dialog, text="Сохранить", command=update_quantity).pack(pady=20)
    
    def show_master_panel(self):
        """Панель мастера"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        
        # Заголовок
        header_frame = tk.Frame(self.current_frame, bg="#27ae60")
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=f"Панель мастера - {self.auth_manager.current_user['full_name']}", 
                font=("Arial", 14, "bold"), bg="#27ae60", fg="white").pack(side="left", padx=20, pady=10)
        
        tk.Button(header_frame, text="Выход", command=self.logout).pack(side="right", padx=20, pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка заказов
        orders_tab = tk.Frame(notebook)
        notebook.add(orders_tab, text="Заказы")
        self.create_orders_view(orders_tab, is_master=True)
        
        # Вкладка склада
        warehouse_tab = tk.Frame(notebook)
        notebook.add(warehouse_tab, text="Склад деталей")
        self.create_warehouse_view(warehouse_tab)
    
    def create_orders_view(self, parent, is_admin=False, is_master=False, is_client=False):
        """Создание представления заказов"""
        # Кнопки управления
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        if is_client:
            tk.Button(btn_frame, text="Новый заказ", 
                     command=self.create_order_dialog).pack(side="left", padx=5)
        
        if is_master:
            tk.Button(btn_frame, text="Изменить статус", 
                     command=self.change_order_status).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Добавить детали", 
                     command=self.add_parts_to_order).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Обновить", 
                 command=lambda: self.refresh_orders_list(is_client)).pack(side="left", padx=5)
        
        # Таблица заказов
        columns = ("ID", "Клиент", "Устройство", "Описание", "Статус", "Дата", "Стоимость")
        self.orders_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            if col == "Описание":
                self.orders_tree.column(col, width=250)
            else:
                self.orders_tree.column(col, width=120)
        
        self.orders_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.orders_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_orders_list(is_client)
    
    def refresh_orders_list(self, is_client=False):
        """Обновление списка заказов"""
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        data = self.load_data()
        orders = data.get('orders', [])
        
        # Фильтрация для клиента
        if is_client:
            client_name = self.auth_manager.current_user['full_name']
            orders = [o for o in orders if o.get('client') == client_name]
        
        for order in orders:
            self.orders_tree.insert("", "end", values=(
                order.get('id', ''),
                order.get('client', ''),
                order.get('device', ''),
                order.get('description', ''),
                order.get('status', 'Новый'),
                order.get('date', ''),
                f"{order.get('cost', 0)} руб."
            ))
    
    def create_order_dialog(self):
        """Диалог создания заказа"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый заказ")
        dialog.geometry("500x400")
        
        tk.Label(dialog, text="Устройство:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        device_entry = tk.Entry(dialog, width=40)
        device_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Описание проблемы:").grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        description_text = tk.Text(dialog, width=40, height=5)
        description_text.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Контактный телефон:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        phone_entry = tk.Entry(dialog, width=40)
        phone_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save_order():
            data = self.load_data()
            orders = data.get('orders', [])
            
            new_id = max([o.get('id', 0) for o in orders], default=0) + 1
            new_order = {
                'id': new_id,
                'client': self.auth_manager.current_user['full_name'],
                'device': device_entry.get(),
                'description': description_text.get('1.0', 'end-1c'),
                'phone': phone_entry.get(),
                'status': 'Новый',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'cost': 0,
                'parts_used': []
            }
            
            orders.append(new_order)
            data['orders'] = orders
            
            # Обновление статистики
            stats = data.get('statistics', {})
            stats['total_orders'] = stats.get('total_orders', 0) + 1
            data['statistics'] = stats
            
            self.save_data(data)
            
            messagebox.showinfo("Успех", f"Заказ №{new_id} создан")
            self.refresh_orders_list(True)
            dialog.destroy()
        
        tk.Button(dialog, text="Создать заказ", command=save_order).grid(row=3, column=0, columnspan=2, pady=20)
    
    def change_order_status(self):
        """Изменение статуса заказа"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ")
            return
        
        item = self.orders_tree.item(selected[0])
        order_id = item['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменить статус")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text="Новый статус:").pack(pady=10)
        
        status_var = tk.StringVar(value="В работе")
        status_combo = ttk.Combobox(dialog, textvariable=status_var, width=30, state="readonly")
        status_combo['values'] = ("Новый", "В работе", "Ожидание деталей", "Готов", "Выдан")
        status_combo.pack(pady=10)
        
        def update_status():
            data = self.load_data()
            orders = data.get('orders', [])
            
            for order in orders:
                if order.get('id') == order_id:
                    old_status = order.get('status')
                    new_status = status_var.get()
                    order['status'] = new_status
                    
                    # Обновление статистики при завершении
                    if new_status == "Выдан" and old_status != "Выдан":
                        stats = data.get('statistics', {})
                        stats['completed_orders'] = stats.get('completed_orders', 0) + 1
                        stats['total_revenue'] = stats.get('total_revenue', 0) + order.get('cost', 0)
                        data['statistics'] = stats
                    break
            
            data['orders'] = orders
            self.save_data(data)
            
            messagebox.showinfo("Успех", "Статус обновлен")
            self.refresh_orders_list()
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=update_status).pack(pady=20)
    
    def add_parts_to_order(self):
        """Добавление деталей к заказу"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ")
            return
        
        item = self.orders_tree.item(selected[0])
        order_id = item['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить детали к заказу")
        dialog.geometry("500x400")
        
        # Список доступных деталей
        data = self.load_data()
        parts = data.get('parts', [])
        
        tk.Label(dialog, text="Выберите деталь:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        part_var = tk.StringVar()
        part_combo = ttk.Combobox(dialog, textvariable=part_var, width=40, state="readonly")
        part_combo['values'] = [f"{p['id']} - {p['name']} ({p['quantity']} шт.)" for p in parts]
        part_combo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Количество:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        quantity_entry = tk.Entry(dialog, width=20)
        quantity_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Список добавленных деталей
        tk.Label(dialog, text="Добавленные детали:").grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        added_parts_listbox = tk.Listbox(dialog, width=60, height=10)
        added_parts_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        added_parts = []
        
        def add_part():
            try:
                part_info = part_var.get()
                if not part_info:
                    messagebox.showwarning("Предупреждение", "Выберите деталь")
                    return
                
                part_id = int(part_info.split(' - ')[0])
                quantity = int(quantity_entry.get())
                
                # Поиск детали
                part = next((p for p in parts if p['id'] == part_id), None)
                if not part:
                    return
                
                if quantity > part['quantity']:
                    messagebox.showerror("Ошибка", "Недостаточно деталей на складе")
                    return
                
                added_parts.append({'id': part_id, 'name': part['name'], 'quantity': quantity, 'price': part['price']})
                added_parts_listbox.insert(tk.END, f"{part['name']} - {quantity} шт. - {quantity * part['price']} руб.")
                
                quantity_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное количество")
        
        tk.Button(dialog, text="Добавить деталь", command=add_part).grid(row=1, column=2, padx=10)
        
        def save_parts():
            if not added_parts:
                messagebox.showwarning("Предупреждение", "Добавьте хотя бы одну деталь")
                return
            
            data = self.load_data()
            orders = data.get('orders', [])
            parts = data.get('parts', [])
            
            total_cost = 0
            
            # Обновление заказа
            for order in orders:
                if order.get('id') == order_id:
                    if 'parts_used' not in order:
                        order['parts_used'] = []
                    
                    for added_part in added_parts:
                        order['parts_used'].append(added_part)
                        total_cost += added_part['quantity'] * added_part['price']
                        
                        # Уменьшение количества на складе
                        for part in parts:
                            if part['id'] == added_part['id']:
                                part['quantity'] -= added_part['quantity']
                                break
                    
                    order['cost'] = order.get('cost', 0) + total_cost
                    break
            
            data['orders'] = orders
            data['parts'] = parts
            self.save_data(data)
            
            messagebox.showinfo("Успех", f"Детали добавлены. Стоимость: {total_cost} руб.")
            self.refresh_orders_list()
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_parts).grid(row=4, column=0, columnspan=3, pady=20)
    
    def create_warehouse_view(self, parent):
        """Представление склада для мастера"""
        # Таблица деталей
        columns = ("ID", "Название", "Доступно", "Цена")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Загрузка данных
        data = self.load_data()
        parts = data.get('parts', [])
        
        for part in parts:
            color = "red" if part['quantity'] < 10 else "black"
            tree.insert("", "end", values=(
                part['id'],
                part['name'],
                part['quantity'],
                f"{part['price']} руб."
            ))
        
        # Информация
        info_frame = tk.Frame(parent)
        info_frame.pack(pady=10)
        tk.Label(info_frame, text="* Детали с количеством менее 10 шт. требуют пополнения", 
                font=("Arial", 9, "italic")).pack()
    
    def show_client_panel(self):
        """Панель клиента"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True)
        
        # Заголовок
        header_frame = tk.Frame(self.current_frame, bg="#3498db")
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text=f"Панель клиента - {self.auth_manager.current_user['full_name']}", 
                font=("Arial", 14, "bold"), bg="#3498db", fg="white").pack(side="left", padx=20, pady=10)
        
        tk.Button(header_frame, text="Выход", command=self.logout).pack(side="right", padx=20, pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.current_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка заказов
        orders_tab = tk.Frame(notebook)
        notebook.add(orders_tab, text="Мои заказы")
        self.create_orders_view(orders_tab, is_client=True)
        
        # Вкладка отзывов
        feedback_tab = tk.Frame(notebook)
        notebook.add(feedback_tab, text="Оставить отзыв")
        self.create_feedback_view(feedback_tab)
    
    def create_feedback_view(self, parent):
        """Форма для отзывов"""
        tk.Label(parent, text="Оставить отзыв о работе сервиса", 
                font=("Arial", 14, "bold")).pack(pady=20)
        
        tk.Label(parent, text="Номер заказа:").pack(pady=5)
        order_entry = tk.Entry(parent, width=30)
        order_entry.pack(pady=5)
        
        tk.Label(parent, text="Оценка (1-5):").pack(pady=5)
        rating_var = tk.StringVar(value="5")
        rating_combo = ttk.Combobox(parent, textvariable=rating_var, width=28, state="readonly")
        rating_combo['values'] = ("1", "2", "3", "4", "5")
        rating_combo.pack(pady=5)
        
        tk.Label(parent, text="Комментарий:").pack(pady=5)
        comment_text = tk.Text(parent, width=50, height=10)
        comment_text.pack(pady=5)
        
        def submit_feedback():
            order_id = order_entry.get()
            rating = rating_var.get()
            comment = comment_text.get('1.0', 'end-1c')
            
            if not order_id:
                messagebox.showwarning("Предупреждение", "Введите номер заказа")
                return
            
            # Здесь можно добавить сохранение отзыва
            messagebox.showinfo("Спасибо", "Ваш отзыв принят!")
            order_entry.delete(0, tk.END)
            comment_text.delete('1.0', tk.END)
        
        tk.Button(parent, text="Отправить отзыв", command=submit_feedback).pack(pady=20)
    
    def logout(self):
        """Выход из системы"""
        self.auth_manager.logout()
        self.show_login_window()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RepairServiceApp()
    app.run()