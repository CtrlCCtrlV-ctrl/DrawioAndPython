import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from auth import AuthManager

class CinemaSystem:
    def __init__(self):
        self.auth = AuthManager()
        self.data_file = 'data.json'
        self.initialize_data()
        self.root = tk.Tk()
        self.root.title("Система управления кинотеатром")
        self.root.geometry("900x600")
        self.show_login()
    
    def initialize_data(self):
        """Проверка существования базы данных"""
        pass
    
    def load_data(self):
        """Загрузка данных"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Вход в систему", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, show='*', width=25)
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            if self.auth.login(username, password):
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=do_login, width=20).grid(row=3, column=0, columnspan=2, pady=10)
        
        info = tk.Label(frame, text="admin/admin123 | cashier/cashier123 | client/client123", 
                       font=('Arial', 8), fg='gray')
        info.grid(row=4, column=0, columnspan=2, pady=10)
    
    def show_main_menu(self):
        """Главное меню"""
        self.clear_window()
        
        user = self.auth.get_current_user()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"Пользователь: {user['username']} ({user['role']})", 
                bg='#2c3e50', fg='white', font=('Arial', 10)).pack(side='left', padx=10, pady=10)
        
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side='right', padx=10, pady=10)
        
        # Контейнер меню
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=50)
        
        tk.Label(menu_frame, text="Главное меню", font=('Arial', 18, 'bold')).pack(pady=20)
        
        if user['role'] == 'administrator':
            self.show_admin_menu(menu_frame)
        elif user['role'] == 'cashier':
            self.show_cashier_menu(menu_frame)
        elif user['role'] == 'client':
            self.show_client_menu(menu_frame)
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Button(parent, text="Управление фильмами", width=30, 
                 command=self.manage_movies).pack(pady=5)
        tk.Button(parent, text="Управление сеансами", width=30, 
                 command=self.manage_sessions).pack(pady=5)
        tk.Button(parent, text="Управление залами", width=30, 
                 command=self.manage_halls).pack(pady=5)
        tk.Button(parent, text="Просмотр статистики", width=30, 
                 command=self.view_statistics).pack(pady=5)
        tk.Button(parent, text="Управление пользователями", width=30, 
                 command=self.manage_users).pack(pady=5)
    
    def show_cashier_menu(self, parent):
        """Меню кассира"""
        tk.Button(parent, text="Продажа билетов", width=30, 
                 command=self.sell_tickets).pack(pady=5)
        tk.Button(parent, text="Просмотр расписания", width=30, 
                 command=self.view_schedule).pack(pady=5)
        tk.Button(parent, text="Отмена бронирования", width=30, 
                 command=self.cancel_booking).pack(pady=5)
        tk.Button(parent, text="Поиск сеансов", width=30, 
                 command=self.search_sessions).pack(pady=5)
    
    def show_client_menu(self, parent):
        """Меню клиента"""
        tk.Button(parent, text="Просмотр афиши", width=30, 
                 command=self.view_movies).pack(pady=5)
        tk.Button(parent, text="Бронирование билетов", width=30, 
                 command=self.book_tickets).pack(pady=5)
        tk.Button(parent, text="Просмотр истории", width=30, 
                 command=self.view_history).pack(pady=5)
        tk.Button(parent, text="Поиск фильмов", width=30, 
                 command=self.search_movies).pack(pady=5)
    
    # === ФУНКЦИИ АДМИНИСТРАТОРА ===
    
    def manage_movies(self):
        """Управление фильмами"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Управление фильмами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Таблица фильмов
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Жанр', 'Длительность', 'Рейтинг')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        data = self.load_data()
        for movie in data['movies']:
            tree.insert('', 'end', values=(movie['id'], movie['title'], movie['genre'], 
                                          f"{movie['duration']} мин", movie['rating']))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def add_movie():
            win = tk.Toplevel(self.root)
            win.title("Добавить фильм")
            win.geometry("300x250")
            
            tk.Label(win, text="Название:").pack(pady=5)
            title_entry = tk.Entry(win, width=30)
            title_entry.pack()
            
            tk.Label(win, text="Жанр:").pack(pady=5)
            genre_entry = tk.Entry(win, width=30)
            genre_entry.pack()
            
            tk.Label(win, text="Длительность (мин):").pack(pady=5)
            duration_entry = tk.Entry(win, width=30)
            duration_entry.pack()
            
            tk.Label(win, text="Рейтинг:").pack(pady=5)
            rating_entry = tk.Entry(win, width=30)
            rating_entry.pack()
            
            def save():
                if not all([title_entry.get(), genre_entry.get(), duration_entry.get(), rating_entry.get()]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                try:
                    duration = int(duration_entry.get())
                except:
                    messagebox.showerror("Ошибка", "Длительность должна быть числом")
                    return
                
                data = self.load_data()
                new_id = max([m['id'] for m in data['movies']], default=0) + 1
                
                data['movies'].append({
                    'id': new_id,
                    'title': title_entry.get(),
                    'genre': genre_entry.get(),
                    'duration': duration,
                    'rating': rating_entry.get()
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Фильм добавлен")
                win.destroy()
                self.manage_movies()
            
            tk.Button(win, text="Сохранить", command=save).pack(pady=10)
        
        def delete_movie():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите фильм")
                return
            
            item = tree.item(selected[0])
            movie_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить фильм?"):
                data = self.load_data()
                data['movies'] = [m for m in data['movies'] if m['id'] != movie_id]
                self.save_data(data)
                messagebox.showinfo("Успех", "Фильм удален")
                self.manage_movies()
        
        tk.Button(btn_frame, text="Добавить", command=add_movie).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_movie).pack(side='left', padx=5)
    
    def manage_sessions(self):
        """Управление сеансами"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Управление сеансами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Фильм', 'Зал', 'Дата/Время', 'Цена')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        data = self.load_data()
        for session in data['sessions']:
            movie = next((m for m in data['movies'] if m['id'] == session['movie_id']), None)
            hall = next((h for h in data['halls'] if h['id'] == session['hall_id']), None)
            
            tree.insert('', 'end', values=(
                session['id'],
                movie['title'] if movie else 'N/A',
                hall['name'] if hall else 'N/A',
                session['datetime'],
                f"{session['price']} ₽"
            ))
        
        tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def add_session():
            win = tk.Toplevel(self.root)
            win.title("Добавить сеанс")
            win.geometry("300x300")
            
            tk.Label(win, text="Фильм:").pack(pady=5)
            movie_var = tk.StringVar()
            movie_combo = ttk.Combobox(win, textvariable=movie_var, width=28)
            movie_combo['values'] = [f"{m['id']}: {m['title']}" for m in data['movies']]
            movie_combo.pack()
            
            tk.Label(win, text="Зал:").pack(pady=5)
            hall_var = tk.StringVar()
            hall_combo = ttk.Combobox(win, textvariable=hall_var, width=28)
            hall_combo['values'] = [f"{h['id']}: {h['name']}" for h in data['halls']]
            hall_combo.pack()
            
            tk.Label(win, text="Дата/Время (YYYY-MM-DD HH:MM):").pack(pady=5)
            datetime_entry = tk.Entry(win, width=30)
            datetime_entry.pack()
            
            tk.Label(win, text="Цена:").pack(pady=5)
            price_entry = tk.Entry(win, width=30)
            price_entry.pack()
            
            def save():
                if not all([movie_var.get(), hall_var.get(), datetime_entry.get(), price_entry.get()]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                try:
                    movie_id = int(movie_var.get().split(':')[0])
                    hall_id = int(hall_var.get().split(':')[0])
                    price = int(price_entry.get())
                except:
                    messagebox.showerror("Ошибка", "Неверный формат данных")
                    return
                
                data = self.load_data()
                new_id = max([s['id'] for s in data['sessions']], default=0) + 1
                
                data['sessions'].append({
                    'id': new_id,
                    'movie_id': movie_id,
                    'hall_id': hall_id,
                    'datetime': datetime_entry.get(),
                    'price': price
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Сеанс добавлен")
                win.destroy()
                self.manage_sessions()
            
            tk.Button(win, text="Сохранить", command=save).pack(pady=10)
        
        def delete_session():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите сеанс")
                return
            
            item = tree.item(selected[0])
            session_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить сеанс?"):
                data = self.load_data()
                data['sessions'] = [s for s in data['sessions'] if s['id'] != session_id]
                self.save_data(data)
                messagebox.showinfo("Успех", "Сеанс удален")
                self.manage_sessions()
        
        tk.Button(btn_frame, text="Добавить", command=add_session).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_session).pack(side='left', padx=5)
    
    def manage_halls(self):
        """Управление залами"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Управление залами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Название', 'Вместимость')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        data = self.load_data()
        for hall in data['halls']:
            tree.insert('', 'end', values=(hall['id'], hall['name'], hall['capacity']))
        
        tree.pack(fill='both', expand=True)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def add_hall():
            win = tk.Toplevel(self.root)
            win.title("Добавить зал")
            win.geometry("300x200")
            
            tk.Label(win, text="Название:").pack(pady=5)
            name_entry = tk.Entry(win, width=30)
            name_entry.pack()
            
            tk.Label(win, text="Вместимость:").pack(pady=5)
            capacity_entry = tk.Entry(win, width=30)
            capacity_entry.pack()
            
            def save():
                if not all([name_entry.get(), capacity_entry.get()]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                try:
                    capacity = int(capacity_entry.get())
                except:
                    messagebox.showerror("Ошибка", "Вместимость должна быть числом")
                    return
                
                data = self.load_data()
                new_id = max([h['id'] for h in data['halls']], default=0) + 1
                
                data['halls'].append({
                    'id': new_id,
                    'name': name_entry.get(),
                    'capacity': capacity
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", "Зал добавлен")
                win.destroy()
                self.manage_halls()
            
            tk.Button(win, text="Сохранить", command=save).pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_hall).pack(side='left', padx=5)
    
    def view_statistics(self):
        """Просмотр статистики"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Статистика системы", font=('Arial', 14, 'bold')).pack(pady=20)
        
        data = self.load_data()
        
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=20)
        
        tk.Label(stats_frame, text=f"Всего фильмов: {len(data['movies'])}", 
                font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Всего сеансов: {len(data['sessions'])}", 
                font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Всего залов: {len(data['halls'])}", 
                font=('Arial', 12)).pack(pady=5)
        tk.Label(stats_frame, text=f"Всего бронирований: {len(data['bookings'])}", 
                font=('Arial', 12)).pack(pady=5)
        
        total_revenue = sum(b['price'] for b in data['bookings'])
        tk.Label(stats_frame, text=f"Общая выручка: {total_revenue} ₽", 
                font=('Arial', 12, 'bold'), fg='green').pack(pady=10)
    
    def manage_users(self):
        """Управление пользователями"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Управление пользователями", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('Логин', 'Роль', 'Дата создания')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        users = self.auth.get_all_users()
        for user in users:
            tree.insert('', 'end', values=(user['username'], user['role'], user['created']))
        
        tree.pack(fill='both', expand=True)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def add_user():
            win = tk.Toplevel(self.root)
            win.title("Добавить пользователя")
            win.geometry("300x250")
            
            tk.Label(win, text="Логин:").pack(pady=5)
            username_entry = tk.Entry(win, width=30)
            username_entry.pack()
            
            tk.Label(win, text="Пароль:").pack(pady=5)
            password_entry = tk.Entry(win, show='*', width=30)
            password_entry.pack()
            
            tk.Label(win, text="Роль:").pack(pady=5)
            role_var = tk.StringVar(value="client")
            role_combo = ttk.Combobox(win, textvariable=role_var, width=28, 
                                     values=['administrator', 'cashier', 'client'])
            role_combo.pack()
            
            def save():
                if not all([username_entry.get(), password_entry.get()]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                if self.auth.create_user(username_entry.get(), password_entry.get(), role_var.get()):
                    messagebox.showinfo("Успех", "Пользователь создан")
                    win.destroy()
                    self.manage_users()
                else:
                    messagebox.showerror("Ошибка", "Пользователь уже существует")
            
            tk.Button(win, text="Сохранить", command=save).pack(pady=10)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите пользователя")
                return
            
            item = tree.item(selected[0])
            username = item['values'][0]
            
            if username == 'admin':
                messagebox.showerror("Ошибка", "Нельзя удалить администратора")
                return
            
            if messagebox.askyesno("Подтверждение", "Удалить пользователя?"):
                self.auth.delete_user(username)
                messagebox.showinfo("Успех", "Пользователь удален")
                self.manage_users()
        
        tk.Button(btn_frame, text="Добавить", command=add_user).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user).pack(side='left', padx=5)
    
    # === ФУНКЦИИ КАССИРА ===
    
    def sell_tickets(self):
        """Продажа билетов"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Продажа билетов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID сеанса', 'Фильм', 'Зал', 'Дата/Время', 'Цена')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for session in data['sessions']:
            movie = next((m for m in data['movies'] if m['id'] == session['movie_id']), None)
            hall = next((h for h in data['halls'] if h['id'] == session['hall_id']), None)
            
            tree.insert('', 'end', values=(
                session['id'],
                movie['title'] if movie else 'N/A',
                hall['name'] if hall else 'N/A',
                session['datetime'],
                f"{session['price']} ₽"
            ))
        
        tree.pack(fill='both', expand=True)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        def sell():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите сеанс")
                return
            
            item = tree.item(selected[0])
            session_id = item['values'][0]
            
            win = tk.Toplevel(self.root)
            win.title("Продажа билета")
            win.geometry("300x200")
            
            tk.Label(win, text="Имя клиента:").pack(pady=5)
            client_entry = tk.Entry(win, width=30)
            client_entry.pack()
            
            tk.Label(win, text="Количество билетов:").pack(pady=5)
            qty_entry = tk.Entry(win, width=30)
            qty_entry.insert(0, "1")
            qty_entry.pack()
            
            def confirm():
                if not client_entry.get():
                    messagebox.showerror("Ошибка", "Введите имя клиента")
                    return
                
                try:
                    qty = int(qty_entry.get())
                    if qty <= 0:
                        raise ValueError
                except:
                    messagebox.showerror("Ошибка", "Неверное количество")
                    return
                
                data = self.load_data()
                session = next(s for s in data['sessions'] if s['id'] == session_id)
                
                new_id = max([b['id'] for b in data['bookings']], default=0) + 1
                
                data['bookings'].append({
                    'id': new_id,
                    'session_id': session_id,
                    'client_name': client_entry.get(),
                    'quantity': qty,
                    'price': session['price'] * qty,
                    'status': 'sold',
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", f"Продано {qty} билет(ов)")
                win.destroy()
            
            tk.Button(win, text="Продать", command=confirm).pack(pady=10)
        
        tk.Button(btn_frame, text="Продать билет", command=sell).pack()
    
    def view_schedule(self):
        """Просмотр расписания"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Расписание сеансов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Фильм', 'Зал', 'Дата/Время', 'Цена', 'Продано')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        data = self.load_data()
        for session in data['sessions']:
            movie = next((m for m in data['movies'] if m['id'] == session['movie_id']), None)
            hall = next((h for h in data['halls'] if h['id'] == session['hall_id']), None)
            
            sold = sum(b['quantity'] for b in data['bookings'] if b['session_id'] == session['id'])
            
            tree.insert('', 'end', values=(
                session['id'],
                movie['title'] if movie else 'N/A',
                hall['name'] if hall else 'N/A',
                session['datetime'],
                f"{session['price']} ₽",
                sold
            ))
        
        tree.pack(fill='both', expand=True)
    
    def cancel_booking(self):
        """Отмена бронирования"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Отмена бронирования", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Клиент', 'Сеанс', 'Кол-во', 'Сумма', 'Статус')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        data = self.load_data()
        for booking in data['bookings']:
            tree.insert('', 'end', values=(
                booking['id'],
                booking['client_name'],
                booking['session_id'],
                booking['quantity'],
                f"{booking['price']} ₽",
                booking['status']
            ))
        
        tree.pack(fill='both', expand=True)
        
        def cancel():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите бронирование")
                return
            
            item = tree.item(selected[0])
            booking_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Отменить бронирование?"):
                data = self.load_data()
                data['bookings'] = [b for b in data['bookings'] if b['id'] != booking_id]
                self.save_data(data)
                messagebox.showinfo("Успех", "Бронирование отменено")
                self.cancel_booking()
        
        tk.Button(self.root, text="Отменить выбранное", command=cancel).pack(pady=10)
    
    def search_sessions(self):
        """Поиск сеансов"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Поиск сеансов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск по названию фильма:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Фильм', 'Зал', 'Дата/Время', 'Цена')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill='both', expand=True)
        
        def search():
            query = search_entry.get().lower()
            tree.delete(*tree.get_children())
            
            data = self.load_data()
            for session in data['sessions']:
                movie = next((m for m in data['movies'] if m['id'] == session['movie_id']), None)
                
                if movie and query in movie['title'].lower():
                    hall = next((h for h in data['halls'] if h['id'] == session['hall_id']), None)
                    
                    tree.insert('', 'end', values=(
                        session['id'],
                        movie['title'],
                        hall['name'] if hall else 'N/A',
                        session['datetime'],
                        f"{session['price']} ₽"
                    ))
        
        tk.Button(search_frame, text="Найти", command=search).pack(side='left', padx=5)
    
    # === ФУНКЦИИ КЛИЕНТА ===
    
    def view_movies(self):
        """Просмотр афиши"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Афиша фильмов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('Название', 'Жанр', 'Длительность', 'Рейтинг')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        data = self.load_data()
        for movie in data['movies']:
            tree.insert('', 'end', values=(
                movie['title'],
                movie['genre'],
                f"{movie['duration']} мин",
                movie['rating']
            ))
        
        tree.pack(fill='both', expand=True)
    
    def book_tickets(self):
        """Бронирование билетов"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Бронирование билетов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        data = self.load_data()
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID сеанса', 'Фильм', 'Дата/Время', 'Цена')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for session in data['sessions']:
            movie = next((m for m in data['movies'] if m['id'] == session['movie_id']), None)
            
            tree.insert('', 'end', values=(
                session['id'],
                movie['title'] if movie else 'N/A',
                session['datetime'],
                f"{session['price']} ₽"
            ))
        
        tree.pack(fill='both', expand=True)
        
        def book():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите сеанс")
                return
            
            item = tree.item(selected[0])
            session_id = item['values'][0]
            
            win = tk.Toplevel(self.root)
            win.title("Бронирование")
            win.geometry("300x150")
            
            tk.Label(win, text="Количество билетов:").pack(pady=5)
            qty_entry = tk.Entry(win, width=30)
            qty_entry.insert(0, "1")
            qty_entry.pack()
            
            def confirm():
                try:
                    qty = int(qty_entry.get())
                    if qty <= 0:
                        raise ValueError
                except:
                    messagebox.showerror("Ошибка", "Неверное количество")
                    return
                
                data = self.load_data()
                session = next(s for s in data['sessions'] if s['id'] == session_id)
                
                new_id = max([b['id'] for b in data['bookings']], default=0) + 1
                
                data['bookings'].append({
                    'id': new_id,
                    'session_id': session_id,
                    'client_name': self.auth.get_current_user()['username'],
                    'quantity': qty,
                    'price': session['price'] * qty,
                    'status': 'booked',
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                self.save_data(data)
                messagebox.showinfo("Успех", f"Забронировано {qty} билет(ов)")
                win.destroy()
            
            tk.Button(win, text="Забронировать", command=confirm).pack(pady=10)
        
        tk.Button(self.root, text="Забронировать", command=book).pack(pady=10)
    
    def view_history(self):
        """Просмотр истории"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="История бронирований", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('ID', 'Сеанс', 'Кол-во', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        data = self.load_data()
        username = self.auth.get_current_user()['username']
        
        for booking in data['bookings']:
            if booking['client_name'] == username:
                tree.insert('', 'end', values=(
                    booking['id'],
                    booking['session_id'],
                    booking['quantity'],
                    f"{booking['price']} ₽",
                    booking['status'],
                    booking['created']
                ))
        
        tree.pack(fill='both', expand=True)
    
    def search_movies(self):
        """Поиск фильмов"""
        self.clear_window()
        
        tk.Button(self.root, text="← Назад", command=self.show_main_menu).pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Поиск фильмов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        columns = ('Название', 'Жанр', 'Длительность', 'Рейтинг')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill='both', expand=True)
        
        def search():
            query = search_entry.get().lower()
            tree.delete(*tree.get_children())
            
            data = self.load_data()
            for movie in data['movies']:
                if query in movie['title'].lower() or query in movie['genre'].lower():
                    tree.insert('', 'end', values=(
                        movie['title'],
                        movie['genre'],
                        f"{movie['duration']} мин",
                        movie['rating']
                    ))
        
        tk.Button(search_frame, text="Найти", command=search).pack(side='left', padx=5)
    
    def logout(self):
        """Выход из системы"""
        self.auth.logout()
        self.show_login()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == '__main__':
    app = CinemaSystem()
    app.run()