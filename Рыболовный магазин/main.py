import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import AuthManager

class FishingShopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Рыболовный магазин")
        self.root.geometry("900x600")
        
        self.auth = AuthManager()
        self.data_file = 'data.json'
        
        # Показываем окно входа
        self.show_login_window()
        
    
    def load_data(self):
        # Загрузка данных из JSON
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        # Сохранение данных в JSON
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        # Окно входа в систему
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="🎣 Рыболовный магазин", font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, font=('Arial', 12), width=20)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, font=('Arial', 12), width=20, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, role = self.auth.login(username, password)
            if success:
                self.show_main_window(role)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", font=('Arial', 12), width=15, command=do_login).grid(row=3, column=0, columnspan=2, pady=10)
        
        info_text = "Тестовые аккаунты:\nadmin / admin123\nseller / seller123\nclient / client123"
        tk.Label(frame, text=info_text, font=('Arial', 9), fg='gray', justify='left').grid(row=4, column=0, columnspan=2, pady=10)
    
    def show_main_window(self, role):
        # Главное окно в зависимости от роли
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"🎣 Рыболовный магазин", bg='#2c3e50', fg='white', font=('Arial', 16, 'bold')).pack(side='left', padx=20, pady=10)
        tk.Label(top_frame, text=f"Пользователь: {self.auth.current_user['username']} ({role})", bg='#2c3e50', fg='white', font=('Arial', 10)).pack(side='right', padx=20)
        
        # Боковая панель меню
        menu_frame = tk.Frame(self.root, bg='#34495e', width=200)
        menu_frame.pack(side='left', fill='y')
        
        # Основная область
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Меню в зависимости от роли
        if role == 'administrator':
            self.create_admin_menu(menu_frame)
        elif role == 'seller':
            self.create_seller_menu(menu_frame)
        else:  # client
            self.create_client_menu(menu_frame)
        
        # Кнопка выхода
        tk.Button(menu_frame, text="Выход", bg='#e74c3c', fg='white', font=('Arial', 10), 
                 command=self.logout).pack(side='bottom', fill='x', pady=10)
    
    def create_admin_menu(self, parent):
        # Меню администратора
        buttons = [
            ("Управление пользователями", self.show_users_management),
            ("Управление товарами", self.show_products_management),
            ("Управление категориями", self.show_categories_management),
            ("Просмотр заказов", self.show_orders_view),
            ("Отчеты", self.show_reports),
            ("Резервное копирование", self.backup_data)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, bg='#34495e', fg='white', font=('Arial', 10),
                     command=command, relief='flat', anchor='w', padx=20, pady=10).pack(fill='x')
    
    def create_seller_menu(self, parent):
        # Меню продавца
        buttons = [
            ("Оформление заказа", self.show_create_order),
            ("Просмотр заказов", self.show_orders_view),
            ("Управление клиентами", self.show_customers_management),
            ("Поиск товаров", self.show_products_search),
            ("Отчеты продаж", self.show_sales_report)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, bg='#34495e', fg='white', font=('Arial', 10),
                     command=command, relief='flat', anchor='w', padx=20, pady=10).pack(fill='x')
    
    def create_client_menu(self, parent):
        # Меню клиента
        buttons = [
            ("Каталог товаров", self.show_catalog),
            ("Поиск по категории", self.show_category_search),
            ("Моя корзина", self.show_cart),
            ("Создать заказ", self.show_client_create_order),
            ("Мои заказы", self.show_my_orders)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, bg='#34495e', fg='white', font=('Arial', 10),
                     command=command, relief='flat', anchor='w', padx=20, pady=10).pack(fill='x')
        
        # Инициализация корзины
        if not hasattr(self, 'cart'):
            self.cart = []
    
    def logout(self):
        # Выход из системы
        self.auth.logout()
        self.show_login_window()
    
    # === ФУНКЦИИ АДМИНИСТРАТОРА ===
    
    def show_users_management(self):
        # Управление пользователями
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление пользователями", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Таблица пользователей
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Логин', 'Роль', 'Дата создания')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Загрузка пользователей
        users = self.auth.get_all_users()
        for user in users:
            tree.insert('', 'end', values=(user['username'], user['role'], user['created']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        def add_user():
            # Окно добавления пользователя
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить пользователя")
            dialog.geometry("300x250")
            
            tk.Label(dialog, text="Логин:").pack(pady=5)
            username_entry = tk.Entry(dialog)
            username_entry.pack(pady=5)
            
            tk.Label(dialog, text="Пароль:").pack(pady=5)
            password_entry = tk.Entry(dialog, show='*')
            password_entry.pack(pady=5)
            
            tk.Label(dialog, text="Роль:").pack(pady=5)
            role_var = tk.StringVar(value='client')
            role_combo = ttk.Combobox(dialog, textvariable=role_var, values=['administrator', 'seller', 'client'])
            role_combo.pack(pady=5)
            
            def save_user():
                username = username_entry.get()
                password = password_entry.get()
                role = role_var.get()
                
                if not username or not password:
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                success, msg = self.auth.register(username, password, role)
                if success:
                    messagebox.showinfo("Успех", msg)
                    dialog.destroy()
                    self.show_users_management()
                else:
                    messagebox.showerror("Ошибка", msg)
            
            tk.Button(dialog, text="Сохранить", command=save_user).pack(pady=10)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите пользователя")
                return
            
            username = tree.item(selected[0])['values'][0]
            if username == self.auth.current_user['username']:
                messagebox.showerror("Ошибка", "Нельзя удалить текущего пользователя")
                return
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                self.auth.delete_user(username)
                self.show_users_management()
        
        tk.Button(btn_frame, text="Добавить", command=add_user, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, width=15).pack(side='left', padx=5)
    
    def show_products_management(self):
        # Управление товарами
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление товарами", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Название', 'Категория', 'Цена', 'Остаток')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        data = self.load_data()
        for product in data['products']:
            tree.insert('', 'end', values=(product['id'], product['name'], product['category'], 
                                          f"{product['price']} ₽", product['stock']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        def add_product():
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить товар")
            dialog.geometry("350x300")
            
            tk.Label(dialog, text="Название:").pack(pady=5)
            name_entry = tk.Entry(dialog, width=30)
            name_entry.pack(pady=5)
            
            tk.Label(dialog, text="Категория:").pack(pady=5)
            cat_var = tk.StringVar()
            categories = [c['name'] for c in data['categories']]
            cat_combo = ttk.Combobox(dialog, textvariable=cat_var, values=categories, width=28)
            cat_combo.pack(pady=5)
            
            tk.Label(dialog, text="Цена:").pack(pady=5)
            price_entry = tk.Entry(dialog, width=30)
            price_entry.pack(pady=5)
            
            tk.Label(dialog, text="Количество:").pack(pady=5)
            stock_entry = tk.Entry(dialog, width=30)
            stock_entry.pack(pady=5)
            
            def save_product():
                name = name_entry.get()
                category = cat_var.get()
                
                try:
                    price = float(price_entry.get())
                    stock = int(stock_entry.get())
                except:
                    messagebox.showerror("Ошибка", "Неверный формат цены или количества")
                    return
                
                if not name or not category:
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                data = self.load_data()
                new_id = max([p['id'] for p in data['products']], default=0) + 1
                data['products'].append({
                    'id': new_id,
                    'name': name,
                    'category': category,
                    'price': price,
                    'stock': stock
                })
                self.save_data(data)
                messagebox.showinfo("Успех", "Товар добавлен")
                dialog.destroy()
                self.show_products_management()
            
            tk.Button(dialog, text="Сохранить", command=save_product).pack(pady=10)
        
        def delete_product():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите товар")
                return
            
            product_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить товар?"):
                data = self.load_data()
                data['products'] = [p for p in data['products'] if p['id'] != product_id]
                self.save_data(data)
                self.show_products_management()
        
        tk.Button(btn_frame, text="Добавить", command=add_product, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_product, width=15).pack(side='left', padx=5)
    
    def show_categories_management(self):
        # Управление категориями
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление категориями", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Название категории')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        tree.heading('ID', text='ID')
        tree.column('ID', width=100)
        tree.heading('Название категории', text='Название категории')
        tree.column('Название категории', width=400)
        
        data = self.load_data()
        for cat in data['categories']:
            tree.insert('', 'end', values=(cat['id'], cat['name']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        def add_category():
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить категорию")
            dialog.geometry("300x150")
            
            tk.Label(dialog, text="Название категории:").pack(pady=10)
            name_entry = tk.Entry(dialog, width=30)
            name_entry.pack(pady=10)
            
            def save_category():
                name = name_entry.get()
                if not name:
                    messagebox.showerror("Ошибка", "Введите название")
                    return
                
                data = self.load_data()
                new_id = max([c['id'] for c in data['categories']], default=0) + 1
                data['categories'].append({'id': new_id, 'name': name})
                self.save_data(data)
                messagebox.showinfo("Успех", "Категория добавлена")
                dialog.destroy()
                self.show_categories_management()
            
            tk.Button(dialog, text="Сохранить", command=save_category).pack(pady=10)
        
        def delete_category():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите категорию")
                return
            
            cat_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить категорию?"):
                data = self.load_data()
                data['categories'] = [c for c in data['categories'] if c['id'] != cat_id]
                self.save_data(data)
                self.show_categories_management()
        
        tk.Button(btn_frame, text="Добавить", command=add_category, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_category, width=15).pack(side='left', padx=5)
    
    def show_reports(self):
        # Отчеты
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Отчеты системы", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        report_frame = tk.Frame(self.content_frame)
        report_frame.pack(pady=20)
        
        # Статистика
        total_products = len(data['products'])
        total_orders = len(data['orders'])
        total_customers = len(data['customers'])
        total_revenue = sum(order['total'] for order in data['orders'])
        
        stats = [
            f"Всего товаров: {total_products}",
            f"Всего заказов: {total_orders}",
            f"Всего клиентов: {total_customers}",
            f"Общая выручка: {total_revenue} ₽"
        ]
        
        for stat in stats:
            tk.Label(report_frame, text=stat, font=('Arial', 14), anchor='w').pack(fill='x', pady=5)
    
    def backup_data(self):
        # Резервное копирование отключено (тестовые данные)
        messagebox.showinfo("Информация", "Резервное копирование не требуется для тестовых данных")
    
    # === ФУНКЦИИ ПРОДАВЦА ===
    
    def show_create_order(self):
        # Оформление заказа продавцом
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Оформление заказа", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        # Выбор клиента
        tk.Label(self.content_frame, text="Клиент:").pack(pady=5)
        customer_var = tk.StringVar()
        customers = [c['name'] for c in data['customers']]
        customer_combo = ttk.Combobox(self.content_frame, textvariable=customer_var, values=customers, width=30)
        customer_combo.pack(pady=5)
        
        # Список товаров для заказа
        order_items = []
        
        items_frame = tk.Frame(self.content_frame)
        items_frame.pack(pady=10)
        
        tk.Label(items_frame, text="Товары в заказе:", font=('Arial', 12, 'bold')).pack()
        
        items_listbox = tk.Listbox(items_frame, width=60, height=10)
        items_listbox.pack(pady=5)
        
        def add_item_to_order():
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить товар")
            dialog.geometry("300x200")
            
            tk.Label(dialog, text="Товар:").pack(pady=5)
            product_var = tk.StringVar()
            products = [f"{p['name']} ({p['price']} ₽)" for p in data['products']]
            product_combo = ttk.Combobox(dialog, textvariable=product_var, values=products, width=30)
            product_combo.pack(pady=5)
            
            tk.Label(dialog, text="Количество:").pack(pady=5)
            qty_entry = tk.Entry(dialog, width=30)
            qty_entry.pack(pady=5)
            
            def save_item():
                try:
                    qty = int(qty_entry.get())
                    product_name = product_var.get().split(' (')[0]
                    product = next(p for p in data['products'] if p['name'] == product_name)
                    
                    if qty > product['stock']:
                        messagebox.showerror("Ошибка", "Недостаточно товара на складе")
                        return
                    
                    order_items.append({
                        'product': product['name'],
                        'quantity': qty,
                        'price': product['price']
                    })
                    items_listbox.insert('end', f"{product['name']} x{qty} = {product['price']*qty} ₽")
                    dialog.destroy()
                except:
                    messagebox.showerror("Ошибка", "Проверьте введенные данные")
            
            tk.Button(dialog, text="Добавить", command=save_item).pack(pady=10)
        
        def remove_item():
            selected = items_listbox.curselection()
            if selected:
                items_listbox.delete(selected[0])
                order_items.pop(selected[0])
        
        btn_frame = tk.Frame(items_frame)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Добавить товар", command=add_item_to_order).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=remove_item).pack(side='left', padx=5)
        
        def save_order():
            customer = customer_var.get()
            if not customer or not order_items:
                messagebox.showerror("Ошибка", "Выберите клиента и добавьте товары")
                return
            
            total = sum(item['price'] * item['quantity'] for item in order_items)
            
            data = self.load_data()
            new_id = max([o['id'] for o in data['orders']], default=0) + 1
            
            new_order = {
                'id': new_id,
                'customer': customer,
                'items': order_items,
                'total': total,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status': 'Новый',
                'user': self.auth.current_user['username']
            }
            
            # Обновляем остатки товаров
            for item in order_items:
                for product in data['products']:
                    if product['name'] == item['product']:
                        product['stock'] -= item['quantity']
            
            data['orders'].append(new_order)
            self.save_data(data)
            
            messagebox.showinfo("Успех", f"Заказ #{new_id} создан на сумму {total} ₽")
            self.show_orders_view()
        
        tk.Button(self.content_frame, text="Оформить заказ", command=save_order, width=20, bg='#27ae60', fg='white').pack(pady=20)
    
    def show_orders_view(self):
        # Просмотр заказов
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Список заказов", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Клиент', 'Сумма', 'Дата', 'Статус')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        data = self.load_data()
        for order in data['orders']:
            tree.insert('', 'end', values=(order['id'], order['customer'], 
                                          f"{order['total']} ₽", order['date'], order['status']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        def view_details():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите заказ")
                return
            
            order_id = tree.item(selected[0])['values'][0]
            order = next(o for o in data['orders'] if o['id'] == order_id)
            
            details = f"Заказ #{order['id']}\n"
            details += f"Клиент: {order['customer']}\n"
            details += f"Дата: {order['date']}\n"
            details += f"Статус: {order['status']}\n\n"
            details += "Товары:\n"
            for item in order['items']:
                details += f"  - {item['product']} x{item['quantity']} = {item['price']*item['quantity']} ₽\n"
            details += f"\nИтого: {order['total']} ₽"
            
            messagebox.showinfo("Детали заказа", details)
        
        tk.Button(self.content_frame, text="Просмотр деталей", command=view_details, width=20).pack(pady=10)
    
    def show_customers_management(self):
        # Управление клиентами
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление клиентами", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Имя', 'Телефон', 'Email')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        data = self.load_data()
        for customer in data['customers']:
            tree.insert('', 'end', values=(customer['id'], customer['name'], 
                                          customer['phone'], customer['email']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        def add_customer():
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить клиента")
            dialog.geometry("300x250")
            
            tk.Label(dialog, text="Имя:").pack(pady=5)
            name_entry = tk.Entry(dialog, width=30)
            name_entry.pack(pady=5)
            
            tk.Label(dialog, text="Телефон:").pack(pady=5)
            phone_entry = tk.Entry(dialog, width=30)
            phone_entry.pack(pady=5)
            
            tk.Label(dialog, text="Email:").pack(pady=5)
            email_entry = tk.Entry(dialog, width=30)
            email_entry.pack(pady=5)
            
            def save_customer():
                name = name_entry.get()
                phone = phone_entry.get()
                email = email_entry.get()
                
                if not name or not phone:
                    messagebox.showerror("Ошибка", "Заполните обязательные поля")
                    return
                
                data = self.load_data()
                new_id = max([c['id'] for c in data['customers']], default=0) + 1
                data['customers'].append({
                    'id': new_id,
                    'name': name,
                    'phone': phone,
                    'email': email
                })
                self.save_data(data)
                messagebox.showinfo("Успех", "Клиент добавлен")
                dialog.destroy()
                self.show_customers_management()
            
            tk.Button(dialog, text="Сохранить", command=save_customer).pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить клиента", command=add_customer, width=20).pack()
    
    def show_products_search(self):
        # Поиск товаров
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Поиск товаров", font=('Arial', 16, 'bold')).pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Название', 'Категория', 'Цена', 'Остаток')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        def do_search():
            query = search_entry.get().lower()
            tree.delete(*tree.get_children())
            
            data = self.load_data()
            for product in data['products']:
                if query in product['name'].lower() or query in product['category'].lower():
                    tree.insert('', 'end', values=(product['id'], product['name'], 
                                                  product['category'], f"{product['price']} ₽", 
                                                  product['stock']))
        
        tk.Button(search_frame, text="Найти", command=do_search).pack(side='left', padx=5)
        
        # Показываем все товары по умолчанию
        do_search()
    
    def show_sales_report(self):
        # Отчет продаж
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Отчет продаж", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        report_frame = tk.Frame(self.content_frame)
        report_frame.pack(pady=20)
        
        total_orders = len(data['orders'])
        total_revenue = sum(order['total'] for order in data['orders'])
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        
        stats = [
            f"Всего заказов: {total_orders}",
            f"Общая выручка: {total_revenue} ₽",
            f"Средний чек: {avg_order:.2f} ₽"
        ]
        
        for stat in stats:
            tk.Label(report_frame, text=stat, font=('Arial', 14), anchor='w').pack(fill='x', pady=5)
    
    # === ФУНКЦИИ КЛИЕНТА ===
    
    def show_catalog(self):
        # Каталог товаров
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Каталог товаров", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Название', 'Категория', 'Цена', 'В наличии')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        data = self.load_data()
        for product in data['products']:
            tree.insert('', 'end', values=(product['id'], product['name'], 
                                          product['category'], f"{product['price']} ₽", 
                                          product['stock']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        def add_to_cart():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите товар")
                return
            
            product_id = tree.item(selected[0])['values'][0]
            product = next(p for p in data['products'] if p['id'] == product_id)
            
            # Проверяем, есть ли товар уже в корзине
            for item in self.cart:
                if item['id'] == product_id:
                    item['quantity'] += 1
                    messagebox.showinfo("Успех", f"Товар {product['name']} добавлен в корзину")
                    return
            
            self.cart.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            })
            messagebox.showinfo("Успех", f"Товар {product['name']} добавлен в корзину")
        
        tk.Button(self.content_frame, text="Добавить в корзину", command=add_to_cart, width=20).pack(pady=10)
    
    def show_category_search(self):
        # Поиск по категории
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Поиск по категории", font=('Arial', 16, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        tk.Label(self.content_frame, text="Выберите категорию:").pack(pady=10)
        
        category_var = tk.StringVar()
        categories = [c['name'] for c in data['categories']]
        category_combo = ttk.Combobox(self.content_frame, textvariable=category_var, values=categories, width=30)
        category_combo.pack(pady=5)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Название', 'Цена', 'В наличии')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        def search_by_category():
            category = category_var.get()
            tree.delete(*tree.get_children())
            
            for product in data['products']:
                if product['category'] == category:
                    tree.insert('', 'end', values=(product['id'], product['name'], 
                                                  f"{product['price']} ₽", product['stock']))
        
        tk.Button(self.content_frame, text="Найти", command=search_by_category, width=15).pack(pady=10)
    
    def show_cart(self):
        # Корзина
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Моя корзина", font=('Arial', 16, 'bold')).pack(pady=10)
        
        if not self.cart:
            tk.Label(self.content_frame, text="Корзина пуста", font=('Arial', 14)).pack(pady=50)
            return
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Название', 'Цена', 'Количество', 'Сумма')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        total = 0
        for item in self.cart:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            tree.insert('', 'end', values=(item['name'], f"{item['price']} ₽", 
                                          item['quantity'], f"{subtotal} ₽"))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        tk.Label(self.content_frame, text=f"ИТОГО: {total} ₽", font=('Arial', 14, 'bold')).pack(pady=10)
        
        def clear_cart():
            if messagebox.askyesno("Подтверждение", "Очистить корзину?"):
                self.cart.clear()
                self.show_cart()
        
        tk.Button(self.content_frame, text="Очистить корзину", command=clear_cart, width=20).pack(pady=5)
    
    def show_client_create_order(self):
        # Создание заказа клиентом
        if not self.cart:
            messagebox.showwarning("Внимание", "Корзина пуста")
            return
        
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        
        if messagebox.askyesno("Подтверждение", f"Оформить заказ на сумму {total} ₽?"):
            data = self.load_data()
            new_id = max([o['id'] for o in data['orders']], default=0) + 1
            
            order_items = [{'product': item['name'], 'quantity': item['quantity'], 
                           'price': item['price']} for item in self.cart]
            
            new_order = {
                'id': new_id,
                'customer': self.auth.current_user['username'],
                'items': order_items,
                'total': total,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status': 'Новый',
                'user': self.auth.current_user['username']
            }
            
            # Обновляем остатки
            for item in self.cart:
                for product in data['products']:
                    if product['id'] == item['id']:
                        product['stock'] -= item['quantity']
            
            data['orders'].append(new_order)
            self.save_data(data)
            
            self.cart.clear()
            messagebox.showinfo("Успех", f"Заказ #{new_id} оформлен!\nСумма: {total} ₽")
            self.show_my_orders()
    
    def show_my_orders(self):
        # Мои заказы
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои заказы", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.content_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Дата', 'Сумма', 'Статус')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        data = self.load_data()
        my_orders = [o for o in data['orders'] if o['user'] == self.auth.current_user['username']]
        
        for order in my_orders:
            tree.insert('', 'end', values=(order['id'], order['date'], 
                                          f"{order['total']} ₽", order['status']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        def view_details():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите заказ")
                return
            
            order_id = tree.item(selected[0])['values'][0]
            order = next(o for o in my_orders if o['id'] == order_id)
            
            details = f"Заказ #{order['id']}\n"
            details += f"Дата: {order['date']}\n"
            details += f"Статус: {order['status']}\n\n"
            details += "Товары:\n"
            for item in order['items']:
                details += f"  - {item['product']} x{item['quantity']} = {item['price']*item['quantity']} ₽\n"
            details += f"\nИтого: {order['total']} ₽"
            
            messagebox.showinfo("Детали заказа", details)
        
        tk.Button(self.content_frame, text="Просмотр деталей", command=view_details, width=20).pack(pady=10)
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = FishingShopApp()
    app.run()