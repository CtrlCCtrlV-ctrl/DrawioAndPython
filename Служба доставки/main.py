import tkinter as tk
from tkinter import ttk, messagebox
import json
from auth import AuthSystem

class DeliverySystemApp:
    def __init__(self):
        self.auth = AuthSystem()
        self.data_file = 'data.json'
        self.root = None
    
    def load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def start(self):
        # Запуск приложения с окна входа
        self.show_login_window()
    
    def show_login_window(self):
        # Окно авторизации
        if self.root:
            self.root.destroy()
        
        self.root = tk.Tk()
        self.root.title("Служба доставки - Вход в систему")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Центрирование окна
        self.center_window(self.root, 400, 300)
        
        # Заголовок
        title = tk.Label(self.root, text="🚚 СЛУЖБА ДОСТАВКИ", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # Форма входа
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Логин:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(frame, width=25, show="*", font=("Arial", 10))
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, user = self.auth.authenticate(username, password)
            if success:
                self.show_main_window(user)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        # Кнопки
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Войти", command=login, width=15, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Регистрация", command=self.show_register_window, width=15, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Подсказка
        hint = tk.Label(self.root, text="Демо: admin/admin123, courier1/courier123, client1/client123", 
                       font=("Arial", 8), fg="gray")
        hint.pack(pady=10)
        
        self.root.mainloop()
    
    def show_register_window(self):
        # Окно регистрации
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Регистрация нового пользователя")
        reg_window.geometry("400x350")
        reg_window.resizable(False, False)
        self.center_window(reg_window, 400, 350)
        
        frame = tk.Frame(reg_window)
        frame.pack(pady=20, padx=20)
        
        tk.Label(frame, text="Логин:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(frame, width=25, show="*", font=("Arial", 10))
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="ФИО:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        fullname_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        fullname_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Телефон:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        phone_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        phone_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Роль:", font=("Arial", 10)).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        role_var = tk.StringVar(value="client")
        role_combo = ttk.Combobox(frame, textvariable=role_var, values=["client", "courier"], 
                                 state="readonly", width=23, font=("Arial", 10))
        role_combo.grid(row=4, column=1, padx=5, pady=5)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            phone = phone_entry.get().strip()
            role = role_var.get()
            
            if not all([username, password, fullname, phone]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = self.auth.register_user(username, password, role, fullname, phone)
            if success:
                messagebox.showinfo("Успех", message)
                reg_window.destroy()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(reg_window, text="Зарегистрироваться", command=register, 
                 width=20, font=("Arial", 10)).pack(pady=10)
    
    def show_main_window(self, user):
        # Главное окно системы
        if self.root:
            self.root.destroy()
        
        self.root = tk.Tk()
        self.root.title(f"Служба доставки - {user['full_name']} ({user['role']})")
        self.root.geometry("900x600")
        self.center_window(self.root, 900, 600)
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text=f"👤 {user['full_name']}", bg="#2c3e50", fg="white", 
                font=("Arial", 12)).pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Button(top_frame, text="Выйти", command=self.show_login_window, 
                 bg="#e74c3c", fg="white", font=("Arial", 10)).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Контейнер для контента
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Отображение интерфейса в зависимости от роли
        if user['role'] == 'admin':
            self.show_admin_interface(content_frame, user)
        elif user['role'] == 'courier':
            self.show_courier_interface(content_frame, user)
        elif user['role'] == 'client':
            self.show_client_interface(content_frame, user)
        
        self.root.mainloop()
    
    def show_admin_interface(self, parent, user):
        # Интерфейс администратора
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка: Все заказы
        orders_tab = tk.Frame(notebook)
        notebook.add(orders_tab, text="📦 Все заказы")
        self.create_orders_table(orders_tab, all_orders=True)
        
        # Вкладка: Пользователи
        users_tab = tk.Frame(notebook)
        notebook.add(users_tab, text="👥 Пользователи")
        self.create_users_table(users_tab)
        
        # Вкладка: Тарифы
        tariffs_tab = tk.Frame(notebook)
        notebook.add(tariffs_tab, text="💰 Тарифы")
        self.create_tariffs_table(tariffs_tab)
        
        # Вкладка: Отчеты
        reports_tab = tk.Frame(notebook)
        notebook.add(reports_tab, text="📊 Отчеты")
        self.create_reports_interface(reports_tab)
    
    def show_courier_interface(self, parent, user):
        # Интерфейс курьера
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка: Мои заказы
        orders_tab = tk.Frame(notebook)
        notebook.add(orders_tab, text="📦 Мои заказы")
        self.create_orders_table(orders_tab, courier_id=user['id'])
        
        # Вкладка: Профиль
        profile_tab = tk.Frame(notebook)
        notebook.add(profile_tab, text="👤 Мой профиль")
        self.create_profile_interface(profile_tab, user)
    
    def show_client_interface(self, parent, user):
        # Интерфейс клиента
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка: Создать заказ
        create_tab = tk.Frame(notebook)
        notebook.add(create_tab, text="➕ Создать заказ")
        self.create_order_form(create_tab, user)
        
        # Вкладка: Мои заказы
        orders_tab = tk.Frame(notebook)
        notebook.add(orders_tab, text="📦 Мои заказы")
        self.create_orders_table(orders_tab, client_id=user['id'])
    
    def create_orders_table(self, parent, all_orders=False, courier_id=None, client_id=None):
        # Таблица заказов
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Кнопки управления
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="🔄 Обновить", command=lambda: self.refresh_orders_table(tree, all_orders, courier_id, client_id), 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        if courier_id:
            tk.Button(btn_frame, text="✅ Изменить статус", 
                     command=lambda: self.change_order_status(tree), 
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        if client_id:
            tk.Button(btn_frame, text="❌ Отменить заказ", 
                     command=lambda: self.cancel_order(tree, client_id), 
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Таблица
        columns = ("ID", "Клиент", "Курьер", "Откуда", "Куда", "Статус", "Цена", "Дата")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_orders_table(tree, all_orders, courier_id, client_id)
    
    def refresh_orders_table(self, tree, all_orders=False, courier_id=None, client_id=None):
        # Обновление таблицы заказов
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        orders = data['orders']
        
        # Фильтрация
        if courier_id:
            orders = [o for o in orders if o.get('courier_id') == courier_id]
        elif client_id:
            orders = [o for o in orders if o.get('client_id') == client_id]
        
        # Заполнение таблицы
        for order in orders:
            status_text = {
                'pending': '⏳ Ожидает',
                'in_transit': '🚚 В пути',
                'delivered': '✅ Доставлен',
                'cancelled': '❌ Отменен'
            }.get(order['status'], order['status'])
            
            tree.insert("", tk.END, values=(
                order['id'],
                order.get('client_name', 'N/A'),
                order.get('courier_name', 'Не назначен'),
                order['pickup_address'][:20] + '...',
                order['delivery_address'][:20] + '...',
                status_text,
                f"{order['price']} ₽",
                order['created']
            ), tags=(order['id'],))
    
    def change_order_status(self, tree):
        # Изменение статуса заказа курьером
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите заказ")
            return
        
        order_id = tree.item(selection[0])['values'][0]
        
        status_window = tk.Toplevel(self.root)
        status_window.title("Изменить статус")
        status_window.geometry("300x150")
        self.center_window(status_window, 300, 150)
        
        tk.Label(status_window, text="Выберите новый статус:", font=("Arial", 10)).pack(pady=10)
        
        status_var = tk.StringVar(value="in_transit")
        statuses = [
            ("⏳ Ожидает", "pending"),
            ("🚚 В пути", "in_transit"),
            ("✅ Доставлен", "delivered")
        ]
        
        for text, value in statuses:
            tk.Radiobutton(status_window, text=text, variable=status_var, value=value, 
                          font=("Arial", 10)).pack(anchor=tk.W, padx=20)
        
        def update_status():
            data = self.load_data()
            for order in data['orders']:
                if order['id'] == order_id:
                    order['status'] = status_var.get()
                    break
            self.save_data(data)
            messagebox.showinfo("Успех", "Статус обновлен")
            status_window.destroy()
            self.refresh_orders_table(tree, courier_id=self.auth.current_user['id'])
        
        tk.Button(status_window, text="Сохранить", command=update_status, 
                 font=("Arial", 10)).pack(pady=10)
    
    def cancel_order(self, tree, client_id):
        # Отмена заказа клиентом
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите заказ")
            return
        
        order_id = tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Отменить заказ?"):
            data = self.load_data()
            for order in data['orders']:
                if order['id'] == order_id and order['client_id'] == client_id:
                    if order['status'] in ['pending', 'in_transit']:
                        order['status'] = 'cancelled'
                        self.save_data(data)
                        messagebox.showinfo("Успех", "Заказ отменен")
                        self.refresh_orders_table(tree, client_id=client_id)
                    else:
                        messagebox.showwarning("Внимание", "Заказ нельзя отменить")
                    break
    
    def create_order_form(self, parent, user):
        # Форма создания заказа
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Создание нового заказа", font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = tk.Frame(frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Адрес отправления:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        pickup_entry = tk.Entry(form_frame, width=40, font=("Arial", 10))
        pickup_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Адрес доставки:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        delivery_entry = tk.Entry(form_frame, width=40, font=("Arial", 10))
        delivery_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Описание груза:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        desc_entry = tk.Entry(form_frame, width=40, font=("Arial", 10))
        desc_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Тариф:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        
        data = self.load_data()
        tariff_options = [f"{t['name']} - {t['base_price']}₽ (база)" for t in data['tariffs']]
        tariff_var = tk.StringVar(value=tariff_options[0] if tariff_options else "")
        tariff_combo = ttk.Combobox(form_frame, textvariable=tariff_var, values=tariff_options, 
                                   state="readonly", width=37, font=("Arial", 10))
        tariff_combo.grid(row=3, column=1, padx=5, pady=5)
        
        def create_order():
            pickup = pickup_entry.get().strip()
            delivery = delivery_entry.get().strip()
            description = desc_entry.get().strip()
            
            if not all([pickup, delivery, description]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            # Получение выбранного тарифа
            tariff_index = tariff_options.index(tariff_var.get())
            selected_tariff = data['tariffs'][tariff_index]
            
            # Создание заказа
            data = self.load_data()
            new_id = max([o['id'] for o in data['orders']]) + 1 if data['orders'] else 1
            
            # Назначение курьера (первый доступный)
            couriers = [u for u in self.auth.get_all_users() if u['role'] == 'courier']
            courier = couriers[0] if couriers else None
            
            new_order = {
                "id": new_id,
                "client_id": user['id'],
                "client_name": user['full_name'],
                "courier_id": courier['id'] if courier else None,
                "courier_name": courier['full_name'] if courier else "Не назначен",
                "pickup_address": pickup,
                "delivery_address": delivery,
                "status": "pending",
                "created": "2024-01-17 09:15:00",
                "price": selected_tariff['base_price'],
                "description": description
            }
            
            data['orders'].append(new_order)
            self.save_data(data)
            
            messagebox.showinfo("Успех", f"Заказ #{new_id} создан!\nСтоимость: {new_order['price']}₽")
            pickup_entry.delete(0, tk.END)
            delivery_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
        
        tk.Button(frame, text="Создать заказ", command=create_order, 
                 width=20, font=("Arial", 12, "bold"), bg="#27ae60", fg="white").pack(pady=20)
    
    def create_users_table(self, parent):
        # Таблица пользователей (для админа)
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="🔄 Обновить", command=lambda: self.refresh_users_table(tree), 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="➕ Добавить", command=lambda: self.add_user_admin(tree), 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Удалить", command=lambda: self.delete_user_admin(tree), 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        columns = ("ID", "Логин", "ФИО", "Роль", "Телефон", "Дата создания")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_users_table(tree)
    
    def refresh_users_table(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        users = self.auth.get_all_users()
        for user in users:
            role_text = {'admin': '👑 Админ', 'courier': '🚚 Курьер', 'client': '👤 Клиент'}.get(user['role'], user['role'])
            tree.insert("", tk.END, values=(
                user['id'],
                user['username'],
                user['full_name'],
                role_text,
                user['phone'],
                user['created']
            ), tags=(user['id'],))
    
    def add_user_admin(self, tree):
        # Добавление пользователя администратором
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить пользователя")
        add_window.geometry("400x350")
        self.center_window(add_window, 400, 350)
        
        frame = tk.Frame(add_window)
        frame.pack(pady=20, padx=20)
        
        tk.Label(frame, text="Логин:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="ФИО:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        fullname_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        fullname_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Телефон:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        phone_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        phone_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Роль:", font=("Arial", 10)).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        role_var = tk.StringVar(value="client")
        role_combo = ttk.Combobox(frame, textvariable=role_var, values=["admin", "courier", "client"], 
                                 state="readonly", width=23, font=("Arial", 10))
        role_combo.grid(row=4, column=1, padx=5, pady=5)
        
        def save_user():
            success, message = self.auth.register_user(
                username_entry.get().strip(),
                password_entry.get().strip(),
                role_var.get(),
                fullname_entry.get().strip(),
                phone_entry.get().strip()
            )
            if success:
                messagebox.showinfo("Успех", message)
                add_window.destroy()
                self.refresh_users_table(tree)
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(add_window, text="Сохранить", command=save_user, width=20, font=("Arial", 10)).pack(pady=10)
    
    def delete_user_admin(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        
        user_id = tree.item(selection[0])['values'][0]
        
        if user_id == self.auth.current_user['id']:
            messagebox.showerror("Ошибка", "Нельзя удалить себя")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить пользователя?"):
            self.auth.delete_user(user_id)
            messagebox.showinfo("Успех", "Пользователь удален")
            self.refresh_users_table(tree)
    
    def create_tariffs_table(self, parent):
        # Таблица тарифов
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="🔄 Обновить", command=lambda: self.refresh_tariffs_table(tree), 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="➕ Добавить", command=lambda: self.add_tariff(tree), 
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        columns = ("ID", "Название", "Базовая цена", "Цена за км")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_tariffs_table(tree)
    
    def refresh_tariffs_table(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        for tariff in data['tariffs']:
            tree.insert("", tk.END, values=(
                tariff['id'],
                tariff['name'],
                f"{tariff['base_price']} ₽",
                f"{tariff['price_per_km']} ₽"
            ))
    
    def add_tariff(self, tree):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить тариф")
        add_window.geometry("350x200")
        self.center_window(add_window, 350, 200)
        
        frame = tk.Frame(add_window)
        frame.pack(pady=20, padx=20)
        
        tk.Label(frame, text="Название:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        name_entry = tk.Entry(frame, width=20, font=("Arial", 10))
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Базовая цена:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        base_entry = tk.Entry(frame, width=20, font=("Arial", 10))
        base_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Цена за км:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        km_entry = tk.Entry(frame, width=20, font=("Arial", 10))
        km_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def save_tariff():
            try:
                data = self.load_data()
                new_id = max([t['id'] for t in data['tariffs']]) + 1 if data['tariffs'] else 1
                
                new_tariff = {
                    "id": new_id,
                    "name": name_entry.get().strip(),
                    "base_price": int(base_entry.get().strip()),
                    "price_per_km": int(km_entry.get().strip())
                }
                
                data['tariffs'].append(new_tariff)
                self.save_data(data)
                messagebox.showinfo("Успех", "Тариф добавлен")
                add_window.destroy()
                self.refresh_tariffs_table(tree)
            except ValueError:
                messagebox.showerror("Ошибка", "Цены должны быть числами")
        
        tk.Button(add_window, text="Сохранить", command=save_tariff, width=15, font=("Arial", 10)).pack(pady=10)
    
    def create_reports_interface(self, parent):
        # Интерфейс отчетов
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Статистика и отчеты", font=("Arial", 14, "bold")).pack(pady=10)
        
        stats_frame = tk.Frame(frame, relief=tk.RIDGE, borderwidth=2)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        data = self.load_data()
        users = self.auth.get_all_users()
        
        total_orders = len(data['orders'])
        total_clients = len([u for u in users if u['role'] == 'client'])
        total_couriers = len([u for u in users if u['role'] == 'courier'])
        total_revenue = sum([o['price'] for o in data['orders'] if o['status'] == 'delivered'])
        
        delivered = len([o for o in data['orders'] if o['status'] == 'delivered'])
        in_transit = len([o for o in data['orders'] if o['status'] == 'in_transit'])
        pending = len([o for o in data['orders'] if o['status'] == 'pending'])
        cancelled = len([o for o in data['orders'] if o['status'] == 'cancelled'])
        
        stats_text = f"""
        📊 ОБЩАЯ СТАТИСТИКА
        
        Всего заказов: {total_orders}
        Клиентов: {total_clients}
        Курьеров: {total_couriers}
        Общая выручка: {total_revenue} ₽
        
        📦 СТАТУСЫ ЗАКАЗОВ
        
        ✅ Доставлено: {delivered}
        🚚 В пути: {in_transit}
        ⏳ Ожидает: {pending}
        ❌ Отменено: {cancelled}
        """
        
        tk.Label(stats_frame, text=stats_text, font=("Courier", 11), justify=tk.LEFT).pack(pady=20, padx=20)
    
    def create_profile_interface(self, parent, user):
        # Интерфейс профиля
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="Мой профиль", font=("Arial", 14, "bold")).pack(pady=10)
        
        info_frame = tk.Frame(frame)
        info_frame.pack(pady=20)
        
        tk.Label(info_frame, text=f"👤 ФИО: {user['full_name']}", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"📧 Логин: {user['username']}", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"📱 Телефон: {user['phone']}", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"🎭 Роль: {user['role']}", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        tk.Label(info_frame, text=f"📅 Дата регистрации: {user['created']}", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
    
    def center_window(self, window, width, height):
        # Центрирование окна на экране
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = DeliverySystemApp()
    app.start()