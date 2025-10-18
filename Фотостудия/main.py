import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

DATA_FILE = 'data.json'

class PhotoStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система - Фотостудия")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.current_user = None
        self.init_data()
        self.show_login()
    
    def init_data(self):
        """Инициализация базы данных"""
        # Файлы уже созданы с тестовыми данными
        pass
    
    def load_data(self):
        """Загрузка данных"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно входа"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Фотостудия", font=('Arial', 24, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=10)
        username_entry = tk.Entry(frame, font=('Arial', 12), width=20)
        username_entry.grid(row=1, column=1, padx=5, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12), bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=10)
        password_entry = tk.Entry(frame, font=('Arial', 12), width=20, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=10)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            user = auth.authenticate(username, password)
            if user:
                self.current_user = user
                auth.current_user = user
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", font=('Arial', 12), width=15, command=login, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        info_text = "Тестовые учетные записи:\nadmin/admin123\nphotographer/photo123\nclient/client123"
        tk.Label(frame, text=info_text, font=('Arial', 9), bg='#f0f0f0', fg='#666').grid(row=4, column=0, columnspan=2)
    
    def show_main_menu(self):
        """Главное меню"""
        self.clear_window()
        
        header = tk.Frame(self.root, bg='#2196F3', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Фотостудия - {self.current_user['full_name']}", font=('Arial', 16, 'bold'), bg='#2196F3', fg='white').pack(side='left', padx=20, pady=15)
        tk.Button(header, text="Выход", command=self.show_login, bg='#f44336', fg='white').pack(side='right', padx=20)
        
        content = tk.Frame(self.root)
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        role = self.current_user['role']
        
        if role == 'administrator':
            self.show_admin_menu(content)
        elif role == 'photographer':
            self.show_photographer_menu(content)
        elif role == 'client':
            self.show_client_menu(content)
    
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=('Arial', 18, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Управление пользователями", width=25, command=self.manage_users).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(buttons_frame, text="Управление залами", width=25, command=self.manage_studios).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(buttons_frame, text="Управление оборудованием", width=25, command=self.manage_equipment).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(buttons_frame, text="Управление тарифами", width=25, command=self.manage_tariffs).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(buttons_frame, text="Просмотр отчетов", width=25, command=self.view_reports).grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    
    def show_photographer_menu(self, parent):
        """Меню фотографа"""
        tk.Label(parent, text="Панель фотографа", font=('Arial', 18, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Просмотр расписания", width=25, command=self.view_schedule).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(buttons_frame, text="Создание фотосессии", width=25, command=self.create_session).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(buttons_frame, text="Редактирование фотосессии", width=25, command=self.edit_session).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(buttons_frame, text="Просмотр клиентов", width=25, command=self.view_clients).grid(row=1, column=1, padx=10, pady=5)
    
    def show_client_menu(self, parent):
        """Меню клиента"""
        tk.Label(parent, text="Панель клиента", font=('Arial', 18, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Бронирование фотосессии", width=25, command=self.book_session).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(buttons_frame, text="Мои заказы", width=25, command=self.view_my_orders).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(buttons_frame, text="Оплата услуг", width=25, command=self.payment).grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    
    # Функции администратора
    
    def manage_users(self):
        """Управление пользователями"""
        win = tk.Toplevel(self.root)
        win.title("Управление пользователями")
        win.geometry("700x400")
        
        tree = ttk.Treeview(win, columns=('username', 'role', 'full_name', 'created'), show='headings')
        tree.heading('username', text='Логин')
        tree.heading('role', text='Роль')
        tree.heading('full_name', text='ФИО')
        tree.heading('created', text='Дата создания')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        def refresh():
            tree.delete(*tree.get_children())
            for user in auth.get_all_users():
                tree.insert('', 'end', values=(user['username'], user['role'], user['full_name'], user['created']))
        
        def add_user():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить пользователя")
            add_win.geometry("300x250")
            
            tk.Label(add_win, text="Логин:").grid(row=0, column=0, padx=10, pady=5)
            username = tk.Entry(add_win)
            username.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
            password = tk.Entry(add_win, show='*')
            password.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Роль:").grid(row=2, column=0, padx=10, pady=5)
            role = ttk.Combobox(add_win, values=['administrator', 'photographer', 'client'])
            role.grid(row=2, column=1, padx=10, pady=5)
            role.current(2)
            
            tk.Label(add_win, text="ФИО:").grid(row=3, column=0, padx=10, pady=5)
            full_name = tk.Entry(add_win)
            full_name.grid(row=3, column=1, padx=10, pady=5)
            
            def save():
                if auth.create_user(username.get(), password.get(), role.get(), full_name.get()):
                    messagebox.showinfo("Успех", "Пользователь добавлен")
                    add_win.destroy()
                    refresh()
                else:
                    messagebox.showerror("Ошибка", "Пользователь уже существует")
            
            tk.Button(add_win, text="Сохранить", command=save).grid(row=4, column=0, columnspan=2, pady=10)
        
        def delete_user():
            selected = tree.selection()
            if selected:
                username = tree.item(selected[0])['values'][0]
                if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                    auth.delete_user(username)
                    refresh()
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Добавить", command=add_user).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user).pack(side='left', padx=5)
        
        refresh()
    
    def manage_studios(self):
        """Управление залами"""
        win = tk.Toplevel(self.root)
        win.title("Управление залами")
        win.geometry("600x400")
        
        tree = ttk.Treeview(win, columns=('id', 'name', 'area', 'price'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('name', text='Название')
        tree.heading('area', text='Площадь (м²)')
        tree.heading('price', text='Цена/час')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        def refresh():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for studio in data['studios']:
                tree.insert('', 'end', values=(studio['id'], studio['name'], studio['area'], studio['price_hour']))
        
        def add_studio():
            add_win = tk.Toplevel(win)
            add_win.title("Добавить зал")
            add_win.geometry("300x200")
            
            tk.Label(add_win, text="Название:").grid(row=0, column=0, padx=10, pady=5)
            name = tk.Entry(add_win)
            name.grid(row=0, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Площадь:").grid(row=1, column=0, padx=10, pady=5)
            area = tk.Entry(add_win)
            area.grid(row=1, column=1, padx=10, pady=5)
            
            tk.Label(add_win, text="Цена/час:").grid(row=2, column=0, padx=10, pady=5)
            price = tk.Entry(add_win)
            price.grid(row=2, column=1, padx=10, pady=5)
            
            def save():
                data = self.load_data()
                new_id = max([s['id'] for s in data['studios']], default=0) + 1
                data['studios'].append({
                    'id': new_id,
                    'name': name.get(),
                    'area': int(area.get()),
                    'price_hour': int(price.get())
                })
                self.save_data(data)
                messagebox.showinfo("Успех", "Зал добавлен")
                add_win.destroy()
                refresh()
            
            tk.Button(add_win, text="Сохранить", command=save).grid(row=3, column=0, columnspan=2, pady=10)
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Добавить", command=add_studio).pack(side='left', padx=5)
        
        refresh()
    
    def manage_equipment(self):
        """Управление оборудованием"""
        win = tk.Toplevel(self.root)
        win.title("Управление оборудованием")
        win.geometry("600x400")
        
        tree = ttk.Treeview(win, columns=('id', 'name', 'type', 'available'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('name', text='Название')
        tree.heading('type', text='Тип')
        tree.heading('available', text='Доступно')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        def refresh():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for eq in data['equipment']:
                tree.insert('', 'end', values=(eq['id'], eq['name'], eq['type'], 'Да' if eq['available'] else 'Нет'))
        
        refresh()
    
    def manage_tariffs(self):
        """Управление тарифами"""
        win = tk.Toplevel(self.root)
        win.title("Управление тарифами")
        win.geometry("700x400")
        
        tree = ttk.Treeview(win, columns=('id', 'name', 'duration', 'price', 'photos'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('name', text='Название')
        tree.heading('duration', text='Часов')
        tree.heading('price', text='Цена')
        tree.heading('photos', text='Фото')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        def refresh():
            tree.delete(*tree.get_children())
            data = self.load_data()
            for tariff in data['tariffs']:
                tree.insert('', 'end', values=(tariff['id'], tariff['name'], tariff['duration'], tariff['price'], tariff['photos']))
        
        refresh()
    
    def view_reports(self):
        """Просмотр отчетов"""
        data = self.load_data()
        total_sessions = len(data['sessions'])
        paid_sessions = len([s for s in data['sessions'] if s.get('paid', False)])
        total_revenue = sum([s.get('price', 0) for s in data['sessions'] if s.get('paid', False)])
        
        report = f"""
        === ОТЧЕТ ПО ФОТОСТУДИИ ===
        
        Всего фотосессий: {total_sessions}
        Оплаченных сессий: {paid_sessions}
        Общая выручка: {total_revenue} руб.
        Студий: {len(data['studios'])}
        Единиц оборудования: {len(data['equipment'])}
        """
        
        messagebox.showinfo("Отчет", report)
    
    # Функции фотографа
    
    def view_schedule(self):
        """Просмотр расписания"""
        win = tk.Toplevel(self.root)
        win.title("Расписание")
        win.geometry("800x400")
        
        tree = ttk.Treeview(win, columns=('id', 'date', 'time', 'client', 'studio', 'status'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('client', text='Клиент')
        tree.heading('studio', text='Студия')
        tree.heading('status', text='Статус')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        data = self.load_data()
        for session in data['sessions']:
            if session['photographer'] == self.current_user['username']:
                studio = next((s for s in data['studios'] if s['id'] == session['studio_id']), None)
                tree.insert('', 'end', values=(
                    session['id'],
                    session['date'],
                    session['time'],
                    session['client'],
                    studio['name'] if studio else 'N/A',
                    session['status']
                ))
    
    def create_session(self):
        """Создание фотосессии"""
        win = tk.Toplevel(self.root)
        win.title("Создание фотосессии")
        win.geometry("400x400")
        
        tk.Label(win, text="Клиент (логин):").grid(row=0, column=0, padx=10, pady=5)
        client = tk.Entry(win)
        client.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Дата (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        date = tk.Entry(win)
        date.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Время (HH:MM):").grid(row=2, column=0, padx=10, pady=5)
        time = tk.Entry(win)
        time.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Студия ID:").grid(row=3, column=0, padx=10, pady=5)
        studio_id = tk.Entry(win)
        studio_id.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Длительность (часов):").grid(row=4, column=0, padx=10, pady=5)
        duration = tk.Entry(win)
        duration.grid(row=4, column=1, padx=10, pady=5)
        
        def save():
            data = self.load_data()
            new_id = max([s['id'] for s in data['sessions']], default=0) + 1
            data['sessions'].append({
                'id': new_id,
                'client': client.get(),
                'photographer': self.current_user['username'],
                'studio_id': int(studio_id.get()),
                'date': date.get(),
                'time': time.get(),
                'duration': int(duration.get()),
                'status': 'Запланирована',
                'paid': False
            })
            self.save_data(data)
            messagebox.showinfo("Успех", "Фотосессия создана")
            win.destroy()
        
        tk.Button(win, text="Сохранить", command=save).grid(row=5, column=0, columnspan=2, pady=20)
    
    def edit_session(self):
        """Редактирование фотосессии"""
        win = tk.Toplevel(self.root)
        win.title("Редактирование фотосессии")
        win.geometry("600x400")
        
        tree = ttk.Treeview(win, columns=('id', 'date', 'client', 'status'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('date', text='Дата')
        tree.heading('client', text='Клиент')
        tree.heading('status', text='Статус')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        data = self.load_data()
        for session in data['sessions']:
            if session['photographer'] == self.current_user['username']:
                tree.insert('', 'end', values=(session['id'], session['date'], session['client'], session['status']))
        
        def change_status():
            selected = tree.selection()
            if selected:
                session_id = tree.item(selected[0])['values'][0]
                new_status = tk.simpledialog.askstring("Изменить статус", "Новый статус:")
                if new_status:
                    for session in data['sessions']:
                        if session['id'] == session_id:
                            session['status'] = new_status
                    self.save_data(data)
                    messagebox.showinfo("Успех", "Статус изменен")
                    win.destroy()
        
        tk.Button(win, text="Изменить статус", command=change_status).pack(pady=5)
    
    def view_clients(self):
        """Просмотр клиентов"""
        win = tk.Toplevel(self.root)
        win.title("Клиенты")
        win.geometry("600x400")
        
        tree = ttk.Treeview(win, columns=('username', 'full_name', 'sessions'), show='headings')
        tree.heading('username', text='Логин')
        tree.heading('full_name', text='ФИО')
        tree.heading('sessions', text='Сессий')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        data = self.load_data()
        clients = {}
        for session in data['sessions']:
            if session['photographer'] == self.current_user['username']:
                client = session['client']
                clients[client] = clients.get(client, 0) + 1
        
        for user in auth.get_all_users():
            if user['role'] == 'client' and user['username'] in clients:
                tree.insert('', 'end', values=(user['username'], user['full_name'], clients[user['username']]))
    
    # Функции клиента
    
    def book_session(self):
        """Бронирование фотосессии"""
        win = tk.Toplevel(self.root)
        win.title("Бронирование фотосессии")
        win.geometry("400x350")
        
        data = self.load_data()
        
        tk.Label(win, text="Выберите тариф:").grid(row=0, column=0, padx=10, pady=5)
        tariff_var = tk.StringVar()
        tariff_combo = ttk.Combobox(win, textvariable=tariff_var)
        tariff_combo['values'] = [f"{t['name']} - {t['price']} руб." for t in data['tariffs']]
        tariff_combo.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Выберите студию:").grid(row=1, column=0, padx=10, pady=5)
        studio_var = tk.StringVar()
        studio_combo = ttk.Combobox(win, textvariable=studio_var)
        studio_combo['values'] = [f"{s['name']} (ID: {s['id']})" for s in data['studios']]
        studio_combo.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        date = tk.Entry(win)
        date.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Время (HH:MM):").grid(row=3, column=0, padx=10, pady=5)
        time = tk.Entry(win)
        time.grid(row=3, column=1, padx=10, pady=5)
        
        def save():
            new_id = max([s['id'] for s in data['sessions']], default=0) + 1
            studio_text = studio_var.get()
            studio_id = int(studio_text.split('ID: ')[1].rstrip(')'))
            
            data['sessions'].append({
                'id': new_id,
                'client': self.current_user['username'],
                'photographer': 'photographer',
                'studio_id': studio_id,
                'date': date.get(),
                'time': time.get(),
                'duration': 2,
                'status': 'Ожидает подтверждения',
                'paid': False
            })
            self.save_data(data)
            messagebox.showinfo("Успех", "Бронирование создано")
            win.destroy()
        
        tk.Button(win, text="Забронировать", command=save).grid(row=4, column=0, columnspan=2, pady=20)
    
    def view_my_orders(self):
        """Просмотр заказов клиента"""
        win = tk.Toplevel(self.root)
        win.title("Мои заказы")
        win.geometry("800x400")
        
        tree = ttk.Treeview(win, columns=('id', 'date', 'time', 'studio', 'status', 'paid'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('studio', text='Студия')
        tree.heading('status', text='Статус')
        tree.heading('paid', text='Оплачено')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        data = self.load_data()
        for session in data['sessions']:
            if session['client'] == self.current_user['username']:
                studio = next((s for s in data['studios'] if s['id'] == session['studio_id']), None)
                tree.insert('', 'end', values=(
                    session['id'],
                    session['date'],
                    session['time'],
                    studio['name'] if studio else 'N/A',
                    session['status'],
                    'Да' if session.get('paid', False) else 'Нет'
                ))
    
    def payment(self):
        """Оплата услуг"""
        win = tk.Toplevel(self.root)
        win.title("Оплата услуг")
        win.geometry("600x400")
        
        tree = ttk.Treeview(win, columns=('id', 'date', 'status', 'paid'), show='headings')
        tree.heading('id', text='ID')
        tree.heading('date', text='Дата')
        tree.heading('status', text='Статус')
        tree.heading('paid', text='Оплачено')
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        data = self.load_data()
        for session in data['sessions']:
            if session['client'] == self.current_user['username']:
                tree.insert('', 'end', values=(
                    session['id'],
                    session['date'],
                    session['status'],
                    'Да' if session.get('paid', False) else 'Нет'
                ))
        
        def pay():
            selected = tree.selection()
            if selected:
                session_id = tree.item(selected[0])['values'][0]
                for session in data['sessions']:
                    if session['id'] == session_id:
                        session['paid'] = True
                self.save_data(data)
                messagebox.showinfo("Успех", "Оплата прошла успешно")
                win.destroy()
        
        tk.Button(win, text="Оплатить выбранную сессию", command=pay).pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = PhotoStudioApp(root)
    root.mainloop()