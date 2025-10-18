import tkinter as tk
from tkinter import ttk, messagebox
import json
from auth import AuthManager

class MarketplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Маркетплейс - Вход в систему")
        self.root.geometry("900x600")

        self.auth = AuthManager()
        self.data_file = 'data.json'

        self.show_login_window()
    
    
    def _load_data(self):
        """Загрузка данных"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Сохранение данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ОКНО ВХОДА
    def show_login_window(self):
        """Окно авторизации"""
        self.clear_window()
        self.root.title("Маркетплейс - Вход")
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack(expand=True)
        
        tk.Label(frame, text="ВХОД В СИСТЕМУ", font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', pady=10)
        self.login_entry = tk.Entry(frame, font=('Arial', 12), width=25)
        self.login_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', pady=10)
        self.password_entry = tk.Entry(frame, font=('Arial', 12), width=25, show='*')
        self.password_entry.grid(row=2, column=1, pady=10)
        
        tk.Button(frame, text="Войти", font=('Arial', 12), width=20, 
                 command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка с учетными данными
        hint_text = "Демо-доступ:\nadmin/admin123\nseller1/seller123\nbuyer1/buyer123"
        tk.Label(frame, text=hint_text, font=('Arial', 9), fg='gray', justify='left').grid(row=4, column=0, columnspan=2)
    
    def login(self):
        """Обработка входа"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if self.auth.login(username, password):
            role = self.auth.current_user['role']
            if role == 'administrator':
                self.show_admin_window()
            elif role == 'seller':
                self.show_seller_window()
            elif role == 'buyer':
                self.show_buyer_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    # ОКНО АДМИНИСТРАТОРА
    def show_admin_window(self):
        """Главное окно администратора"""
        self.clear_window()
        self.root.title(f"Маркетплейс - Администратор ({self.auth.current_user['username']})")
        
        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.logout)
        
        # Основной фрейм
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="ПАНЕЛЬ АДМИНИСТРАТОРА", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Кнопки действий
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Управление пользователями", width=25,
                 command=self.admin_manage_users).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Управление категориями", width=25,
                 command=self.admin_manage_categories).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Просмотр всех заказов", width=25,
                 command=self.admin_view_orders).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Модерация отзывов", width=25,
                 command=self.admin_moderate_reviews).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Генерация отчетов", width=25,
                 command=self.admin_generate_report).grid(row=2, column=0, padx=5, pady=5)
        
        # Область для отображения данных
        self.admin_display_frame = tk.Frame(main_frame)
        self.admin_display_frame.pack(fill='both', expand=True, pady=10)
    
    def admin_manage_users(self):
        """Управление пользователями"""
        for widget in self.admin_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.admin_display_frame, text="Пользователи системы",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        # Таблица пользователей
        columns = ('Логин', 'Роль', 'Email', 'Дата создания')
        tree = ttk.Treeview(self.admin_display_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        users = self.auth.get_all_users()
        for user in users:
            tree.insert('', 'end', values=(
                user['username'],
                user['role'],
                user.get('email', ''),
                user['created']
            ))
        
        tree.pack(pady=5)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.admin_display_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить пользователя",
                 command=self.admin_add_user).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить выбранного",
                 command=lambda: self.admin_delete_user(tree)).pack(side='left', padx=5)
    
    def admin_add_user(self):
        """Добавление пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("350x250")
        
        tk.Label(dialog, text="Логин:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        username_entry = tk.Entry(dialog, width=25)
        username_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        password_entry = tk.Entry(dialog, width=25, show='*')
        password_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(dialog, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        email_entry = tk.Entry(dialog, width=25)
        email_entry.grid(row=2, column=1, pady=10)
        
        tk.Label(dialog, text="Роль:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        role_var = tk.StringVar(value='buyer')
        role_combo = ttk.Combobox(dialog, textvariable=role_var, 
                                  values=['administrator', 'seller', 'buyer'], width=22)
        role_combo.grid(row=3, column=1, pady=10)
        
        def save_user():
            success, msg = self.auth.register(
                username_entry.get(),
                password_entry.get(),
                role_var.get(),
                email_entry.get()
            )
            if success:
                messagebox.showinfo("Успех", msg)
                dialog.destroy()
                self.admin_manage_users()
            else:
                messagebox.showerror("Ошибка", msg)
        
        tk.Button(dialog, text="Сохранить", command=save_user).grid(row=4, column=0, columnspan=2, pady=20)
    
    def admin_delete_user(self, tree):
        """Удаление пользователя"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        username = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            self.auth.delete_user(username)
            self.admin_manage_users()
    
    def admin_manage_categories(self):
        """Управление категориями"""
        for widget in self.admin_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.admin_display_frame, text="Категории товаров",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        
        listbox = tk.Listbox(self.admin_display_frame, font=('Arial', 12), height=10)
        listbox.pack(pady=5, fill='both', expand=True)
        
        for cat in data['categories']:
            listbox.insert('end', cat)
        
        # Форма добавления
        form_frame = tk.Frame(self.admin_display_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Новая категория:").pack(side='left', padx=5)
        cat_entry = tk.Entry(form_frame, width=30)
        cat_entry.pack(side='left', padx=5)
        
        def add_category():
            new_cat = cat_entry.get().strip()
            if new_cat and new_cat not in data['categories']:
                data['categories'].append(new_cat)
                self._save_data(data)
                listbox.insert('end', new_cat)
                cat_entry.delete(0, 'end')
        
        def delete_category():
            selected = listbox.curselection()
            if selected:
                cat = listbox.get(selected[0])
                data['categories'].remove(cat)
                self._save_data(data)
                listbox.delete(selected[0])
        
        tk.Button(form_frame, text="Добавить", command=add_category).pack(side='left', padx=5)
        tk.Button(form_frame, text="Удалить выбранную", command=delete_category).pack(side='left', padx=5)
    
    def admin_view_orders(self):
        """Просмотр всех заказов"""
        for widget in self.admin_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.admin_display_frame, text="Все заказы системы",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        
        columns = ('ID', 'Покупатель', 'Товар', 'Количество', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(self.admin_display_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for order in data['orders']:
            tree.insert('', 'end', values=(
                order['id'],
                order['buyer'],
                order['product_name'],
                order['quantity'],
                order['total'],
                order['status'],
                order['date']
            ))
        
        tree.pack(fill='both', expand=True, pady=5)
    
    def admin_moderate_reviews(self):
        """Модерация отзывов"""
        for widget in self.admin_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.admin_display_frame, text="Отзывы пользователей",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        
        if not data['reviews']:
            tk.Label(self.admin_display_frame, text="Отзывов пока нет",
                    font=('Arial', 12)).pack(pady=20)
            return
        
        for review in data['reviews']:
            frame = tk.Frame(self.admin_display_frame, relief='solid', borderwidth=1)
            frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(frame, text=f"Товар: {review['product_name']} | Автор: {review['buyer']} | Рейтинг: {review['rating']}/5",
                    font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=2)
            tk.Label(frame, text=review['text'], wraplength=700).pack(anchor='w', padx=5, pady=2)
            
            def delete_review(r_id=review['id']):
                data['reviews'] = [r for r in data['reviews'] if r['id'] != r_id]
                self._save_data(data)
                self.admin_moderate_reviews()
            
            tk.Button(frame, text="Удалить", command=delete_review).pack(anchor='e', padx=5, pady=2)
    
    def admin_generate_report(self):
        """Генерация отчетов"""
        for widget in self.admin_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.admin_display_frame, text="Статистика системы",
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self._load_data()
        users = self.auth.get_all_users()
        
        total_users = len(users)
        total_products = len(data['products'])
        total_orders = len(data['orders'])
        total_revenue = sum(o['total'] for o in data['orders'])
        
        stats_frame = tk.Frame(self.admin_display_frame)
        stats_frame.pack(pady=20)
        
        stats = [
            ("Всего пользователей:", total_users),
            ("Всего товаров:", total_products),
            ("Всего заказов:", total_orders),
            ("Общая выручка:", f"{total_revenue} руб.")
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 12)).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            tk.Label(stats_frame, text=str(value), font=('Arial', 12, 'bold')).grid(row=i, column=1, sticky='w', padx=10, pady=5)
    
    # ОКНО ПРОДАВЦА
    def show_seller_window(self):
        """Главное окно продавца"""
        self.clear_window()
        self.root.title(f"Маркетплейс - Продавец ({self.auth.current_user['username']})")
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.logout)
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="ПАНЕЛЬ ПРОДАВЦА", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Мои товары", width=20,
                 command=self.seller_my_products).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Добавить товар", width=20,
                 command=self.seller_add_product).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Заказы", width=20,
                 command=self.seller_orders).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Статистика", width=20,
                 command=self.seller_stats).grid(row=1, column=1, padx=5, pady=5)
        
        self.seller_display_frame = tk.Frame(main_frame)
        self.seller_display_frame.pack(fill='both', expand=True, pady=10)
    
    def seller_my_products(self):
        """Товары продавца"""
        for widget in self.seller_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.seller_display_frame, text="Мои товары",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        my_products = [p for p in data['products'] 
                      if p['seller'] == self.auth.current_user['username']]
        
        columns = ('ID', 'Название', 'Категория', 'Цена', 'Остаток')
        tree = ttk.Treeview(self.seller_display_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for product in my_products:
            tree.insert('', 'end', values=(
                product['id'],
                product['name'],
                product['category'],
                product['price'],
                product['stock']
            ))
        
        tree.pack(fill='both', expand=True, pady=5)
        
        btn_frame = tk.Frame(self.seller_display_frame)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Редактировать",
                 command=lambda: self.seller_edit_product(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить",
                 command=lambda: self.seller_delete_product(tree)).pack(side='left', padx=5)
    
    def seller_add_product(self):
        """Добавление товара"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить товар")
        dialog.geometry("400x350")
        
        data = self._load_data()
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        name_entry = tk.Entry(dialog, width=25)
        name_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(dialog, text="Категория:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(dialog, textvariable=category_var, 
                                     values=data['categories'], width=22)
        category_combo.grid(row=1, column=1, pady=10)
        
        tk.Label(dialog, text="Цена:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        price_entry = tk.Entry(dialog, width=25)
        price_entry.grid(row=2, column=1, pady=10)
        
        tk.Label(dialog, text="Количество:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        stock_entry = tk.Entry(dialog, width=25)
        stock_entry.grid(row=3, column=1, pady=10)
        
        tk.Label(dialog, text="Описание:").grid(row=4, column=0, padx=10, pady=10, sticky='ne')
        desc_text = tk.Text(dialog, width=25, height=4)
        desc_text.grid(row=4, column=1, pady=10)
        
        def save_product():
            try:
                new_product = {
                    "id": max([p['id'] for p in data['products']], default=0) + 1,
                    "name": name_entry.get(),
                    "category": category_var.get(),
                    "price": float(price_entry.get()),
                    "seller": self.auth.current_user['username'],
                    "stock": int(stock_entry.get()),
                    "description": desc_text.get('1.0', 'end').strip()
                }
                data['products'].append(new_product)
                self._save_data(data)
                messagebox.showinfo("Успех", "Товар добавлен")
                dialog.destroy()
                self.seller_my_products()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте правильность данных")
        
        tk.Button(dialog, text="Сохранить", command=save_product).grid(row=5, column=0, columnspan=2, pady=20)
    
    def seller_edit_product(self, tree):
        """Редактирование товара"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите товар")
            return
        
        product_id = tree.item(selected[0])['values'][0]
        data = self._load_data()
        product = next((p for p in data['products'] if p['id'] == product_id), None)
        
        if not product:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать товар")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        name_entry = tk.Entry(dialog, width=25)
        name_entry.insert(0, product['name'])
        name_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(dialog, text="Цена:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        price_entry = tk.Entry(dialog, width=25)
        price_entry.insert(0, product['price'])
        price_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(dialog, text="Количество:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        stock_entry = tk.Entry(dialog, width=25)
        stock_entry.insert(0, product['stock'])
        stock_entry.grid(row=2, column=1, pady=10)
        
        tk.Label(dialog, text="Описание:").grid(row=3, column=0, padx=10, pady=10, sticky='ne')
        desc_text = tk.Text(dialog, width=25, height=4)
        desc_text.insert('1.0', product['description'])
        desc_text.grid(row=3, column=1, pady=10)
        
        def save_changes():
            try:
                product['name'] = name_entry.get()
                product['price'] = float(price_entry.get())
                product['stock'] = int(stock_entry.get())
                product['description'] = desc_text.get('1.0', 'end').strip()
                self._save_data(data)
                messagebox.showinfo("Успех", "Изменения сохранены")
                dialog.destroy()
                self.seller_my_products()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте правильность данных")
        
        tk.Button(dialog, text="Сохранить", command=save_changes).grid(row=4, column=0, columnspan=2, pady=20)
    
    def seller_delete_product(self, tree):
        """Удаление товара"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите товар")
            return
        
        product_id = tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить товар?"):
            data = self._load_data()
            data['products'] = [p for p in data['products'] if p['id'] != product_id]
            self._save_data(data)
            self.seller_my_products()
    
    def seller_orders(self):
        """Заказы продавца"""
        for widget in self.seller_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.seller_display_frame, text="Мои заказы",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        my_orders = [o for o in data['orders'] if o['seller'] == self.auth.current_user['username']]
        
        columns = ('ID', 'Покупатель', 'Товар', 'Количество', 'Сумма', 'Статус')
        tree = ttk.Treeview(self.seller_display_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for order in my_orders:
            tree.insert('', 'end', values=(
                order['id'],
                order['buyer'],
                order['product_name'],
                order['quantity'],
                order['total'],
                order['status']
            ))
        
        tree.pack(fill='both', expand=True, pady=5)
        
        def change_status():
            selected = tree.selection()
            if not selected:
                return
            
            order_id = tree.item(selected[0])['values'][0]
            order = next((o for o in data['orders'] if o['id'] == order_id), None)
            
            statuses = ['Новый', 'Обработан', 'Отправлен', 'Доставлен', 'Отменен']
            
            status_dialog = tk.Toplevel(self.root)
            status_dialog.title("Изменить статус")
            status_dialog.geometry("300x150")
            
            tk.Label(status_dialog, text="Выберите статус:").pack(pady=10)
            
            status_var = tk.StringVar(value=order['status'])
            for status in statuses:
                tk.Radiobutton(status_dialog, text=status, variable=status_var, value=status).pack(anchor='w', padx=50)
            
            def save_status():
                order['status'] = status_var.get()
                self._save_data(data)
                status_dialog.destroy()
                self.seller_orders()
            
            tk.Button(status_dialog, text="Сохранить", command=save_status).pack(pady=10)
        
        tk.Button(self.seller_display_frame, text="Изменить статус заказа",
                 command=change_status).pack(pady=5)
    
    def seller_stats(self):
        """Статистика продавца"""
        for widget in self.seller_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.seller_display_frame, text="Моя статистика",
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self._load_data()
        my_products = [p for p in data['products'] 
                      if p['seller'] == self.auth.current_user['username']]
        my_orders = [o for o in data['orders'] 
                    if o['seller'] == self.auth.current_user['username']]
        
        total_products = len(my_products)
        total_orders = len(my_orders)
        total_revenue = sum(o['total'] for o in my_orders)
        
        stats_frame = tk.Frame(self.seller_display_frame)
        stats_frame.pack(pady=20)
        
        stats = [
            ("Товаров в каталоге:", total_products),
            ("Получено заказов:", total_orders),
            ("Общая выручка:", f"{total_revenue} руб.")
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 12)).grid(row=i, column=0, sticky='e', padx=10, pady=10)
            tk.Label(stats_frame, text=str(value), font=('Arial', 12, 'bold')).grid(row=i, column=1, sticky='w', padx=10, pady=10)
    
    # ОКНО ПОКУПАТЕЛЯ
    def show_buyer_window(self):
        """Главное окно покупателя"""
        self.clear_window()
        self.root.title(f"Маркетплейс - Покупатель ({self.auth.current_user['username']})")
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=self.logout)
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="МАРКЕТПЛЕЙС", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Каталог товаров", width=20,
                 command=self.buyer_catalog).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Корзина", width=20,
                 command=self.buyer_cart).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Мои заказы", width=20,
                 command=self.buyer_orders).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Мои отзывы", width=20,
                 command=self.buyer_reviews).grid(row=1, column=1, padx=5, pady=5)
        
        self.buyer_display_frame = tk.Frame(main_frame)
        self.buyer_display_frame.pack(fill='both', expand=True, pady=10)
        
        self.buyer_catalog()
    
    def buyer_catalog(self):
        """Каталог товаров"""
        for widget in self.buyer_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.buyer_display_frame, text="Каталог товаров",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        # Поиск
        search_frame = tk.Frame(self.buyer_display_frame)
        search_frame.pack(pady=5)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        data = self._load_data()
        
        columns = ('ID', 'Название', 'Категория', 'Цена', 'Продавец', 'Остаток')
        tree = ttk.Treeview(self.buyer_display_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
        
        def update_catalog(search_text=''):
            tree.delete(*tree.get_children())
            for product in data['products']:
                if search_text.lower() in product['name'].lower() or not search_text:
                    tree.insert('', 'end', values=(
                        product['id'],
                        product['name'],
                        product['category'],
                        f"{product['price']} руб.",
                        product['seller'],
                        product['stock']
                    ))
        
        update_catalog()
        
        tk.Button(search_frame, text="Искать",
                 command=lambda: update_catalog(search_entry.get())).pack(side='left', padx=5)
        tk.Button(search_frame, text="Сбросить",
                 command=lambda: [search_entry.delete(0, 'end'), update_catalog()]).pack(side='left', padx=5)
        
        tree.pack(fill='both', expand=True, pady=5)
        
        def add_to_cart():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите товар")
                return
            
            product_id = tree.item(selected[0])['values'][0]
            username = self.auth.current_user['username']
            
            if username not in data['cart']:
                data['cart'][username] = []
            
            if product_id not in [item['product_id'] for item in data['cart'][username]]:
                data['cart'][username].append({
                    'product_id': product_id,
                    'quantity': 1
                })
                self._save_data(data)
                messagebox.showinfo("Успех", "Товар добавлен в корзину")
            else:
                messagebox.showinfo("Информация", "Товар уже в корзине")
        
        tk.Button(self.buyer_display_frame, text="Добавить в корзину",
                 command=add_to_cart).pack(pady=5)
    
    def buyer_cart(self):
        """Корзина покупателя"""
        for widget in self.buyer_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.buyer_display_frame, text="Моя корзина",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        username = self.auth.current_user['username']
        
        if username not in data['cart'] or not data['cart'][username]:
            tk.Label(self.buyer_display_frame, text="Корзина пуста",
                    font=('Arial', 12)).pack(pady=20)
            return
        
        columns = ('Товар', 'Цена', 'Количество', 'Сумма')
        tree = ttk.Treeview(self.buyer_display_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
        
        total_sum = 0
        for item in data['cart'][username]:
            product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
            if product:
                item_total = product['price'] * item['quantity']
                total_sum += item_total
                tree.insert('', 'end', values=(
                    product['name'],
                    f"{product['price']} руб.",
                    item['quantity'],
                    f"{item_total} руб."
                ))
        
        tree.pack(fill='both', expand=True, pady=5)
        
        tk.Label(self.buyer_display_frame, text=f"ИТОГО: {total_sum} руб.",
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(self.buyer_display_frame)
        btn_frame.pack(pady=5)
        
        def clear_cart():
            data['cart'][username] = []
            self._save_data(data)
            self.buyer_cart()
        
        def make_order():
            for item in data['cart'][username]:
                product = next((p for p in data['products'] if p['id'] == item['product_id']), None)
                if product and product['stock'] >= item['quantity']:
                    new_order = {
                        'id': max([o['id'] for o in data['orders']], default=0) + 1,
                        'buyer': username,
                        'seller': product['seller'],
                        'product_name': product['name'],
                        'product_id': product['id'],
                        'quantity': item['quantity'],
                        'total': product['price'] * item['quantity'],
                        'status': 'Новый',
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    data['orders'].append(new_order)
                    product['stock'] -= item['quantity']
            
            data['cart'][username] = []
            self._save_data(data)
            messagebox.showinfo("Успех", "Заказ оформлен!")
            self.buyer_cart()
        
        tk.Button(btn_frame, text="Оформить заказ", command=make_order).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Очистить корзину", command=clear_cart).pack(side='left', padx=5)
    
    def buyer_orders(self):
        """Заказы покупателя"""
        for widget in self.buyer_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.buyer_display_frame, text="Мои заказы",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        my_orders = [o for o in data['orders'] 
                    if o['buyer'] == self.auth.current_user['username']]
        
        if not my_orders:
            tk.Label(self.buyer_display_frame, text="Заказов пока нет",
                    font=('Arial', 12)).pack(pady=20)
            return
        
        columns = ('ID', 'Товар', 'Количество', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(self.buyer_display_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for order in my_orders:
            tree.insert('', 'end', values=(
                order['id'],
                order['product_name'],
                order['quantity'],
                f"{order['total']} руб.",
                order['status'],
                order['date']
            ))
        
        tree.pack(fill='both', expand=True, pady=5)
        
        def leave_review():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите заказ")
                return
            
            order_id = tree.item(selected[0])['values'][0]
            order = next((o for o in data['orders'] if o['id'] == order_id), None)
            
            review_dialog = tk.Toplevel(self.root)
            review_dialog.title("Оставить отзыв")
            review_dialog.geometry("400x300")
            
            tk.Label(review_dialog, text=f"Отзыв на: {order['product_name']}",
                    font=('Arial', 12, 'bold')).pack(pady=10)
            
            tk.Label(review_dialog, text="Рейтинг (1-5):").pack(pady=5)
            rating_var = tk.IntVar(value=5)
            tk.Scale(review_dialog, from_=1, to=5, orient='horizontal',
                    variable=rating_var).pack(pady=5)
            
            tk.Label(review_dialog, text="Текст отзыва:").pack(pady=5)
            text_widget = tk.Text(review_dialog, width=40, height=8)
            text_widget.pack(pady=5)
            
            def save_review():
                new_review = {
                    'id': max([r['id'] for r in data['reviews']], default=0) + 1,
                    'buyer': self.auth.current_user['username'],
                    'product_id': order['product_id'],
                    'product_name': order['product_name'],
                    'rating': rating_var.get(),
                    'text': text_widget.get('1.0', 'end').strip(),
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                data['reviews'].append(new_review)
                self._save_data(data)
                messagebox.showinfo("Успех", "Отзыв добавлен!")
                review_dialog.destroy()
            
            tk.Button(review_dialog, text="Сохранить отзыв", command=save_review).pack(pady=10)
        
        tk.Button(self.buyer_display_frame, text="Оставить отзыв на заказ",
                 command=leave_review).pack(pady=5)
    
    def buyer_reviews(self):
        """Отзывы покупателя"""
        for widget in self.buyer_display_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.buyer_display_frame, text="Мои отзывы",
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        data = self._load_data()
        my_reviews = [r for r in data['reviews'] 
                     if r['buyer'] == self.auth.current_user['username']]
        
        if not my_reviews:
            tk.Label(self.buyer_display_frame, text="Отзывов пока нет",
                    font=('Arial', 12)).pack(pady=20)
            return
        
        for review in my_reviews:
            frame = tk.Frame(self.buyer_display_frame, relief='solid', borderwidth=1)
            frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(frame, text=f"Товар: {review['product_name']} | Рейтинг: {review['rating']}/5",
                    font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=2)
            tk.Label(frame, text=review['text'], wraplength=700).pack(anchor='w', padx=5, pady=2)
            tk.Label(frame, text=f"Дата: {review['date']}", font=('Arial', 9), fg='gray').pack(anchor='w', padx=5, pady=2)
    
    def logout(self):
        """Выход из системы"""
        self.auth.logout()
        self.show_login_window()


if __name__ == "__main__":
    root = tk.Tk()
    app = MarketplaceApp(root)
    root.mainloop()