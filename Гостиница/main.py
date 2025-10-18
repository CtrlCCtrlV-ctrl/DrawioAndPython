import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from pathlib import Path
import auth

# Путь к файлу данных
DATA_FILE = Path(__file__).parent / 'data.json'


class HotelManagementSystem:
    """Главный класс информационной системы гостиницы"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ИС Гостиница")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.data = self.load_data()
        self.show_login_window()
    
    def load_data(self):
        """Загрузка данных из JSON"""
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self):
        """Сохранение данных в JSON"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна от всех виджетов"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        """Окно входа в систему"""
        self.clear_window()
        self.root.title("Вход в систему - ИС Гостиница")
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Информационная система", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(frame, text="ГОСТИНИЦА", font=('Arial', 14)).grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(frame, text="Логин:", font=('Arial', 10)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25, font=('Arial', 10))
        username_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 10)).grid(row=3, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, show='*', width=25, font=('Arial', 10))
        password_entry.grid(row=3, column=1, pady=5)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            user = auth.authenticate(username, password)
            if user:
                auth.set_current_user(user)
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login, width=20, bg='#4CAF50', fg='white', font=('Arial', 10)).grid(row=4, column=0, columnspan=2, pady=20)
        
        info_text = "Тестовые учетные записи:\nadmin/admin123\nmanager/manager123\nguest/guest123"
        tk.Label(frame, text=info_text, font=('Arial', 8), fg='gray', justify='left').grid(row=5, column=0, columnspan=2)
        
        username_entry.focus()
        password_entry.bind('<Return>', lambda e: login())
    
    def show_main_menu(self):
        """Главное меню системы"""
        self.clear_window()
        user = auth.get_current_user()
        self.root.title(f"ИС Гостиница - {user['full_name']} ({user['role']})")
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text="ИНФОРМАЦИОННАЯ СИСТЕМА ГОСТИНИЦА", 
                bg='#2196F3', fg='white', font=('Arial', 16, 'bold')).pack(side='left', padx=20, pady=15)
        
        tk.Button(top_frame, text="Выход", command=self.logout, 
                 bg='#f44336', fg='white', font=('Arial', 10)).pack(side='right', padx=20)
        
        tk.Label(top_frame, text=f"Пользователь: {user['full_name']}", 
                bg='#2196F3', fg='white', font=('Arial', 10)).pack(side='right', padx=10)
        
        # Боковое меню
        menu_frame = tk.Frame(self.root, bg='#f5f5f5', width=200)
        menu_frame.pack(side='left', fill='y')
        menu_frame.pack_propagate(False)
        
        # Основная область
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Кнопки меню в зависимости от роли
        if user['role'] == 'administrator':
            self.create_menu_button(menu_frame, "👤 Пользователи", self.show_users_management)
            self.create_menu_button(menu_frame, "🏠 Номера", self.show_rooms_management)
            self.create_menu_button(menu_frame, "📊 Статистика", self.show_statistics)
            self.create_menu_button(menu_frame, "📋 Все бронирования", self.show_all_bookings)
            self.create_menu_button(menu_frame, "👥 Гости", self.show_guests_management)
        
        elif user['role'] == 'manager':
            self.create_menu_button(menu_frame, "📋 Бронирования", self.show_bookings_management)
            self.create_menu_button(menu_frame, "✅ Регистрация заезда", self.show_check_in)
            self.create_menu_button(menu_frame, "❌ Регистрация выезда", self.show_check_out)
            self.create_menu_button(menu_frame, "👥 Гости", self.show_guests_management)
            self.create_menu_button(menu_frame, "🔍 Поиск", self.show_search)
            self.create_menu_button(menu_frame, "🏠 Номера", self.show_rooms_view)
        
        elif user['role'] == 'guest':
            self.create_menu_button(menu_frame, "🏠 Доступные номера", self.show_available_rooms)
            self.create_menu_button(menu_frame, "➕ Создать бронирование", self.show_create_booking)
            self.create_menu_button(menu_frame, "📋 Мои бронирования", self.show_my_bookings)
        
        self.show_dashboard()
    
    def create_menu_button(self, parent, text, command):
        """Создание кнопки меню"""
        btn = tk.Button(parent, text=text, command=command, 
                       bg='#f5f5f5', relief='flat', anchor='w',
                       font=('Arial', 10), padx=20, pady=12)
        btn.pack(fill='x', pady=2)
        btn.bind('<Enter>', lambda e: btn.config(bg='#e0e0e0'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#f5f5f5'))
    
    def show_dashboard(self):
        """Панель управления (главный экран)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        user = auth.get_current_user()
        
        tk.Label(self.content_frame, text="Панель управления", 
                font=('Arial', 18, 'bold'), bg='white').pack(pady=20)
        
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=20)
        
        # Статистика
        total_rooms = len(self.data['rooms'])
        available_rooms = len([r for r in self.data['rooms'] if r['status'] == 'available'])
        total_bookings = len(self.data['bookings'])
        total_guests = len(self.data['guests'])
        
        self.create_stat_card(stats_frame, "Всего номеров", total_rooms, 0, 0, '#2196F3')
        self.create_stat_card(stats_frame, "Доступно", available_rooms, 0, 1, '#4CAF50')
        self.create_stat_card(stats_frame, "Бронирований", total_bookings, 1, 0, '#FF9800')
        self.create_stat_card(stats_frame, "Гостей", total_guests, 1, 1, '#9C27B0')
        
        # Приветствие
        welcome_text = f"Добро пожаловать, {user['full_name']}!\n\nВаша роль: {self.get_role_name(user['role'])}"
        tk.Label(self.content_frame, text=welcome_text, 
                font=('Arial', 12), bg='white', fg='#666').pack(pady=30)
    
    def create_stat_card(self, parent, title, value, row, col, color):
        """Создание карточки статистики"""
        card = tk.Frame(parent, bg=color, width=150, height=100)
        card.grid(row=row, column=col, padx=10, pady=10)
        card.pack_propagate(False)
        
        tk.Label(card, text=str(value), font=('Arial', 28, 'bold'), 
                bg=color, fg='white').pack(expand=True)
        tk.Label(card, text=title, font=('Arial', 10), 
                bg=color, fg='white').pack()
    
    def get_role_name(self, role):
        """Получение названия роли на русском"""
        roles = {
            'administrator': 'Администратор',
            'manager': 'Менеджер',
            'guest': 'Гость'
        }
        return roles.get(role, role)
    
    # === УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ (Администратор) ===
    
    def show_users_management(self):
        """Управление пользователями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление пользователями", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Кнопки действий
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Добавить пользователя", 
                 command=self.add_user_dialog, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Удалить", 
                 command=lambda: self.delete_selected_user(tree), bg='#f44336', fg='white').pack(side='left', padx=5)
        
        # Таблица пользователей
        columns = ('Логин', 'Имя', 'Роль', 'Дата создания')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Загрузка данных
        for user in auth.get_all_users():
            tree.insert('', 'end', values=(
                user['username'],
                user['full_name'],
                self.get_role_name(user['role']),
                user['created']
            ))
    
    def add_user_dialog(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="Новый пользователь", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(dialog)
        frame.pack(pady=20, padx=20)
        
        tk.Label(frame, text="Логин:").grid(row=0, column=0, sticky='e', pady=5, padx=5)
        username_entry = tk.Entry(frame, width=25)
        username_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=1, column=0, sticky='e', pady=5, padx=5)
        password_entry = tk.Entry(frame, show='*', width=25)
        password_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Полное имя:").grid(row=2, column=0, sticky='e', pady=5, padx=5)
        fullname_entry = tk.Entry(frame, width=25)
        fullname_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="Роль:").grid(row=3, column=0, sticky='e', pady=5, padx=5)
        role_var = tk.StringVar(value="guest")
        role_combo = ttk.Combobox(frame, textvariable=role_var, width=22, state='readonly')
        role_combo['values'] = ('administrator', 'manager', 'guest')
        role_combo.grid(row=3, column=1, pady=5)
        
        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            role = role_var.get()
            
            if not username or not password or not fullname:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = auth.create_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
                self.show_users_management()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(dialog, text="Сохранить", command=save_user, 
                 bg='#4CAF50', fg='white', width=15).pack(pady=10)
    
    def delete_selected_user(self, tree):
        """Удаление выбранного пользователя"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        item = tree.item(selected[0])
        username = item['values'][0]
        
        if username == 'admin':
            messagebox.showerror("Ошибка", "Нельзя удалить главного администратора")
            return
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            auth.delete_user(username)
            self.show_users_management()
    
    # === УПРАВЛЕНИЕ НОМЕРАМИ ===
    
    def show_rooms_management(self):
        """Управление номерами (администратор)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление номерами", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Добавить номер", 
                 command=self.add_room_dialog, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="✏️ Редактировать", 
                 command=lambda: self.edit_room_dialog(tree), bg='#2196F3', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Удалить", 
                 command=lambda: self.delete_room(tree), bg='#f44336', fg='white').pack(side='left', padx=5)
        
        columns = ('ID', 'Номер', 'Тип', 'Цена', 'Статус', 'Этаж')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        for room in self.data['rooms']:
            status_text = 'Доступен' if room['status'] == 'available' else 'Занят'
            tree.insert('', 'end', values=(
                room['id'],
                room['number'],
                room['type'],
                f"{room['price']} ₽",
                status_text,
                room['floor']
            ))
    
    def add_room_dialog(self):
        """Диалог добавления номера"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить номер")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="Новый номер", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(dialog)
        frame.pack(pady=20, padx=20)
        
        fields = [
            ("Номер:", tk.Entry(frame, width=25)),
            ("Тип:", ttk.Combobox(frame, width=22, state='readonly', values=['Одноместный', 'Двухместный', 'Люкс', 'Апартаменты'])),
            ("Цена (₽):", tk.Entry(frame, width=25)),
            ("Этаж:", tk.Entry(frame, width=25)),
            ("Описание:", tk.Entry(frame, width=25))
        ]
        
        entries = {}
        for i, (label, widget) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='e', pady=5, padx=5)
            widget.grid(row=i, column=1, pady=5)
            entries[label] = widget
        
        def save_room():
            try:
                number = entries["Номер:"].get().strip()
                room_type = entries["Тип:"].get().strip()
                price = int(entries["Цена (₽):"].get().strip())
                floor = int(entries["Этаж:"].get().strip())
                description = entries["Описание:"].get().strip()
                
                if not number or not room_type:
                    messagebox.showerror("Ошибка", "Заполните обязательные поля")
                    return
                
                new_id = f"R{str(len(self.data['rooms']) + 1).zfill(3)}"
                new_room = {
                    "id": new_id,
                    "number": number,
                    "type": room_type,
                    "price": price,
                    "status": "available",
                    "floor": floor,
                    "description": description
                }
                
                self.data['rooms'].append(new_room)
                self.save_data()
                messagebox.showinfo("Успех", "Номер добавлен")
                dialog.destroy()
                self.show_rooms_management()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте корректность данных")
        
        tk.Button(dialog, text="Сохранить", command=save_room, 
                 bg='#4CAF50', fg='white', width=15).pack(pady=10)
    
    def edit_room_dialog(self, tree):
        """Диалог редактирования номера"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите номер")
            return
        
        item = tree.item(selected[0])
        room_id = item['values'][0]
        room = next((r for r in self.data['rooms'] if r['id'] == room_id), None)
        
        if not room:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать номер")
        dialog.geometry("400x350")
        
        tk.Label(dialog, text="Редактирование номера", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(dialog)
        frame.pack(pady=20, padx=20)
        
        tk.Label(frame, text="Номер:").grid(row=0, column=0, sticky='e', pady=5)
        number_entry = tk.Entry(frame, width=25)
        number_entry.insert(0, room['number'])
        number_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Цена (₽):").grid(row=1, column=0, sticky='e', pady=5)
        price_entry = tk.Entry(frame, width=25)
        price_entry.insert(0, room['price'])
        price_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Статус:").grid(row=2, column=0, sticky='e', pady=5)
        status_var = tk.StringVar(value=room['status'])
        status_combo = ttk.Combobox(frame, textvariable=status_var, width=22, state='readonly')
        status_combo['values'] = ('available', 'occupied', 'maintenance')
        status_combo.grid(row=2, column=1, pady=5)
        
        def save_changes():
            try:
                room['number'] = number_entry.get().strip()
                room['price'] = int(price_entry.get().strip())
                room['status'] = status_var.get()
                self.save_data()
                messagebox.showinfo("Успех", "Изменения сохранены")
                dialog.destroy()
                self.show_rooms_management()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте корректность данных")
        
        tk.Button(dialog, text="Сохранить", command=save_changes, 
                 bg='#4CAF50', fg='white', width=15).pack(pady=10)
    
    def delete_room(self, tree):
        """Удаление номера"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите номер")
            return
        
        item = tree.item(selected[0])
        room_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить номер?"):
            self.data['rooms'] = [r for r in self.data['rooms'] if r['id'] != room_id]
            self.save_data()
            self.show_rooms_management()
    
    # === СТАТИСТИКА ===
    
    def show_statistics(self):
        """Показать статистику"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Статистика системы", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=20)
        
        total_rooms = len(self.data['rooms'])
        available_rooms = len([r for r in self.data['rooms'] if r['status'] == 'available'])
        occupied_rooms = len([r for r in self.data['rooms'] if r['status'] == 'occupied'])
        total_bookings = len(self.data['bookings'])
        confirmed_bookings = len([b for b in self.data['bookings'] if b['status'] == 'confirmed'])
        total_revenue = sum(b['total_price'] for b in self.data['bookings'] if b['status'] == 'confirmed')
        
        stats = [
            ("Всего номеров:", total_rooms),
            ("Доступных номеров:", available_rooms),
            ("Занятых номеров:", occupied_rooms),
            ("Всего бронирований:", total_bookings),
            ("Подтвержденных бронирований:", confirmed_bookings),
            ("Общая выручка:", f"{total_revenue} ₽")
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=('Arial', 12, 'bold'), 
                    bg='white', anchor='w', width=30).grid(row=i, column=0, pady=5, sticky='w')
            tk.Label(stats_frame, text=str(value), font=('Arial', 12), 
                    bg='white', anchor='e', width=20).grid(row=i, column=1, pady=5, sticky='e')
    
    # === БРОНИРОВАНИЯ ===
    
    def show_all_bookings(self):
        """Показать все бронирования (для администратора)"""
        self.show_bookings_management()
    
    def show_bookings_management(self):
        """Управление бронированиями (менеджер)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление бронированиями", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Новое бронирование", 
                 command=self.add_booking_dialog, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Отменить", 
                 command=lambda: self.cancel_booking(tree), bg='#f44336', fg='white').pack(side='left', padx=5)
        
        columns = ('ID', 'Номер', 'Гость', 'Заезд', 'Выезд', 'Статус', 'Сумма')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        for booking in self.data['bookings']:
            room = next((r for r in self.data['rooms'] if r['id'] == booking['room_id']), None)
            guest = next((g for g in self.data['guests'] if g['id'] == booking['guest_id']), None)
            
            tree.insert('', 'end', values=(
                booking['id'],
                room['number'] if room else 'N/A',
                guest['full_name'] if guest else 'N/A',
                booking['check_in'],
                booking['check_out'],
                booking['status'],
                f"{booking['total_price']} ₽"
            ))
    
    def add_booking_dialog(self):
        """Диалог создания бронирования"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новое бронирование")
        dialog.geometry("450x450")
        
        tk.Label(dialog, text="Создание бронирования", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(dialog)
        frame.pack(pady=20, padx=20)
        
        tk.Label(frame, text="Номер:").grid(row=0, column=0, sticky='e', pady=5)
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(frame, textvariable=room_var, width=25, state='readonly')
        available_rooms = [r for r in self.data['rooms'] if r['status'] == 'available']
        room_combo['values'] = [f"{r['number']} - {r['type']} ({r['price']}₽)" for r in available_rooms]
        room_combo.grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Гость:").grid(row=1, column=0, sticky='e', pady=5)
        guest_var = tk.StringVar()
        guest_combo = ttk.Combobox(frame, textvariable=guest_var, width=25, state='readonly')
        guest_combo['values'] = [g['full_name'] for g in self.data['guests']]
        guest_combo.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Дата заезда:").grid(row=2, column=0, sticky='e', pady=5)
        checkin_entry = tk.Entry(frame, width=27)
        checkin_entry.insert(0, "2024-02-01")
        checkin_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="Дата выезда:").grid(row=3, column=0, sticky='e', pady=5)
        checkout_entry = tk.Entry(frame, width=27)
        checkout_entry.insert(0, "2024-02-05")
        checkout_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(frame, text="(Формат: YYYY-MM-DD)", font=('Arial', 8), fg='gray').grid(row=4, column=1, sticky='w')
        
        def save_booking():
            if not room_var.get() or not guest_var.get():
                messagebox.showerror("Ошибка", "Выберите номер и гостя")
                return
            
            room_idx = room_combo.current()
            guest_idx = guest_combo.current()
            
            room = available_rooms[room_idx]
            guest = self.data['guests'][guest_idx]
            
            try:
                check_in = checkin_entry.get().strip()
                check_out = checkout_entry.get().strip()
                
                # Расчет количества дней
                from datetime import datetime
                d1 = datetime.strptime(check_in, "%Y-%m-%d")
                d2 = datetime.strptime(check_out, "%Y-%m-%d")
                days = (d2 - d1).days
                
                if days <= 0:
                    messagebox.showerror("Ошибка", "Некорректные даты")
                    return
                
                total_price = room['price'] * days
                
                new_id = f"B{str(len(self.data['bookings']) + 1).zfill(3)}"
                new_booking = {
                    "id": new_id,
                    "room_id": room['id'],
                    "guest_id": guest['id'],
                    "check_in": check_in,
                    "check_out": check_out,
                    "status": "confirmed",
                    "total_price": total_price,
                    "created": datetime.now().strftime("%Y-%m-%d"),
                    "created_by": auth.get_current_user()['username']
                }
                
                self.data['bookings'].append(new_booking)
                
                # Обновление статуса номера
                room['status'] = 'occupied'
                
                self.save_data()
                messagebox.showinfo("Успех", f"Бронирование создано!\nСумма: {total_price} ₽")
                dialog.destroy()
                self.show_bookings_management()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка создания бронирования: {str(e)}")
        
        tk.Button(dialog, text="Создать бронирование", command=save_booking, 
                 bg='#4CAF50', fg='white', width=20).pack(pady=20)
    
    def cancel_booking(self, tree):
        """Отмена бронирования"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите бронирование")
            return
        
        item = tree.item(selected[0])
        booking_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Отменить бронирование?"):
            booking = next((b for b in self.data['bookings'] if b['id'] == booking_id), None)
            if booking:
                booking['status'] = 'cancelled'
                # Освобождение номера
                room = next((r for r in self.data['rooms'] if r['id'] == booking['room_id']), None)
                if room:
                    room['status'] = 'available'
                self.save_data()
                self.show_bookings_management()
    
    # === ГОСТИ ===
    
    def show_guests_management(self):
        """Управление гостями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление гостями", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Добавить гостя", 
                 command=self.add_guest_dialog, bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        columns = ('ID', 'ФИО', 'Паспорт', 'Телефон', 'Email', 'Дата регистрации')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        for guest in self.data['guests']:
            tree.insert('', 'end', values=(
                guest['id'],
                guest['full_name'],
                guest['passport'],
                guest['phone'],
                guest['email'],
                guest['created']
            ))
    
    def add_guest_dialog(self):
        """Диалог добавления гостя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить гостя")
        dialog.geometry("400x350")
        
        tk.Label(dialog, text="Регистрация гостя", font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame = tk.Frame(dialog)
        frame.pack(pady=20, padx=20)
        
        fields = [
            ("ФИО:", tk.Entry(frame, width=30)),
            ("Паспорт:", tk.Entry(frame, width=30)),
            ("Телефон:", tk.Entry(frame, width=30)),
            ("Email:", tk.Entry(frame, width=30))
        ]
        
        entries = {}
        for i, (label, widget) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky='e', pady=5, padx=5)
            widget.grid(row=i, column=1, pady=5)
            entries[label] = widget
        
        def save_guest():
            full_name = entries["ФИО:"].get().strip()
            passport = entries["Паспорт:"].get().strip()
            phone = entries["Телефон:"].get().strip()
            email = entries["Email:"].get().strip()
            
            if not full_name or not passport:
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            new_id = f"G{str(len(self.data['guests']) + 1).zfill(3)}"
            new_guest = {
                "id": new_id,
                "full_name": full_name,
                "passport": passport,
                "phone": phone,
                "email": email,
                "created": datetime.now().strftime("%Y-%m-%d")
            }
            
            self.data['guests'].append(new_guest)
            self.save_data()
            messagebox.showinfo("Успех", "Гость добавлен")
            dialog.destroy()
            self.show_guests_management()
        
        tk.Button(dialog, text="Сохранить", command=save_guest, 
                 bg='#4CAF50', fg='white', width=15).pack(pady=10)
    
    # === РЕГИСТРАЦИЯ ЗАЕЗДА/ВЫЕЗДА ===
    
    def show_check_in(self):
        """Регистрация заезда"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Регистрация заезда", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        pending_bookings = [b for b in self.data['bookings'] if b['status'] == 'confirmed']
        
        if not pending_bookings:
            tk.Label(self.content_frame, text="Нет подтвержденных бронирований для заезда", 
                    font=('Arial', 12), bg='white', fg='gray').pack(pady=50)
            return
        
        columns = ('ID', 'Номер', 'Гость', 'Дата заезда', 'Дата выезда')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        for booking in pending_bookings:
            room = next((r for r in self.data['rooms'] if r['id'] == booking['room_id']), None)
            guest = next((g for g in self.data['guests'] if g['id'] == booking['guest_id']), None)
            
            tree.insert('', 'end', values=(
                booking['id'],
                room['number'] if room else 'N/A',
                guest['full_name'] if guest else 'N/A',
                booking['check_in'],
                booking['check_out']
            ))
        
        def confirm_checkin():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите бронирование")
                return
            
            item = tree.item(selected[0])
            booking_id = item['values'][0]
            booking = next((b for b in self.data['bookings'] if b['id'] == booking_id), None)
            
            if booking:
                booking['status'] = 'checked_in'
                self.save_data()
                messagebox.showinfo("Успех", "Заезд зарегистрирован")
                self.show_check_in()
        
        tk.Button(self.content_frame, text="✅ Подтвердить заезд", command=confirm_checkin,
                 bg='#4CAF50', fg='white', font=('Arial', 11)).pack(pady=10)
    
    def show_check_out(self):
        """Регистрация выезда"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Регистрация выезда", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        active_bookings = [b for b in self.data['bookings'] if b['status'] == 'checked_in']
        
        if not active_bookings:
            tk.Label(self.content_frame, text="Нет активных бронирований", 
                    font=('Arial', 12), bg='white', fg='gray').pack(pady=50)
            return
        
        columns = ('ID', 'Номер', 'Гость', 'Дата выезда', 'Сумма')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        for booking in active_bookings:
            room = next((r for r in self.data['rooms'] if r['id'] == booking['room_id']), None)
            guest = next((g for g in self.data['guests'] if g['id'] == booking['guest_id']), None)
            
            tree.insert('', 'end', values=(
                booking['id'],
                room['number'] if room else 'N/A',
                guest['full_name'] if guest else 'N/A',
                booking['check_out'],
                f"{booking['total_price']} ₽"
            ))
        
        def confirm_checkout():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите бронирование")
                return
            
            item = tree.item(selected[0])
            booking_id = item['values'][0]
            booking = next((b for b in self.data['bookings'] if b['id'] == booking_id), None)
            
            if booking:
                booking['status'] = 'completed'
                # Освобождение номера
                room = next((r for r in self.data['rooms'] if r['id'] == booking['room_id']), None)
                if room:
                    room['status'] = 'available'
                self.save_data()
                messagebox.showinfo("Успех", f"Выезд оформлен\nК оплате: {booking['total_price']} ₽")
                self.show_check_out()
        
        tk.Button(self.content_frame, text="✅ Подтвердить выезд", command=confirm_checkout,
                 bg='#f44336', fg='white', font=('Arial', 11)).pack(pady=10)
    
    # === ПОИСК ===
    
    def show_search(self):
        """Поиск бронирований"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Поиск бронирований", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск по ФИО гостя:", bg='white').pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side='left', padx=5)
        
        columns = ('ID', 'Номер', 'Гость', 'Заезд', 'Выезд', 'Статус')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        def do_search():
            query = search_entry.get().strip().lower()
            tree.delete(*tree.get_children())
            
            for booking in self.data['bookings']:
                guest = next((g for g in self.data['guests'] if g['id'] == booking['guest_id']), None)
                if guest and query in guest['full_name'].lower():
                    room = next((r for r in self.data['rooms'] if r['id'] == booking['room_id']), None)
                    tree.insert('', 'end', values=(
                        booking['id'],
                        room['number'] if room else 'N/A',
                        guest['full_name'],
                        booking['check_in'],
                        booking['check_out'],
                        booking['status']
                    ))
        
        tk.Button(search_frame, text="🔍 Найти", command=do_search, 
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
    
    # === ПРОСМОТР НОМЕРОВ (для гостя) ===
    
    def show_rooms_view(self):
        """Просмотр номеров (менеджер)"""
        self.show_available_rooms()
    
    def show_available_rooms(self):
        """Просмотр доступных номеров (гость)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Доступные номера", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        available = [r for r in self.data['rooms'] if r['status'] == 'available']
        
        if not available:
            tk.Label(self.content_frame, text="Нет доступных номеров", 
                    font=('Arial', 12), bg='white', fg='gray').pack(pady=50)
            return
        
        # Карточки номеров
        canvas = tk.Canvas(self.content_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, room in enumerate(available):
            card = tk.Frame(scrollable_frame, bg='#f9f9f9', relief='solid', borderwidth=1)
            card.pack(pady=10, padx=20, fill='x')
            
            tk.Label(card, text=f"Номер {room['number']}", font=('Arial', 14, 'bold'), 
                    bg='#f9f9f9').pack(anchor='w', padx=10, pady=5)
            tk.Label(card, text=f"Тип: {room['type']}", font=('Arial', 11), 
                    bg='#f9f9f9').pack(anchor='w', padx=10)
            tk.Label(card, text=f"Цена: {room['price']} ₽/сутки", font=('Arial', 11), 
                    bg='#f9f9f9', fg='green').pack(anchor='w', padx=10)
            tk.Label(card, text=f"Этаж: {room['floor']}", font=('Arial', 10), 
                    bg='#f9f9f9').pack(anchor='w', padx=10)
            tk.Label(card, text=room['description'], font=('Arial', 9), 
                    bg='#f9f9f9', fg='gray').pack(anchor='w', padx=10, pady=(0, 5))
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
    
    # === СОЗДАНИЕ БРОНИРОВАНИЯ (гость) ===
    
    def show_create_booking(self):
        """Создание бронирования (гость)"""
        self.add_booking_dialog()
    
    def show_my_bookings(self):
        """Мои бронирования (гость)"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои бронирования", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        user = auth.get_current_user()
        my_bookings = [b for b in self.data['bookings'] if b.get('created_by') == user['username']]
        
        if not my_bookings:
            tk.Label(self.content_frame, text="У вас пока нет бронирований", 
                    font=('Arial', 12), bg='white', fg='gray').pack(pady=50)
            return
        
        columns = ('ID', 'Номер', 'Заезд', 'Выезд', 'Статус', 'Сумма')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=20, fill='both', expand=True)
        
        for booking in my_bookings:
            room = next((r for r in self.data['rooms'] if r['id'] == booking['room_id']), None)
            
            tree.insert('', 'end', values=(
                booking['id'],
                room['number'] if room else 'N/A',
                booking['check_in'],
                booking['check_out'],
                booking['status'],
                f"{booking['total_price']} ₽"
            ))
    
    def logout(self):
        """Выход из системы"""
        auth.logout()
        self.show_login_window()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


if __name__ == "__main__":
    app = HotelManagementSystem()
    app.run()