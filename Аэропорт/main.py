import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import AuthManager, get_current_user, logout_user

class AirportSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Информационная система Аэропорт")
        self.root.geometry("1000x600")
        
        
        # Менеджер аутентификации
        self.auth_manager = AuthManager()
        
        # Показ окна входа
        self.show_login_window()
        
    
    def show_login_window(self):
        """Окно авторизации"""
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Фрейм для входа
        login_frame = tk.Frame(self.root)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(login_frame, text="Вход в систему", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(login_frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.login_entry = tk.Entry(login_frame, width=20)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = tk.Entry(login_frame, width=20, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(login_frame, text="Войти", command=self.login, width=15).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Информация о тестовых пользователях
        info_text = "Тестовые пользователи:\nadmin/admin123 - Администратор\ndispatcher/disp123 - Диспетчер\nuser/user123 - Пассажир"
        tk.Label(login_frame, text=info_text, font=("Arial", 9), fg="gray").grid(row=4, column=0, columnspan=2, pady=10)
        
    def login(self):
        """Обработка входа"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
            
        if self.auth_manager.login(username, password):
            user = get_current_user()
            self.show_main_window(user['role'])
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_main_window(self, role):
        """Главное окно в зависимости от роли"""
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_frame.pack(fill='x')
        
        user = get_current_user()
        tk.Label(top_frame, text=f"Пользователь: {user['username']} ({self.get_role_name(role)})", 
                bg='#2c3e50', fg='white', font=("Arial", 10)).pack(side='left', padx=10, pady=10)
        
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side='right', padx=10, pady=10)
        
        # Главный контейнер
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        # Меню слева
        menu_frame = tk.Frame(main_container, bg='#34495e', width=200)
        menu_frame.pack(side='left', fill='y')
        
        # Контент справа
        self.content_frame = tk.Frame(main_container, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Создание меню в зависимости от роли
        if role == 'admin':
            self.create_admin_menu(menu_frame)
        elif role == 'dispatcher':
            self.create_dispatcher_menu(menu_frame)
        else:
            self.create_passenger_menu(menu_frame)
    
    def get_role_name(self, role):
        """Получение названия роли на русском"""
        roles = {
            'admin': 'Администратор',
            'dispatcher': 'Диспетчер', 
            'passenger': 'Пассажир'
        }
        return roles.get(role, role)
    
    def create_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="МЕНЮ", bg='#34495e', fg='white', font=("Arial", 12, "bold")).pack(pady=10)
        
        buttons = [
            ("Управление рейсами", self.manage_flights),
            ("Управление персоналом", self.manage_staff),
            ("Статистика", self.show_statistics),
            ("Настройки системы", self.system_settings),
            ("Все билеты", self.show_all_tickets)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, command=command, width=20, bg='#3498db', fg='white').pack(pady=5)
    
    def create_dispatcher_menu(self, parent):
        """Меню диспетчера"""
        tk.Label(parent, text="МЕНЮ", bg='#34495e', fg='white', font=("Arial", 12, "bold")).pack(pady=10)
        
        buttons = [
            ("Регистрация рейсов", self.register_flight),
            ("Статус рейсов", self.change_flight_status),
            ("Управление посадкой", self.manage_boarding),
            ("Расписание", self.view_schedule)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, command=command, width=20, bg='#27ae60', fg='white').pack(pady=5)
    
    def create_passenger_menu(self, parent):
        """Меню пассажира"""
        tk.Label(parent, text="МЕНЮ", bg='#34495e', fg='white', font=("Arial", 12, "bold")).pack(pady=10)
        
        buttons = [
            ("Расписание рейсов", self.view_schedule),
            ("Купить билет", self.buy_ticket),
            ("Мои билеты", self.my_tickets),
            ("Регистрация на рейс", self.check_in)
        ]
        
        for text, command in buttons:
            tk.Button(parent, text=text, command=command, width=20, bg='#e67e22', fg='white').pack(pady=5)
    
    def clear_content(self):
        """Очистка области контента"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def manage_flights(self):
        """Управление рейсами (админ)"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Управление рейсами", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблица рейсов
        columns = ('ID', 'Номер', 'Откуда', 'Куда', 'Вылет', 'Прилет', 'Статус', 'Выход')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=10)
        
        # Загрузка данных
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for flight in data['flights']:
            tree.insert('', 'end', values=(
                flight['id'], flight['number'], flight['from'], flight['to'],
                flight['departure'], flight['arrival'], flight['status'], flight['gate']
            ))
        
        # Кнопки управления
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить рейс", command=lambda: self.add_flight_dialog()).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить рейс", command=lambda: self.delete_flight(tree)).pack(side='left', padx=5)
    
    def add_flight_dialog(self):
        """Диалог добавления рейса"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить рейс")
        dialog.geometry("300x300")
        
        fields = [
            ("Номер рейса:", tk.Entry(dialog)),
            ("Откуда:", tk.Entry(dialog)),
            ("Куда:", tk.Entry(dialog)),
            ("Время вылета:", tk.Entry(dialog)),
            ("Время прилета:", tk.Entry(dialog)),
            ("Выход:", tk.Entry(dialog))
        ]
        
        for i, (label, entry) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry.grid(row=i, column=1, padx=5, pady=5)
        
        def save_flight():
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            new_flight = {
                "id": max([f['id'] for f in data['flights']], default=0) + 1,
                "number": fields[0][1].get(),
                "from": fields[1][1].get(),
                "to": fields[2][1].get(),
                "departure": fields[3][1].get(),
                "arrival": fields[4][1].get(),
                "status": "По расписанию",
                "gate": fields[5][1].get()
            }
            
            data['flights'].append(new_flight)
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", "Рейс добавлен")
            dialog.destroy()
            self.manage_flights()
        
        tk.Button(dialog, text="Сохранить", command=save_flight).grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    def delete_flight(self, tree):
        """Удаление выбранного рейса"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите рейс для удаления")
            return
        
        item = tree.item(selection[0])
        flight_id = item['values'][0]
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data['flights'] = [f for f in data['flights'] if f['id'] != flight_id]
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Успех", "Рейс удален")
        self.manage_flights()
    
    def manage_staff(self):
        """Управление персоналом"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Управление персоналом", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблица персонала
        columns = ('ID', 'ФИО', 'Должность', 'Смена')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10)
        
        # Загрузка данных
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for staff in data['staff']:
            tree.insert('', 'end', values=(
                staff['id'], staff['name'], staff['position'], staff['shift']
            ))
    
    def show_statistics(self):
        """Показ статистики"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Статистика системы", font=("Arial", 14, "bold")).pack(pady=10)
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stats_frame = tk.Frame(self.content_frame)
        stats_frame.pack(pady=20)
        
        stats = [
            ("Всего рейсов:", len(data['flights'])),
            ("Проданных билетов:", len(data['tickets'])),
            ("Сотрудников:", len(data['staff'])),
            ("Активных рейсов:", len([f for f in data['flights'] if f['status'] == 'По расписанию']))
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=("Arial", 12)).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            tk.Label(stats_frame, text=str(value), font=("Arial", 12, "bold")).grid(row=i, column=1, sticky='w', padx=10, pady=5)
    
    def system_settings(self):
        """Настройки системы"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Настройки системы", font=("Arial", 14, "bold")).pack(pady=10)
        
        settings_frame = tk.Frame(self.content_frame)
        settings_frame.pack(pady=20)
        
        tk.Label(settings_frame, text="Настройки аэропорта").pack(pady=5)
        tk.Label(settings_frame, text="Название: Международный аэропорт").pack(pady=5)
        tk.Label(settings_frame, text="Код IATA: DME").pack(pady=5)
        tk.Label(settings_frame, text="Часовой пояс: UTC+3").pack(pady=5)
    
    def register_flight(self):
        """Регистрация нового рейса (диспетчер)"""
        self.add_flight_dialog()
    
    def change_flight_status(self):
        """Изменение статуса рейса"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Изменение статуса рейсов", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблица рейсов
        columns = ('ID', 'Номер', 'Статус')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10)
        
        # Загрузка данных
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for flight in data['flights']:
            tree.insert('', 'end', values=(flight['id'], flight['number'], flight['status']))
        
        # Выбор нового статуса
        status_frame = tk.Frame(self.content_frame)
        status_frame.pack(pady=10)
        
        tk.Label(status_frame, text="Новый статус:").pack(side='left', padx=5)
        
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(status_frame, textvariable=status_var, width=20)
        status_combo['values'] = ('По расписанию', 'Задерживается', 'Посадка', 'Вылетел', 'Отменен')
        status_combo.pack(side='left', padx=5)
        
        def update_status():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Предупреждение", "Выберите рейс")
                return
            
            if not status_var.get():
                messagebox.showwarning("Предупреждение", "Выберите статус")
                return
            
            item = tree.item(selection[0])
            flight_id = item['values'][0]
            
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for flight in data['flights']:
                if flight['id'] == flight_id:
                    flight['status'] = status_var.get()
                    break
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", "Статус обновлен")
            self.change_flight_status()
        
        tk.Button(status_frame, text="Обновить", command=update_status).pack(side='left', padx=5)
    
    def manage_boarding(self):
        """Управление посадкой"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Управление посадкой", font=("Arial", 14, "bold")).pack(pady=10)
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for flight in data['flights']:
            if flight['status'] in ['По расписанию', 'Посадка']:
                frame = tk.Frame(self.content_frame, relief='ridge', borderwidth=1)
                frame.pack(pady=5, padx=10, fill='x')
                
                tk.Label(frame, text=f"Рейс {flight['number']}: {flight['from']} - {flight['to']}").pack(side='left', padx=10)
                tk.Label(frame, text=f"Выход: {flight['gate']}").pack(side='left', padx=10)
                tk.Button(frame, text="Начать посадку" if flight['status'] != 'Посадка' else "Завершить посадку",
                         command=lambda f=flight: self.toggle_boarding(f)).pack(side='right', padx=10)
    
    def toggle_boarding(self, flight):
        """Переключение статуса посадки"""
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for f in data['flights']:
            if f['id'] == flight['id']:
                f['status'] = 'Посадка' if f['status'] == 'По расписанию' else 'Вылетел'
                break
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.manage_boarding()
    
    def view_schedule(self):
        """Просмотр расписания"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Расписание рейсов", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблица рейсов
        columns = ('Номер', 'Откуда', 'Куда', 'Вылет', 'Прилет', 'Статус')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10)
        
        # Загрузка данных
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for flight in data['flights']:
            tree.insert('', 'end', values=(
                flight['number'], flight['from'], flight['to'],
                flight['departure'], flight['arrival'], flight['status']
            ))
    
    def buy_ticket(self):
        """Покупка билета"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Покупка билета", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Форма покупки
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tk.Label(form_frame, text="Выберите рейс:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        
        flight_var = tk.StringVar()
        flight_combo = ttk.Combobox(form_frame, textvariable=flight_var, width=30)
        flight_combo['values'] = [f"{f['number']}: {f['from']} - {f['to']}" for f in data['flights']]
        flight_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="ФИО пассажира:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Паспорт:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        passport_entry = tk.Entry(form_frame, width=30)
        passport_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def purchase():
            if not flight_var.get() or not name_entry.get() or not passport_entry.get():
                messagebox.showwarning("Предупреждение", "Заполните все поля")
                return
            
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            flight_number = flight_var.get().split(':')[0]
            
            new_ticket = {
                "id": max([t['id'] for t in data['tickets']], default=0) + 1,
                "flight_number": flight_number,
                "passenger_name": name_entry.get(),
                "passport": passport_entry.get(),
                "seat": f"{len(data['tickets']) + 1}A",
                "status": "Оплачен",
                "user": get_current_user()['username']
            }
            
            data['tickets'].append(new_ticket)
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", f"Билет куплен! Место: {new_ticket['seat']}")
            self.view_schedule()
        
        tk.Button(form_frame, text="Купить", command=purchase).grid(row=3, column=0, columnspan=2, pady=10)
    
    def my_tickets(self):
        """Мои билеты"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Мои билеты", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблица билетов
        columns = ('ID', 'Рейс', 'ФИО', 'Место', 'Статус')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10)
        
        # Загрузка данных
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        current_user = get_current_user()
        for ticket in data['tickets']:
            if ticket.get('user') == current_user['username']:
                tree.insert('', 'end', values=(
                    ticket['id'], ticket['flight_number'], ticket['passenger_name'],
                    ticket['seat'], ticket['status']
                ))
    
    def show_all_tickets(self):
        """Показ всех билетов (админ)"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Все билеты", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Таблица билетов
        columns = ('ID', 'Рейс', 'Пассажир', 'Паспорт', 'Место', 'Статус', 'Пользователь')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=10)
        
        # Загрузка данных
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for ticket in data['tickets']:
            tree.insert('', 'end', values=(
                ticket['id'], ticket['flight_number'], ticket['passenger_name'],
                ticket['passport'], ticket['seat'], ticket['status'], ticket.get('user', 'N/A')
            ))
    
    def check_in(self):
        """Регистрация на рейс"""
        self.clear_content()
        
        tk.Label(self.content_frame, text="Регистрация на рейс", font=("Arial", 14, "bold")).pack(pady=10)
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        current_user = get_current_user()
        user_tickets = [t for t in data['tickets'] if t.get('user') == current_user['username']]
        
        if not user_tickets:
            tk.Label(self.content_frame, text="У вас нет билетов для регистрации").pack(pady=20)
            return
        
        for ticket in user_tickets:
            if ticket['status'] == 'Оплачен':
                frame = tk.Frame(self.content_frame, relief='ridge', borderwidth=1)
                frame.pack(pady=5, padx=10, fill='x')
                
                tk.Label(frame, text=f"Билет #{ticket['id']}: Рейс {ticket['flight_number']}").pack(side='left', padx=10)
                tk.Label(frame, text=f"Место: {ticket['seat']}").pack(side='left', padx=10)
                tk.Button(frame, text="Зарегистрироваться",
                         command=lambda t=ticket: self.register_for_flight(t)).pack(side='right', padx=10)
    
    def register_for_flight(self, ticket):
        """Регистрация на конкретный рейс"""
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for t in data['tickets']:
            if t['id'] == ticket['id']:
                t['status'] = 'Зарегистрирован'
                break
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Успех", "Вы зарегистрированы на рейс!")
        self.check_in()
    
    def logout(self):
        """Выход из системы"""
        logout_user()
        self.show_login_window()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AirportSystem()
    app.run()