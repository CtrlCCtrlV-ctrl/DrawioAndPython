import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import Auth

class FitnessClubApp:
    """Главное приложение фитнес клуба"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Информационная система - Фитнес Клуб")
        self.root.geometry("900x600")
        
        self.auth = Auth()
        self.data_file = 'data.json'

        self.show_login_window()
    
    def load_data(self):
        """Загрузка данных из JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_data(self, data):
        """Сохранение данных в JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Фитнес Клуб - Вход в систему", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, width=25, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def login_action():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, role, name = self.auth.login(username, password)
            
            if success:
                messagebox.showinfo("Успех", f"Добро пожаловать, {name}!")
                self.show_main_menu(role, name)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login_action, width=20).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка
        hint_text = "Тестовые данные:\nadmin/admin123\ntrainer1/trainer123\nclient1/client123"
        tk.Label(frame, text=hint_text, font=("Arial", 9), fg="gray", justify='left').grid(row=4, column=0, columnspan=2)
    
    def show_main_menu(self, role, name):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"Фитнес Клуб", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white").pack(side='left', padx=20, pady=15)
        tk.Label(top_frame, text=f"Пользователь: {name}", font=("Arial", 10), bg="#2c3e50", fg="white").pack(side='right', padx=20)
        
        def logout_action():
            self.auth.logout()
            self.show_login_window()
        
        tk.Button(top_frame, text="Выход", command=logout_action, bg="#e74c3c", fg="white").pack(side='right', padx=5)
        
        # Основное меню
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if role == "administrator":
            self.show_admin_menu(menu_frame)
        elif role == "trainer":
            self.show_trainer_menu(menu_frame)
        elif role == "client":
            self.show_client_menu(menu_frame)
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=("Arial", 14, "bold")).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Управление пользователями", width=30, height=2, command=self.manage_users).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Управление тренерами", width=30, height=2, command=self.manage_trainers).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="Управление абонементами", width=30, height=2, command=self.manage_memberships).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Управление расписанием", width=30, height=2, command=self.manage_schedule).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="Просмотр статистики", width=30, height=2, command=self.view_statistics).grid(row=2, column=0, padx=10, pady=10)
    
    def show_trainer_menu(self, parent):
        """Меню тренера"""
        tk.Label(parent, text="Панель тренера", font=("Arial", 14, "bold")).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Мое расписание", width=30, height=2, command=self.view_trainer_schedule).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Список клиентов", width=30, height=2, command=self.view_clients).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="Отметка посещаемости", width=30, height=2, command=self.mark_attendance).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Управление тренировками", width=30, height=2, command=self.manage_trainings).grid(row=1, column=1, padx=10, pady=10)
    
    def show_client_menu(self, parent):
        """Меню клиента"""
        tk.Label(parent, text="Панель клиента", font=("Arial", 14, "bold")).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Расписание тренировок", width=30, height=2, command=self.view_schedule).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Записаться на тренировку", width=30, height=2, command=self.book_training).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="Мой абонемент", width=30, height=2, command=self.view_my_membership).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="История посещений", width=30, height=2, command=self.view_my_history).grid(row=1, column=1, padx=10, pady=10)
    
    # ФУНКЦИИ АДМИНИСТРАТОРА
    def manage_users(self):
        """Управление пользователями"""
        window = tk.Toplevel(self.root)
        window.title("Управление пользователями")
        window.geometry("700x500")
        
        # Таблица пользователей
        columns = ("Логин", "Имя", "Роль", "Дата создания")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10)
        
        def refresh_users():
            tree.delete(*tree.get_children())
            users = self.auth.get_all_users()
            for user in users:
                tree.insert('', 'end', values=(user['username'], user['name'], user['role'], user['created']))
        
        refresh_users()
        
        # Кнопки управления
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_user():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить пользователя")
            add_window.geometry("400x300")
            
            tk.Label(add_window, text="Логин:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            username_entry = tk.Entry(add_window, width=25)
            username_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Пароль:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            password_entry = tk.Entry(add_window, width=25, show="*")
            password_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Имя:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            name_entry = tk.Entry(add_window, width=25)
            name_entry.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Роль:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
            role_var = tk.StringVar(value="client")
            tk.Radiobutton(add_window, text="Администратор", variable=role_var, value="administrator").grid(row=3, column=1, sticky='w')
            tk.Radiobutton(add_window, text="Тренер", variable=role_var, value="trainer").grid(row=4, column=1, sticky='w')
            tk.Radiobutton(add_window, text="Клиент", variable=role_var, value="client").grid(row=5, column=1, sticky='w')
            
            def save_user():
                username = username_entry.get().strip()
                password = password_entry.get().strip()
                name = name_entry.get().strip()
                role = role_var.get()
                
                if not all([username, password, name]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                success, message = self.auth.register(username, password, role, name)
                if success:
                    messagebox.showinfo("Успех", message)
                    refresh_users()
                    add_window.destroy()
                else:
                    messagebox.showerror("Ошибка", message)
            
            tk.Button(add_window, text="Сохранить", command=save_user, width=15).grid(row=6, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите пользователя")
                return
            
            item = tree.item(selected[0])
            username = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                self.auth.delete_user(username)
                refresh_users()
                messagebox.showinfo("Успех", "Пользователь удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_user, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, width=15).pack(side='left', padx=5)
    
    def manage_trainers(self):
        """Управление тренерами"""
        window = tk.Toplevel(self.root)
        window.title("Управление тренерами")
        window.geometry("800x500")
        
        columns = ("ID", "Имя", "Специализация", "Телефон")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        
        tree.pack(pady=10, padx=10)
        
        def refresh_trainers():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for trainer in data.get('trainers', []):
                tree.insert('', 'end', values=(trainer['id'], trainer['name'], trainer['specialization'], trainer['phone']))
        
        refresh_trainers()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_trainer():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить тренера")
            add_window.geometry("400x250")
            
            tk.Label(add_window, text="Имя:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            name_entry = tk.Entry(add_window, width=25)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Специализация:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            spec_entry = tk.Entry(add_window, width=25)
            spec_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Телефон:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            phone_entry = tk.Entry(add_window, width=25)
            phone_entry.grid(row=2, column=1, padx=10, pady=5)
            
            def save_trainer():
                name = name_entry.get().strip()
                spec = spec_entry.get().strip()
                phone = phone_entry.get().strip()
                
                if not all([name, spec, phone]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                data = self.load_data()
                new_id = max([t['id'] for t in data.get('trainers', [])], default=0) + 1
                
                data.setdefault('trainers', []).append({
                    "id": new_id,
                    "name": name,
                    "specialization": spec,
                    "phone": phone
                })
                
                self.save_data(data)
                refresh_trainers()
                add_window.destroy()
                messagebox.showinfo("Успех", "Тренер добавлен")
            
            tk.Button(add_window, text="Сохранить", command=save_trainer, width=15).grid(row=3, column=0, columnspan=2, pady=20)
        
        def delete_trainer():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Внимание", "Выберите тренера")
                return
            
            item = tree.item(selected[0])
            trainer_id = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", "Удалить тренера?"):
                data = self.load_data()
                data['trainers'] = [t for t in data.get('trainers', []) if t['id'] != trainer_id]
                self.save_data(data)
                refresh_trainers()
                messagebox.showinfo("Успех", "Тренер удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_trainer, width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_trainer, width=15).pack(side='left', padx=5)
    
    def manage_memberships(self):
        """Управление абонементами"""
        window = tk.Toplevel(self.root)
        window.title("Управление абонементами")
        window.geometry("900x500")
        
        columns = ("ID", "Клиент", "Тип", "Начало", "Окончание", "Посещения")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(pady=10, padx=10)
        
        def refresh_memberships():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for membership in data.get('memberships', []):
                tree.insert('', 'end', values=(membership['id'], membership['client'], membership['type'], 
                                              membership['start'], membership['end'], membership['visits']))
        
        refresh_memberships()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_membership():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить абонемент")
            add_window.geometry("400x300")
            
            tk.Label(add_window, text="Клиент:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            client_entry = tk.Entry(add_window, width=25)
            client_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Тип:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            type_var = tk.StringVar(value="Месячный")
            types = ["Месячный", "Квартальный", "Годовой"]
            tk.OptionMenu(add_window, type_var, *types).grid(row=1, column=1, padx=10, pady=5, sticky='w')
            
            tk.Label(add_window, text="Дата начала:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            start_entry = tk.Entry(add_window, width=25)
            start_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            start_entry.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Дата окончания:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
            end_entry = tk.Entry(add_window, width=25)
            end_entry.grid(row=3, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Посещения:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
            visits_entry = tk.Entry(add_window, width=25)
            visits_entry.insert(0, "0")
            visits_entry.grid(row=4, column=1, padx=10, pady=5)
            
            def save_membership():
                client = client_entry.get().strip()
                mtype = type_var.get()
                start = start_entry.get().strip()
                end = end_entry.get().strip()
                visits = visits_entry.get().strip()
                
                if not all([client, start, end, visits]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                data = self.load_data()
                new_id = max([m['id'] for m in data.get('memberships', [])], default=0) + 1
                
                data.setdefault('memberships', []).append({
                    "id": new_id,
                    "client": client,
                    "type": mtype,
                    "start": start,
                    "end": end,
                    "visits": int(visits)
                })
                
                self.save_data(data)
                refresh_memberships()
                add_window.destroy()
                messagebox.showinfo("Успех", "Абонемент добавлен")
            
            tk.Button(add_window, text="Сохранить", command=save_membership, width=15).grid(row=5, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Добавить", command=add_membership, width=15).pack(side='left', padx=5)
    
    def manage_schedule(self):
        """Управление расписанием"""
        window = tk.Toplevel(self.root)
        window.title("Управление расписанием")
        window.geometry("900x500")
        
        columns = ("ID", "Тренер", "Тип", "Дата", "Время", "Вместимость", "Записано")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10)
        
        def refresh_schedule():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for item in data.get('schedule', []):
                tree.insert('', 'end', values=(item['id'], item['trainer'], item['type'], 
                                              item['date'], item['time'], item['capacity'], item['booked']))
        
        refresh_schedule()
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=10)
        
        def add_schedule():
            add_window = tk.Toplevel(window)
            add_window.title("Добавить занятие")
            add_window.geometry("400x350")
            
            tk.Label(add_window, text="Тренер:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
            trainer_entry = tk.Entry(add_window, width=25)
            trainer_entry.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Тип тренировки:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
            type_entry = tk.Entry(add_window, width=25)
            type_entry.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Дата:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
            date_entry = tk.Entry(add_window, width=25)
            date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            date_entry.grid(row=2, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Время:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
            time_entry = tk.Entry(add_window, width=25)
            time_entry.grid(row=3, column=1, padx=10, pady=5)
            
            tk.Label(add_window, text="Вместимость:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
            capacity_entry = tk.Entry(add_window, width=25)
            capacity_entry.insert(0, "10")
            capacity_entry.grid(row=4, column=1, padx=10, pady=5)
            
            def save_schedule():
                trainer = trainer_entry.get().strip()
                stype = type_entry.get().strip()
                date = date_entry.get().strip()
                time = time_entry.get().strip()
                capacity = capacity_entry.get().strip()
                
                if not all([trainer, stype, date, time, capacity]):
                    messagebox.showerror("Ошибка", "Заполните все поля")
                    return
                
                data = self.load_data()
                new_id = max([s['id'] for s in data.get('schedule', [])], default=0) + 1
                
                data.setdefault('schedule', []).append({
                    "id": new_id,
                    "trainer": trainer,
                    "type": stype,
                    "date": date,
                    "time": time,
                    "capacity": int(capacity),
                    "booked": 0
                })
                
                self.save_data(data)
                refresh_schedule()
                add_window.destroy()
                messagebox.showinfo("Успех", "Занятие добавлено в расписание")
            
            tk.Button(add_window, text="Сохранить", command=save_schedule, width=15).grid(row=5, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Добавить", command=add_schedule, width=15).pack(side='left', padx=5)
    
    def view_statistics(self):
        """Просмотр статистики"""
        window = tk.Toplevel(self.root)
        window.title("Статистика")
        window.geometry("600x400")
        
        data = self.load_data()
        
        stats_frame = tk.Frame(window, padx=30, pady=30)
        stats_frame.pack(fill='both', expand=True)
        
        tk.Label(stats_frame, text="Статистика фитнес клуба", font=("Arial", 14, "bold")).pack(pady=10)
        
        total_trainers = len(data.get('trainers', []))
        total_memberships = len(data.get('memberships', []))
        total_schedule = len(data.get('schedule', []))
        total_bookings = len(data.get('bookings', []))
        total_attendance = len(data.get('attendance', []))
        
        stats_text = f"""
        Всего тренеров: {total_trainers}
        Всего абонементов: {total_memberships}
        Занятий в расписании: {total_schedule}
        Всего записей: {total_bookings}
        Всего посещений: {total_attendance}
        """
        
        tk.Label(stats_frame, text=stats_text, font=("Arial", 12), justify='left').pack(pady=20)
    
    # ФУНКЦИИ ТРЕНЕРА
    def view_trainer_schedule(self):
        """Просмотр расписания тренера"""
        window = tk.Toplevel(self.root)
        window.title("Мое расписание")
        window.geometry("800x500")
        
        columns = ("ID", "Тип", "Дата", "Время", "Вместимость", "Записано")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=10)
        
        data = self.load_data()
        trainer_name = self.auth.current_user['name']
        
        for item in data.get('schedule', []):
            if item['trainer'] == trainer_name:
                tree.insert('', 'end', values=(item['id'], item['type'], item['date'], 
                                              item['time'], item['capacity'], item['booked']))
    
    def view_clients(self):
        """Просмотр списка клиентов"""
        window = tk.Toplevel(self.root)
        window.title("Список клиентов")
        window.geometry("700x500")
        
        columns = ("Клиент", "Тип абонемента", "Окончание", "Посещения")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=165)
        
        tree.pack(pady=10, padx=10)
        
        data = self.load_data()
        for membership in data.get('memberships', []):
            tree.insert('', 'end', values=(membership['client'], membership['type'], 
                                          membership['end'], membership['visits']))
    
    def mark_attendance(self):
        """Отметка посещаемости"""
        window = tk.Toplevel(self.root)
        window.title("Отметка посещаемости")
        window.geometry("500x350")
        
        frame = tk.Frame(window, padx=30, pady=30)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Отметка посещаемости", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(frame, text="Клиент:").pack(pady=5)
        client_entry = tk.Entry(frame, width=30)
        client_entry.pack(pady=5)
        
        tk.Label(frame, text="ID тренировки:").pack(pady=5)
        training_entry = tk.Entry(frame, width=30)
        training_entry.pack(pady=5)
        
        tk.Label(frame, text="Дата:").pack(pady=5)
        date_entry = tk.Entry(frame, width=30)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)
        
        def save_attendance():
            client = client_entry.get().strip()
            training_id = training_entry.get().strip()
            date = date_entry.get().strip()
            
            if not all([client, training_id, date]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            data = self.load_data()
            new_id = max([a['id'] for a in data.get('attendance', [])], default=0) + 1
            
            data.setdefault('attendance', []).append({
                "id": new_id,
                "client": client,
                "training_id": int(training_id),
                "date": date,
                "status": "Присутствовал"
            })
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Посещение отмечено")
            window.destroy()
        
        tk.Button(frame, text="Сохранить", command=save_attendance, width=15).pack(pady=20)
    
    def manage_trainings(self):
        """Управление тренировками (для тренера)"""
        self.manage_schedule()  # Используем ту же функцию
    
    # ФУНКЦИИ КЛИЕНТА
    def view_schedule(self):
        """Просмотр расписания тренировок"""
        window = tk.Toplevel(self.root)
        window.title("Расписание тренировок")
        window.geometry("900x500")
        
        columns = ("ID", "Тренер", "Тип", "Дата", "Время", "Вместимость", "Записано", "Доступно")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        tree.pack(pady=10, padx=10)
        
        data = self.load_data()
        for item in data.get('schedule', []):
            available = item['capacity'] - item['booked']
            tree.insert('', 'end', values=(item['id'], item['trainer'], item['type'], 
                                          item['date'], item['time'], item['capacity'], 
                                          item['booked'], available))
    
    def book_training(self):
        """Запись на тренировку"""
        window = tk.Toplevel(self.root)
        window.title("Запись на тренировку")
        window.geometry("500x300")
        
        frame = tk.Frame(window, padx=30, pady=30)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Запись на тренировку", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(frame, text="ID тренировки:").pack(pady=5)
        training_entry = tk.Entry(frame, width=30)
        training_entry.pack(pady=5)
        
        tk.Label(frame, text="Дата:").pack(pady=5)
        date_entry = tk.Entry(frame, width=30)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)
        
        def save_booking():
            training_id = training_entry.get().strip()
            date = date_entry.get().strip()
            
            if not all([training_id, date]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            data = self.load_data()
            client_name = self.auth.current_user['name']
            
            # Проверка доступности мест
            training = next((s for s in data.get('schedule', []) if s['id'] == int(training_id)), None)
            if not training:
                messagebox.showerror("Ошибка", "Тренировка не найдена")
                return
            
            if training['booked'] >= training['capacity']:
                messagebox.showerror("Ошибка", "Нет свободных мест")
                return
            
            new_id = max([b['id'] for b in data.get('bookings', [])], default=0) + 1
            
            data.setdefault('bookings', []).append({
                "id": new_id,
                "client": client_name,
                "training_id": int(training_id),
                "date": date,
                "status": "Подтверждено"
            })
            
            # Увеличить счетчик записавшихся
            for s in data['schedule']:
                if s['id'] == int(training_id):
                    s['booked'] += 1
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Вы успешно записаны на тренировку!")
            window.destroy()
        
        tk.Button(frame, text="Записаться", command=save_booking, width=15).pack(pady=20)
    
    def view_my_membership(self):
        """Просмотр своего абонемента"""
        window = tk.Toplevel(self.root)
        window.title("Мой абонемент")
        window.geometry("600x400")
        
        frame = tk.Frame(window, padx=30, pady=30)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Информация об абонементе", font=("Arial", 14, "bold")).pack(pady=10)
        
        data = self.load_data()
        client_name = self.auth.current_user['name']
        
        membership = next((m for m in data.get('memberships', []) if m['client'] == client_name), None)
        
        if membership:
            info_text = f"""
            Клиент: {membership['client']}
            Тип: {membership['type']}
            Дата начала: {membership['start']}
            Дата окончания: {membership['end']}
            Посещений: {membership['visits']}
            """
        else:
            info_text = "У вас нет активного абонемента"
        
        tk.Label(frame, text=info_text, font=("Arial", 11), justify='left').pack(pady=20)
    
    def view_my_history(self):
        """История посещений"""
        window = tk.Toplevel(self.root)
        window.title("История посещений")
        window.geometry("700x500")
        
        columns = ("ID", "ID тренировки", "Дата", "Статус")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=165)
        
        tree.pack(pady=10, padx=10)
        
        data = self.load_data()
        client_name = self.auth.current_user['name']
        
        for attendance in data.get('attendance', []):
            if attendance['client'] == client_name:
                tree.insert('', 'end', values=(attendance['id'], attendance['training_id'], 
                                              attendance['date'], attendance['status']))
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = FitnessClubApp()
    app.run()