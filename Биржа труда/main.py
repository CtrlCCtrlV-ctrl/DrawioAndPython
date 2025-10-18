import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import auth

DATA_FILE = 'data.json'

class JobExchangeApp:
    """Главное приложение Биржи труда"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Биржа труда")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        self.current_user = None

        self.show_login_screen()
    
    
    def load_data(self):
        """Загрузка данных из файла"""
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"vacancies": [], "applications": [], "resumes": [], "categories": []}
    
    def save_data(self, data):
        """Сохранение данных в файл"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Экран авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Биржа труда", font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', padx=5, pady=10)
        username_entry = tk.Entry(frame, font=('Arial', 12), width=25)
        username_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', padx=5, pady=10)
        password_entry = tk.Entry(frame, font=('Arial', 12), width=25, show='*')
        password_entry.grid(row=2, column=1, pady=10)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            user = auth.authenticate(username, password)
            if user:
                self.current_user = user
                self.show_main_screen()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        def show_register():
            self.show_register_screen()
        
        tk.Button(frame, text="Войти", font=('Arial', 12), width=15, command=login).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(frame, text="Регистрация", font=('Arial', 10), width=15, command=show_register).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Подсказка
        hint_text = "Тестовые учетные записи:\nadmin/admin123 (Администратор)\nemployer1/emp123 (Работодатель)\nseeker1/seek123 (Соискатель)"
        tk.Label(frame, text=hint_text, font=('Arial', 9), fg='gray', justify='left').grid(row=5, column=0, columnspan=2, pady=20)
        
        password_entry.bind('<Return>', lambda e: login())
    
    def show_register_screen(self):
        """Экран регистрации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=30, pady=30)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Регистрация", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=15)
        
        tk.Label(frame, text="Логин:", font=('Arial', 11)).grid(row=1, column=0, sticky='e', padx=5, pady=8)
        username_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        username_entry.grid(row=1, column=1, pady=8)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 11)).grid(row=2, column=0, sticky='e', padx=5, pady=8)
        password_entry = tk.Entry(frame, font=('Arial', 11), width=30, show='*')
        password_entry.grid(row=2, column=1, pady=8)
        
        tk.Label(frame, text="ФИО/Название:", font=('Arial', 11)).grid(row=3, column=0, sticky='e', padx=5, pady=8)
        fullname_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        fullname_entry.grid(row=3, column=1, pady=8)
        
        tk.Label(frame, text="Email:", font=('Arial', 11)).grid(row=4, column=0, sticky='e', padx=5, pady=8)
        email_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        email_entry.grid(row=4, column=1, pady=8)
        
        tk.Label(frame, text="Роль:", font=('Arial', 11)).grid(row=5, column=0, sticky='e', padx=5, pady=8)
        role_var = tk.StringVar(value="jobseeker")
        role_frame = tk.Frame(frame)
        role_frame.grid(row=5, column=1, sticky='w', pady=8)
        tk.Radiobutton(role_frame, text="Соискатель", variable=role_var, value="jobseeker", font=('Arial', 10)).pack(side='left', padx=5)
        tk.Radiobutton(role_frame, text="Работодатель", variable=role_var, value="employer", font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Label(frame, text="Компания:", font=('Arial', 11)).grid(row=6, column=0, sticky='e', padx=5, pady=8)
        company_entry = tk.Entry(frame, font=('Arial', 11), width=30)
        company_entry.grid(row=6, column=1, pady=8)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            email = email_entry.get().strip()
            role = role_var.get()
            company = company_entry.get().strip()
            
            if not username or not password or not fullname or not email:
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            if role == "employer" and not company:
                messagebox.showerror("Ошибка", "Укажите название компании")
                return
            
            success, message = auth.register_user(username, password, role, fullname, email, company)
            if success:
                messagebox.showinfo("Успех", message)
                self.show_login_screen()
            else:
                messagebox.showerror("Ошибка", message)
        
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Зарегистрироваться", font=('Arial', 11), width=18, command=register).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Назад", font=('Arial', 11), width=12, command=self.show_login_screen).pack(side='left', padx=5)
    
    def show_main_screen(self):
        """Главный экран в зависимости от роли"""
        if self.current_user['role'] == 'administrator':
            self.show_admin_screen()
        elif self.current_user['role'] == 'employer':
            self.show_employer_screen()
        else:
            self.show_jobseeker_screen()
    
    # ========== ИНТЕРФЕЙС АДМИНИСТРАТОРА ==========
    
    def show_admin_screen(self):
        """Интерфейс администратора"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text=f"Администратор: {self.current_user['full_name']}", 
                bg='#2c3e50', fg='white', font=('Arial', 12)).pack(side='left', padx=20, pady=15)
        tk.Button(top_frame, text="Выход", command=self.show_login_screen, 
                 bg='#e74c3c', fg='white', font=('Arial', 10), width=10).pack(side='right', padx=20, pady=15)
        
        # Боковое меню
        menu_frame = tk.Frame(self.root, bg='#34495e', width=200)
        menu_frame.pack(side='left', fill='y')
        menu_frame.pack_propagate(False)
        
        tk.Label(menu_frame, text="МЕНЮ", bg='#34495e', fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=20)
        
        menu_buttons = [
            ("Пользователи", self.admin_users),
            ("Вакансии", self.admin_vacancies),
            ("Статистика", self.admin_statistics),
            ("Категории", self.admin_categories)
        ]
        
        for text, command in menu_buttons:
            tk.Button(menu_frame, text=text, command=command, bg='#34495e', fg='white',
                     font=('Arial', 11), width=18, anchor='w', relief='flat',
                     activebackground='#2c3e50').pack(pady=5, padx=10)
        
        # Основная область
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        self.admin_users()
    
    def admin_users(self):
        """Управление пользователями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление пользователями", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        # Таблица пользователей
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Логин', 'ФИО', 'Роль', 'Email', 'Дата создания')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Загрузка данных
        users = auth.get_all_users()
        role_names = {'administrator': 'Администратор', 'employer': 'Работодатель', 'jobseeker': 'Соискатель'}
        
        for user in users:
            tree.insert('', 'end', values=(
                user['username'],
                user['full_name'],
                role_names.get(user['role'], user['role']),
                user.get('email', ''),
                user['created']
            ))
        
        # Кнопки действий
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            username = tree.item(selected[0])['values'][0]
            if username == self.current_user['username']:
                messagebox.showerror("Ошибка", "Нельзя удалить себя")
                return
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                auth.delete_user(username)
                self.admin_users()
        
        tk.Button(btn_frame, text="Удалить пользователя", command=delete_user, 
                 font=('Arial', 10), width=20).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.admin_users, 
                 font=('Arial', 10), width=15).pack(side='left', padx=5)
    
    def admin_vacancies(self):
        """Модерация вакансий"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Модерация вакансий", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        data = self.load_data()
        
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Должность', 'Компания', 'Зарплата', 'Статус')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for vacancy in data['vacancies']:
            tree.insert('', 'end', values=(
                vacancy['id'],
                vacancy['title'],
                vacancy['company'],
                vacancy['salary'],
                vacancy['status']
            ))
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        def delete_vacancy():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите вакансию")
                return
            
            vacancy_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить вакансию?"):
                data['vacancies'] = [v for v in data['vacancies'] if v['id'] != vacancy_id]
                self.save_data(data)
                self.admin_vacancies()
        
        tk.Button(btn_frame, text="Удалить вакансию", command=delete_vacancy, 
                 font=('Arial', 10), width=18).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.admin_vacancies, 
                 font=('Arial', 10), width=15).pack(side='left', padx=5)
    
    def admin_statistics(self):
        """Статистика системы"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Статистика системы", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        data = self.load_data()
        users = auth.get_all_users()
        
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=30)
        
        stats = [
            ("Всего пользователей:", len(users)),
            ("Соискателей:", len([u for u in users if u['role'] == 'jobseeker'])),
            ("Работодателей:", len([u for u in users if u['role'] == 'employer'])),
            ("Всего вакансий:", len(data['vacancies'])),
            ("Активных вакансий:", len([v for v in data['vacancies'] if v['status'] == 'active'])),
            ("Всего откликов:", len(data['applications'])),
            ("Резюме в системе:", len(data['resumes']))
        ]
        
        for i, (label, value) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg='#ecf0f1', relief='raised', borderwidth=1)
            frame.pack(fill='x', pady=8, padx=50)
            tk.Label(frame, text=label, font=('Arial', 12, 'bold'), bg='#ecf0f1', 
                    anchor='w').pack(side='left', padx=20, pady=15)
            tk.Label(frame, text=str(value), font=('Arial', 14, 'bold'), bg='#ecf0f1', 
                    fg='#2980b9', anchor='e').pack(side='right', padx=20, pady=15)
    
    def admin_categories(self):
        """Управление категориями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление категориями", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        data = self.load_data()
        
        list_frame = tk.Frame(self.content_frame, bg='white')
        list_frame.pack(pady=20)
        
        listbox = tk.Listbox(list_frame, font=('Arial', 12), width=40, height=15)
        listbox.pack(side='left', padx=10)
        
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        for category in data['categories']:
            listbox.insert('end', category)
        
        entry_frame = tk.Frame(self.content_frame, bg='white')
        entry_frame.pack(pady=10)
        
        tk.Label(entry_frame, text="Новая категория:", font=('Arial', 11), bg='white').pack(side='left', padx=5)
        category_entry = tk.Entry(entry_frame, font=('Arial', 11), width=25)
        category_entry.pack(side='left', padx=5)
        
        def add_category():
            category = category_entry.get().strip()
            if category and category not in data['categories']:
                data['categories'].append(category)
                self.save_data(data)
                self.admin_categories()
            else:
                messagebox.showwarning("Предупреждение", "Категория уже существует или пустая")
        
        def delete_category():
            selected = listbox.curselection()
            if selected:
                category = listbox.get(selected[0])
                data['categories'].remove(category)
                self.save_data(data)
                self.admin_categories()
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Добавить", command=add_category, 
                 font=('Arial', 10), width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить выбранную", command=delete_category, 
                 font=('Arial', 10), width=18).pack(side='left', padx=5)
    
    # ========== ИНТЕРФЕЙС РАБОТОДАТЕЛЯ ==========
    
    def show_employer_screen(self):
        """Интерфейс работодателя"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text=f"Работодатель: {self.current_user['full_name']}", 
                bg='#2c3e50', fg='white', font=('Arial', 12)).pack(side='left', padx=20, pady=15)
        tk.Button(top_frame, text="Выход", command=self.show_login_screen, 
                 bg='#e74c3c', fg='white', font=('Arial', 10), width=10).pack(side='right', padx=20, pady=15)
        
        menu_frame = tk.Frame(self.root, bg='#34495e', width=200)
        menu_frame.pack(side='left', fill='y')
        menu_frame.pack_propagate(False)
        
        tk.Label(menu_frame, text="МЕНЮ", bg='#34495e', fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=20)
        
        menu_buttons = [
            ("Мои вакансии", self.employer_vacancies),
            ("Добавить вакансию", self.employer_add_vacancy),
            ("Отклики", self.employer_applications),
            ("Профиль", self.employer_profile)
        ]
        
        for text, command in menu_buttons:
            tk.Button(menu_frame, text=text, command=command, bg='#34495e', fg='white',
                     font=('Arial', 11), width=18, anchor='w', relief='flat',
                     activebackground='#2c3e50').pack(pady=5, padx=10)
        
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        self.employer_vacancies()
    
    def employer_vacancies(self):
        """Список вакансий работодателя"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои вакансии", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        data = self.load_data()
        my_vacancies = [v for v in data['vacancies'] if v['employer'] == self.current_user['username']]
        
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Должность', 'Зарплата', 'Категория', 'Статус', 'Дата')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for vacancy in my_vacancies:
            tree.insert('', 'end', values=(
                vacancy['id'],
                vacancy['title'],
                vacancy['salary'],
                vacancy['category'],
                vacancy['status'],
                vacancy['created'][:10]
            ))
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        def delete_vacancy():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите вакансию")
                return
            
            vacancy_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Удалить вакансию?"):
                data['vacancies'] = [v for v in data['vacancies'] if v['id'] != vacancy_id]
                self.save_data(data)
                self.employer_vacancies()
        
        def change_status():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите вакансию")
                return
            
            vacancy_id = tree.item(selected[0])['values'][0]
            for vacancy in data['vacancies']:
                if vacancy['id'] == vacancy_id:
                    vacancy['status'] = 'closed' if vacancy['status'] == 'active' else 'active'
                    break
            self.save_data(data)
            self.employer_vacancies()
        
        tk.Button(btn_frame, text="Удалить", command=delete_vacancy, 
                 font=('Arial', 10), width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Изменить статус", command=change_status, 
                 font=('Arial', 10), width=18).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.employer_vacancies, 
                 font=('Arial', 10), width=15).pack(side='left', padx=5)
    
    def employer_add_vacancy(self):
        """Добавление новой вакансии"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Добавить вакансию", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        form_frame = tk.Frame(self.content_frame, bg='white')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Должность:", font=('Arial', 11), bg='white').grid(row=0, column=0, sticky='e', padx=10, pady=10)
        title_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        title_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(form_frame, text="Зарплата:", font=('Arial', 11), bg='white').grid(row=1, column=0, sticky='e', padx=10, pady=10)
        salary_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        salary_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(form_frame, text="Категория:", font=('Arial', 11), bg='white').grid(row=2, column=0, sticky='e', padx=10, pady=10)
        
        data = self.load_data()
        category_var = tk.StringVar(value=data['categories'][0] if data['categories'] else '')
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, 
                                     values=data['categories'], font=('Arial', 11), width=33, state='readonly')
        category_combo.grid(row=2, column=1, pady=10)
        
        tk.Label(form_frame, text="Описание:", font=('Arial', 11), bg='white').grid(row=3, column=0, sticky='ne', padx=10, pady=10)
        description_text = scrolledtext.ScrolledText(form_frame, font=('Arial', 11), width=35, height=8)
        description_text.grid(row=3, column=1, pady=10)
        
        def save_vacancy():
            title = title_entry.get().strip()
            salary = salary_entry.get().strip()
            category = category_var.get()
            description = description_text.get('1.0', 'end').strip()
            
            if not title or not salary or not description:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            data = self.load_data()
            new_id = max([v['id'] for v in data['vacancies']], default=0) + 1
            
            new_vacancy = {
                'id': new_id,
                'title': title,
                'company': self.current_user.get('company', self.current_user['full_name']),
                'employer': self.current_user['username'],
                'salary': salary,
                'description': description,
                'category': category,
                'status': 'active',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            data['vacancies'].append(new_vacancy)
            self.save_data(data)
            
            messagebox.showinfo("Успех", "Вакансия успешно добавлена")
            self.employer_vacancies()
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Сохранить", command=save_vacancy, 
                 font=('Arial', 11), width=15).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Отмена", command=self.employer_vacancies, 
                 font=('Arial', 11), width=15).pack(side='left', padx=10)
    
    def employer_applications(self):
        """Отклики на вакансии работодателя"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Отклики на мои вакансии", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        data = self.load_data()
        my_vacancy_ids = [v['id'] for v in data['vacancies'] if v['employer'] == self.current_user['username']]
        my_applications = [a for a in data['applications'] if a['vacancy_id'] in my_vacancy_ids]
        
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Вакансия', 'Соискатель', 'Email', 'Статус', 'Дата')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for app in my_applications:
            vacancy = next((v for v in data['vacancies'] if v['id'] == app['vacancy_id']), None)
            vacancy_title = vacancy['title'] if vacancy else 'Неизвестно'
            
            tree.insert('', 'end', values=(
                app['id'],
                vacancy_title,
                app['applicant_name'],
                app['applicant_email'],
                app['status'],
                app['created'][:10]
            ))
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        def change_status(new_status):
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите отклик")
                return
            
            app_id = tree.item(selected[0])['values'][0]
            for app in data['applications']:
                if app['id'] == app_id:
                    app['status'] = new_status
                    break
            self.save_data(data)
            self.employer_applications()
        
        tk.Button(btn_frame, text="Принять", command=lambda: change_status('accepted'), 
                 font=('Arial', 10), width=15, bg='#27ae60', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Отклонить", command=lambda: change_status('rejected'), 
                 font=('Arial', 10), width=15, bg='#e74c3c', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.employer_applications, 
                 font=('Arial', 10), width=15).pack(side='left', padx=5)
    
    def employer_profile(self):
        """Профиль работодателя"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Профиль компании", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        info_frame = tk.Frame(self.content_frame, bg='white')
        info_frame.pack(pady=30)
        
        info = [
            ("Компания:", self.current_user.get('company', 'Не указано')),
            ("Логин:", self.current_user['username']),
            ("Email:", self.current_user.get('email', 'Не указано')),
            ("Роль:", "Работодатель")
        ]
        
        for i, (label, value) in enumerate(info):
            tk.Label(info_frame, text=label, font=('Arial', 12, 'bold'), 
                    bg='white', anchor='w').grid(row=i, column=0, sticky='w', padx=20, pady=10)
            tk.Label(info_frame, text=value, font=('Arial', 12), 
                    bg='white', anchor='w').grid(row=i, column=1, sticky='w', padx=20, pady=10)
    
    # ========== ИНТЕРФЕЙС СОИСКАТЕЛЯ ==========
    
    def show_jobseeker_screen(self):
        """Интерфейс соискателя"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text=f"Соискатель: {self.current_user['full_name']}", 
                bg='#2c3e50', fg='white', font=('Arial', 12)).pack(side='left', padx=20, pady=15)
        tk.Button(top_frame, text="Выход", command=self.show_login_screen, 
                 bg='#e74c3c', fg='white', font=('Arial', 10), width=10).pack(side='right', padx=20, pady=15)
        
        menu_frame = tk.Frame(self.root, bg='#34495e', width=200)
        menu_frame.pack(side='left', fill='y')
        menu_frame.pack_propagate(False)
        
        tk.Label(menu_frame, text="МЕНЮ", bg='#34495e', fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=20)
        
        menu_buttons = [
            ("Вакансии", self.jobseeker_vacancies),
            ("Мои отклики", self.jobseeker_applications),
            ("Резюме", self.jobseeker_resume),
            ("Профиль", self.jobseeker_profile)
        ]
        
        for text, command in menu_buttons:
            tk.Button(menu_frame, text=text, command=command, bg='#34495e', fg='white',
                     font=('Arial', 11), width=18, anchor='w', relief='flat',
                     activebackground='#2c3e50').pack(pady=5, padx=10)
        
        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        self.jobseeker_vacancies()
    
    def jobseeker_vacancies(self):
        """Просмотр вакансий"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Доступные вакансии", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        # Поиск
        search_frame = tk.Frame(self.content_frame, bg='white')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Поиск:", font=('Arial', 11), bg='white').pack(side='left', padx=5)
        search_entry = tk.Entry(search_frame, font=('Arial', 11), width=30)
        search_entry.pack(side='left', padx=5)
        
        data = self.load_data()
        active_vacancies = [v for v in data['vacancies'] if v['status'] == 'active']
        
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Должность', 'Компания', 'Зарплата', 'Категория')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def load_vacancies(search_text=''):
            tree.delete(*tree.get_children())
            for vacancy in active_vacancies:
                if search_text.lower() in vacancy['title'].lower() or \
                   search_text.lower() in vacancy['company'].lower() or \
                   search_text.lower() in vacancy['category'].lower():
                    tree.insert('', 'end', values=(
                        vacancy['id'],
                        vacancy['title'],
                        vacancy['company'],
                        vacancy['salary'],
                        vacancy['category']
                    ))
        
        load_vacancies()
        
        def search():
            load_vacancies(search_entry.get().strip())
        
        tk.Button(search_frame, text="Найти", command=search, 
                 font=('Arial', 10), width=12).pack(side='left', padx=5)
        tk.Button(search_frame, text="Сбросить", command=lambda: [search_entry.delete(0, 'end'), load_vacancies()], 
                 font=('Arial', 10), width=12).pack(side='left', padx=5)
        
        # Детали вакансии
        details_frame = tk.Frame(self.content_frame, bg='white')
        details_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(details_frame, text="Описание вакансии:", font=('Arial', 11, 'bold'), 
                bg='white').pack(anchor='w')
        details_text = scrolledtext.ScrolledText(details_frame, font=('Arial', 10), 
                                                 height=6, wrap='word', state='disabled')
        details_text.pack(fill='both', expand=True, pady=5)
        
        def show_details(event):
            selected = tree.selection()
            if selected:
                vacancy_id = tree.item(selected[0])['values'][0]
                vacancy = next((v for v in active_vacancies if v['id'] == vacancy_id), None)
                if vacancy:
                    details_text.config(state='normal')
                    details_text.delete('1.0', 'end')
                    details_text.insert('1.0', vacancy['description'])
                    details_text.config(state='disabled')
        
        tree.bind('<<TreeviewSelect>>', show_details)
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        def apply_vacancy():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите вакансию")
                return
            
            vacancy_id = tree.item(selected[0])['values'][0]
            
            # Проверка на повторный отклик
            data = self.load_data()
            existing = [a for a in data['applications'] 
                       if a['vacancy_id'] == vacancy_id and a['applicant'] == self.current_user['username']]
            
            if existing:
                messagebox.showinfo("Информация", "Вы уже откликались на эту вакансию")
                return
            
            new_id = max([a['id'] for a in data['applications']], default=0) + 1
            
            new_application = {
                'id': new_id,
                'vacancy_id': vacancy_id,
                'applicant': self.current_user['username'],
                'applicant_name': self.current_user['full_name'],
                'applicant_email': self.current_user.get('email', ''),
                'status': 'pending',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            data['applications'].append(new_application)
            self.save_data(data)
            
            messagebox.showinfo("Успех", "Отклик успешно отправлен")
        
        tk.Button(btn_frame, text="Откликнуться", command=apply_vacancy, 
                 font=('Arial', 11), width=18, bg='#27ae60', fg='white').pack(side='left', padx=5)
    
    def jobseeker_applications(self):
        """Мои отклики"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои отклики", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        data = self.load_data()
        my_applications = [a for a in data['applications'] if a['applicant'] == self.current_user['username']]
        
        tree_frame = tk.Frame(self.content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Вакансия', 'Компания', 'Статус', 'Дата')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        status_colors = {
            'pending': 'Ожидание',
            'accepted': 'Принят',
            'rejected': 'Отклонен'
        }
        
        for app in my_applications:
            vacancy = next((v for v in data['vacancies'] if v['id'] == app['vacancy_id']), None)
            vacancy_title = vacancy['title'] if vacancy else 'Удалена'
            company = vacancy['company'] if vacancy else '-'
            
            tree.insert('', 'end', values=(
                app['id'],
                vacancy_title,
                company,
                status_colors.get(app['status'], app['status']),
                app['created'][:10]
            ))
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=10)
        
        def delete_application():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите отклик")
                return
            
            app_id = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Подтверждение", "Отозвать отклик?"):
                data['applications'] = [a for a in data['applications'] if a['id'] != app_id]
                self.save_data(data)
                self.jobseeker_applications()
        
        tk.Button(btn_frame, text="Отозвать отклик", command=delete_application, 
                 font=('Arial', 10), width=18).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.jobseeker_applications, 
                 font=('Arial', 10), width=15).pack(side='left', padx=5)
    
    def jobseeker_resume(self):
        """Управление резюме"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мое резюме", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        data = self.load_data()
        my_resume = next((r for r in data['resumes'] if r['username'] == self.current_user['username']), None)
        
        form_frame = tk.Frame(self.content_frame, bg='white')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Желаемая должность:", font=('Arial', 11), bg='white').grid(row=0, column=0, sticky='e', padx=10, pady=10)
        position_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        position_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(form_frame, text="Желаемая зарплата:", font=('Arial', 11), bg='white').grid(row=1, column=0, sticky='e', padx=10, pady=10)
        salary_entry = tk.Entry(form_frame, font=('Arial', 11), width=35)
        salary_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(form_frame, text="Опыт работы:", font=('Arial', 11), bg='white').grid(row=2, column=0, sticky='ne', padx=10, pady=10)
        experience_text = scrolledtext.ScrolledText(form_frame, font=('Arial', 11), width=35, height=6)
        experience_text.grid(row=2, column=1, pady=10)
        
        tk.Label(form_frame, text="Навыки:", font=('Arial', 11), bg='white').grid(row=3, column=0, sticky='ne', padx=10, pady=10)
        skills_text = scrolledtext.ScrolledText(form_frame, font=('Arial', 11), width=35, height=6)
        skills_text.grid(row=3, column=1, pady=10)
        
        if my_resume:
            position_entry.insert(0, my_resume['position'])
            salary_entry.insert(0, my_resume['salary'])
            experience_text.insert('1.0', my_resume['experience'])
            skills_text.insert('1.0', my_resume['skills'])
        
        def save_resume():
            position = position_entry.get().strip()
            salary = salary_entry.get().strip()
            experience = experience_text.get('1.0', 'end').strip()
            skills = skills_text.get('1.0', 'end').strip()
            
            if not position or not salary:
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            data = self.load_data()
            
            if my_resume:
                my_resume['position'] = position
                my_resume['salary'] = salary
                my_resume['experience'] = experience
                my_resume['skills'] = skills
                my_resume['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                new_resume = {
                    'username': self.current_user['username'],
                    'full_name': self.current_user['full_name'],
                    'email': self.current_user.get('email', ''),
                    'position': position,
                    'salary': salary,
                    'experience': experience,
                    'skills': skills,
                    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                data['resumes'].append(new_resume)
            
            self.save_data(data)
            messagebox.showinfo("Успех", "Резюме успешно сохранено")
            self.jobseeker_resume()
        
        btn_frame = tk.Frame(self.content_frame, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Сохранить", command=save_resume, 
                 font=('Arial', 11), width=15).pack(side='left', padx=10)
    
    def jobseeker_profile(self):
        """Профиль соискателя"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мой профиль", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        info_frame = tk.Frame(self.content_frame, bg='white')
        info_frame.pack(pady=30)
        
        info = [
            ("ФИО:", self.current_user['full_name']),
            ("Логин:", self.current_user['username']),
            ("Email:", self.current_user.get('email', 'Не указано')),
            ("Роль:", "Соискатель")
        ]
        
        for i, (label, value) in enumerate(info):
            tk.Label(info_frame, text=label, font=('Arial', 12, 'bold'), 
                    bg='white', anchor='w').grid(row=i, column=0, sticky='w', padx=20, pady=10)
            tk.Label(info_frame, text=value, font=('Arial', 12), 
                    bg='white', anchor='w').grid(row=i, column=1, sticky='w', padx=20, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    app = JobExchangeApp(root)
    root.mainloop()