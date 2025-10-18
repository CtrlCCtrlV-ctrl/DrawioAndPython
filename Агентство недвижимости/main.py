import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime
from auth import AuthManager

class RealEstateApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Агентство Недвижимости")
        self.root.geometry("900x600")
        
        self.auth = AuthManager()
        self.data_file = 'data.json'
        
        self.show_login_screen()
        
    
    def _load_data(self):
        """Загрузка данных из файла"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"properties": [], "deals": [], "requests": []}
    
    def _save_data(self, data):
        """Сохранение данных в файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # === ЭКРАН ВХОДА ===
    def show_login_screen(self):
        """Отображение экрана авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="🏢 Агентство Недвижимости", font=('Arial', 18, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=25)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:", bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, width=25, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            if self.auth.login(username, password):
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", command=login, width=20, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Регистрация (Клиент)", command=self.show_registration, width=20).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Подсказка
        hint_text = "Тестовые данные:\nadmin/admin123\nagent1/agent123\nclient1/client123"
        tk.Label(frame, text=hint_text, bg='#f0f0f0', fg='gray', font=('Arial', 9)).grid(row=5, column=0, columnspan=2, pady=10)
    
    def show_registration(self):
        """Регистрация нового клиента"""
        self.clear_window()
        
        frame = tk.Frame(self.root)
        frame.pack(pady=50)
        
        tk.Label(frame, text="Регистрация нового клиента", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=15)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(frame, width=30)
        username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(frame, width=30, show='*')
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="ФИО:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        fullname_entry = tk.Entry(frame, width=30)
        fullname_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            fullname = fullname_entry.get().strip()
            
            if not username or not password or not fullname:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = self.auth.register_user(username, password, "client", fullname)
            if success:
                messagebox.showinfo("Успех", message)
                self.show_login_screen()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(frame, text="Зарегистрироваться", command=register, bg='#4CAF50', fg='white', width=20).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Назад", command=self.show_login_screen, width=20).grid(row=5, column=0, columnspan=2, pady=5)
    
    # === ГЛАВНОЕ МЕНЮ ===
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        role = self.auth.get_role()
        username = self.auth.current_user['full_name']
        
        # Шапка
        header = tk.Frame(self.root, bg='#2196F3', height=60)
        header.pack(fill='x')
        
        tk.Label(header, text=f"👤 {username} ({role})", bg='#2196F3', fg='white', font=('Arial', 12)).pack(side='left', padx=20, pady=15)
        tk.Button(header, text="Выход", command=self.logout, bg='#f44336', fg='white').pack(side='right', padx=20, pady=10)
        
        # Контент
        content = tk.Frame(self.root)
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        if role == 'administrator':
            self.show_admin_menu(content)
        elif role == 'agent':
            self.show_agent_menu(content)
        elif role == 'client':
            self.show_client_menu(content)
    
    def logout(self):
        """Выход из системы"""
        self.auth.logout()
        self.show_login_screen()
    
    # === МЕНЮ АДМИНИСТРАТОРА ===
    def show_admin_menu(self, parent):
        """Меню администратора"""
        tk.Label(parent, text="Панель администратора", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="👥 Управление пользователями", command=self.manage_users, width=30, height=2, bg='#2196F3', fg='white').grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="🏠 Управление объектами", command=self.manage_properties_admin, width=30, height=2, bg='#4CAF50', fg='white').grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="📊 Просмотр отчетов", command=self.view_reports, width=30, height=2, bg='#FF9800', fg='white').grid(row=1, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="💼 Управление сделками", command=self.manage_deals_admin, width=30, height=2, bg='#9C27B0', fg='white').grid(row=1, column=1, padx=10, pady=10)
    
    def manage_users(self):
        """Управление пользователями"""
        win = tk.Toplevel(self.root)
        win.title("Управление пользователями")
        win.geometry("700x400")
        
        # Таблица пользователей
        columns = ('Логин', 'ФИО', 'Роль', 'Дата создания')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def load_users():
            tree.delete(*tree.get_children())
            users = self.auth.get_all_users()
            for user in users:
                tree.insert('', 'end', values=(user['username'], user['full_name'], user['role'], user['created']))
        
        load_users()
        
        # Кнопки
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        def add_user():
            AddUserDialog(win, self.auth, load_users)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            item = tree.item(selected[0])
            username = item['values'][0]
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                self.auth.delete_user(username)
                load_users()
                messagebox.showinfo("Успех", "Пользователь удален")
        
        tk.Button(btn_frame, text="Добавить", command=add_user, bg='#4CAF50', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, bg='#f44336', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=load_users, width=15).pack(side='left', padx=5)
    
    def manage_properties_admin(self):
        """Управление объектами (администратор)"""
        self.show_properties_list(admin_mode=True)
    
    def manage_deals_admin(self):
        """Управление сделками (администратор)"""
        win = tk.Toplevel(self.root)
        win.title("Управление сделками")
        win.geometry("800x400")
        
        columns = ('ID', 'Объект', 'Клиент', 'Агент', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def load_deals():
            tree.delete(*tree.get_children())
            data = self._load_data()
            for deal in data['deals']:
                prop = next((p for p in data['properties'] if p['id'] == deal['property_id']), None)
                prop_addr = prop['address'][:30] if prop else 'N/A'
                tree.insert('', 'end', values=(
                    deal['id'], prop_addr, deal['client'], deal['agent'],
                    f"{deal['amount']:,}", deal['status'], deal['date']
                ))
        
        load_deals()
        
        tk.Button(win, text="Обновить", command=load_deals, width=15).pack(pady=5)
    
    def view_reports(self):
        """Просмотр отчетов"""
        data = self._load_data()
        
        total_properties = len(data['properties'])
        active_properties = len([p for p in data['properties'] if p['status'] == 'Продается'])
        total_deals = len(data['deals'])
        total_requests = len(data['requests'])
        
        total_sum = sum(d['amount'] for d in data['deals'] if d['status'] == 'Завершена')
        
        report = f"""
