import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
from auth import AuthManager

class CarRentalSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Система проката автомобилей")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.auth_manager = AuthManager()
        self.data_file = 'data.json'

        self.show_login_window()
    
    
    def load_data(self):
        """Загрузка данных"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"cars": [], "clients": [], "rentals": [], "bookings": []}
    
    def save_data(self, data):
        """Сохранение данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def show_login_window(self):
        """Окно входа в систему"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Рамка для формы входа
        login_frame = tk.Frame(self.root)
        login_frame.place(relx=0.5, rely=0.4, anchor='center')
        
        tk.Label(login_frame, text="Вход в систему", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(login_frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.login_entry = tk.Entry(login_frame, width=20)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(login_frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = tk.Entry(login_frame, width=20, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(login_frame, text="Войти", command=self.login, width=15).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Информация о тестовых учетных записях
        info_frame = tk.Frame(self.root)
        info_frame.place(relx=0.5, rely=0.7, anchor='center')
        tk.Label(info_frame, text="Тестовые учетные записи:", font=("Arial", 10)).pack()
        tk.Label(info_frame, text="Администратор: admin / admin123", font=("Arial", 9)).pack()
        tk.Label(info_frame, text="Менеджер: manager / manager123", font=("Arial", 9)).pack()
        tk.Label(info_frame, text="Клиент: client / client123", font=("Arial", 9)).pack()
    
    def login(self):
        """Обработка входа"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
        
        success, role = self.auth_manager.authenticate(username, password)
        
        if success:
            if role == "administrator":
                self.show_admin_menu()
            elif role == "manager":
                self.show_manager_menu()
            elif role == "client":
                self.show_client_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_admin_menu(self):
        """Меню администратора"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        user = self.auth_manager.get_current_user()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_frame.pack(fill='x')
        tk.Label(top_frame, text=f"Администратор: {user['full_name']}", 
                bg='#2c3e50', fg='white', font=("Arial", 12)).pack(side='left', padx=20, pady=10)
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side='right', padx=20, pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка управления автомобилями
        cars_frame = ttk.Frame(notebook)
        notebook.add(cars_frame, text="Автопарк")
        self.create_cars_management(cars_frame)
        
        # Вкладка управления пользователями
        users_frame = ttk.Frame(notebook)
        notebook.add(users_frame, text="Пользователи")
        self.create_users_management(users_frame)
        
        # Вкладка отчетов
        reports_frame = ttk.Frame(notebook)
        notebook.add(reports_frame, text="Отчеты")
        self.create_reports_panel(reports_frame)
    
    def show_manager_menu(self):
        """Меню менеджера"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        user = self.auth_manager.get_current_user()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#27ae60', height=50)
        top_frame.pack(fill='x')
        tk.Label(top_frame, text=f"Менеджер: {user['full_name']}", 
                bg='#27ae60', fg='white', font=("Arial", 12)).pack(side='left', padx=20, pady=10)
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side='right', padx=20, pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка аренды
        rental_frame = ttk.Frame(notebook)
        notebook.add(rental_frame, text="Оформление аренды")
        self.create_rental_management(rental_frame)
        
        # Вкладка клиентов
        clients_frame = ttk.Frame(notebook)
        notebook.add(clients_frame, text="Клиенты")
        self.create_clients_management(clients_frame)
        
        # Вкладка возврата
        return_frame = ttk.Frame(notebook)
        notebook.add(return_frame, text="Возврат автомобилей")
        self.create_return_management(return_frame)
    
    def show_client_menu(self):
        """Меню клиента"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        user = self.auth_manager.get_current_user()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#3498db', height=50)
        top_frame.pack(fill='x')
        tk.Label(top_frame, text=f"Клиент: {user['full_name']}", 
                bg='#3498db', fg='white', font=("Arial", 12)).pack(side='left', padx=20, pady=10)
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side='right', padx=20, pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка доступных автомобилей
        available_frame = ttk.Frame(notebook)
        notebook.add(available_frame, text="Доступные автомобили")
        self.create_available_cars_view(available_frame)
        
        # Вкладка бронирования
        booking_frame = ttk.Frame(notebook)
        notebook.add(booking_frame, text="Мои бронирования")
        self.create_bookings_view(booking_frame)
        
        # Вкладка истории
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="История аренды")
        self.create_history_view(history_frame)
    
    def create_cars_management(self, parent):
        """Управление автопарком"""
        # Панель кнопок
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Добавить автомобиль", command=self.add_car_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_car_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_car).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_cars_table()).pack(side='left', padx=5)
        
        # Таблица автомобилей
        columns = ('ID', 'Марка', 'Модель', 'Год', 'Цена/день', 'Статус')
        self.cars_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.cars_tree.heading(col, text=col)
            self.cars_tree.column(col, width=140)
        
        self.cars_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.cars_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.cars_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_cars_table()
    
    def refresh_cars_table(self):
        """Обновление таблицы автомобилей"""
        for item in self.cars_tree.get_children():
            self.cars_tree.delete(item)
        
        data = self.load_data()
        for car in data['cars']:
            status_text = "Доступен" if car['status'] == "available" else "В аренде"
            self.cars_tree.insert('', 'end', values=(
                car['id'], car['brand'], car['model'], 
                car['year'], f"{car['price_per_day']} руб.", status_text
            ))
    
    def add_car_dialog(self):
        """Диалог добавления автомобиля"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить автомобиль")
        dialog.geometry("400x300")
        
        # Поля ввода
        tk.Label(dialog, text="Марка:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        brand_entry = tk.Entry(dialog, width=25)
        brand_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Модель:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        model_entry = tk.Entry(dialog, width=25)
        model_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Год:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        year_entry = tk.Entry(dialog, width=25)
        year_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Цена/день:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        price_entry = tk.Entry(dialog, width=25)
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def save_car():
            if not all([brand_entry.get(), model_entry.get(), year_entry.get(), price_entry.get()]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                data = self.load_data()
                new_id = max([c['id'] for c in data['cars']] + [0]) + 1
                
                new_car = {
                    "id": new_id,
                    "brand": brand_entry.get(),
                    "model": model_entry.get(),
                    "year": int(year_entry.get()),
                    "price_per_day": int(price_entry.get()),
                    "status": "available"
                }
                
                data['cars'].append(new_car)
                self.save_data(data)
                self.refresh_cars_table()
                dialog.destroy()
                messagebox.showinfo("Успех", "Автомобиль добавлен")
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте корректность данных")
        
        tk.Button(dialog, text="Сохранить", command=save_car).grid(row=4, column=0, columnspan=2, pady=20)
    
    def edit_car_dialog(self):
        """Диалог редактирования автомобиля"""
        selected = self.cars_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите автомобиль")
            return
        
        item = self.cars_tree.item(selected[0])
        car_id = item['values'][0]
        
        data = self.load_data()
        car = next((c for c in data['cars'] if c['id'] == car_id), None)
        if not car:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать автомобиль")
        dialog.geometry("400x300")
        
        # Поля ввода с текущими значениями
        tk.Label(dialog, text="Марка:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        brand_entry = tk.Entry(dialog, width=25)
        brand_entry.insert(0, car['brand'])
        brand_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Модель:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        model_entry = tk.Entry(dialog, width=25)
        model_entry.insert(0, car['model'])
        model_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Год:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        year_entry = tk.Entry(dialog, width=25)
        year_entry.insert(0, str(car['year']))
        year_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Цена/день:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        price_entry = tk.Entry(dialog, width=25)
        price_entry.insert(0, str(car['price_per_day']))
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def update_car():
            try:
                car['brand'] = brand_entry.get()
                car['model'] = model_entry.get()
                car['year'] = int(year_entry.get())
                car['price_per_day'] = int(price_entry.get())
                
                self.save_data(data)
                self.refresh_cars_table()
                dialog.destroy()
                messagebox.showinfo("Успех", "Автомобиль обновлен")
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте корректность данных")
        
        tk.Button(dialog, text="Сохранить", command=update_car).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_car(self):
        """Удаление автомобиля"""
        selected = self.cars_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите автомобиль")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный автомобиль?"):
            item = self.cars_tree.item(selected[0])
            car_id = item['values'][0]
            
            data = self.load_data()
            data['cars'] = [c for c in data['cars'] if c['id'] != car_id]
            self.save_data(data)
            self.refresh_cars_table()
            messagebox.showinfo("Успех", "Автомобиль удален")
    
    def create_users_management(self, parent):
        """Управление пользователями"""
        # Панель добавления пользователя
        add_frame = tk.LabelFrame(parent, text="Добавить пользователя")
        add_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(add_frame, text="Логин:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.new_username = tk.Entry(add_frame, width=20)
        self.new_username.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Пароль:").grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.new_password = tk.Entry(add_frame, width=20)
        self.new_password.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(add_frame, text="ФИО:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.new_fullname = tk.Entry(add_frame, width=20)
        self.new_fullname.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Роль:").grid(row=1, column=2, sticky='e', padx=5, pady=5)
        self.new_role = ttk.Combobox(add_frame, values=["administrator", "manager", "client"], width=17)
        self.new_role.grid(row=1, column=3, padx=5, pady=5)
        self.new_role.set("client")
        
        tk.Button(add_frame, text="Добавить", command=self.add_user).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Таблица пользователей
        columns = ('Логин', 'Роль', 'ФИО', 'Дата создания')
        self.users_tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=200)
        
        self.users_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.refresh_users_table()
    
    def refresh_users_table(self):
        """Обновление таблицы пользователей"""
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        users_data = self.auth_manager.load_users()
        for user in users_data['users']:
            role_text = {"administrator": "Администратор", "manager": "Менеджер", "client": "Клиент"}.get(user['role'], user['role'])
            self.users_tree.insert('', 'end', values=(
                user['username'], role_text, user['full_name'], user['created']
            ))
    
    def add_user(self):
        """Добавление пользователя"""
        username = self.new_username.get()
        password = self.new_password.get()
        fullname = self.new_fullname.get()
        role = self.new_role.get()
        
        if not all([username, password, fullname, role]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        success, message = self.auth_manager.register_user(username, password, role, fullname)
        if success:
            messagebox.showinfo("Успех", message)
            self.new_username.delete(0, tk.END)
            self.new_password.delete(0, tk.END)
            self.new_fullname.delete(0, tk.END)
            self.refresh_users_table()
        else:
            messagebox.showerror("Ошибка", message)
    
    def create_reports_panel(self, parent):
        """Панель отчетов"""
        tk.Label(parent, text="Статистика системы", font=("Arial", 14, "bold")).pack(pady=10)
        
        stats_frame = tk.Frame(parent)
        stats_frame.pack(padx=20, pady=20)
        
        data = self.load_data()
        
        # Статистика
        total_cars = len(data['cars'])
        available_cars = len([c for c in data['cars'] if c['status'] == 'available'])
        rented_cars = len([c for c in data['cars'] if c['status'] == 'rented'])
        total_clients = len(data['clients'])
        active_rentals = len([r for r in data['rentals'] if r['status'] == 'active'])
        
        stats = [
            ("Всего автомобилей:", total_cars),
            ("Доступно для аренды:", available_cars),
            ("В аренде:", rented_cars),
            ("Зарегистрировано клиентов:", total_clients),
            ("Активных аренд:", active_rentals)
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(stats_frame, text=label, font=("Arial", 11)).grid(row=i, column=0, sticky='e', padx=10, pady=5)
            tk.Label(stats_frame, text=str(value), font=("Arial", 11, "bold")).grid(row=i, column=1, sticky='w', padx=10, pady=5)
        
        # Кнопка экспорта
        tk.Button(parent, text="Экспорт отчета", command=self.export_report).pack(pady=20)
    
    def export_report(self):
        """Экспорт отчета"""
        data = self.load_data()
        report_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = f"report_{report_time}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("ОТЧЕТ СИСТЕМЫ ПРОКАТА АВТОМОБИЛЕЙ\n")
            f.write(f"Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            
            f.write("АВТОПАРК:\n")
            for car in data['cars']:
                f.write(f"- {car['brand']} {car['model']} ({car['year']}) - {car['price_per_day']} руб/день - {car['status']}\n")
            
            f.write("\nАКТИВНЫЕ АРЕНДЫ:\n")
            for rental in [r for r in data['rentals'] if r['status'] == 'active']:
                f.write(f"- ID: {rental['id']}, Авто ID: {rental['car_id']}, Клиент ID: {rental['client_id']}, {rental['start_date']} - {rental['end_date']}\n")
        
        messagebox.showinfo("Успех", f"Отчет сохранен в файл {report_file}")
    
    def create_rental_management(self, parent):
        """Управление арендой"""
        # Форма оформления аренды
        form_frame = tk.LabelFrame(parent, text="Оформить аренду")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(form_frame, text="Клиент:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.client_combo = ttk.Combobox(form_frame, width=30)
        self.client_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Автомобиль:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.car_combo = ttk.Combobox(form_frame, width=30)
        self.car_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Дней аренды:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.days_entry = tk.Entry(form_frame, width=10)
        self.days_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        tk.Button(form_frame, text="Рассчитать стоимость", command=self.calculate_rental_price).grid(row=3, column=0, pady=10)
        tk.Button(form_frame, text="Оформить", command=self.create_rental).grid(row=3, column=1, pady=10)
        
        self.price_label = tk.Label(form_frame, text="Стоимость: 0 руб.", font=("Arial", 12, "bold"))
        self.price_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Таблица активных аренд
        tk.Label(parent, text="Активные аренды", font=("Arial", 12, "bold")).pack(pady=10)
        
        columns = ('ID', 'Клиент', 'Автомобиль', 'Начало', 'Окончание', 'Стоимость')
        self.rentals_tree = ttk.Treeview(parent, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.rentals_tree.heading(col, text=col)
            self.rentals_tree.column(col, width=140)
        
        self.rentals_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_rental_data()
    
    def refresh_rental_data(self):
        """Обновление данных аренды"""
        data = self.load_data()
        
        # Обновление комбобоксов
        clients = [f"{c['id']}. {c['name']}" for c in data['clients']]
        self.client_combo['values'] = clients
        
        available_cars = [c for c in data['cars'] if c['status'] == 'available']
        cars = [f"{c['id']}. {c['brand']} {c['model']} ({c['price_per_day']} руб/день)" for c in available_cars]
        self.car_combo['values'] = cars
        
        # Обновление таблицы аренд
        for item in self.rentals_tree.get_children():
            self.rentals_tree.delete(item)
        
        for rental in [r for r in data['rentals'] if r['status'] == 'active']:
            client = next((c for c in data['clients'] if c['id'] == rental['client_id']), {})
            car = next((c for c in data['cars'] if c['id'] == rental['car_id']), {})
            
            self.rentals_tree.insert('', 'end', values=(
                rental['id'],
                client.get('name', 'N/A'),
                f"{car.get('brand', '')} {car.get('model', '')}",
                rental['start_date'],
                rental['end_date'],
                f"{rental['total_price']} руб."
            ))
    
    def calculate_rental_price(self):
        """Расчет стоимости аренды"""
        try:
            days = int(self.days_entry.get())
            car_info = self.car_combo.get()
            
            if not car_info:
                messagebox.showerror("Ошибка", "Выберите автомобиль")
                return
            
            car_id = int(car_info.split('.')[0])
            data = self.load_data()
            car = next((c for c in data['cars'] if c['id'] == car_id), None)
            
            if car:
                total_price = car['price_per_day'] * days
                self.price_label.config(text=f"Стоимость: {total_price} руб.")
                return total_price
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество дней")
        return 0
    
    def create_rental(self):
        """Создание аренды"""
        client_info = self.client_combo.get()
        car_info = self.car_combo.get()
        days_str = self.days_entry.get()
        
        if not all([client_info, car_info, days_str]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        try:
            client_id = int(client_info.split('.')[0])
            car_id = int(car_info.split('.')[0])
            days = int(days_str)
            
            data = self.load_data()
            car = next((c for c in data['cars'] if c['id'] == car_id), None)
            
            if not car or car['status'] != 'available':
                messagebox.showerror("Ошибка", "Автомобиль недоступен")
                return
            
            # Создание новой аренды
            new_id = max([r['id'] for r in data['rentals']] + [0]) + 1
            start_date = datetime.now().strftime("%Y-%m-%d")
            end_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            total_price = car['price_per_day'] * days
            
            new_rental = {
                "id": new_id,
                "car_id": car_id,
                "client_id": client_id,
                "start_date": start_date,
                "end_date": end_date,
                "total_price": total_price,
                "status": "active"
            }
            
            data['rentals'].append(new_rental)
            
            # Обновление статуса автомобиля
            car['status'] = 'rented'
            
            self.save_data(data)
            self.refresh_rental_data()
            
            # Очистка формы
            self.client_combo.set('')
            self.car_combo.set('')
            self.days_entry.delete(0, tk.END)
            self.price_label.config(text="Стоимость: 0 руб.")
            
            messagebox.showinfo("Успех", f"Аренда оформлена. ID: {new_id}")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность данных")
    
    def create_clients_management(self, parent):
        """Управление клиентами"""
        # Форма добавления клиента
        form_frame = tk.LabelFrame(parent, text="Добавить клиента")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(form_frame, text="ФИО:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.client_name = tk.Entry(form_frame, width=30)
        self.client_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Телефон:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.client_phone = tk.Entry(form_frame, width=30)
        self.client_phone.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Паспорт:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.client_passport = tk.Entry(form_frame, width=30)
        self.client_passport.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(form_frame, text="Добавить", command=self.add_client).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Таблица клиентов
        columns = ('ID', 'ФИО', 'Телефон', 'Паспорт')
        self.clients_tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=200)
        
        self.clients_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.refresh_clients_table()
    
    def refresh_clients_table(self):
        """Обновление таблицы клиентов"""
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        data = self.load_data()
        for client in data['clients']:
            self.clients_tree.insert('', 'end', values=(
                client['id'], client['name'], client['phone'], client['passport']
            ))
    
    def add_client(self):
        """Добавление клиента"""
        name = self.client_name.get()
        phone = self.client_phone.get()
        passport = self.client_passport.get()
        
        if not all([name, phone, passport]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        data = self.load_data()
        new_id = max([c['id'] for c in data['clients']] + [0]) + 1
        
        new_client = {
            "id": new_id,
            "name": name,
            "phone": phone,
            "passport": passport
        }
        
        data['clients'].append(new_client)
        self.save_data(data)
        
        # Очистка формы
        self.client_name.delete(0, tk.END)
        self.client_phone.delete(0, tk.END)
        self.client_passport.delete(0, tk.END)
        
        self.refresh_clients_table()
        messagebox.showinfo("Успех", "Клиент добавлен")
    
    def create_return_management(self, parent):
        """Управление возвратом автомобилей"""
        tk.Label(parent, text="Активные аренды для возврата", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Таблица активных аренд
        columns = ('ID', 'Клиент', 'Автомобиль', 'Начало', 'Окончание', 'Стоимость')
        self.return_tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.return_tree.heading(col, text=col)
            self.return_tree.column(col, width=140)
        
        self.return_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Кнопка возврата
        tk.Button(parent, text="Оформить возврат", command=self.process_return, width=20, height=2).pack(pady=10)
        
        self.refresh_return_table()
    
    def refresh_return_table(self):
        """Обновление таблицы возвратов"""
        for item in self.return_tree.get_children():
            self.return_tree.delete(item)
        
        data = self.load_data()
        for rental in [r for r in data['rentals'] if r['status'] == 'active']:
            client = next((c for c in data['clients'] if c['id'] == rental['client_id']), {})
            car = next((c for c in data['cars'] if c['id'] == rental['car_id']), {})
            
            self.return_tree.insert('', 'end', values=(
                rental['id'],
                client.get('name', 'N/A'),
                f"{car.get('brand', '')} {car.get('model', '')}",
                rental['start_date'],
                rental['end_date'],
                f"{rental['total_price']} руб."
            ))
    
    def process_return(self):
        """Обработка возврата автомобиля"""
        selected = self.return_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите аренду для возврата")
            return
        
        if messagebox.askyesno("Подтверждение", "Оформить возврат автомобиля?"):
            item = self.return_tree.item(selected[0])
            rental_id = item['values'][0]
            
            data = self.load_data()
            
            # Найти аренду и обновить статус
            for rental in data['rentals']:
                if rental['id'] == rental_id:
                    rental['status'] = 'completed'
                    
                    # Освободить автомобиль
                    for car in data['cars']:
                        if car['id'] == rental['car_id']:
                            car['status'] = 'available'
                            break
                    break
            
            self.save_data(data)
            self.refresh_return_table()
            messagebox.showinfo("Успех", "Возврат оформлен")
    
    def create_available_cars_view(self, parent):
        """Просмотр доступных автомобилей для клиента"""
        tk.Label(parent, text="Доступные для аренды автомобили", font=("Arial", 12, "bold")).pack(pady=10)
        
        columns = ('ID', 'Марка', 'Модель', 'Год', 'Цена/день')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=160)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Заполнение таблицы
        data = self.load_data()
        for car in data['cars']:
            if car['status'] == 'available':
                tree.insert('', 'end', values=(
                    car['id'], car['brand'], car['model'], 
                    car['year'], f"{car['price_per_day']} руб."
                ))
    
    def create_bookings_view(self, parent):
        """Просмотр бронирований клиента"""
        # Форма бронирования
        form_frame = tk.LabelFrame(parent, text="Забронировать автомобиль")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(form_frame, text="ID автомобиля:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.booking_car_id = tk.Entry(form_frame, width=10)
        self.booking_car_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(form_frame, text="Дата начала (ГГГГ-ММ-ДД):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.booking_start = tk.Entry(form_frame, width=15)
        self.booking_start.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        tk.Label(form_frame, text="Дней:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.booking_days = tk.Entry(form_frame, width=10)
        self.booking_days.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        tk.Button(form_frame, text="Забронировать", command=self.create_booking).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Таблица бронирований
        tk.Label(parent, text="Мои бронирования", font=("Arial", 12, "bold")).pack(pady=10)
        
        columns = ('ID', 'Автомобиль', 'Дата начала', 'Дней', 'Статус')
        self.bookings_tree = ttk.Treeview(parent, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.bookings_tree.heading(col, text=col)
            self.bookings_tree.column(col, width=150)
        
        self.bookings_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Button(parent, text="Отменить бронирование", command=self.cancel_booking).pack(pady=5)
        
        self.refresh_bookings_table()
    
    def refresh_bookings_table(self):
        """Обновление таблицы бронирований"""
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        data = self.load_data()
        user = self.auth_manager.get_current_user()
        
        # Фильтрация бронирований текущего клиента
        for booking in data.get('bookings', []):
            if booking.get('client_name') == user['full_name']:
                car = next((c for c in data['cars'] if c['id'] == booking['car_id']), {})
                self.bookings_tree.insert('', 'end', values=(
                    booking['id'],
                    f"{car.get('brand', '')} {car.get('model', '')}",
                    booking['start_date'],
                    booking['days'],
                    booking['status']
                ))
    
    def create_booking(self):
        """Создание бронирования"""
        try:
            car_id = int(self.booking_car_id.get())
            start_date = self.booking_start.get()
            days = int(self.booking_days.get())
            
            data = self.load_data()
            car = next((c for c in data['cars'] if c['id'] == car_id), None)
            
            if not car:
                messagebox.showerror("Ошибка", "Автомобиль не найден")
                return
            
            if car['status'] != 'available':
                messagebox.showerror("Ошибка", "Автомобиль недоступен")
                return
            
            user = self.auth_manager.get_current_user()
            new_id = max([b['id'] for b in data.get('bookings', [])] + [0]) + 1
            
            new_booking = {
                "id": new_id,
                "car_id": car_id,
                "client_name": user['full_name'],
                "start_date": start_date,
                "days": days,
                "status": "active"
            }
            
            if 'bookings' not in data:
                data['bookings'] = []
            
            data['bookings'].append(new_booking)
            self.save_data(data)
            
            # Очистка формы
            self.booking_car_id.delete(0, tk.END)
            self.booking_start.delete(0, tk.END)
            self.booking_days.delete(0, tk.END)
            
            self.refresh_bookings_table()
            messagebox.showinfo("Успех", "Бронирование создано")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность данных")
    
    def cancel_booking(self):
        """Отмена бронирования"""
        selected = self.bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите бронирование")
            return
        
        if messagebox.askyesno("Подтверждение", "Отменить бронирование?"):
            item = self.bookings_tree.item(selected[0])
            booking_id = item['values'][0]
            
            data = self.load_data()
            for booking in data.get('bookings', []):
                if booking['id'] == booking_id:
                    booking['status'] = 'cancelled'
                    break
            
            self.save_data(data)
            self.refresh_bookings_table()
            messagebox.showinfo("Успех", "Бронирование отменено")
    
    def create_history_view(self, parent):
        """История аренды клиента"""
        tk.Label(parent, text="История моих аренд", font=("Arial", 12, "bold")).pack(pady=10)
        
        columns = ('ID', 'Автомобиль', 'Начало', 'Окончание', 'Стоимость', 'Статус')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Заполнение истории (демо-данные для клиента)
        data = self.load_data()
        user = self.auth_manager.get_current_user()
        
        # Поиск клиента по имени
        client = next((c for c in data['clients'] if c['name'] == user['full_name']), None)
        
        if client:
            for rental in data['rentals']:
                if rental['client_id'] == client['id']:
                    car = next((c for c in data['cars'] if c['id'] == rental['car_id']), {})
                    status_text = "Активна" if rental['status'] == 'active' else "Завершена"
                    tree.insert('', 'end', values=(
                        rental['id'],
                        f"{car.get('brand', '')} {car.get('model', '')}",
                        rental['start_date'],
                        rental['end_date'],
                        f"{rental['total_price']} руб.",
                        status_text
                    ))
    
    def logout(self):
        """Выход из системы"""
        self.auth_manager.logout()
        self.show_login_window()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CarRentalSystem()
    app.run()