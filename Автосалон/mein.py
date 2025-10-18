import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

DATA_FILE = "data.json"

class AutostoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Автосалон - Информационная система")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        self.current_user = None

        # Показать окно входа
        self.show_login_screen()
    
    
    def load_data(self):
        """Загрузка данных из файла"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна от всех виджетов"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Автосалон", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(frame, text="Авторизация в системе", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="Логин:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        username_entry = tk.Entry(frame, font=("Arial", 11), width=25)
        username_entry.grid(row=2, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=10)
        password_entry = tk.Entry(frame, font=("Arial", 11), width=25, show="*")
        password_entry.grid(row=3, column=1, pady=10)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            user = auth.authenticate(username, password)
            if user:
                self.current_user = user
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", font=("Arial", 11), width=20, command=login).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Подсказки для тестирования
        tk.Label(frame, text="Тестовые учетные записи:", font=("Arial", 9, "italic")).grid(row=5, column=0, columnspan=2, pady=(30, 5))
        tk.Label(frame, text="admin/admin123 | manager/manager123 | client/client123", font=("Arial", 8)).grid(row=6, column=0, columnspan=2)
        
        password_entry.bind('<Return>', lambda e: login())
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        # Шапка
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill="x")
        
        tk.Label(header, text=f"Автосалон | {self.current_user['full_name']} ({self.current_user['role']})", 
                 bg="#2c3e50", fg="white", font=("Arial", 12)).pack(side="left", padx=20, pady=15)
        
        tk.Button(header, text="Выход", command=self.logout, bg="#e74c3c", fg="white", 
                 font=("Arial", 10), padx=15).pack(side="right", padx=20, pady=15)
        
        # Контейнер для меню
        menu_frame = tk.Frame(self.root, padx=20, pady=20)
        menu_frame.pack(fill="both", expand=True)
        
        if self.current_user['role'] == 'administrator':
            self.show_admin_menu(menu_frame)
        elif self.current_user['role'] == 'manager':
            self.show_manager_menu(menu_frame)
        elif self.current_user['role'] == 'client':
            self.show_client_menu(menu_frame)
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=("Arial", 18, "bold")).pack(pady=20)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=20)
        
        buttons = [
            ("Управление пользователями", self.manage_users_window),
            ("Управление автомобилями", self.manage_cars_window),
            ("Просмотр всех продаж", self.view_all_sales_window),
            ("Управление сотрудниками", self.manage_staff_window),
            ("Генерация отчетов", self.generate_reports_window)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=("Arial", 12), width=30, height=2, 
                     command=command).grid(row=i, column=0, pady=10, padx=20)
    
    def show_manager_menu(self, parent):
        """Меню менеджера"""
        tk.Label(parent, text="Панель менеджера", font=("Arial", 18, "bold")).pack(pady=20)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=20)
        
        buttons = [
            ("Просмотр каталога автомобилей", self.view_cars_window),
            ("Оформление продажи", self.create_sale_window),
            ("Работа с клиентами", self.manage_clients_window),
            ("Мои продажи", self.view_my_sales_window),
            ("Резервирование автомобиля", self.reserve_car_window)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=("Arial", 12), width=30, height=2, 
                     command=command).grid(row=i, column=0, pady=10, padx=20)
    
    def show_client_menu(self, parent):
        """Меню клиента"""
        tk.Label(parent, text="Личный кабинет клиента", font=("Arial", 18, "bold")).pack(pady=20)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=20)
        
        buttons = [
            ("Просмотр доступных автомобилей", self.browse_catalog_window),
            ("Мои покупки", self.view_purchases_window),
            ("Запись на тест-драйв", self.book_testdrive_window),
            ("Характеристики автомобилей", self.view_car_info_window)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=("Arial", 12), width=30, height=2, 
                     command=command).grid(row=i, column=0, pady=10, padx=20)
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.show_login_screen()
    
    # === АДМИНИСТРАТОР ===
    
    def manage_users_window(self):
        """Управление пользователями"""
        win = tk.Toplevel(self.root)
        win.title("Управление пользователями")
        win.geometry("800x500")
        
        tk.Label(win, text="Управление пользователями", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблица пользователей
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Логин", "ФИО", "Роль", "Дата создания")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            users = auth.get_all_users()
            for user in users:
                tree.insert("", "end", values=(user['username'], user['full_name'], 
                                              user['role'], user['created']))
        
        refresh_table()
        
        # Кнопки действий
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        def add_user():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить пользователя")
            add_win.geometry("400x300")
            
            tk.Label(add_win, text="Логин:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
            username_entry = tk.Entry(add_win, width=25)
            username_entry.grid(row=0, column=1, pady=10)
            
            tk.Label(add_win, text="Пароль:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
            password_entry = tk.Entry(add_win, width=25, show="*")
            password_entry.grid(row=1, column=1, pady=10)
            
            tk.Label(add_win, text="ФИО:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
            name_entry = tk.Entry(add_win, width=25)
            name_entry.grid(row=2, column=1, pady=10)
            
            tk.Label(add_win, text="Роль:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
            role_var = tk.StringVar(value="manager")
            role_combo = ttk.Combobox(add_win, textvariable=role_var, width=22,
                                     values=["administrator", "manager", "client"], state="readonly")
            role_combo.grid(row=3, column=1, pady=10)
            
            def save():
                success, msg = auth.create_user(username_entry.get(), password_entry.get(),
                                               role_var.get(), name_entry.get())
                if success:
                    messagebox.showinfo("Успех", msg)
                    refresh_table()
                    add_win.destroy()
                else:
                    messagebox.showerror("Ошибка", msg)
            
            tk.Button(add_win, text="Создать", command=save, width=20).grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            username = tree.item(selected[0])['values'][0]
            if username == "admin":
                messagebox.showerror("Ошибка", "Нельзя удалить главного администратора")
                return
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                auth.delete_user(username)
                refresh_table()
                messagebox.showinfo("Успех", "Пользователь удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_user, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Закрыть", command=win.destroy, width=15).pack(side="left", padx=5)
    
    def manage_cars_window(self):
        """Управление автомобилями"""
        win = tk.Toplevel(self.root)
        win.title("Управление автомобилями")
        win.geometry("900x500")
        
        tk.Label(win, text="Управление автомобилями", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Марка", "Модель", "Год", "Цена", "VIN", "Цвет", "Статус")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        widths = [40, 100, 100, 60, 100, 150, 80, 100]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for car in data['cars']:
                tree.insert("", "end", values=(car['id'], car['brand'], car['model'], 
                                              car['year'], f"{car['price']:,}", car['vin'],
                                              car['color'], car['status']))
        
        refresh_table()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        def add_car():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить автомобиль")
            add_win.geometry("400x400")
            
            fields = [
                ("Марка:", "brand"),
                ("Модель:", "model"),
                ("Год:", "year"),
                ("Цена:", "price"),
                ("VIN:", "vin"),
                ("Цвет:", "color")
            ]
            
            entries = {}
            for i, (label, key) in enumerate(fields):
                tk.Label(add_win, text=label).grid(row=i, column=0, padx=10, pady=10, sticky="e")
                entry = tk.Entry(add_win, width=25)
                entry.grid(row=i, column=1, pady=10)
                entries[key] = entry
            
            tk.Label(add_win, text="Статус:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
            status_var = tk.StringVar(value="available")
            status_combo = ttk.Combobox(add_win, textvariable=status_var, width=22,
                                       values=["available", "sold", "reserved"], state="readonly")
            status_combo.grid(row=6, column=1, pady=10)
            
            def save():
                try:
                    data = self.load_data()
                    new_id = max([c['id'] for c in data['cars']], default=0) + 1
                    
                    new_car = {
                        "id": new_id,
                        "brand": entries['brand'].get(),
                        "model": entries['model'].get(),
                        "year": int(entries['year'].get()),
                        "price": int(entries['price'].get()),
                        "vin": entries['vin'].get(),
                        "color": entries['color'].get(),
                        "status": status_var.get()
                    }
                    
                    if not all([v for k, v in new_car.items() if k != 'id']):
                        raise ValueError("Заполните все поля")
                    
                    data['cars'].append(new_car)
                    self.save_data(data)
                    messagebox.showinfo("Успех", "Автомобиль добавлен")
                    refresh_table()
                    add_win.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при добавлении: {str(e)}")
            
            tk.Button(add_win, text="Добавить", command=save, width=20).grid(row=7, column=0, columnspan=2, pady=20)
        
        def delete_car():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите автомобиль")
                return
            
            car_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", f"Удалить автомобиль ID {car_id}?"):
                data = self.load_data()
                data['cars'] = [c for c in data['cars'] if c['id'] != car_id]
                self.save_data(data)
                refresh_table()
                messagebox.showinfo("Успех", "Автомобиль удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_car, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_car, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_table, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Закрыть", command=win.destroy, width=15).pack(side="left", padx=5)
    
    def view_all_sales_window(self):
        """Просмотр всех продаж"""
        win = tk.Toplevel(self.root)
        win.title("Все продажи")
        win.geometry("900x500")
        
        tk.Label(win, text="Все продажи", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Автомобиль", "Клиент", "Менеджер", "Дата", "Цена")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        widths = [40, 200, 200, 150, 150, 120]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        data = self.load_data()
        total = 0
        for sale in data['sales']:
            tree.insert("", "end", values=(sale['id'], sale['car'], sale['client'], 
                                          sale['manager'], sale['date'], f"{sale['price']:,}"))
            total += sale['price']
        
        tk.Label(win, text=f"Всего продаж: {len(data['sales'])} | Общая сумма: {total:,} руб.", 
                font=("Arial", 11, "bold")).pack(pady=10)
        
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=5)
    
    def manage_staff_window(self):
        """Управление сотрудниками"""
        win = tk.Toplevel(self.root)
        win.title("Управление сотрудниками")
        win.geometry("700x400")
        
        tk.Label(win, text="Сотрудники (менеджеры)", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Логин", "ФИО", "Дата приема")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=220)
        
        tree.pack(side="left", fill="both", expand=True)
        
        users = auth.get_all_users()
        managers = [u for u in users if u['role'] == 'manager']
        
        for manager in managers:
            tree.insert("", "end", values=(manager['username'], manager['full_name'], manager['created']))
        
        tk.Label(win, text=f"Всего менеджеров: {len(managers)}", font=("Arial", 10)).pack(pady=5)
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=5)
    
    def generate_reports_window(self):
        """Генерация отчетов"""
        win = tk.Toplevel(self.root)
        win.title("Отчеты")
        win.geometry("600x400")
        
        tk.Label(win, text="Статистика и отчеты", font=("Arial", 14, "bold")).pack(pady=20)
        
        data = self.load_data()
        
        stats_frame = tk.Frame(win)
        stats_frame.pack(pady=20)
        
        stats = [
            ("Всего автомобилей:", len(data['cars'])),
            ("Доступно для продажи:", len([c for c in data['cars'] if c['status'] == 'available'])),
            ("Продано:", len([c for c in data['cars'] if c['status'] == 'sold'])),
            ("Зарезервировано:", len([c for c in data['cars'] if c['status'] == 'reserved'])),
            ("Всего продаж:", len(data['sales'])),
            ("Выручка:", f"{sum([s['price'] for s in data['sales']]):,} руб."),
            ("Клиентов:", len(data['clients'])),
            ("Тест-драйвов:", len(data['testdrives']))
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=("Arial", 11), anchor="w", width=25).grid(row=i, column=0, sticky="w", padx=20, pady=5)
            tk.Label(stats_frame, text=str(value), font=("Arial", 11, "bold"), anchor="e", width=20).grid(row=i, column=1, sticky="e", padx=20, pady=5)
        
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=20)
    
    # === МЕНЕДЖЕР ===
    
    def view_cars_window(self):
        """Просмотр каталога автомобилей (менеджер)"""
        win = tk.Toplevel(self.root)
        win.title("Каталог автомобилей")
        win.geometry("900x500")
        
        tk.Label(win, text="Каталог автомобилей", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Марка", "Модель", "Год", "Цена", "Цвет", "Статус")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        widths = [50, 120, 120, 80, 120, 100, 120]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        data = self.load_data()
        for car in data['cars']:
            tree.insert("", "end", values=(car['id'], car['brand'], car['model'], 
                                          car['year'], f"{car['price']:,}", car['color'], car['status']))
        
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=10)
    
    def create_sale_window(self):
        """Оформление продажи"""
        win = tk.Toplevel(self.root)
        win.title("Оформление продажи")
        win.geometry("500x400")
        
        tk.Label(win, text="Оформление новой продажи", font=("Arial", 14, "bold")).pack(pady=20)
        
        form_frame = tk.Frame(win)
        form_frame.pack(pady=20)
        
        data = self.load_data()
        available_cars = [c for c in data['cars'] if c['status'] == 'available']
        
        tk.Label(form_frame, text="Автомобиль:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        car_var = tk.StringVar()
        car_options = [f"ID {c['id']}: {c['brand']} {c['model']} ({c['year']}) - {c['price']:,} руб." for c in available_cars]
        if car_options:
            car_combo = ttk.Combobox(form_frame, textvariable=car_var, width=35, values=car_options, state="readonly")
            car_combo.grid(row=0, column=1, pady=10)
        else:
            tk.Label(form_frame, text="Нет доступных автомобилей", fg="red").grid(row=0, column=1, pady=10)
        
        tk.Label(form_frame, text="Клиент:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        client_var = tk.StringVar()
        client_options = [f"{c['name']} ({c['phone']})" for c in data['clients']]
        client_combo = ttk.Combobox(form_frame, textvariable=client_var, width=35, values=client_options, state="readonly")
        client_combo.grid(row=1, column=1, pady=10)
        
        tk.Label(form_frame, text="Цена продажи:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        price_entry = tk.Entry(form_frame, width=37)
        price_entry.grid(row=2, column=1, pady=10)
        
        def complete_sale():
            if not car_var.get() or not client_var.get() or not price_entry.get():
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                car_id = int(car_var.get().split("ID ")[1].split(":")[0])
                car = next(c for c in available_cars if c['id'] == car_id)
                
                sale = {
                    "id": len(data['sales']) + 1,
                    "car": f"{car['brand']} {car['model']} ({car['year']})",
                    "car_id": car_id,
                    "client": client_var.get().split(" (")[0],
                    "manager": self.current_user['full_name'],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "price": int(price_entry.get())
                }
                
                data['sales'].append(sale)
                
                # Обновить статус автомобиля
                for c in data['cars']:
                    if c['id'] == car_id:
                        c['status'] = 'sold'
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Продажа оформлена успешно!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при оформлении: {str(e)}")
        
        tk.Button(win, text="Оформить продажу", command=complete_sale, width=20, height=2).pack(pady=30)
        tk.Button(win, text="Отмена", command=win.destroy, width=20).pack(pady=5)
    
    def manage_clients_window(self):
        """Работа с клиентами"""
        win = tk.Toplevel(self.root)
        win.title("Клиенты")
        win.geometry("700x500")
        
        tk.Label(win, text="База клиентов", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "ФИО", "Телефон", "Email")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        widths = [50, 220, 150, 200]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        def refresh_table():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for client in data['clients']:
                tree.insert("", "end", values=(client['id'], client['name'], 
                                              client['phone'], client['email']))
        
        refresh_table()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        def add_client():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить клиента")
            add_win.geometry("400x250")
            
            tk.Label(add_win, text="ФИО:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
            name_entry = tk.Entry(add_win, width=30)
            name_entry.grid(row=0, column=1, pady=10)
            
            tk.Label(add_win, text="Телефон:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
            phone_entry = tk.Entry(add_win, width=30)
            phone_entry.grid(row=1, column=1, pady=10)
            
            tk.Label(add_win, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
            email_entry = tk.Entry(add_win, width=30)
            email_entry.grid(row=2, column=1, pady=10)
            
            def save():
                if not name_entry.get() or not phone_entry.get():
                    messagebox.showerror("Ошибка", "Заполните обязательные поля")
                    return
                
                data = self.load_data()
                new_client = {
                    "id": len(data['clients']) + 1,
                    "name": name_entry.get(),
                    "phone": phone_entry.get(),
                    "email": email_entry.get()
                }
                data['clients'].append(new_client)
                self.save_data(data)
                messagebox.showinfo("Успех", "Клиент добавлен")
                refresh_table()
                add_win.destroy()
            
            tk.Button(add_win, text="Добавить", command=save, width=20).grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Добавить клиента", command=add_client, width=20).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Закрыть", command=win.destroy, width=15).pack(side="left", padx=5)
    
    def view_my_sales_window(self):
        """Просмотр своих продаж"""
        win = tk.Toplevel(self.root)
        win.title("Мои продажи")
        win.geometry("800x500")
        
        tk.Label(win, text="Мои продажи", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Автомобиль", "Клиент", "Дата", "Цена")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        widths = [50, 250, 200, 180, 120]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        data = self.load_data()
        my_sales = [s for s in data['sales'] if s['manager'] == self.current_user['full_name']]
        total = 0
        
        for sale in my_sales:
            tree.insert("", "end", values=(sale['id'], sale['car'], sale['client'], 
                                          sale['date'], f"{sale['price']:,}"))
            total += sale['price']
        
        tk.Label(win, text=f"Всего продаж: {len(my_sales)} | Сумма: {total:,} руб.", 
                font=("Arial", 11, "bold")).pack(pady=10)
        
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=5)
    
    def reserve_car_window(self):
        """Резервирование автомобиля"""
        win = tk.Toplevel(self.root)
        win.title("Резервирование")
        win.geometry("500x300")
        
        tk.Label(win, text="Резервирование автомобиля", font=("Arial", 14, "bold")).pack(pady=20)
        
        form_frame = tk.Frame(win)
        form_frame.pack(pady=20)
        
        data = self.load_data()
        available_cars = [c for c in data['cars'] if c['status'] == 'available']
        
        tk.Label(form_frame, text="Автомобиль:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        car_var = tk.StringVar()
        car_options = [f"ID {c['id']}: {c['brand']} {c['model']} ({c['year']})" for c in available_cars]
        car_combo = ttk.Combobox(form_frame, textvariable=car_var, width=35, values=car_options, state="readonly")
        car_combo.grid(row=0, column=1, pady=10)
        
        tk.Label(form_frame, text="Клиент:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        client_var = tk.StringVar()
        client_options = [c['name'] for c in data['clients']]
        client_combo = ttk.Combobox(form_frame, textvariable=client_var, width=35, values=client_options, state="readonly")
        client_combo.grid(row=1, column=1, pady=10)
        
        def reserve():
            if not car_var.get() or not client_var.get():
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            car_id = int(car_var.get().split("ID ")[1].split(":")[0])
            for c in data['cars']:
                if c['id'] == car_id:
                    c['status'] = 'reserved'
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Автомобиль зарезервирован")
            win.destroy()
        
        tk.Button(win, text="Зарезервировать", command=reserve, width=20, height=2).pack(pady=20)
        tk.Button(win, text="Отмена", command=win.destroy, width=20).pack(pady=5)
    
    # === КЛИЕНТ ===
    
    def browse_catalog_window(self):
        """Просмотр доступных автомобилей (клиент)"""
        win = tk.Toplevel(self.root)
        win.title("Каталог автомобилей")
        win.geometry("800x500")
        
        tk.Label(win, text="Доступные автомобили", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Марка", "Модель", "Год", "Цена", "Цвет")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        widths = [150, 150, 80, 150, 120]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        data = self.load_data()
        available = [c for c in data['cars'] if c['status'] == 'available']
        
        for car in available:
            tree.insert("", "end", values=(car['brand'], car['model'], car['year'], 
                                          f"{car['price']:,} руб.", car['color']))
        
        tk.Label(win, text=f"Доступно автомобилей: {len(available)}", font=("Arial", 10)).pack(pady=5)
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=5)
    
    def view_purchases_window(self):
        """Просмотр своих покупок"""
        win = tk.Toplevel(self.root)
        win.title("Мои покупки")
        win.geometry("700x400")
        
        tk.Label(win, text="История покупок", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Автомобиль", "Менеджер", "Дата", "Цена")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        widths = [250, 180, 150, 120]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        data = self.load_data()
        my_purchases = [s for s in data['sales'] if s['client'] == self.current_user['full_name']]
        
        for purchase in my_purchases:
            tree.insert("", "end", values=(purchase['car'], purchase['manager'], 
                                          purchase['date'], f"{purchase['price']:,}"))
        
        if not my_purchases:
            tk.Label(win, text="У вас пока нет покупок", font=("Arial", 10), fg="gray").pack(pady=10)
        
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=10)
    
    def book_testdrive_window(self):
        """Запись на тест-драйв"""
        win = tk.Toplevel(self.root)
        win.title("Тест-драйв")
        win.geometry("500x300")
        
        tk.Label(win, text="Запись на тест-драйв", font=("Arial", 14, "bold")).pack(pady=20)
        
        form_frame = tk.Frame(win)
        form_frame.pack(pady=20)
        
        data = self.load_data()
        available_cars = [c for c in data['cars'] if c['status'] == 'available']
        
        tk.Label(form_frame, text="Автомобиль:").grid(row=0, column=0, padx=10, pady=15, sticky="e")
        car_var = tk.StringVar()
        car_options = [f"{c['brand']} {c['model']} ({c['year']})" for c in available_cars]
        car_combo = ttk.Combobox(form_frame, textvariable=car_var, width=35, values=car_options, state="readonly")
        car_combo.grid(row=0, column=1, pady=15)
        
        tk.Label(form_frame, text="Дата и время:").grid(row=1, column=0, padx=10, pady=15, sticky="e")
        date_entry = tk.Entry(form_frame, width=37)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        date_entry.grid(row=1, column=1, pady=15)
        
        def book():
            if not car_var.get():
                messagebox.showerror("Ошибка", "Выберите автомобиль")
                return
            
            testdrive = {
                "id": len(data['testdrives']) + 1,
                "client": self.current_user['full_name'],
                "car": car_var.get(),
                "date": date_entry.get(),
                "status": "scheduled"
            }
            
            data['testdrives'].append(testdrive)
            self.save_data(data)
            messagebox.showinfo("Успех", "Вы записаны на тест-драйв!")
            win.destroy()
        
        tk.Button(win, text="Записаться", command=book, width=20, height=2).pack(pady=20)
        tk.Button(win, text="Отмена", command=win.destroy, width=20).pack(pady=5)
    
    def view_car_info_window(self):
        """Просмотр характеристик автомобилей"""
        win = tk.Toplevel(self.root)
        win.title("Характеристики автомобилей")
        win.geometry("900x500")
        
        tk.Label(win, text="Подробная информация об автомобилях", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Марка", "Модель", "Год", "Цена", "VIN", "Цвет", "Статус")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        widths = [120, 120, 70, 110, 150, 100, 100]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        data = self.load_data()
        for car in data['cars']:
            status_text = {"available": "Доступен", "sold": "Продан", "reserved": "Зарезервирован"}
            tree.insert("", "end", values=(car['brand'], car['model'], car['year'], 
                                          f"{car['price']:,}", car['vin'], car['color'], 
                                          status_text.get(car['status'], car['status'])))
        
        tk.Button(win, text="Закрыть", command=win.destroy, width=15).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutostoreApp(root)
    root.mainloop()