import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import auth

DATA_FILE = 'data.json'

class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Книжный магазин - Авторизация")
        self.root.geometry("400x300")
        self.current_user = None
        self.cart = []
        
        # Инициализация данных
        self.init_data()
        
        # Показать окно входа
        self.show_login_window()
    
    def init_data(self):
        """Инициализация данных - проверка существования файлов"""
        if not os.path.exists(DATA_FILE):
            raise FileNotFoundError(f"Файл {DATA_FILE} не найден. Запустите программу с существующими тестовыми данными.")

        if not os.path.exists('users.json'):
            raise FileNotFoundError("Файл users.json не найден. Запустите программу с существующими тестовыми данными.")
    
    def load_data(self):
        """Загрузка данных из файла"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        """Окно авторизации"""
        self.clear_window()
        self.root.geometry("400x300")
        self.root.title("Книжный магазин - Авторизация")
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="КНИЖНЫЙ МАГАЗИН", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky="e", pady=5)
        self.login_entry = tk.Entry(frame, width=25)
        self.login_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(frame, show="*", width=25)
        self.password_entry.grid(row=2, column=1, pady=5)
        
        tk.Button(frame, text="Войти", command=self.login, width=20, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Регистрация", command=self.show_register_window, width=20).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Подсказка
        hint = tk.Label(frame, text="Подсказка: admin/admin123, seller/seller123, client/client123", 
                       font=("Arial", 8), fg="gray")
        hint.grid(row=5, column=0, columnspan=2, pady=10)
    
    def login(self):
        """Обработка входа"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        user = auth.authenticate(username, password)
        if user:
            self.current_user = user
            self.show_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_register_window(self):
        """Окно регистрации"""
        self.clear_window()
        self.root.geometry("400x350")
        self.root.title("Регистрация")
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="РЕГИСТРАЦИЯ", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky="e", pady=5)
        login_entry = tk.Entry(frame, width=25)
        login_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky="e", pady=5)
        password_entry = tk.Entry(frame, show="*", width=25)
        password_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="Полное имя:").grid(row=3, column=0, sticky="e", pady=5)
        name_entry = tk.Entry(frame, width=25)
        name_entry.grid(row=3, column=1, pady=5)
        
        def register():
            username = login_entry.get()
            password = password_entry.get()
            full_name = name_entry.get()
            
            if not username or not password or not full_name:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = auth.register_user(username, password, full_name, "client")
            if success:
                messagebox.showinfo("Успех", message)
                self.show_login_window()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(frame, text="Зарегистрироваться", command=register, width=20, bg="#2196F3", fg="white").grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Назад", command=self.show_login_window, width=20).grid(row=5, column=0, columnspan=2, pady=5)
    
    def show_main_window(self):
        """Главное окно в зависимости от роли"""
        self.clear_window()
        self.root.geometry("900x600")
        self.root.title(f"Книжный магазин - {self.current_user['full_name']} ({self.current_user['role']})")
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg="#2196F3", height=50)
        top_frame.pack(fill="x")
        
        tk.Label(top_frame, text=f"Пользователь: {self.current_user['full_name']}", 
                bg="#2196F3", fg="white", font=("Arial", 10)).pack(side="left", padx=10, pady=10)
        tk.Button(top_frame, text="Выход", command=self.logout, bg="#f44336", fg="white").pack(side="right", padx=10, pady=10)
        
        # Основной контент
        if self.current_user['role'] == 'admin':
            self.show_admin_panel()
        elif self.current_user['role'] == 'seller':
            self.show_seller_panel()
        else:
            self.show_client_panel()
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.cart = []
        self.show_login_window()
    
    # АДМИН ПАНЕЛЬ
    def show_admin_panel(self):
        """Панель администратора"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка управления книгами
        books_frame = tk.Frame(notebook)
        notebook.add(books_frame, text="Управление книгами")
        self.create_books_management(books_frame)
        
        # Вкладка управления заказами
        orders_frame = tk.Frame(notebook)
        notebook.add(orders_frame, text="Управление заказами")
        self.create_orders_management(orders_frame)
        
        # Вкладка управления пользователями
        users_frame = tk.Frame(notebook)
        notebook.add(users_frame, text="Управление пользователями")
        self.create_users_management(users_frame)
        
        # Вкладка статистики
        stats_frame = tk.Frame(notebook)
        notebook.add(stats_frame, text="Статистика")
        self.create_statistics(stats_frame)
    
    def create_books_management(self, parent):
        """Управление книгами"""
        # Кнопки действий
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(btn_frame, text="Добавить книгу", command=self.add_book, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Редактировать", command=lambda: self.edit_book(tree), bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_book(tree), bg="#f44336", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_books(tree), bg="#FF9800", fg="white").pack(side="left", padx=5)
        
        # Поиск
        search_frame = tk.Frame(parent)
        search_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(search_frame, text="Поиск:").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Найти", command=lambda: self.search_books(tree, search_entry.get())).pack(side="left", padx=5)
        
        # Таблица книг
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Название", "Автор", "Жанр", "Цена", "Наличие", "ISBN"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Название", text="Название")
        tree.heading("Автор", text="Автор")
        tree.heading("Жанр", text="Жанр")
        tree.heading("Цена", text="Цена")
        tree.heading("Наличие", text="Наличие")
        tree.heading("ISBN", text="ISBN")
        
        tree.column("ID", width=40)
        tree.column("Название", width=200)
        tree.column("Автор", width=150)
        tree.column("Жанр", width=100)
        tree.column("Цена", width=80)
        tree.column("Наличие", width=80)
        tree.column("ISBN", width=150)
        
        tree.pack(fill="both", expand=True)
        
        self.refresh_books(tree)
    
    def refresh_books(self, tree, books_list=None):
        """Обновление списка книг"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        books = books_list if books_list else data['books']
        
        for book in books:
            tree.insert("", "end", values=(
                book['id'], book['title'], book['author'], 
                book['genre'], f"{book['price']:.2f} ₽", 
                book['stock'], book['isbn']
            ))
    
    def search_books(self, tree, query):
        """Поиск книг"""
        if not query:
            self.refresh_books(tree)
            return
        
        data = self.load_data()
        filtered = [b for b in data['books'] if 
                   query.lower() in b['title'].lower() or 
                   query.lower() in b['author'].lower() or
                   query.lower() in b['genre'].lower()]
        
        self.refresh_books(tree, filtered)
    
    def add_book(self):
        """Добавление новой книги"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить книгу")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Автор:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        author_entry = tk.Entry(dialog, width=30)
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Жанр:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        genre_entry = tk.Entry(dialog, width=30)
        genre_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Цена:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        price_entry = tk.Entry(dialog, width=30)
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Количество:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        stock_entry = tk.Entry(dialog, width=30)
        stock_entry.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="ISBN:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        isbn_entry = tk.Entry(dialog, width=30)
        isbn_entry.grid(row=5, column=1, padx=5, pady=5)
        
        def save():
            try:
                title = title_entry.get()
                author = author_entry.get()
                genre = genre_entry.get()
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                isbn = isbn_entry.get()
                
                if not all([title, author, genre, isbn]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                data = self.load_data()
                new_id = max([b['id'] for b in data['books']]) + 1 if data['books'] else 1
                
                new_book = {
                    "id": new_id,
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "price": price,
                    "stock": stock,
                    "isbn": isbn
                }
                
                data['books'].append(new_book)
                self.save_data(data)
                
                messagebox.showinfo("Успех", "Книга добавлена")
                dialog.destroy()
                self.show_main_window()
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат цены или количества")
        
        tk.Button(dialog, text="Сохранить", command=save, bg="#4CAF50", fg="white").grid(row=6, column=0, columnspan=2, pady=20)
    
    def edit_book(self, tree):
        """Редактирование книги"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу")
            return
        
        item = tree.item(selected[0])
        book_id = int(item['values'][0])
        
        data = self.load_data()
        book = next((b for b in data['books'] if b['id'] == book_id), None)
        
        if not book:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать книгу")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.insert(0, book['title'])
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Автор:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        author_entry = tk.Entry(dialog, width=30)
        author_entry.insert(0, book['author'])
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Жанр:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        genre_entry = tk.Entry(dialog, width=30)
        genre_entry.insert(0, book['genre'])
        genre_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Цена:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        price_entry = tk.Entry(dialog, width=30)
        price_entry.insert(0, str(book['price']))
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Количество:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        stock_entry = tk.Entry(dialog, width=30)
        stock_entry.insert(0, str(book['stock']))
        stock_entry.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="ISBN:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        isbn_entry = tk.Entry(dialog, width=30)
        isbn_entry.insert(0, book['isbn'])
        isbn_entry.grid(row=5, column=1, padx=5, pady=5)
        
        def save():
            try:
                book['title'] = title_entry.get()
                book['author'] = author_entry.get()
                book['genre'] = genre_entry.get()
                book['price'] = float(price_entry.get())
                book['stock'] = int(stock_entry.get())
                book['isbn'] = isbn_entry.get()
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Книга обновлена")
                dialog.destroy()
                self.show_main_window()
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат данных")
        
        tk.Button(dialog, text="Сохранить", command=save, bg="#4CAF50", fg="white").grid(row=6, column=0, columnspan=2, pady=20)
    
    def delete_book(self, tree):
        """Удаление книги"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить выбранную книгу?"):
            return
        
        item = tree.item(selected[0])
        book_id = int(item['values'][0])
        
        data = self.load_data()
        data['books'] = [b for b in data['books'] if b['id'] != book_id]
        self.save_data(data)
        
        messagebox.showinfo("Успех", "Книга удалена")
        self.refresh_books(tree)
    
    def create_orders_management(self, parent):
        """Управление заказами"""
        # Кнопки
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_orders(tree), bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Изменить статус", command=lambda: self.change_order_status(tree), bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_order(tree), bg="#f44336", fg="white").pack(side="left", padx=5)
        
        # Таблица заказов
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Клиент", "Дата", "Сумма", "Статус"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Клиент", text="Клиент")
        tree.heading("Дата", text="Дата")
        tree.heading("Сумма", text="Сумма")
        tree.heading("Статус", text="Статус")
        
        tree.column("ID", width=50)
        tree.column("Клиент", width=200)
        tree.column("Дата", width=150)
        tree.column("Сумма", width=100)
        tree.column("Статус", width=150)
        
        tree.pack(fill="both", expand=True)
        
        self.refresh_orders(tree)
    
    def refresh_orders(self, tree):
        """Обновление списка заказов"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        
        for order in data['orders']:
            tree.insert("", "end", values=(
                order['id'], order['client_name'], order['date'],
                f"{order['total']:.2f} ₽", order['status']
            ))
    
    def change_order_status(self, tree):
        """Изменение статуса заказа"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ")
            return
        
        item = tree.item(selected[0])
        order_id = int(item['values'][0])
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменить статус")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Выберите новый статус:").pack(pady=10)
        
        status_var = tk.StringVar(value="новый")
        statuses = ["новый", "в обработке", "доставляется", "выполнен", "отменен"]
        
        for status in statuses:
            tk.Radiobutton(dialog, text=status, variable=status_var, value=status).pack(anchor="w", padx=20)
        
        def save():
            data = self.load_data()
            for order in data['orders']:
                if order['id'] == order_id:
                    order['status'] = status_var.get()
                    break
            self.save_data(data)
            messagebox.showinfo("Успех", "Статус изменен")
            dialog.destroy()
            self.refresh_orders(tree)
        
        tk.Button(dialog, text="Сохранить", command=save, bg="#4CAF50", fg="white").pack(pady=10)
    
    def delete_order(self, tree):
        """Удаление заказа"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить выбранный заказ?"):
            return
        
        item = tree.item(selected[0])
        order_id = int(item['values'][0])
        
        data = self.load_data()
        data['orders'] = [o for o in data['orders'] if o['id'] != order_id]
        self.save_data(data)
        
        messagebox.showinfo("Успех", "Заказ удален")
        self.refresh_orders(tree)
    
    def create_users_management(self, parent):
        """Управление пользователями"""
        # Кнопки
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(btn_frame, text="Добавить пользователя", command=self.add_user, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Редактировать", command=lambda: self.edit_user(tree), bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_user(tree), bg="#f44336", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_users(tree), bg="#FF9800", fg="white").pack(side="left", padx=5)
        
        # Таблица пользователей
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Логин", "Полное имя", "Роль", "Дата создания"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Логин", text="Логин")
        tree.heading("Полное имя", text="Полное имя")
        tree.heading("Роль", text="Роль")
        tree.heading("Дата создания", text="Дата создания")
        
        tree.column("ID", width=50)
        tree.column("Логин", width=150)
        tree.column("Полное имя", width=200)
        tree.column("Роль", width=100)
        tree.column("Дата создания", width=150)
        
        tree.pack(fill="both", expand=True)
        
        self.refresh_users(tree)
    
    def refresh_users(self, tree):
        """Обновление списка пользователей"""
        for item in tree.get_children():
            tree.delete(item)
        
        users = auth.get_all_users()
        
        for user in users:
            tree.insert("", "end", values=(
                user['id'], user['username'], user['full_name'],
                user['role'], user['created']
            ))
    
    def add_user(self):
        """Добавление пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Логин:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        login_entry = tk.Entry(dialog, width=30)
        login_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(dialog, show="*", width=30)
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Полное имя:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Роль:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        role_var = tk.StringVar(value="client")
        role_combo = ttk.Combobox(dialog, textvariable=role_var, values=["admin", "seller", "client"], width=27)
        role_combo.grid(row=3, column=1, padx=5, pady=5)
        
        def save():
            success, message = auth.register_user(
                login_entry.get(),
                password_entry.get(),
                name_entry.get(),
                role_var.get()
            )
            
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
                self.show_main_window()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(dialog, text="Сохранить", command=save, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=20)
    
    def edit_user(self, tree):
        """Редактирование пользователя"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        item = tree.item(selected[0])
        user_id = int(item['values'][0])
        
        users = auth.get_all_users()
        user = next((u for u in users if u['id'] == user_id), None)
        
        if not user:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать пользователя")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Полное имя:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.insert(0, user['full_name'])
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Роль:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        role_var = tk.StringVar(value=user['role'])
        role_combo = ttk.Combobox(dialog, textvariable=role_var, values=["admin", "seller", "client"], width=27)
        role_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Новый пароль:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Label(dialog, text="(оставьте пустым для сохранения)", font=("Arial", 8)).grid(row=3, column=1, sticky="w", padx=5)
        password_entry = tk.Entry(dialog, show="*", width=30)
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def save():
            password = password_entry.get() if password_entry.get() else None
            auth.update_user(user_id, name_entry.get(), role_var.get(), password)
            messagebox.showinfo("Успех", "Пользователь обновлен")
            dialog.destroy()
            self.show_main_window()
        
        tk.Button(dialog, text="Сохранить", command=save, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_user(self, tree):
        """Удаление пользователя"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        item = tree.item(selected[0])
        user_id = int(item['values'][0])
        
        if user_id == self.current_user['id']:
            messagebox.showerror("Ошибка", "Нельзя удалить текущего пользователя")
            return
        
        if not messagebox.askyesno("Подтверждение", "Удалить выбранного пользователя?"):
            return
        
        auth.delete_user(user_id)
        messagebox.showinfo("Успех", "Пользователь удален")
        self.refresh_users(tree)
    
    def create_statistics(self, parent):
        """Статистика"""
        data = self.load_data()
        
        stats_frame = tk.Frame(parent, padx=20, pady=20)
        stats_frame.pack(fill="both", expand=True)
        
        tk.Label(stats_frame, text="СТАТИСТИКА МАГАЗИНА", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Общая информация
        total_books = len(data['books'])
        total_orders = len(data['orders'])
        total_revenue = sum(order['total'] for order in data['orders'])
        total_users = len(auth.get_all_users())
        
        info_frame = tk.Frame(stats_frame)
        info_frame.pack(pady=10)
        
        stats_data = [
            ("Всего книг в каталоге:", total_books),
            ("Всего заказов:", total_orders),
            ("Общая выручка:", f"{total_revenue:.2f} ₽"),
            ("Зарегистрировано пользователей:", total_users),
        ]
        
        for i, (label, value) in enumerate(stats_data):
            tk.Label(info_frame, text=label, font=("Arial", 12)).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            tk.Label(info_frame, text=str(value), font=("Arial", 12, "bold")).grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # Статистика по статусам заказов
        tk.Label(stats_frame, text="Заказы по статусам:", font=("Arial", 12, "bold")).pack(pady=10)
        
        status_counts = {}
        for order in data['orders']:
            status = order['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        status_frame = tk.Frame(stats_frame)
        status_frame.pack(pady=5)
        
        for status, count in status_counts.items():
            tk.Label(status_frame, text=f"{status}: {count}", font=("Arial", 10)).pack(anchor="w", padx=20)
    
    # ПРОДАВЕЦ ПАНЕЛЬ
    def show_seller_panel(self):
        """Панель продавца"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка каталога
        catalog_frame = tk.Frame(notebook)
        notebook.add(catalog_frame, text="Каталог книг")
        self.create_seller_catalog(catalog_frame)
        
        # Вкладка заказов
        orders_frame = tk.Frame(notebook)
        notebook.add(orders_frame, text="Заказы")
        self.create_seller_orders(orders_frame)
    
    def create_seller_catalog(self, parent):
        """Каталог для продавца"""
        # Поиск
        search_frame = tk.Frame(parent)
        search_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(search_frame, text="Поиск:").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Найти", command=lambda: self.search_books(tree, search_entry.get())).pack(side="left", padx=5)
        tk.Button(search_frame, text="Обновить", command=lambda: self.refresh_books(tree), bg="#FF9800", fg="white").pack(side="left", padx=5)
        
        # Таблица
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Название", "Автор", "Жанр", "Цена", "Наличие", "ISBN"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Название", text="Название")
        tree.heading("Автор", text="Автор")
        tree.heading("Жанр", text="Жанр")
        tree.heading("Цена", text="Цена")
        tree.heading("Наличие", text="Наличие")
        tree.heading("ISBN", text="ISBN")
        
        tree.column("ID", width=40)
        tree.column("Название", width=200)
        tree.column("Автор", width=150)
        tree.column("Жанр", width=100)
        tree.column("Цена", width=80)
        tree.column("Наличие", width=80)
        tree.column("ISBN", width=150)
        
        tree.pack(fill="both", expand=True)
        
        self.refresh_books(tree)
    
    def create_seller_orders(self, parent):
        """Заказы для продавца"""
        # Кнопки
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_orders(tree), bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Изменить статус", command=lambda: self.change_order_status(tree), bg="#2196F3", fg="white").pack(side="left", padx=5)
        
        # Таблица
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Клиент", "Дата", "Сумма", "Статус"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Клиент", text="Клиент")
        tree.heading("Дата", text="Дата")
        tree.heading("Сумма", text="Сумма")
        tree.heading("Статус", text="Статус")
        
        tree.column("ID", width=50)
        tree.column("Клиент", width=200)
        tree.column("Дата", width=150)
        tree.column("Сумма", width=100)
        tree.column("Статус", width=150)
        
        tree.pack(fill="both", expand=True)
        
        self.refresh_orders(tree)
    
    # КЛИЕНТ ПАНЕЛЬ
    def show_client_panel(self):
        """Панель клиента"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Каталог
        catalog_frame = tk.Frame(notebook)
        notebook.add(catalog_frame, text="Каталог книг")
        self.create_client_catalog(catalog_frame)
        
        # Корзина
        cart_frame = tk.Frame(notebook)
        notebook.add(cart_frame, text=f"Корзина ({len(self.cart)})")
        self.create_cart(cart_frame)
        
        # Мои заказы
        orders_frame = tk.Frame(notebook)
        notebook.add(orders_frame, text="Мои заказы")
        self.create_client_orders(orders_frame)
    
    def create_client_catalog(self, parent):
        """Каталог для клиента"""
        # Поиск
        search_frame = tk.Frame(parent)
        search_frame.pack(fill="x", padx=5, pady=5)
        tk.Label(search_frame, text="Поиск:").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Найти", command=lambda: self.search_books(tree, search_entry.get())).pack(side="left", padx=5)
        tk.Button(search_frame, text="Добавить в корзину", command=lambda: self.add_to_cart(tree), bg="#4CAF50", fg="white").pack(side="left", padx=5)
        
        # Таблица
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Название", "Автор", "Жанр", "Цена", "Наличие"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Название", text="Название")
        tree.heading("Автор", text="Автор")
        tree.heading("Жанр", text="Жанр")
        tree.heading("Цена", text="Цена")
        tree.heading("Наличие", text="Наличие")
        
        tree.column("ID", width=40)
        tree.column("Название", width=250)
        tree.column("Автор", width=200)
        tree.column("Жанр", width=120)
        tree.column("Цена", width=100)
        tree.column("Наличие", width=100)
        
        tree.pack(fill="both", expand=True)
        
        self.refresh_books(tree)
    
    def add_to_cart(self, tree):
        """Добавление в корзину"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу")
            return
        
        item = tree.item(selected[0])
        book_id = int(item['values'][0])
        
        data = self.load_data()
        book = next((b for b in data['books'] if b['id'] == book_id), None)
        
        if not book or book['stock'] == 0:
            messagebox.showerror("Ошибка", "Книга недоступна")
            return
        
        # Запрос количества
        quantity = simpledialog.askinteger("Количество", f"Введите количество (доступно: {book['stock']}):", 
                                          minvalue=1, maxvalue=book['stock'])
        
        if quantity:
            cart_item = {
                "book_id": book['id'],
                "title": book['title'],
                "price": book['price'],
                "quantity": quantity
            }
            self.cart.append(cart_item)
            messagebox.showinfo("Успех", f"Добавлено в корзину: {book['title']} (x{quantity})")
            self.show_main_window()
    
    def create_cart(self, parent):
        """Корзина"""
        # Кнопки
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(btn_frame, text="Удалить из корзины", command=lambda: self.remove_from_cart(tree), bg="#f44336", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Оформить заказ", command=self.create_order, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Очистить корзину", command=lambda: self.clear_cart(tree), bg="#FF9800", fg="white").pack(side="left", padx=5)
        
        # Таблица
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("Название", "Цена", "Количество", "Сумма"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("Название", text="Название")
        tree.heading("Цена", text="Цена")
        tree.heading("Количество", text="Количество")
        tree.heading("Сумма", text="Сумма")
        
        tree.column("Название", width=350)
        tree.column("Цена", width=100)
        tree.column("Количество", width=100)
        tree.column("Сумма", width=100)
        
        tree.pack(fill="both", expand=True)
        
        # Обновление корзины
        for item in self.cart:
            tree.insert("", "end", values=(
                item['title'], f"{item['price']:.2f} ₽",
                item['quantity'], f"{item['price'] * item['quantity']:.2f} ₽"
            ))
        
        # Итого
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        total_frame = tk.Frame(parent)
        total_frame.pack(fill="x", padx=5, pady=10)
        tk.Label(total_frame, text=f"ИТОГО: {total:.2f} ₽", font=("Arial", 14, "bold")).pack(side="right", padx=20)
    
    def remove_from_cart(self, tree):
        """Удаление из корзины"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите товар")
            return
        
        index = tree.index(selected[0])
        self.cart.pop(index)
        messagebox.showinfo("Успех", "Товар удален из корзины")
        self.show_main_window()
    
    def clear_cart(self, tree):
        """Очистка корзины"""
        if not self.cart:
            return
        
        if messagebox.askyesno("Подтверждение", "Очистить корзину?"):
            self.cart = []
            messagebox.showinfo("Успех", "Корзина очищена")
            self.show_main_window()
    
    def create_order(self):
        """Создание заказа"""
        if not self.cart:
            messagebox.showwarning("Предупреждение", "Корзина пуста")
            return
        
        data = self.load_data()
        
        # Проверка наличия
        for item in self.cart:
            book = next((b for b in data['books'] if b['id'] == item['book_id']), None)
            if not book or book['stock'] < item['quantity']:
                messagebox.showerror("Ошибка", f"Недостаточно книг: {item['title']}")
                return
        
        # Создание заказа
        new_id = max([o['id'] for o in data['orders']]) + 1 if data['orders'] else 1
        
        order = {
            "id": new_id,
            "client_id": self.current_user['id'],
            "client_name": self.current_user['full_name'],
            "books": self.cart.copy(),
            "total": sum(item['price'] * item['quantity'] for item in self.cart),
            "status": "новый",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Обновление остатков
        for item in self.cart:
            book = next((b for b in data['books'] if b['id'] == item['book_id']), None)
            if book:
                book['stock'] -= item['quantity']
        
        data['orders'].append(order)
        self.save_data(data)
        
        self.cart = []
        messagebox.showinfo("Успех", f"Заказ #{new_id} успешно создан!")
        self.show_main_window()
    
    def create_client_orders(self, parent):
        """Заказы клиента"""
        # Кнопки
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_client_orders(tree), bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Просмотреть детали", command=lambda: self.view_order_details(tree), bg="#2196F3", fg="white").pack(side="left", padx=5)
        
        # Таблица
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Дата", "Сумма", "Статус"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("ID", text="ID")
        tree.heading("Дата", text="Дата")
        tree.heading("Сумма", text="Сумма")
        tree.heading("Статус", text="Статус")
        
        tree.column("ID", width=50)
        tree.column("Дата", width=200)
        tree.column("Сумма", width=150)
        tree.column("Статус", width=150)
        
        tree.pack(fill="both", expand=True)
        
        self.refresh_client_orders(tree)
    
    def refresh_client_orders(self, tree):
        """Обновление заказов клиента"""
        for item in tree.get_children():
            tree.delete(item)
        
        data = self.load_data()
        client_orders = [o for o in data['orders'] if o['client_id'] == self.current_user['id']]
        
        for order in client_orders:
            tree.insert("", "end", values=(
                order['id'], order['date'], f"{order['total']:.2f} ₽", order['status']
            ))
    
    def view_order_details(self, tree):
        """Просмотр деталей заказа"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ")
            return
        
        item = tree.item(selected[0])
        order_id = int(item['values'][0])
        
        data = self.load_data()
        order = next((o for o in data['orders'] if o['id'] == order_id), None)
        
        if not order:
            return
        
        # Окно с деталями
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Заказ #{order_id}")
        dialog.geometry("600x400")
        
        tk.Label(dialog, text=f"ЗАКАЗ #{order_id}", font=("Arial", 16, "bold")).pack(pady=10)
        
        info_frame = tk.Frame(dialog)
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text=f"Дата: {order['date']}", font=("Arial", 10)).pack(anchor="w", padx=20)
        tk.Label(info_frame, text=f"Статус: {order['status']}", font=("Arial", 10)).pack(anchor="w", padx=20)
        
        tk.Label(dialog, text="Состав заказа:", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Таблица товаров
        tree_frame = tk.Frame(dialog)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        details_tree = ttk.Treeview(tree_frame, columns=("Название", "Цена", "Количество", "Сумма"), show="headings")
        
        details_tree.heading("Название", text="Название")
        details_tree.heading("Цена", text="Цена")
        details_tree.heading("Количество", text="Количество")
        details_tree.heading("Сумма", text="Сумма")
        
        details_tree.pack(fill="both", expand=True)
        
        for book in order['books']:
            details_tree.insert("", "end", values=(
                book['title'], f"{book['price']:.2f} ₽",
                book['quantity'], f"{book['price'] * book['quantity']:.2f} ₽"
            ))
        
        tk.Label(dialog, text=f"ИТОГО: {order['total']:.2f} ₽", font=("Arial", 14, "bold")).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()