import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

# Путь к файлу данных
DATA_FILE = 'data.json'

class ComputerShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Компьютерный магазин")
        self.root.geometry("900x600")
        
        # Инициализация данных
        self.init_data()
        
        # Показать окно входа
        self.show_login()
    
    def init_data(self):
        """Инициализация данных из JSON"""
        self.data = self.load_data()
    
    def load_data(self):
        """Загрузка данных из JSON"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в JSON"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна от всех виджетов"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ОКНО ВХОДА
    def show_login(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Компьютерный магазин", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=10)
        self.login_entry = tk.Entry(frame, font=("Arial", 12), width=20)
        self.login_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=10)
        self.password_entry = tk.Entry(frame, font=("Arial", 12), width=20, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)
        
        tk.Button(frame, text="Войти", font=("Arial", 12), command=self.do_login, width=15).grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(frame, text="Регистрация", font=("Arial", 10), command=self.show_register, width=15).grid(row=4, column=0, columnspan=2)
        
        # Подсказка
        hint_text = "Подсказка:\nadmin/admin123\nseller/seller123\nclient/client123"
        tk.Label(frame, text=hint_text, font=("Arial", 9), fg="gray", justify="left").grid(row=5, column=0, columnspan=2, pady=20)
    
    def do_login(self):
        """Обработка входа"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        user = auth.authenticate(username, password)
        if user:
            auth.Session.login(user)
            self.show_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_register(self):
        """Окно регистрации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Регистрация", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=10)
        username_entry = tk.Entry(frame, font=("Arial", 12), width=20)
        username_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=10)
        password_entry = tk.Entry(frame, font=("Arial", 12), width=20, show="*")
        password_entry.grid(row=2, column=1, pady=10)
        
        tk.Label(frame, text="ФИО:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=10)
        fullname_entry = tk.Entry(frame, font=("Arial", 12), width=20)
        fullname_entry.grid(row=3, column=1, pady=10)
        
        def register():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            
            if not username or not password or not fullname:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = auth.register_user(username, password, "client", fullname)
            if success:
                messagebox.showinfo("Успех", message)
                self.show_login()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(frame, text="Зарегистрироваться", font=("Arial", 12), command=register, width=20).grid(row=4, column=0, columnspan=2, pady=20)
        tk.Button(frame, text="Назад", font=("Arial", 10), command=self.show_login, width=15).grid(row=5, column=0, columnspan=2)
    
    # ГЛАВНОЕ МЕНЮ
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        role = auth.Session.get_role()
        
        if role == "administrator":
            self.show_admin_menu()
        elif role == "seller":
            self.show_seller_menu()
        elif role == "client":
            self.show_client_menu()
    
    # МЕНЮ АДМИНИСТРАТОРА
    def show_admin_menu(self):
        """Меню администратора"""
        self.clear_window()
        
        user = auth.Session.current_user
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        top_frame.pack(fill="x")
        
        tk.Label(top_frame, text=f"Администратор: {user['full_name']}", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side="right", padx=10, pady=10)
        
        # Контейнер для кнопок меню
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=30)
        
        tk.Label(menu_frame, text="Панель администратора", font=("Arial", 18, "bold")).pack(pady=20)
        
        buttons = [
            ("Управление пользователями", self.show_users_management),
            ("Управление товарами", self.show_products_management),
            ("Управление категориями", self.show_categories_management),
            ("Просмотр статистики", self.show_statistics),
            ("Резервное копирование", self.backup_data)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, font=("Arial", 12), width=30, command=command).pack(pady=10)
    
    def show_users_management(self):
        """Управление пользователями"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_admin_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Управление пользователями", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        # Кнопки действий
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)
        tk.Button(action_frame, text="Добавить пользователя", command=self.add_user_dialog).pack(side="left", padx=5)
        tk.Button(action_frame, text="Удалить выбранного", command=lambda: self.delete_user_from_tree(tree)).pack(side="left", padx=5)
        
        # Таблица пользователей
        columns = ("Логин", "Роль", "ФИО", "Дата создания")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Заполнение данными
        for user in auth.get_all_users():
            tree.insert("", "end", values=(user['username'], user['role'], user['full_name'], user['created']))
    
    def add_user_dialog(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Логин:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        username_entry = tk.Entry(dialog, font=("Arial", 11))
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Пароль:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        password_entry = tk.Entry(dialog, font=("Arial", 11), show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="ФИО:", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        fullname_entry = tk.Entry(dialog, font=("Arial", 11))
        fullname_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Роль:", font=("Arial", 11)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        role_var = tk.StringVar(value="client")
        role_combo = ttk.Combobox(dialog, textvariable=role_var, values=["administrator", "seller", "client"], state="readonly")
        role_combo.grid(row=3, column=1, padx=10, pady=10)
        
        def save():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            role = role_var.get()
            
            if not username or not password or not fullname:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = auth.register_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
                self.show_users_management()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_user_from_tree(self, tree):
        """Удаление пользователя из списка"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        
        item = tree.item(selected[0])
        username = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            auth.delete_user(username)
            self.show_users_management()
    
    def show_products_management(self):
        """Управление товарами"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_admin_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Управление товарами", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)
        tk.Button(action_frame, text="Добавить товар", command=self.add_product_dialog).pack(side="left", padx=5)
        tk.Button(action_frame, text="Редактировать", command=lambda: self.edit_product_dialog(tree)).pack(side="left", padx=5)
        tk.Button(action_frame, text="Удалить", command=lambda: self.delete_product(tree)).pack(side="left", padx=5)
        
        columns = ("ID", "Название", "Категория", "Цена", "Остаток")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        for product in self.data['products']:
            tree.insert("", "end", values=(product['id'], product['name'], product['category'], product['price'], product['stock']))
    
    def add_product_dialog(self):
        """Диалог добавления товара"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить товар")
        dialog.geometry("400x350")
        
        tk.Label(dialog, text="Название:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Категория:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(dialog, textvariable=category_var, values=self.data['categories'], width=23)
        category_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Цена:", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        price_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Остаток:", font=("Arial", 11)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        stock_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        stock_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save():
            name = name_entry.get()
            category = category_var.get()
            price = price_entry.get()
            stock = stock_entry.get()
            
            if not name or not category or not price or not stock:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                price = float(price)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат цены или остатка")
                return
            
            new_id = max([p['id'] for p in self.data['products']], default=0) + 1
            new_product = {
                "id": new_id,
                "name": name,
                "category": category,
                "price": price,
                "stock": stock
            }
            
            self.data['products'].append(new_product)
            self.save_data(self.data)
            messagebox.showinfo("Успех", "Товар добавлен")
            dialog.destroy()
            self.show_products_management()
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=4, column=0, columnspan=2, pady=20)
    
    def edit_product_dialog(self, tree):
        """Диалог редактирования товара"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите товар")
            return
        
        item = tree.item(selected[0])
        product_id = item['values'][0]
        product = next((p for p in self.data['products'] if p['id'] == product_id), None)
        
        if not product:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать товар")
        dialog.geometry("400x350")
        
        tk.Label(dialog, text="Название:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        name_entry.insert(0, product['name'])
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Категория:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        category_var = tk.StringVar(value=product['category'])
        category_combo = ttk.Combobox(dialog, textvariable=category_var, values=self.data['categories'], width=23)
        category_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Цена:", font=("Arial", 11)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        price_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        price_entry.insert(0, product['price'])
        price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Остаток:", font=("Arial", 11)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        stock_entry = tk.Entry(dialog, font=("Arial", 11), width=25)
        stock_entry.insert(0, product['stock'])
        stock_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save():
            product['name'] = name_entry.get()
            product['category'] = category_var.get()
            
            try:
                product['price'] = float(price_entry.get())
                product['stock'] = int(stock_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат")
                return
            
            self.save_data(self.data)
            messagebox.showinfo("Успех", "Товар обновлен")
            dialog.destroy()
            self.show_products_management()
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_product(self, tree):
        """Удаление товара"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите товар")
            return
        
        item = tree.item(selected[0])
        product_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить товар?"):
            self.data['products'] = [p for p in self.data['products'] if p['id'] != product_id]
            self.save_data(self.data)
            self.show_products_management()
    
    def show_categories_management(self):
        """Управление категориями"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_admin_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Управление категориями", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=30)
        
        tk.Label(frame, text="Категории товаров:", font=("Arial", 12)).pack(pady=10)
        
        listbox = tk.Listbox(frame, font=("Arial", 11), width=40, height=15)
        listbox.pack(pady=10)
        
        for cat in self.data['categories']:
            listbox.insert("end", cat)
        
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)
        
        def add_category():
            new_cat = tk.simpledialog.askstring("Добавить", "Введите название категории:")
            if new_cat and new_cat not in self.data['categories']:
                self.data['categories'].append(new_cat)
                self.save_data(self.data)
                self.show_categories_management()
        
        def delete_category():
            selected = listbox.curselection()
            if selected:
                cat = listbox.get(selected[0])
                if messagebox.askyesno("Подтверждение", f"Удалить категорию '{cat}'?"):
                    self.data['categories'].remove(cat)
                    self.save_data(self.data)
                    self.show_categories_management()
        
        tk.Button(btn_frame, text="Добавить", command=add_category, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_category, width=15).pack(side="left", padx=5)
    
    def show_statistics(self):
        """Просмотр статистики"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_admin_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Статистика", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=30)
        
        total_products = len(self.data['products'])
        total_orders = len(self.data['orders'])
        total_revenue = sum([order.get('total', 0) for order in self.data['orders']])
        total_users = len(auth.get_all_users())
        
        stats = [
            f"Всего товаров: {total_products}",
            f"Всего заказов: {total_orders}",
            f"Общая выручка: {total_revenue:.2f} руб.",
            f"Всего пользователей: {total_users}"
        ]
        
        tk.Label(frame, text="Статистика магазина", font=("Arial", 16, "bold")).pack(pady=20)
        
        for stat in stats:
            tk.Label(frame, text=stat, font=("Arial", 14)).pack(pady=10, anchor="w", padx=50)
    
    def backup_data(self):
        """Резервное копирование"""
        import shutil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            shutil.copy(DATA_FILE, f"data_backup_{timestamp}.json")
            shutil.copy(auth.USERS_FILE, f"users_backup_{timestamp}.json")
            messagebox.showinfo("Успех", f"Резервная копия создана:\ndata_backup_{timestamp}.json\nusers_backup_{timestamp}.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать резервную копию: {e}")
    
    # МЕНЮ ПРОДАВЦА
    def show_seller_menu(self):
        """Меню продавца"""
        self.clear_window()
        
        user = auth.Session.current_user
        
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        top_frame.pack(fill="x")
        
        tk.Label(top_frame, text=f"Продавец: {user['full_name']}", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side="right", padx=10, pady=10)
        
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=30)
        
        tk.Label(menu_frame, text="Панель продавца", font=("Arial", 18, "bold")).pack(pady=20)
        
        buttons = [
            ("Просмотр товаров", self.show_seller_products),
            ("Добавить товар", self.add_product_dialog),
            ("Обработка заказов", self.show_orders_processing),
            ("Просмотр истории продаж", self.show_sales_history)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, font=("Arial", 12), width=30, command=command).pack(pady=10)
    
    def show_seller_products(self):
        """Просмотр товаров для продавца"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_seller_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Просмотр товаров", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        columns = ("ID", "Название", "Категория", "Цена", "Остаток")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        for product in self.data['products']:
            tree.insert("", "end", values=(product['id'], product['name'], product['category'], product['price'], product['stock']))
    
    def show_orders_processing(self):
        """Обработка заказов"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_seller_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Обработка заказов", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)
        
        def complete_order(tree):
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите заказ")
                return
            
            item = tree.item(selected[0])
            order_id = item['values'][0]
            
            for order in self.data['orders']:
                if order['id'] == order_id:
                    order['status'] = 'Выполнен'
                    self.save_data(self.data)
                    messagebox.showinfo("Успех", "Заказ выполнен")
                    self.show_orders_processing()
                    break
        
        tk.Button(action_frame, text="Выполнить заказ", command=lambda: complete_order(tree)).pack(side="left", padx=5)
        
        columns = ("ID", "Клиент", "Товары", "Сумма", "Дата", "Статус")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        for order in self.data['orders']:
            items = ", ".join([f"{item['name']} x{item['quantity']}" for item in order.get('items', [])])
            tree.insert("", "end", values=(order['id'], order['client'], items, order.get('total', 0), order['date'], order.get('status', 'В обработке')))
    
    def show_sales_history(self):
        """История продаж"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_seller_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="История продаж", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        columns = ("ID", "Клиент", "Товары", "Сумма", "Дата", "Статус")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        for order in self.data['orders']:
            items = ", ".join([f"{item['name']} x{item['quantity']}" for item in order.get('items', [])])
            tree.insert("", "end", values=(order['id'], order['client'], items, order.get('total', 0), order['date'], order.get('status', 'В обработке')))
    
    # МЕНЮ КЛИЕНТА
    def show_client_menu(self):
        """Меню клиента"""
        self.clear_window()
        
        user = auth.Session.current_user
        
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        top_frame.pack(fill="x")
        
        tk.Label(top_frame, text=f"Клиент: {user['full_name']}", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(side="left", padx=10)
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side="right", padx=10, pady=10)
        
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=30)
        
        tk.Label(menu_frame, text="Панель клиента", font=("Arial", 18, "bold")).pack(pady=20)
        
        buttons = [
            ("Просмотр каталога", self.show_catalog),
            ("Оформить заказ", self.make_order),
            ("Мои заказы", self.show_my_orders)
        ]
        
        for text, command in buttons:
            tk.Button(menu_frame, text=text, font=("Arial", 12), width=30, command=command).pack(pady=10)
    
    def show_catalog(self):
        """Просмотр каталога для клиента"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_client_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Каталог товаров", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        # Поиск
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:", font=("Arial", 11)).pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        search_entry.pack(side="left", padx=5)
        
        def search():
            query = search_entry.get().lower()
            tree.delete(*tree.get_children())
            
            for product in self.data['products']:
                if query in product['name'].lower() or query in product['category'].lower():
                    tree.insert("", "end", values=(product['id'], product['name'], product['category'], product['price'], product['stock']))
        
        tk.Button(search_frame, text="Поиск", command=search).pack(side="left", padx=5)
        tk.Button(search_frame, text="Показать все", command=lambda: self.show_catalog()).pack(side="left", padx=5)
        
        columns = ("ID", "Название", "Категория", "Цена", "В наличии")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=18)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        for product in self.data['products']:
            tree.insert("", "end", values=(product['id'], product['name'], product['category'], product['price'], product['stock']))
    
    def make_order(self):
        """Оформление заказа"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_client_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Оформление заказа", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        # Левая часть - список товаров
        left_frame = tk.Frame(self.root)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(left_frame, text="Доступные товары:", font=("Arial", 12, "bold")).pack(pady=5)
        
        products_tree = ttk.Treeview(left_frame, columns=("ID", "Название", "Цена", "Остаток"), show="headings", height=20)
        products_tree.heading("ID", text="ID")
        products_tree.heading("Название", text="Название")
        products_tree.heading("Цена", text="Цена")
        products_tree.heading("Остаток", text="Остаток")
        
        for col in ("ID", "Название", "Цена", "Остаток"):
            products_tree.column(col, width=100)
        
        products_tree.pack(fill="both", expand=True)
        
        for product in self.data['products']:
            if product['stock'] > 0:
                products_tree.insert("", "end", values=(product['id'], product['name'], product['price'], product['stock']))
        
        # Правая часть - корзина
        right_frame = tk.Frame(self.root)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(right_frame, text="Корзина:", font=("Arial", 12, "bold")).pack(pady=5)
        
        cart_tree = ttk.Treeview(right_frame, columns=("Название", "Количество", "Цена"), show="headings", height=15)
        cart_tree.heading("Название", text="Название")
        cart_tree.heading("Количество", text="Количество")
        cart_tree.heading("Цена", text="Цена")
        cart_tree.pack(fill="both", expand=True)
        
        cart_items = []
        
        def add_to_cart():
            selected = products_tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите товар")
                return
            
            item = products_tree.item(selected[0])
            product_id = item['values'][0]
            product = next((p for p in self.data['products'] if p['id'] == product_id), None)
            
            if not product:
                return
            
            quantity = tk.simpledialog.askinteger("Количество", f"Введите количество для '{product['name']}':", minvalue=1, maxvalue=product['stock'])
            
            if quantity:
                cart_items.append({
                    'id': product['id'],
                    'name': product['name'],
                    'quantity': quantity,
                    'price': product['price']
                })
                
                cart_tree.insert("", "end", values=(product['name'], quantity, product['price'] * quantity))
                update_total()
        
        def remove_from_cart():
            selected = cart_tree.selection()
            if selected:
                index = cart_tree.index(selected[0])
                cart_tree.delete(selected[0])
                cart_items.pop(index)
                update_total()
        
        total_label = tk.Label(right_frame, text="Итого: 0 руб.", font=("Arial", 12, "bold"))
        total_label.pack(pady=10)
        
        def update_total():
            total = sum([item['price'] * item['quantity'] for item in cart_items])
            total_label.config(text=f"Итого: {total:.2f} руб.")
        
        def confirm_order():
            if not cart_items:
                messagebox.showwarning("Внимание", "Корзина пуста")
                return
            
            total = sum([item['price'] * item['quantity'] for item in cart_items])
            
            new_order = {
                'id': max([o['id'] for o in self.data['orders']], default=0) + 1,
                'client': auth.Session.current_user['full_name'],
                'items': cart_items,
                'total': total,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status': 'В обработке'
            }
            
            # Уменьшение остатков
            for item in cart_items:
                for product in self.data['products']:
                    if product['id'] == item['id']:
                        product['stock'] -= item['quantity']
                        break
            
            self.data['orders'].append(new_order)
            self.save_data(self.data)
            
            messagebox.showinfo("Успех", f"Заказ #{new_order['id']} оформлен на сумму {total:.2f} руб.")
            self.show_client_menu()
        
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить в корзину", command=add_to_cart).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить из корзины", command=remove_from_cart).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Оформить заказ", command=confirm_order, bg="#27ae60", fg="white").pack(side="left", padx=5)
    
    def show_my_orders(self):
        """Мои заказы"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg="#2c3e50")
        top_frame.pack(fill="x")
        tk.Button(top_frame, text="◀ Назад", command=self.show_client_menu).pack(side="left", padx=10, pady=10)
        tk.Label(top_frame, text="Мои заказы", bg="#2c3e50", fg="white", font=("Arial", 14)).pack(side="left", padx=10)
        
        columns = ("ID", "Товары", "Сумма", "Дата", "Статус")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=160)
        
        tree.pack(pady=10, padx=20, fill="both", expand=True)
        
        user_name = auth.Session.current_user['full_name']
        
        for order in self.data['orders']:
            if order['client'] == user_name:
                items = ", ".join([f"{item['name']} x{item['quantity']}" for item in order.get('items', [])])
                tree.insert("", "end", values=(order['id'], items, order.get('total', 0), order['date'], order.get('status', 'В обработке')))
    
    def logout(self):
        """Выход из системы"""
        auth.Session.logout()
        self.show_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = ComputerShopApp(root)
    root.mainloop()