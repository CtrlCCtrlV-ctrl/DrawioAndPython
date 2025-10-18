import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

# Путь к файлу данных
DATA_FILE = "data.json"

class TheaterApp:
    """Главное приложение театральной системы"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Информационная система - Драматический театр")
        self.root.geometry("900x600")
        self.current_user = None

        # Загрузка данных
        self.load_data()

        # Показ окна входа
        self.show_login_window()
        
    def load_data(self):
        """Загрузка данных из файла"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def save_data(self, data=None):
        """Сохранение данных в файл"""
        if data is None:
            data = self.data
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def show_login_window(self):
        """Окно входа в систему"""
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="🎭 Драматический театр", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.login_entry = tk.Entry(frame, font=('Arial', 12), width=20)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = tk.Entry(frame, font=('Arial', 12), width=20, show='*')
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(frame, text="Войти", font=('Arial', 12), width=20, command=self.login).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Подсказка
        hint_text = "Тестовые аккаунты:\nadmin/admin123\ncashier/cashier123\nvisitor/visitor123"
        tk.Label(frame, text=hint_text, font=('Arial', 9), fg='gray', justify='left').grid(row=4, column=0, columnspan=2, pady=10)
        
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Обработка входа"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        user = auth.authenticate(username, password)
        
        if user:
            self.current_user = user
            self.show_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.show_login_window()
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"👤 {self.current_user['full_name']} ({self.current_user['role']})", 
                bg='#2c3e50', fg='white', font=('Arial', 11)).pack(side='left', padx=15, pady=15)
        
        tk.Button(top_frame, text="Выход", command=self.logout, bg='#e74c3c', fg='white', 
                 font=('Arial', 10)).pack(side='right', padx=15, pady=10)
        
        # Основной контент
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if self.current_user['role'] == 'administrator':
            self.show_admin_menu(content_frame)
        elif self.current_user['role'] == 'cashier':
            self.show_cashier_menu(content_frame)
        else:
            self.show_visitor_menu(content_frame)
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        buttons = [
            ("Управление спектаклями", self.manage_plays),
            ("Управление залами", self.manage_halls),
            ("Управление расписанием", self.manage_schedule),
            ("Управление пользователями", self.manage_users),
            ("Просмотр статистики", self.view_statistics)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(buttons_frame, text=text, font=('Arial', 12), width=30, 
                     command=command).grid(row=i, column=0, pady=8)
    
    def show_cashier_menu(self, parent):
        """Меню кассира"""
        tk.Label(parent, text="Панель кассира", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        buttons = [
            ("Просмотр афиши", self.view_schedule_cashier),
            ("Продажа билетов", self.sell_tickets),
            ("Возврат билетов", self.refund_tickets),
            ("Поиск спектаклей", self.search_plays)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(buttons_frame, text=text, font=('Arial', 12), width=30, 
                     command=command).grid(row=i, column=0, pady=8)
    
    def show_visitor_menu(self, parent):
        """Меню посетителя"""
        tk.Label(parent, text="Добро пожаловать в театр!", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        buttons = [
            ("Просмотр репертуара", self.browse_repertoire),
            ("Бронирование билетов", self.book_tickets),
            ("Мои бронирования", self.view_my_bookings),
            ("Отмена бронирования", self.cancel_booking)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(buttons_frame, text=text, font=('Arial', 12), width=30, 
                     command=command).grid(row=i, column=0, pady=8)
    
    # ==================== АДМИНИСТРАТОР ====================
    
    def manage_plays(self):
        """Управление спектаклями"""
        window = tk.Toplevel(self.root)
        window.title("Управление спектаклями")
        window.geometry("800x500")
        
        # Таблица спектаклей
        columns = ('ID', 'Название', 'Автор', 'Жанр', 'Длительность')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for play in self.data['plays']:
            tree.insert('', 'end', values=(play['id'], play['title'], play['author'], 
                                          play['genre'], f"{play['duration']} мин"))
        
        tree.pack(padx=10, pady=10)
        
        # Кнопки
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=lambda: self.add_play(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_play(tree)).pack(side='left', padx=5)
    
    def add_play(self, tree):
        """Добавление спектакля"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить спектакль")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        title_entry = tk.Entry(dialog, width=30)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Автор:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        author_entry = tk.Entry(dialog, width=30)
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Жанр:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        genre_entry = tk.Entry(dialog, width=30)
        genre_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Длительность (мин):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        duration_entry = tk.Entry(dialog, width=30)
        duration_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Описание:").grid(row=4, column=0, sticky='ne', padx=5, pady=5)
        desc_text = tk.Text(dialog, width=30, height=5)
        desc_text.grid(row=4, column=1, padx=5, pady=5)
        
        def save():
            new_id = max([p['id'] for p in self.data['plays']]) + 1 if self.data['plays'] else 1
            new_play = {
                'id': new_id,
                'title': title_entry.get(),
                'author': author_entry.get(),
                'genre': genre_entry.get(),
                'duration': int(duration_entry.get()),
                'description': desc_text.get('1.0', 'end-1c')
            }
            self.data['plays'].append(new_play)
            self.save_data()
            tree.insert('', 'end', values=(new_play['id'], new_play['title'], 
                                          new_play['author'], new_play['genre'], 
                                          f"{new_play['duration']} мин"))
            dialog.destroy()
            messagebox.showinfo("Успех", "Спектакль добавлен")
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=5, column=0, columnspan=2, pady=15)
    
    def delete_play(self, tree):
        """Удаление спектакля"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите спектакль")
            return
        
        item = tree.item(selected[0])
        play_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить спектакль?"):
            self.data['plays'] = [p for p in self.data['plays'] if p['id'] != play_id]
            self.save_data()
            tree.delete(selected[0])
            messagebox.showinfo("Успех", "Спектакль удалён")
    
    def manage_halls(self):
        """Управление залами"""
        window = tk.Toplevel(self.root)
        window.title("Управление залами")
        window.geometry("600x400")
        
        columns = ('ID', 'Название', 'Вместимость')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for hall in self.data['halls']:
            tree.insert('', 'end', values=(hall['id'], hall['name'], hall['capacity']))
        
        tree.pack(padx=10, pady=10)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=lambda: self.add_hall(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_hall(tree)).pack(side='left', padx=5)
    
    def add_hall(self, tree):
        """Добавление зала"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить зал")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Название:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_entry = tk.Entry(dialog, width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Вместимость:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        capacity_entry = tk.Entry(dialog, width=20)
        capacity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def save():
            new_id = max([h['id'] for h in self.data['halls']]) + 1 if self.data['halls'] else 1
            new_hall = {
                'id': new_id,
                'name': name_entry.get(),
                'capacity': int(capacity_entry.get())
            }
            self.data['halls'].append(new_hall)
            self.save_data()
            tree.insert('', 'end', values=(new_hall['id'], new_hall['name'], new_hall['capacity']))
            dialog.destroy()
            messagebox.showinfo("Успех", "Зал добавлен")
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=2, column=0, columnspan=2, pady=15)
    
    def delete_hall(self, tree):
        """Удаление зала"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите зал")
            return
        
        item = tree.item(selected[0])
        hall_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить зал?"):
            self.data['halls'] = [h for h in self.data['halls'] if h['id'] != hall_id]
            self.save_data()
            tree.delete(selected[0])
            messagebox.showinfo("Успех", "Зал удалён")
    
    def manage_schedule(self):
        """Управление расписанием"""
        window = tk.Toplevel(self.root)
        window.title("Управление расписанием")
        window.geometry("900x500")
        
        columns = ('ID', 'Спектакль', 'Зал', 'Дата', 'Время', 'Цена', 'Свободно мест')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        for event in self.data['schedule']:
            play = next((p for p in self.data['plays'] if p['id'] == event['play_id']), None)
            hall = next((h for h in self.data['halls'] if h['id'] == event['hall_id']), None)
            tree.insert('', 'end', values=(event['id'], 
                                          play['title'] if play else 'N/A',
                                          hall['name'] if hall else 'N/A',
                                          event['date'], event['time'], 
                                          event['price'], event['available_seats']))
        
        tree.pack(padx=10, pady=10)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=lambda: self.add_schedule(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_schedule(tree)).pack(side='left', padx=5)
    
    def add_schedule(self, tree):
        """Добавление события в расписание"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить событие")
        dialog.geometry("350x250")
        
        tk.Label(dialog, text="Спектакль:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        play_var = tk.StringVar()
        play_combo = ttk.Combobox(dialog, textvariable=play_var, width=25, state='readonly')
        play_combo['values'] = [f"{p['id']}: {p['title']}" for p in self.data['plays']]
        play_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Зал:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        hall_var = tk.StringVar()
        hall_combo = ttk.Combobox(dialog, textvariable=hall_var, width=25, state='readonly')
        hall_combo['values'] = [f"{h['id']}: {h['name']}" for h in self.data['halls']]
        hall_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        date_entry = tk.Entry(dialog, width=27)
        date_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Время (HH:MM):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        time_entry = tk.Entry(dialog, width=27)
        time_entry.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Цена:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        price_entry = tk.Entry(dialog, width=27)
        price_entry.grid(row=4, column=1, padx=5, pady=5)
        
        def save():
            play_id = int(play_var.get().split(':')[0])
            hall_id = int(hall_var.get().split(':')[0])
            hall = next(h for h in self.data['halls'] if h['id'] == hall_id)
            
            new_id = max([s['id'] for s in self.data['schedule']]) + 1 if self.data['schedule'] else 1
            new_event = {
                'id': new_id,
                'play_id': play_id,
                'hall_id': hall_id,
                'date': date_entry.get(),
                'time': time_entry.get(),
                'price': int(price_entry.get()),
                'available_seats': hall['capacity']
            }
            self.data['schedule'].append(new_event)
            self.save_data()
            
            play = next(p for p in self.data['plays'] if p['id'] == play_id)
            tree.insert('', 'end', values=(new_event['id'], play['title'], hall['name'],
                                          new_event['date'], new_event['time'], 
                                          new_event['price'], new_event['available_seats']))
            dialog.destroy()
            messagebox.showinfo("Успех", "Событие добавлено")
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=5, column=0, columnspan=2, pady=15)
    
    def delete_schedule(self, tree):
        """Удаление события из расписания"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите событие")
            return
        
        item = tree.item(selected[0])
        event_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить событие?"):
            self.data['schedule'] = [s for s in self.data['schedule'] if s['id'] != event_id]
            self.save_data()
            tree.delete(selected[0])
            messagebox.showinfo("Успех", "Событие удалено")
    
    def manage_users(self):
        """Управление пользователями"""
        window = tk.Toplevel(self.root)
        window.title("Управление пользователями")
        window.geometry("700x500")
        
        columns = ('Логин', 'ФИО', 'Роль', 'Создан')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)
        
        for user in auth.get_all_users():
            tree.insert('', 'end', values=(user['username'], user['full_name'], 
                                          user['role'], user['created']))
        
        tree.pack(padx=10, pady=10)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=lambda: self.add_user(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_user(tree)).pack(side='left', padx=5)
    
    def add_user(self, tree):
        """Добавление пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("350x200")
        
        tk.Label(dialog, text="Логин:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(dialog, width=25)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(dialog, width=25, show='*')
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="ФИО:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        fullname_entry = tk.Entry(dialog, width=25)
        fullname_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Роль:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(dialog, textvariable=role_var, width=23, state='readonly')
        role_combo['values'] = ['administrator', 'cashier', 'visitor']
        role_combo.grid(row=3, column=1, padx=5, pady=5)
        
        def save():
            if auth.create_user(username_entry.get(), password_entry.get(), 
                              role_var.get(), fullname_entry.get()):
                tree.insert('', 'end', values=(username_entry.get(), fullname_entry.get(), 
                                              role_var.get(), datetime.now().strftime("%Y-%m-%d")))
                dialog.destroy()
                messagebox.showinfo("Успех", "Пользователь добавлен")
            else:
                messagebox.showerror("Ошибка", "Пользователь уже существует")
        
        tk.Button(dialog, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=15)
    
    def delete_user(self, tree):
        """Удаление пользователя"""
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
            auth.delete_user(username)
            tree.delete(selected[0])
            messagebox.showinfo("Успех", "Пользователь удалён")
    
    def view_statistics(self):
        """Просмотр статистики"""
        window = tk.Toplevel(self.root)
        window.title("Статистика")
        window.geometry("500x400")
        
        total_plays = len(self.data['plays'])
        total_halls = len(self.data['halls'])
        total_events = len(self.data['schedule'])
        total_tickets = len(self.data['tickets'])
        total_bookings = len(self.data['bookings'])
        
        total_revenue = sum([t['price'] for t in self.data['tickets']])
        
        stats_text = f"""
        📊 Статистика театра
        
        Спектаклей в репертуаре: {total_plays}
        Залов: {total_halls}
        Событий в расписании: {total_events}
        
        Продано билетов: {total_tickets}
        Активных бронирований: {total_bookings}
        
        Общая выручка: {total_revenue} руб.
        """
        
        tk.Label(window, text=stats_text, font=('Arial', 12), justify='left').pack(pady=30, padx=30)
    
    # ==================== КАССИР ====================
    
    def view_schedule_cashier(self):
        """Просмотр афиши для кассира"""
        self.browse_repertoire()
    
    def sell_tickets(self):
        """Продажа билетов"""
        window = tk.Toplevel(self.root)
        window.title("Продажа билетов")
        window.geometry("700x400")
        
        tk.Label(window, text="Выберите событие:", font=('Arial', 12)).pack(pady=10)
        
        columns = ('ID', 'Спектакль', 'Дата', 'Время', 'Цена', 'Свободно')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        for event in self.data['schedule']:
            if event['available_seats'] > 0:
                play = next((p for p in self.data['plays'] if p['id'] == event['play_id']), None)
                tree.insert('', 'end', values=(event['id'], play['title'] if play else 'N/A',
                                              event['date'], event['time'], 
                                              event['price'], event['available_seats']))
        
        tree.pack(padx=10, pady=10)
        
        quantity_frame = tk.Frame(window)
        quantity_frame.pack(pady=10)
        
        tk.Label(quantity_frame, text="Количество билетов:").pack(side='left', padx=5)
        quantity_entry = tk.Entry(quantity_frame, width=10)
        quantity_entry.insert(0, '1')
        quantity_entry.pack(side='left', padx=5)
        
        def sell():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите событие")
                return
            
            item = tree.item(selected[0])
            event_id = item['values'][0]
            quantity = int(quantity_entry.get())
            
            event = next(e for e in self.data['schedule'] if e['id'] == event_id)
            
            if event['available_seats'] < quantity:
                messagebox.showerror("Ошибка", "Недостаточно свободных мест")
                return
            
            # Создание билетов
            for _ in range(quantity):
                ticket_id = max([t['id'] for t in self.data['tickets']]) + 1 if self.data['tickets'] else 1
                ticket = {
                    'id': ticket_id,
                    'event_id': event_id,
                    'price': event['price'],
                    'sold_by': self.current_user['username'],
                    'sold_date': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                self.data['tickets'].append(ticket)
            
            event['available_seats'] -= quantity
            self.save_data()
            
            messagebox.showinfo("Успех", f"Продано {quantity} билет(ов)\nСумма: {event['price'] * quantity} руб.")
            window.destroy()
        
        tk.Button(window, text="Продать", font=('Arial', 11), command=sell).pack(pady=10)
    
    def refund_tickets(self):
        """Возврат билетов"""
        window = tk.Toplevel(self.root)
        window.title("Возврат билетов")
        window.geometry("800x400")
        
        columns = ('ID', 'Событие', 'Цена', 'Продано', 'Дата продажи')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=155)
        
        for ticket in self.data['tickets']:
            event = next((e for e in self.data['schedule'] if e['id'] == ticket['event_id']), None)
            if event:
                play = next((p for p in self.data['plays'] if p['id'] == event['play_id']), None)
                tree.insert('', 'end', values=(ticket['id'], 
                                              f"{play['title']} ({event['date']} {event['time']})" if play else 'N/A',
                                              ticket['price'], ticket['sold_by'], ticket['sold_date']))
        
        tree.pack(padx=10, pady=10)
        
        def refund():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите билет")
                return
            
            item = tree.item(selected[0])
            ticket_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Вернуть билет?"):
                ticket = next(t for t in self.data['tickets'] if t['id'] == ticket_id)
                event = next(e for e in self.data['schedule'] if e['id'] == ticket['event_id'])
                event['available_seats'] += 1
                self.data['tickets'] = [t for t in self.data['tickets'] if t['id'] != ticket_id]
                self.save_data()
                tree.delete(selected[0])
                messagebox.showinfo("Успех", "Билет возвращён")
        
        tk.Button(window, text="Вернуть", font=('Arial', 11), command=refund).pack(pady=10)
    
    def search_plays(self):
        """Поиск спектаклей"""
        window = tk.Toplevel(self.root)
        window.title("Поиск спектаклей")
        window.geometry("700x450")
        
        search_frame = tk.Frame(window)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        columns = ('ID', 'Название', 'Автор', 'Жанр')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)
        
        def search():
            tree.delete(*tree.get_children())
            query = search_entry.get().lower()
            for play in self.data['plays']:
                if (query in play['title'].lower() or 
                    query in play['author'].lower() or 
                    query in play['genre'].lower()):
                    tree.insert('', 'end', values=(play['id'], play['title'], 
                                                  play['author'], play['genre']))
        
        tk.Button(search_frame, text="Найти", command=search).pack(side='left', padx=5)
        
        tree.pack(padx=10, pady=10)
        
        # Показать все при открытии
        search()
    
    # ==================== ПОСЕТИТЕЛЬ ====================
    
    def browse_repertoire(self):
        """Просмотр репертуара"""
        window = tk.Toplevel(self.root)
        window.title("Репертуар театра")
        window.geometry("900x500")
        
        columns = ('Спектакль', 'Автор', 'Жанр', 'Дата', 'Время', 'Зал', 'Цена', 'Свободно')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=18)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        for event in self.data['schedule']:
            play = next((p for p in self.data['plays'] if p['id'] == event['play_id']), None)
            hall = next((h for h in self.data['halls'] if h['id'] == event['hall_id']), None)
            if play and hall:
                tree.insert('', 'end', values=(play['title'], play['author'], play['genre'],
                                              event['date'], event['time'], hall['name'],
                                              event['price'], event['available_seats']))
        
        tree.pack(padx=10, pady=10, fill='both', expand=True)
    
    def book_tickets(self):
        """Бронирование билетов"""
        window = tk.Toplevel(self.root)
        window.title("Бронирование билетов")
        window.geometry("700x450")
        
        tk.Label(window, text="Выберите событие для бронирования:", font=('Arial', 12)).pack(pady=10)
        
        columns = ('ID', 'Спектакль', 'Дата', 'Время', 'Цена', 'Свободно')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        for event in self.data['schedule']:
            if event['available_seats'] > 0:
                play = next((p for p in self.data['plays'] if p['id'] == event['play_id']), None)
                tree.insert('', 'end', values=(event['id'], play['title'] if play else 'N/A',
                                              event['date'], event['time'], 
                                              event['price'], event['available_seats']))
        
        tree.pack(padx=10, pady=10)
        
        quantity_frame = tk.Frame(window)
        quantity_frame.pack(pady=10)
        
        tk.Label(quantity_frame, text="Количество:").pack(side='left', padx=5)
        quantity_entry = tk.Entry(quantity_frame, width=10)
        quantity_entry.insert(0, '1')
        quantity_entry.pack(side='left', padx=5)
        
        def book():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите событие")
                return
            
            item = tree.item(selected[0])
            event_id = item['values'][0]
            quantity = int(quantity_entry.get())
            
            event = next(e for e in self.data['schedule'] if e['id'] == event_id)
            
            if event['available_seats'] < quantity:
                messagebox.showerror("Ошибка", "Недостаточно свободных мест")
                return
            
            booking_id = max([b['id'] for b in self.data['bookings']]) + 1 if self.data['bookings'] else 1
            booking = {
                'id': booking_id,
                'event_id': event_id,
                'quantity': quantity,
                'user': self.current_user['username'],
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'status': 'active'
            }
            self.data['bookings'].append(booking)
            event['available_seats'] -= quantity
            self.save_data()
            
            messagebox.showinfo("Успех", f"Забронировано {quantity} билет(ов)\nНомер брони: {booking_id}")
            window.destroy()
        
        tk.Button(window, text="Забронировать", font=('Arial', 11), command=book).pack(pady=10)
    
    def view_my_bookings(self):
        """Просмотр бронирований текущего пользователя"""
        window = tk.Toplevel(self.root)
        window.title("Мои бронирования")
        window.geometry("800x400")
        
        columns = ('ID', 'Спектакль', 'Дата', 'Время', 'Количество', 'Статус')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        user_bookings = [b for b in self.data['bookings'] 
                        if b['user'] == self.current_user['username'] and b['status'] == 'active']
        
        for booking in user_bookings:
            event = next((e for e in self.data['schedule'] if e['id'] == booking['event_id']), None)
            if event:
                play = next((p for p in self.data['plays'] if p['id'] == event['play_id']), None)
                tree.insert('', 'end', values=(booking['id'], 
                                              play['title'] if play else 'N/A',
                                              event['date'], event['time'],
                                              booking['quantity'], booking['status']))
        
        tree.pack(padx=10, pady=10)
        
        if not user_bookings:
            tk.Label(window, text="У вас нет активных бронирований", 
                    font=('Arial', 12)).pack(pady=20)
    
    def cancel_booking(self):
        """Отмена бронирования"""
        window = tk.Toplevel(self.root)
        window.title("Отмена бронирования")
        window.geometry("800x400")
        
        columns = ('ID', 'Спектакль', 'Дата', 'Время', 'Количество')
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=155)
        
        user_bookings = [b for b in self.data['bookings'] 
                        if b['user'] == self.current_user['username'] and b['status'] == 'active']
        
        for booking in user_bookings:
            event = next((e for e in self.data['schedule'] if e['id'] == booking['event_id']), None)
            if event:
                play = next((p for p in self.data['plays'] if p['id'] == event['play_id']), None)
                tree.insert('', 'end', values=(booking['id'], 
                                              play['title'] if play else 'N/A',
                                              event['date'], event['time'], booking['quantity']))
        
        tree.pack(padx=10, pady=10)
        
        def cancel():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите бронирование")
                return
            
            item = tree.item(selected[0])
            booking_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Отменить бронирование?"):
                booking = next(b for b in self.data['bookings'] if b['id'] == booking_id)
                event = next(e for e in self.data['schedule'] if e['id'] == booking['event_id'])
                event['available_seats'] += booking['quantity']
                booking['status'] = 'cancelled'
                self.save_data()
                tree.delete(selected[0])
                messagebox.showinfo("Успех", "Бронирование отменено")
        
        tk.Button(window, text="Отменить бронирование", font=('Arial', 11), 
                 command=cancel).pack(pady=10)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TheaterApp()
    app.run()