📊 ОТЧЕТ ПО СИСТЕМЕ
        
📁 Объекты недвижимости:
   Всего: {total_properties}
   Активных: {active_properties}
   
💼 Сделки:
   Всего: {total_deals}
   Общая сумма: {total_sum:,} руб.
   
📝 Заявки от клиентов: {total_requests}
        """
        
        messagebox.showinfo("Отчет", report)
    
    # === МЕНЮ АГЕНТА ===
    def show_agent_menu(self, parent):
        """Меню агента"""
        tk.Label(parent, text="Панель агента", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="🏠 Мои объекты", command=self.my_properties, width=25, height=2, bg='#4CAF50', fg='white').grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="➕ Добавить объект", command=self.add_property, width=25, height=2, bg='#2196F3', fg='white').grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="🔍 Поиск объектов", command=lambda: self.show_properties_list(agent_mode=True), width=25, height=2, bg='#FF9800', fg='white').grid(row=1, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="💼 Мои сделки", command=self.my_deals, width=25, height=2, bg='#9C27B0', fg='white').grid(row=1, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="📋 Заявки клиентов", command=self.view_client_requests, width=25, height=2, bg='#00BCD4', fg='white').grid(row=2, column=0, padx=10, pady=10)
    
    def my_properties(self):
        """Объекты агента"""
        self.show_properties_list(my_only=True)
    
    def add_property(self):
        """Добавление объекта недвижимости"""
        AddPropertyDialog(self.root, self.auth, self._load_data, self._save_data)
    
    def my_deals(self):
        """Сделки агента"""
        win = tk.Toplevel(self.root)
        win.title("Мои сделки")
        win.geometry("800x400")
        
        columns = ('ID', 'Объект', 'Клиент', 'Сумма', 'Статус', 'Дата')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        username = self.auth.current_user['username']
        
        for deal in data['deals']:
            if deal['agent'] == username:
                prop = next((p for p in data['properties'] if p['id'] == deal['property_id']), None)
                prop_addr = prop['address'][:30] if prop else 'N/A'
                tree.insert('', 'end', values=(
                    deal['id'], prop_addr, deal['client'],
                    f"{deal['amount']:,}", deal['status'], deal['date']
                ))
    
    def view_client_requests(self):
        """Просмотр заявок от клиентов"""
        win = tk.Toplevel(self.root)
        win.title("Заявки клиентов")
        win.geometry("700x400")
        
        columns = ('ID', 'Объект', 'Клиент', 'Дата', 'Статус', 'Комментарий')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        
        for req in data['requests']:
            prop = next((p for p in data['properties'] if p['id'] == req['property_id']), None)
            prop_addr = prop['address'][:25] if prop else 'N/A'
            tree.insert('', 'end', values=(
                req['id'], prop_addr, req['client'],
                req['date'], req['status'], req['comment'][:30]
            ))
    
    # === МЕНЮ КЛИЕНТА ===
    def show_client_menu(self, parent):
        """Меню клиента"""
        tk.Label(parent, text="Панель клиента", font=('Arial', 16, 'bold')).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="🏠 Просмотр объектов", command=lambda: self.show_properties_list(client_mode=True), width=25, height=2, bg='#4CAF50', fg='white').grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="🔍 Поиск по фильтрам", command=self.search_properties, width=25, height=2, bg='#2196F3', fg='white').grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="📋 Мои заявки", command=self.my_requests, width=25, height=2, bg='#FF9800', fg='white').grid(row=1, column=0, padx=10, pady=10)
    
    def search_properties(self):
        """Поиск с фильтрами"""
        SearchDialog(self.root, self._load_data)
    
    def my_requests(self):
        """Заявки клиента"""
        win = tk.Toplevel(self.root)
        win.title("Мои заявки")
        win.geometry("700x400")
        
        columns = ('ID', 'Объект', 'Дата', 'Статус', 'Комментарий')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        data = self._load_data()
        username = self.auth.current_user['username']
        
        for req in data['requests']:
            if req['client'] == username:
                prop = next((p for p in data['properties'] if p['id'] == req['property_id']), None)
                prop_addr = prop['address'] if prop else 'N/A'
                tree.insert('', 'end', values=(
                    req['id'], prop_addr, req['date'], req['status'], req['comment']
                ))
    
    # === ОБЩИЕ ФУНКЦИИ ===
    def show_properties_list(self, admin_mode=False, agent_mode=False, client_mode=False, my_only=False):
        """Универсальный список объектов"""
        win = tk.Toplevel(self.root)
        win.title("Объекты недвижимости")
        win.geometry("900x500")
        
        columns = ('ID', 'Тип', 'Адрес', 'Цена', 'Площадь', 'Комнаты', 'Статус', 'Агент')
        tree = ttk.Treeview(win, columns=columns, show='headings', height=15)
        
        widths = [40, 80, 250, 100, 70, 70, 90, 80]
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        def load_properties():
            tree.delete(*tree.get_children())
            data = self._load_data()
            
            for prop in data['properties']:
                if my_only and prop['agent'] != self.auth.current_user['username']:
                    continue
                
                tree.insert('', 'end', values=(
                    prop['id'], prop['type'], prop['address'],
                    f"{prop['price']:,}", prop['area'], prop['rooms'],
                    prop['status'], prop['agent']
                ))
        
        load_properties()
        
        # Кнопки
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        if client_mode:
            def request_view():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Предупреждение", "Выберите объект")
                    return
                
                item = tree.item(selected[0])
                prop_id = item['values'][0]
                
                comment = simpledialog.askstring("Заявка", "Комментарий к заявке:")
                if comment:
                    data = self._load_data()
                    new_id = max([r['id'] for r in data['requests']], default=0) + 1
                    
                    new_request = {
                        "id": new_id,
                        "property_id": prop_id,
                        "client": self.auth.current_user['username'],
                        "status": "Новая",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "comment": comment
                    }
                    
                    data['requests'].append(new_request)
                    self._save_data(data)
                    messagebox.showinfo("Успех", "Заявка отправлена")
            
            tk.Button(btn_frame, text="Запросить просмотр", command=request_view, bg='#4CAF50', fg='white', width=20).pack(side='left', padx=5)
        
        if admin_mode or my_only:
            def edit_property():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Предупреждение", "Выберите объект")
                    return
                
                item = tree.item(selected[0])
                prop_id = item['values'][0]
                
                data = self._load_data()
                prop = next((p for p in data['properties'] if p['id'] == prop_id), None)
                
                if prop:
                    EditPropertyDialog(win, prop, self._load_data, self._save_data, load_properties)
            
            def delete_property():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Предупреждение", "Выберите объект")
                    return
                
                item = tree.item(selected[0])
                prop_id = item['values'][0]
                
                if messagebox.askyesno("Подтверждение", "Удалить объект?"):
                    data = self._load_data()
                    data['properties'] = [p for p in data['properties'] if p['id'] != prop_id]
                    self._save_data(data)
                    load_properties()
                    messagebox.showinfo("Успех", "Объект удален")
            
            tk.Button(btn_frame, text="Редактировать", command=edit_property, bg='#2196F3', fg='white', width=15).pack(side='left', padx=5)
            tk.Button(btn_frame, text="Удалить", command=delete_property, bg='#f44336', fg='white', width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Обновить", command=load_properties, width=15).pack(side='left', padx=5)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


# === ДИАЛОГОВЫЕ ОКНА ===

class AddUserDialog:
    def __init__(self, parent, auth, callback):
        self.win = tk.Toplevel(parent)
        self.win.title("Добавить пользователя")
        self.win.geometry("400x300")
        
        self.auth = auth
        self.callback = callback
        
        tk.Label(self.win, text="Логин:").grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.username_entry = tk.Entry(self.win, width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Пароль:").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.password_entry = tk.Entry(self.win, width=25, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="ФИО:").grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.fullname_entry = tk.Entry(self.win, width=25)
        self.fullname_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Роль:").grid(row=3, column=0, sticky='e', padx=10, pady=10)
        self.role_var = tk.StringVar(value='client')
        roles = ['administrator', 'agent', 'client']
        tk.OptionMenu(self.win, self.role_var, *roles).grid(row=3, column=1, sticky='w', padx=10, pady=10)
        
        tk.Button(self.win, text="Создать", command=self.create, bg='#4CAF50', fg='white', width=15).grid(row=4, column=0, columnspan=2, pady=20)
    
    def create(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        fullname = self.fullname_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password or not fullname:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        success, message = self.auth.register_user(username, password, role, fullname)
        if success:
            messagebox.showinfo("Успех", message)
            self.callback()
            self.win.destroy()
        else:
            messagebox.showerror("Ошибка", message)


class AddPropertyDialog:
    def __init__(self, parent, auth, load_func, save_func):
        self.win = tk.Toplevel(parent)
        self.win.title("Добавить объект")
        self.win.geometry("450x400")
        
        self.auth = auth
        self.load_func = load_func
        self.save_func = save_func
        
        tk.Label(self.win, text="Тип:").grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.type_var = tk.StringVar(value='Квартира')
        types = ['Квартира', 'Дом', 'Участок', 'Коммерческая']
        tk.OptionMenu(self.win, self.type_var, *types).grid(row=0, column=1, sticky='w', padx=10, pady=10)
        
        tk.Label(self.win, text="Адрес:").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.address_entry = tk.Entry(self.win, width=30)
        self.address_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Цена:").grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.price_entry = tk.Entry(self.win, width=30)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Площадь (м²):").grid(row=3, column=0, sticky='e', padx=10, pady=10)
        self.area_entry = tk.Entry(self.win, width=30)
        self.area_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Комнат:").grid(row=4, column=0, sticky='e', padx=10, pady=10)
        self.rooms_entry = tk.Entry(self.win, width=30)
        self.rooms_entry.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Статус:").grid(row=5, column=0, sticky='e', padx=10, pady=10)
        self.status_var = tk.StringVar(value='Продается')
        statuses = ['Продается', 'Продано', 'Снято с продажи']
        tk.OptionMenu(self.win, self.status_var, *statuses).grid(row=5, column=1, sticky='w', padx=10, pady=10)
        
        tk.Button(self.win, text="Добавить", command=self.add, bg='#4CAF50', fg='white', width=20).grid(row=6, column=0, columnspan=2, pady=20)
    
    def add(self):
        try:
            prop_type = self.type_var.get()
            address = self.address_entry.get().strip()
            price = int(self.price_entry.get())
            area = float(self.area_entry.get())
            rooms = int(self.rooms_entry.get())
            status = self.status_var.get()
            
            if not address:
                raise ValueError("Введите адрес")
            
            data = self.load_func()
            new_id = max([p['id'] for p in data['properties']], default=0) + 1
            
            new_property = {
                "id": new_id,
                "type": prop_type,
                "address": address,
                "price": price,
                "area": area,
                "rooms": rooms,
                "status": status,
                "agent": self.auth.current_user['username'],
                "created": datetime.now().strftime("%Y-%m-%d")
            }
            
            data['properties'].append(new_property)
            self.save_func(data)
            
            messagebox.showinfo("Успех", "Объект добавлен")
            self.win.destroy()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Проверьте данные: {e}")


class EditPropertyDialog:
    def __init__(self, parent, prop, load_func, save_func, callback):
        self.win = tk.Toplevel(parent)
        self.win.title("Редактировать объект")
        self.win.geometry("450x400")
        
        self.prop = prop
        self.load_func = load_func
        self.save_func = save_func
        self.callback = callback
        
        tk.Label(self.win, text="Тип:").grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.type_var = tk.StringVar(value=prop['type'])
        types = ['Квартира', 'Дом', 'Участок', 'Коммерческая']
        tk.OptionMenu(self.win, self.type_var, *types).grid(row=0, column=1, sticky='w', padx=10, pady=10)
        
        tk.Label(self.win, text="Адрес:").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.address_entry = tk.Entry(self.win, width=30)
        self.address_entry.insert(0, prop['address'])
        self.address_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Цена:").grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.price_entry = tk.Entry(self.win, width=30)
        self.price_entry.insert(0, str(prop['price']))
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Площадь (м²):").grid(row=3, column=0, sticky='e', padx=10, pady=10)
        self.area_entry = tk.Entry(self.win, width=30)
        self.area_entry.insert(0, str(prop['area']))
        self.area_entry.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Комнат:").grid(row=4, column=0, sticky='e', padx=10, pady=10)
        self.rooms_entry = tk.Entry(self.win, width=30)
        self.rooms_entry.insert(0, str(prop['rooms']))
        self.rooms_entry.grid(row=4, column=1, padx=10, pady=10)
        
        tk.Label(self.win, text="Статус:").grid(row=5, column=0, sticky='e', padx=10, pady=10)
        self.status_var = tk.StringVar(value=prop['status'])
        statuses = ['Продается', 'Продано', 'Снято с продажи']
        tk.OptionMenu(self.win, self.status_var, *statuses).grid(row=5, column=1, sticky='w', padx=10, pady=10)
        
        tk.Button(self.win, text="Сохранить", command=self.save, bg='#4CAF50', fg='white', width=20).grid(row=6, column=0, columnspan=2, pady=20)
    
    def save(self):
        try:
            data = self.load_func()
            
            for p in data['properties']:
                if p['id'] == self.prop['id']:
                    p['type'] = self.type_var.get()
                    p['address'] = self.address_entry.get().strip()
                    p['price'] = int(self.price_entry.get())
                    p['area'] = float(self.area_entry.get())
                    p['rooms'] = int(self.rooms_entry.get())
                    p['status'] = self.status_var.get()
                    break
            
            self.save_func(data)
            messagebox.showinfo("Успех", "Объект обновлен")
            self.callback()
            self.win.destroy()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Проверьте данные: {e}")


class SearchDialog:
    def __init__(self, parent, load_func):
        self.win = tk.Toplevel(parent)
        self.win.title("Поиск объектов")
        self.win.geometry("800x500")
        
        self.load_func = load_func
        
        # Фильтры
        filter_frame = tk.Frame(self.win)
        filter_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(filter_frame, text="Тип:").grid(row=0, column=0, padx=5)
        self.type_var = tk.StringVar(value='Все')
        types = ['Все', 'Квартира', 'Дом', 'Участок', 'Коммерческая']
        tk.OptionMenu(filter_frame, self.type_var, *types).grid(row=0, column=1, padx=5)
        
        tk.Label(filter_frame, text="Цена от:").grid(row=0, column=2, padx=5)
        self.price_from = tk.Entry(filter_frame, width=15)
        self.price_from.grid(row=0, column=3, padx=5)
        
        tk.Label(filter_frame, text="до:").grid(row=0, column=4, padx=5)
        self.price_to = tk.Entry(filter_frame, width=15)
        self.price_to.grid(row=0, column=5, padx=5)
        
        tk.Button(filter_frame, text="Искать", command=self.search, bg='#4CAF50', fg='white').grid(row=0, column=6, padx=10)
        
        # Результаты
        columns = ('ID', 'Тип', 'Адрес', 'Цена', 'Площадь', 'Комнаты', 'Статус')
        self.tree = ttk.Treeview(self.win, columns=columns, show='headings', height=15)
        
        widths = [40, 100, 300, 100, 70, 70, 90]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.search()
    
    def search(self):
        self.tree.delete(*self.tree.get_children())
        
        data = self.load_func()
        prop_type = self.type_var.get()
        
        try:
            price_from = int(self.price_from.get()) if self.price_from.get() else 0
            price_to = int(self.price_to.get()) if self.price_to.get() else float('inf')
        except:
            price_from = 0
            price_to = float('inf')
        
        for prop in data['properties']:
            if prop['status'] != 'Продается':
                continue
            
            if prop_type != 'Все' and prop['type'] != prop_type:
                continue
            
            if not (price_from <= prop['price'] <= price_to):
                continue
            
            self.tree.insert('', 'end', values=(
                prop['id'], prop['type'], prop['address'],
                f"{prop['price']:,}", prop['area'], prop['rooms'], prop['status']
            ))


if __name__ == '__main__':
    app = RealEstateApp()
    app.run()