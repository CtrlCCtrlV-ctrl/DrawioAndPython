import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from auth import AuthManager

class RailwayStationApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Информационная система - Железнодорожная станция")
        self.root.geometry("900x600")
        
        self.auth_manager = AuthManager()
        self.data_file = 'data.json'
        
        self.show_login_window()
        
    
    def load_data(self):
        """Загрузка данных из JSON"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        """Окно входа в систему"""
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Вход в систему", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, width=25, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            if self.auth_manager.authenticate(username, password):
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login, width=20).grid(row=3, column=0, columnspan=2, pady=10)
        
        info_text = "Тестовые учетные записи:\nadmin/admin123\ncashier/cashier123\npassenger/pass123"
        tk.Label(frame, text=info_text, font=('Arial', 8), fg='gray').grid(row=4, column=0, columnspan=2, pady=10)
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        role = self.auth_manager.current_user['role']
        username = self.auth_manager.current_user['username']
        
        tk.Label(self.root, text=f"Железнодорожная станция", font=('Arial', 18, 'bold')).pack(pady=10)
        tk.Label(self.root, text=f"Пользователь: {username} | Роль: {role}", font=('Arial', 10)).pack()
        
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)
        
        if role == 'administrator':
            self.show_admin_menu(menu_frame)
        elif role == 'cashier':
            self.show_cashier_menu(menu_frame)
        elif role == 'passenger':
            self.show_passenger_menu(menu_frame)
        
        tk.Button(self.root, text="Выход", command=self.logout, width=20).pack(pady=10)
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Button(parent, text="Управление пользователями", command=self.manage_users, width=30).pack(pady=5)
        tk.Button(parent, text="Управление поездами", command=self.manage_trains, width=30).pack(pady=5)
        tk.Button(parent, text="Управление маршрутами", command=self.manage_routes, width=30).pack(pady=5)
        tk.Button(parent, text="Просмотр статистики", command=self.view_statistics, width=30).pack(pady=5)
        tk.Button(parent, text="Просмотр расписания", command=self.view_schedule, width=30).pack(pady=5)
    
    def show_cashier_menu(self, parent):
        """Меню кассира"""
        tk.Label(parent, text="Панель кассира", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Button(parent, text="Продажа билетов", command=self.sell_ticket, width=30).pack(pady=5)
        tk.Button(parent, text="Возврат билетов", command=self.refund_ticket, width=30).pack(pady=5)
        tk.Button(parent, text="Поиск свободных мест", command=self.search_seats, width=30).pack(pady=5)
        tk.Button(parent, text="Просмотр расписания", command=self.view_schedule, width=30).pack(pady=5)
        tk.Button(parent, text="Список проданных билетов", command=self.view_all_tickets, width=30).pack(pady=5)
    
    def show_passenger_menu(self, parent):
        """Меню пассажира"""
        tk.Label(parent, text="Панель пассажира", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Button(parent, text="Просмотр расписания", command=self.view_schedule, width=30).pack(pady=5)
        tk.Button(parent, text="Поиск рейсов", command=self.search_routes, width=30).pack(pady=5)
        tk.Button(parent, text="Бронирование билетов", command=self.book_ticket, width=30).pack(pady=5)
        tk.Button(parent, text="Мои билеты", command=self.view_my_tickets, width=30).pack(pady=5)
    
    # АДМИНИСТРАТОР
    def manage_users(self):
        """Управление пользователями"""
        window = tk.Toplevel(self.root)
        window.title("Управление пользователями")
        window.geometry("700x500")
        
        tk.Label(window, text="Управление пользователями", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('Логин', 'Роль', 'Дата создания')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_users():
            for item in tree.get_children():
                tree.delete(item)
            users = self.auth_manager.get_all_users()
            for user in users:
                tree.insert('', 'end', values=(user['username'], user['role'], user['created']))
        
        def add_user():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить пользователя")
            add_window.geometry("350x200")
            
            tk.Label(add_window, text="Логин:").grid(row=0, column=0, padx=10, pady=10)
            username_entry = tk.Entry(add_window)
            username_entry.grid(row=0, column=1, padx=10, pady=10)
            
            tk.Label(add_window, text="Пароль:").grid(row=1, column=0, padx=10, pady=10)
            password_entry = tk.Entry(add_window, show='*')
            password_entry.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(add_window, text="Роль:").grid(row=2, column=0, padx=10, pady=10)
            role_var = tk.StringVar(value='passenger')
            role_combo = ttk.Combobox(add_window, textvariable=role_var, 
                                     values=['administrator', 'cashier', 'passenger'], state='readonly')
            role_combo.grid(row=2, column=1, padx=10, pady=10)
            
            def save_user():
                if self.auth_manager.create_user(username_entry.get(), password_entry.get(), role_var.get()):
                    messagebox.showinfo("Успех", "Пользователь добавлен")
                    refresh_users()
                    add_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Пользователь уже существует")
            
            tk.Button(add_window, text="Сохранить", command=save_user).grid(row=3, column=0, columnspan=2, pady=10)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            username = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                self.auth_manager.delete_user(username)
                refresh_users()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_user, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_users, width=15).pack(side='left', padx=5)
        
        refresh_users()
    
    def manage_trains(self):
        """Управление поездами"""
        window = tk.Toplevel(self.root)
        window.title("Управление поездами")
        window.geometry("600x500")
        
        tk.Label(window, text="Управление поездами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('ID', 'Номер', 'Тип', 'Мест')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Номер', width=100)
        tree.column('Тип', width=150)
        tree.column('Мест', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_trains():
            for item in tree.get_children():
                tree.delete(item)
            data = self.load_data()
            for train in data['trains']:
                tree.insert('', 'end', values=(train['id'], train['number'], train['type'], train['seats']))
        
        def add_train():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить поезд")
            add_window.geometry("350x250")
            
            tk.Label(add_window, text="Номер поезда:").grid(row=0, column=0, padx=10, pady=10)
            number_entry = tk.Entry(add_window)
            number_entry.grid(row=0, column=1, padx=10, pady=10)
            
            tk.Label(add_window, text="Тип:").grid(row=1, column=0, padx=10, pady=10)
            type_var = tk.StringVar(value='Пассажирский')
            type_combo = ttk.Combobox(add_window, textvariable=type_var, 
                                     values=['Скорый', 'Пассажирский', 'Экспресс'], state='readonly')
            type_combo.grid(row=1, column=1, padx=10, pady=10)
            
            tk.Label(add_window, text="Количество мест:").grid(row=2, column=0, padx=10, pady=10)
            seats_entry = tk.Entry(add_window)
            seats_entry.grid(row=2, column=1, padx=10, pady=10)
            
            def save_train():
                try:
                    data = self.load_data()
                    new_id = max([t['id'] for t in data['trains']]) + 1 if data['trains'] else 1
                    
                    new_train = {
                        'id': new_id,
                        'number': number_entry.get(),
                        'type': type_var.get(),
                        'seats': int(seats_entry.get())
                    }
                    
                    data['trains'].append(new_train)
                    self.save_data(data)
                    
                    messagebox.showinfo("Успех", "Поезд добавлен")
                    refresh_trains()
                    add_window.destroy()
                except ValueError:
                    messagebox.showerror("Ошибка", "Проверьте корректность данных")
            
            tk.Button(add_window, text="Сохранить", command=save_train).grid(row=3, column=0, columnspan=2, pady=10)
        
        def delete_train():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите поезд")
                return
            
            train_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить выбранный поезд?"):
                data = self.load_data()
                data['trains'] = [t for t in data['trains'] if t['id'] != train_id]
                self.save_data(data)
                refresh_trains()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_train, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_train, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_trains, width=15).pack(side='left', padx=5)
        
        refresh_trains()
    
    def manage_routes(self):
        """Управление маршрутами"""
        window = tk.Toplevel(self.root)
        window.title("Управление маршрутами")
        window.geometry("900x500")
        
        tk.Label(window, text="Управление маршрутами", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('ID', 'Поезд', 'Откуда', 'Куда', 'Отпр.', 'Приб.', 'Дата', 'Цена')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_routes():
            for item in tree.get_children():
                tree.delete(item)
            data = self.load_data()
            for route in data['routes']:
                train = next((t for t in data['trains'] if t['id'] == route['train_id']), None)
                train_num = train['number'] if train else 'N/A'
                tree.insert('', 'end', values=(
                    route['id'], train_num, route['from_station'], route['to_station'],
                    route['departure'], route['arrival'], route['date'], route['price']
                ))
        
        def add_route():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить маршрут")
            add_window.geometry("400x400")
            
            data = self.load_data()
            train_options = [f"{t['id']}: {t['number']}" for t in data['trains']]
            
            tk.Label(add_window, text="Поезд:").grid(row=0, column=0, padx=10, pady=5)
            train_var = tk.StringVar()
            train_combo = ttk.Combobox(add_window, textvariable=train_var, values=train_options, state='readonly')
            train_combo.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Откуда:").grid(row=1, column=0, padx=10, pady=5)
            from_entry = tk.Entry(add_window)
            from_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Куда:").grid(row=2, column=0, padx=10, pady=5)
            to_entry = tk.Entry(add_window)
            to_entry.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Отправление:").grid(row=3, column=0, padx=10, pady=5)
            dep_entry = tk.Entry(add_window)
            dep_entry.insert(0, "10:00")
            dep_entry.grid(row=3, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Прибытие:").grid(row=4, column=0, padx=10, pady=5)
            arr_entry = tk.Entry(add_window)
            arr_entry.insert(0, "18:00")
            arr_entry.grid(row=4, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Дата:").grid(row=5, column=0, padx=10, pady=5)
            date_entry = tk.Entry(add_window)
            date_entry.insert(0, "2024-02-20")
            date_entry.grid(row=5, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Цена:").grid(row=6, column=0, padx=10, pady=5)
            price_entry = tk.Entry(add_window)
            price_entry.grid(row=6, column=1, padx=10, pady=5)
            
            def save_route():
                try:
                    data = self.load_data()
                    new_id = max([r['id'] for r in data['routes']]) + 1 if data['routes'] else 1
                    
                    train_id = int(train_var.get().split(':')[0])
                    
                    new_route = {
                        'id': new_id,
                        'train_id': train_id,
                        'from_station': from_entry.get(),
                        'to_station': to_entry.get(),
                        'departure': dep_entry.get(),
                        'arrival': arr_entry.get(),
                        'date': date_entry.get(),
                        'price': int(price_entry.get())
                    }
                    
                    data['routes'].append(new_route)
                    self.save_data(data)
                    
                    messagebox.showinfo("Успех", "Маршрут добавлен")
                    refresh_routes()
                    add_window.destroy()
                except:
                    messagebox.showerror("Ошибка", "Проверьте корректность данных")
            
            tk.Button(add_window, text="Сохранить", command=save_route).grid(row=7, column=0, columnspan=2, pady=15)
        
        def delete_route():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите маршрут")
                return
            
            route_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить выбранный маршрут?"):
                data = self.load_data()
                data['routes'] = [r for r in data['routes'] if r['id'] != route_id]
                self.save_data(data)
                refresh_routes()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_route, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_route, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=refresh_routes, width=15).pack(side='left', padx=5)
        
        refresh_routes()
    
    def view_statistics(self):
        """Просмотр статистики"""
        window = tk.Toplevel(self.root)
        window.title("Статистика")
        window.geometry("500x400")
        
        tk.Label(window, text="Статистика системы", font=('Arial', 14, 'bold')).pack(pady=20)
        
        data = self.load_data()
        users = self.auth_manager.get_all_users()
        
        stats_frame = tk.Frame(window)
        stats_frame.pack(pady=20)
        
        stats = [
            ("Всего пользователей:", len(users)),
            ("Всего поездов:", len(data['trains'])),
            ("Всего маршрутов:", len(data['routes'])),
            ("Всего билетов:", len(data['tickets'])),
            ("Продано билетов:", len([t for t in data['tickets'] if t.get('status') == 'sold'])),
            ("Забронировано:", len([t for t in data['tickets'] if t.get('status') == 'booked'])),
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 12)).grid(row=i, column=0, sticky='w', padx=20, pady=5)
            tk.Label(stats_frame, text=str(value), font=('Arial', 12, 'bold')).grid(row=i, column=1, sticky='e', padx=20, pady=5)
        
        total_revenue = sum(route['price'] for route in data['routes'] 
                          for ticket in data['tickets'] 
                          if ticket['route_id'] == route['id'] and ticket.get('status') == 'sold')
        
        tk.Label(stats_frame, text="Общая выручка:", font=('Arial', 12)).grid(row=len(stats), column=0, sticky='w', padx=20, pady=5)
        tk.Label(stats_frame, text=f"{total_revenue} руб.", font=('Arial', 12, 'bold')).grid(row=len(stats), column=1, sticky='e', padx=20, pady=5)
    
    def view_schedule(self):
        """Просмотр расписания"""
        window = tk.Toplevel(self.root)
        window.title("Расписание")
        window.geometry("900x500")
        
        tk.Label(window, text="Расписание поездов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('Поезд', 'Откуда', 'Куда', 'Отправление', 'Прибытие', 'Дата', 'Цена')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self.load_data()
        for route in data['routes']:
            train = next((t for t in data['trains'] if t['id'] == route['train_id']), None)
            train_num = train['number'] if train else 'N/A'
            tree.insert('', 'end', values=(
                train_num, route['from_station'], route['to_station'],
                route['departure'], route['arrival'], route['date'], f"{route['price']} руб."
            ))
    
    # КАССИР
    def sell_ticket(self):
        """Продажа билетов"""
        window = tk.Toplevel(self.root)
        window.title("Продажа билетов")
        window.geometry("500x400")
        
        tk.Label(window, text="Продажа билетов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        form_frame = tk.Frame(window)
        form_frame.pack(pady=20)
        
        data = self.load_data()
        route_options = [f"{r['id']}: {r['from_station']} → {r['to_station']} ({r['date']})" 
                        for r in data['routes']]
        
        tk.Label(form_frame, text="Маршрут:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        route_var = tk.StringVar()
        route_combo = ttk.Combobox(form_frame, textvariable=route_var, values=route_options, width=30, state='readonly')
        route_combo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form_frame, text="ФИО пассажира:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        passenger_entry = tk.Entry(form_frame, width=32)
        passenger_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(form_frame, text="Номер места:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        seat_entry = tk.Entry(form_frame, width=32)
        seat_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def confirm_sell():
            try:
                route_id = int(route_var.get().split(':')[0])
                passenger = passenger_entry.get()
                seat = int(seat_entry.get())
                
                if not passenger:
                    messagebox.showerror("Ошибка", "Введите ФИО пассажира")
                    return
                
                data = self.load_data()
                
                # Проверка занятости места
                for ticket in data['tickets']:
                    if ticket['route_id'] == route_id and ticket['seat'] == seat:
                        messagebox.showerror("Ошибка", "Это место уже занято")
                        return
                
                new_id = max([t['id'] for t in data['tickets']]) + 1 if data['tickets'] else 1
                
                new_ticket = {
                    'id': new_id,
                    'route_id': route_id,
                    'passenger': passenger,
                    'seat': seat,
                    'status': 'sold',
                    'sold_by': self.auth_manager.current_user['username'],
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                data['tickets'].append(new_ticket)
                self.save_data(data)
                
                messagebox.showinfo("Успех", f"Билет продан\nМесто: {seat}\nПассажир: {passenger}")
                window.destroy()
            except:
                messagebox.showerror("Ошибка", "Проверьте корректность данных")
        
        tk.Button(form_frame, text="Продать билет", command=confirm_sell, width=25).grid(row=3, column=0, columnspan=2, pady=20)
    
    def refund_ticket(self):
        """Возврат билетов"""
        window = tk.Toplevel(self.root)
        window.title("Возврат билетов")
        window.geometry("800x500")
        
        tk.Label(window, text="Возврат билетов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('ID', 'Маршрут', 'Пассажир', 'Место', 'Статус')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Маршрут', width=250)
        tree.column('Пассажир', width=200)
        tree.column('Место', width=80)
        tree.column('Статус', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def refresh_tickets():
            for item in tree.get_children():
                tree.delete(item)
            data = self.load_data()
            for ticket in data['tickets']:
                if ticket['status'] == 'sold':
                    route = next((r for r in data['routes'] if r['id'] == ticket['route_id']), None)
                    route_info = f"{route['from_station']} → {route['to_station']}" if route else 'N/A'
                    tree.insert('', 'end', values=(
                        ticket['id'], route_info, ticket['passenger'], ticket['seat'], ticket['status']
                    ))
        
        def refund():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите билет")
                return
            
            ticket_id = tree.item(selected[0])['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Вернуть выбранный билет?"):
                data = self.load_data()
                data['tickets'] = [t for t in data['tickets'] if t['id'] != ticket_id]
                self.save_data(data)
                messagebox.showinfo("Успех", "Билет возвращен")
                refresh_tickets()
        
        tk.Button(window, text="Вернуть билет", command=refund, width=20).pack(pady=10)
        
        refresh_tickets()
    
    def search_seats(self):
        """Поиск свободных мест"""
        window = tk.Toplevel(self.root)
        window.title("Поиск свободных мест")
        window.geometry("700x500")
        
        tk.Label(window, text="Свободные места по маршрутам", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('Маршрут', 'Дата', 'Всего мест', 'Занято', 'Свободно')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self.load_data()
        for route in data['routes']:
            train = next((t for t in data['trains'] if t['id'] == route['train_id']), None)
            total_seats = train['seats'] if train else 0
            
            occupied = len([t for t in data['tickets'] if t['route_id'] == route['id']])
            free = total_seats - occupied
            
            route_info = f"{route['from_station']} → {route['to_station']}"
            tree.insert('', 'end', values=(route_info, route['date'], total_seats, occupied, free))
    
    def view_all_tickets(self):
        """Список всех проданных билетов"""
        window = tk.Toplevel(self.root)
        window.title("Проданные билеты")
        window.geometry("900x500")
        
        tk.Label(window, text="Список проданных билетов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('ID', 'Маршрут', 'Пассажир', 'Место', 'Статус', 'Дата продажи')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Маршрут', width=250)
        tree.column('Пассажир', width=180)
        tree.column('Место', width=70)
        tree.column('Статус', width=100)
        tree.column('Дата продажи', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self.load_data()
        for ticket in data['tickets']:
            route = next((r for r in data['routes'] if r['id'] == ticket['route_id']), None)
            route_info = f"{route['from_station']} → {route['to_station']}" if route else 'N/A'
            tree.insert('', 'end', values=(
                ticket['id'], route_info, ticket['passenger'], ticket['seat'], 
                ticket['status'], ticket.get('date', 'N/A')
            ))
    
    # ПАССАЖИР
    def search_routes(self):
        """Поиск рейсов"""
        window = tk.Toplevel(self.root)
        window.title("Поиск рейсов")
        window.geometry("800x550")
        
        tk.Label(window, text="Поиск рейсов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        search_frame = tk.Frame(window)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Откуда:").grid(row=0, column=0, padx=5, pady=5)
        from_entry = tk.Entry(search_frame, width=20)
        from_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(search_frame, text="Куда:").grid(row=0, column=2, padx=5, pady=5)
        to_entry = tk.Entry(search_frame, width=20)
        to_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('Поезд', 'Откуда', 'Куда', 'Отпр.', 'Приб.', 'Дата', 'Цена', 'Своб.мест')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=95)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def search():
            for item in tree.get_children():
                tree.delete(item)
            
            data = self.load_data()
            from_text = from_entry.get().lower()
            to_text = to_entry.get().lower()
            
            for route in data['routes']:
                if (not from_text or from_text in route['from_station'].lower()) and \
                   (not to_text or to_text in route['to_station'].lower()):
                    
                    train = next((t for t in data['trains'] if t['id'] == route['train_id']), None)
                    train_num = train['number'] if train else 'N/A'
                    total_seats = train['seats'] if train else 0
                    occupied = len([t for t in data['tickets'] if t['route_id'] == route['id']])
                    free = total_seats - occupied
                    
                    tree.insert('', 'end', values=(
                        train_num, route['from_station'], route['to_station'],
                        route['departure'], route['arrival'], route['date'], 
                        f"{route['price']} р.", free
                    ))
        
        tk.Button(search_frame, text="Найти", command=search, width=15).grid(row=0, column=4, padx=10, pady=5)
        
        search()
    
    def book_ticket(self):
        """Бронирование билетов"""
        window = tk.Toplevel(self.root)
        window.title("Бронирование билетов")
        window.geometry("500x350")
        
        tk.Label(window, text="Бронирование билетов", font=('Arial', 14, 'bold')).pack(pady=10)
        
        form_frame = tk.Frame(window)
        form_frame.pack(pady=20)
        
        data = self.load_data()
        route_options = [f"{r['id']}: {r['from_station']} → {r['to_station']} ({r['date']})" 
                        for r in data['routes']]
        
        tk.Label(form_frame, text="Маршрут:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        route_var = tk.StringVar()
        route_combo = ttk.Combobox(form_frame, textvariable=route_var, values=route_options, width=30, state='readonly')
        route_combo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form_frame, text="Номер места:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        seat_entry = tk.Entry(form_frame, width=32)
        seat_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def confirm_booking():
            try:
                route_id = int(route_var.get().split(':')[0])
                seat = int(seat_entry.get())
                
                data = self.load_data()
                
                # Проверка занятости места
                for ticket in data['tickets']:
                    if ticket['route_id'] == route_id and ticket['seat'] == seat:
                        messagebox.showerror("Ошибка", "Это место уже занято")
                        return
                
                new_id = max([t['id'] for t in data['tickets']]) + 1 if data['tickets'] else 1
                
                new_ticket = {
                    'id': new_id,
                    'route_id': route_id,
                    'passenger': self.auth_manager.current_user['username'],
                    'seat': seat,
                    'status': 'booked',
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                data['tickets'].append(new_ticket)
                self.save_data(data)
                
                messagebox.showinfo("Успех", f"Билет забронирован\nМесто: {seat}")
                window.destroy()
            except:
                messagebox.showerror("Ошибка", "Проверьте корректность данных")
        
        tk.Button(form_frame, text="Забронировать", command=confirm_booking, width=25).grid(row=2, column=0, columnspan=2, pady=20)
    
    def view_my_tickets(self):
        """Мои билеты"""
        window = tk.Toplevel(self.root)
        window.title("Мои билеты")
        window.geometry("800x500")
        
        tk.Label(window, text="Мои билеты", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(pady=10, fill='both', expand=True)
        
        columns = ('ID', 'Маршрут', 'Место', 'Статус', 'Дата')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column('ID', width=50)
        tree.column('Маршрут', width=300)
        tree.column('Место', width=80)
        tree.column('Статус', width=100)
        tree.column('Дата', width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        data = self.load_data()
        username = self.auth_manager.current_user['username']
        
        for ticket in data['tickets']:
            if ticket['passenger'] == username:
                route = next((r for r in data['routes'] if r['id'] == ticket['route_id']), None)
                route_info = f"{route['from_station']} → {route['to_station']} ({route['date']})" if route else 'N/A'
                tree.insert('', 'end', values=(
                    ticket['id'], route_info, ticket['seat'], ticket['status'], ticket.get('date', 'N/A')
                ))
    
    def logout(self):
        """Выход из системы"""
        self.auth_manager.logout()
        self.show_login_window()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == '__main__':
    app = RailwayStationApp()
    app.run()