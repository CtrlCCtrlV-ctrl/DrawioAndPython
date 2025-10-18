import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from auth import AuthManager

class AutoshkolaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система 'Автошкола'")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        self.auth = AuthManager()
        self.show_login_window()
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_window(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Автошкола - Вход в систему", font=('Arial', 18, 'bold'), bg='#f0f0f0').grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.entry_username = tk.Entry(frame, font=('Arial', 12), width=20)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12), bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.entry_password = tk.Entry(frame, font=('Arial', 12), width=20, show='*')
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Button(frame, text="Войти", font=('Arial', 12), command=self.login, width=15, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="По умолчанию: admin/admin123, instructor1/instructor123, student1/student123", font=('Arial', 8), bg='#f0f0f0', fg='gray').grid(row=4, column=0, columnspan=2)
    
    def login(self):
        """Обработка входа"""
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if self.auth.authenticate(username, password):
            role = self.auth.current_user['role']
            if role == 'administrator':
                self.show_admin_panel()
            elif role == 'instructor':
                self.show_instructor_panel()
            elif role == 'student':
                self.show_student_panel()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_admin_panel(self):
        """Панель администратора"""
        self.clear_window()
        
        tk.Label(self.root, text=f"Администратор: {self.auth.current_user['full_name']}", font=('Arial', 14, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Управление пользователями", command=self.manage_users, width=25, bg='#2196F3', fg='white').grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Управление инструкторами", command=self.manage_instructors, width=25, bg='#2196F3', fg='white').grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Управление учениками", command=self.manage_students, width=25, bg='#2196F3', fg='white').grid(row=0, column=2, padx=5, pady=5)
        
        tk.Button(btn_frame, text="Управление автомобилями", command=self.manage_cars, width=25, bg='#FF9800', fg='white').grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Просмотр отчетов", command=self.view_reports, width=25, bg='#FF9800', fg='white').grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Выход", command=self.show_login_window, width=25, bg='#f44336', fg='white').grid(row=1, column=2, padx=5, pady=5)
        
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def show_instructor_panel(self):
        """Панель инструктора"""
        self.clear_window()
        
        tk.Label(self.root, text=f"Инструктор: {self.auth.current_user['full_name']}", font=('Arial', 14, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Мое расписание", command=self.view_instructor_schedule, width=20, bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Управление занятиями", command=self.manage_lessons, width=20, bg='#4CAF50', fg='white').grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Выставить оценки", command=self.set_grades, width=20, bg='#4CAF50', fg='white').grid(row=0, column=2, padx=5)
        
        tk.Button(btn_frame, text="Посещаемость", command=self.mark_attendance, width=20, bg='#FF9800', fg='white').grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Мои ученики", command=self.view_my_students, width=20, bg='#FF9800', fg='white').grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Выход", command=self.show_login_window, width=20, bg='#f44336', fg='white').grid(row=1, column=2, padx=5, pady=5)
        
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def show_student_panel(self):
        """Панель ученика"""
        self.clear_window()
        
        tk.Label(self.root, text=f"Ученик: {self.auth.current_user['full_name']}", font=('Arial', 14, 'bold')).pack(pady=10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Мое расписание", command=self.view_student_schedule, width=20, bg='#9C27B0', fg='white').grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Мой прогресс", command=self.view_progress, width=20, bg='#9C27B0', fg='white').grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Мои оценки", command=self.view_student_grades, width=20, bg='#9C27B0', fg='white').grid(row=0, column=2, padx=5)
        
        tk.Button(btn_frame, text="Записаться на занятие", command=self.book_lesson, width=20, bg='#FF9800', fg='white').grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Информация о курсе", command=self.view_course_info, width=20, bg='#FF9800', fg='white').grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Выход", command=self.show_login_window, width=20, bg='#f44336', fg='white').grid(row=1, column=2, padx=5, pady=5)
        
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # === АДМИНИСТРАТОР ===
    
    def manage_users(self):
        """Управление пользователями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление пользователями", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('username', 'role', 'full_name', 'created'), show='headings', height=15)
        tree.heading('username', text='Логин')
        tree.heading('role', text='Роль')
        tree.heading('full_name', text='ФИО')
        tree.heading('created', text='Дата создания')
        
        tree.column('username', width=150)
        tree.column('role', width=150)
        tree.column('full_name', width=250)
        tree.column('created', width=150)
        
        for user in self.auth.get_all_users():
            role_name = {'administrator': 'Администратор', 'instructor': 'Инструктор', 'student': 'Ученик'}.get(user['role'], user['role'])
            tree.insert('', 'end', values=(user['username'], role_name, user['full_name'], user['created']))
        
        tree.pack(pady=10)
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Добавить", command=self.add_user, width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_user(tree), width=15).grid(row=0, column=1, padx=5)
    
    def add_user(self):
        """Добавление пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Логин:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_user = tk.Entry(dialog, width=25)
        entry_user.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        entry_pass = tk.Entry(dialog, width=25, show='*')
        entry_pass.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="ФИО:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        entry_name = tk.Entry(dialog, width=25)
        entry_name.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Роль:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        role_var = tk.StringVar(value='student')
        tk.Radiobutton(dialog, text="Администратор", variable=role_var, value='administrator').grid(row=3, column=1, sticky='w')
        tk.Radiobutton(dialog, text="Инструктор", variable=role_var, value='instructor').grid(row=4, column=1, sticky='w')
        tk.Radiobutton(dialog, text="Ученик", variable=role_var, value='student').grid(row=5, column=1, sticky='w')
        
        def save():
            if self.auth.create_user(entry_user.get(), entry_pass.get(), role_var.get(), entry_name.get()):
                messagebox.showinfo("Успех", "Пользователь добавлен")
                dialog.destroy()
                self.manage_users()
            else:
                messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=6, column=0, columnspan=2, pady=20)
    
    def delete_user(self, tree):
        """Удаление пользователя"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        
        username = tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            self.auth.delete_user(username)
            self.manage_users()
    
    def manage_instructors(self):
        """Управление инструкторами"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление инструкторами", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'name', 'phone', 'experience', 'category', 'car'), show='headings', height=15)
        tree.heading('id', text='ID')
        tree.heading('name', text='ФИО')
        tree.heading('phone', text='Телефон')
        tree.heading('experience', text='Стаж')
        tree.heading('category', text='Категория')
        tree.heading('car', text='Автомобиль')
        
        tree.column('id', width=50)
        tree.column('name', width=200)
        tree.column('phone', width=130)
        tree.column('experience', width=100)
        tree.column('category', width=100)
        tree.column('car', width=180)
        
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for instr in data['instructors']:
                tree.insert('', 'end', values=(instr['id'], instr['name'], instr['phone'], instr['experience'], instr['category'], instr['car']))

            tree.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
        
        tk.Button(self.content_frame, text="Добавить инструктора", command=lambda: self.add_instructor(), width=20).pack(pady=5)
    
    def add_instructor(self):
        """Добавление инструктора"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить инструктора")
        dialog.geometry("400x350")
        
        tk.Label(dialog, text="ФИО:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_name = tk.Entry(dialog, width=25)
        entry_name.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Телефон:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        entry_phone = tk.Entry(dialog, width=25)
        entry_phone.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Стаж:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        entry_exp = tk.Entry(dialog, width=25)
        entry_exp.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Категория:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        entry_cat = tk.Entry(dialog, width=25)
        entry_cat.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Автомобиль:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        entry_car = tk.Entry(dialog, width=25)
        entry_car.grid(row=4, column=1, padx=10, pady=10)
        
        def save():
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            new_id = max([i['id'] for i in data['instructors']], default=0) + 1
            
            data['instructors'].append({
                'id': new_id,
                'name': entry_name.get(),
                'phone': entry_phone.get(),
                'experience': entry_exp.get(),
                'category': entry_cat.get(),
                'car': entry_car.get()
            })
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", "Инструктор добавлен")
            dialog.destroy()
            self.manage_instructors()
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=5, column=0, columnspan=2, pady=20)
    
    def manage_students(self):
        """Управление учениками"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление учениками", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'name', 'phone', 'course', 'instructor', 'start_date', 'status'), show='headings', height=15)
        tree.heading('id', text='ID')
        tree.heading('name', text='ФИО')
        tree.heading('phone', text='Телефон')
        tree.heading('course', text='Курс')
        tree.heading('instructor', text='Инструктор')
        tree.heading('start_date', text='Дата начала')
        tree.heading('status', text='Статус')
        
        tree.column('id', width=40)
        tree.column('name', width=180)
        tree.column('phone', width=120)
        tree.column('course', width=100)
        tree.column('instructor', width=180)
        tree.column('start_date', width=100)
        tree.column('status', width=100)

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for student in data['students']:
                tree.insert('', 'end', values=(student['id'], student['name'], student['phone'], student['course'], student['instructor'], student['start_date'], student['status']))

            tree.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
        
        tk.Button(self.content_frame, text="Добавить ученика", command=self.add_student, width=20).pack(pady=5)
    
    def add_student(self):
        """Добавление ученика"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить ученика")
        dialog.geometry("400x400")
        
        tk.Label(dialog, text="ФИО:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_name = tk.Entry(dialog, width=25)
        entry_name.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Телефон:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        entry_phone = tk.Entry(dialog, width=25)
        entry_phone.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Курс:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        entry_course = tk.Entry(dialog, width=25)
        entry_course.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Инструктор:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        entry_instr = tk.Entry(dialog, width=25)
        entry_instr.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Дата начала:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        entry_date = tk.Entry(dialog, width=25)
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        entry_date.grid(row=4, column=1, padx=10, pady=10)
        
        def save():
            try:
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)

                new_id = max([s['id'] for s in data['students']], default=0) + 1

                data['students'].append({
                    'id': new_id,
                    'name': entry_name.get(),
                    'phone': entry_phone.get(),
                    'course': entry_course.get(),
                    'instructor': entry_instr.get(),
                    'start_date': entry_date.get(),
                    'status': 'Обучается'
                })

                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                messagebox.showinfo("Успех", "Ученик добавлен")
                dialog.destroy()
                self.manage_students()
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл данных не найден")
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=5, column=0, columnspan=2, pady=20)
    
    def manage_cars(self):
        """Управление автомобилями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление автомобилями", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'model', 'number', 'year', 'category', 'status'), show='headings', height=15)
        tree.heading('id', text='ID')
        tree.heading('model', text='Модель')
        tree.heading('number', text='Номер')
        tree.heading('year', text='Год')
        tree.heading('category', text='Категория')
        tree.heading('status', text='Статус')
        
        tree.column('id', width=50)
        tree.column('model', width=200)
        tree.column('number', width=120)
        tree.column('year', width=80)
        tree.column('category', width=100)
        tree.column('status', width=150)

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            for car in data['cars']:
                tree.insert('', 'end', values=(car['id'], car['model'], car['number'], car['year'], car['category'], car['status']))

            tree.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
    
    def view_reports(self):
        """Просмотр отчетов"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Статистика и отчеты", font=('Arial', 12, 'bold')).pack(pady=5)

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            report_text = f"""
            Общее количество учеников: {len(data['students'])}
            Общее количество инструкторов: {len(data['instructors'])}
            Общее количество автомобилей: {len(data['cars'])}
            Всего занятий: {len(data['lessons'])}
            Всего оценок: {len(data['grades'])}
            """

            tk.Label(self.content_frame, text=report_text, font=('Arial', 11), justify='left').pack(pady=20)
        except FileNotFoundError:
            tk.Label(self.content_frame, text="Файл данных не найден", font=('Arial', 11)).pack(pady=20)
    
    # === ИНСТРУКТОР ===
    
    def view_instructor_schedule(self):
        """Расписание инструктора"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мое расписание", font=('Arial', 12, 'bold')).pack(pady=5)

        tree = ttk.Treeview(self.content_frame, columns=('id', 'student', 'date', 'time', 'type', 'status'), show='headings', height=15)
        tree.heading('id', text='ID')
        tree.heading('student', text='Ученик')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('type', text='Тип')
        tree.heading('status', text='Статус')

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            instructor_name = self.auth.current_user['full_name']
            for lesson in data['lessons']:
                if lesson['instructor'] == instructor_name:
                    tree.insert('', 'end', values=(lesson['id'], lesson['student'], lesson['date'], lesson['time'], lesson['type'], lesson['status']))

            tree.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
    
    def manage_lessons(self):
        """Управление занятиями"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Управление занятиями", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'student', 'date', 'time', 'type', 'status'), show='headings', height=12)
        tree.heading('id', text='ID')
        tree.heading('student', text='Ученик')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('type', text='Тип')
        tree.heading('status', text='Статус')

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            instructor_name = self.auth.current_user['full_name']
            for lesson in data['lessons']:
                if lesson['instructor'] == instructor_name:
                    tree.insert('', 'end', values=(lesson['id'], lesson['student'], lesson['date'], lesson['time'], lesson['type'], lesson['status']))

            tree.pack(pady=10)

            tk.Button(self.content_frame, text="Добавить занятие", command=self.add_lesson, width=20).pack(pady=5)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
    
    def add_lesson(self):
        """Добавление занятия"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить занятие")
        dialog.geometry("400x350")
        
        tk.Label(dialog, text="Ученик:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_student = tk.Entry(dialog, width=25)
        entry_student.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Дата (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        entry_date = tk.Entry(dialog, width=25)
        entry_date.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Время:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        entry_time = tk.Entry(dialog, width=25)
        entry_time.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Тип:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        type_var = tk.StringVar(value='Практика')
        ttk.Combobox(dialog, textvariable=type_var, values=['Теория', 'Практика'], width=22, state='readonly').grid(row=3, column=1, padx=10, pady=10)
        
        def save():
            try:
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)

                new_id = max([l['id'] for l in data['lessons']], default=0) + 1

                data['lessons'].append({
                    'id': new_id,
                    'student': entry_student.get(),
                    'instructor': self.auth.current_user['full_name'],
                    'date': entry_date.get(),
                    'time': entry_time.get(),
                    'type': type_var.get(),
                    'status': 'Запланировано'
                })

                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                messagebox.showinfo("Успех", "Занятие добавлено")
                dialog.destroy()
                self.manage_lessons()
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл данных не найден")
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=4, column=0, columnspan=2, pady=20)
    
    def set_grades(self):
        """Выставление оценок"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Выставление оценок", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'student', 'subject', 'grade', 'date'), show='headings', height=12)
        tree.heading('id', text='ID')
        tree.heading('student', text='Ученик')
        tree.heading('subject', text='Предмет')
        tree.heading('grade', text='Оценка')
        tree.heading('date', text='Дата')

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            instructor_name = self.auth.current_user['full_name']
            for grade in data['grades']:
                if grade['instructor'] == instructor_name:
                    tree.insert('', 'end', values=(grade['id'], grade['student'], grade['subject'], grade['grade'], grade['date']))

            tree.pack(pady=10)

            tk.Button(self.content_frame, text="Добавить оценку", command=self.add_grade, width=20).pack(pady=5)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
    
    def add_grade(self):
        """Добавление оценки"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить оценку")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Ученик:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        entry_student = tk.Entry(dialog, width=25)
        entry_student.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Предмет:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        entry_subject = tk.Entry(dialog, width=25)
        entry_subject.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Оценка:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        grade_var = tk.StringVar(value='5')
        ttk.Combobox(dialog, textvariable=grade_var, values=['2', '3', '4', '5'], width=22, state='readonly').grid(row=2, column=1, padx=10, pady=10)
        
        def save():
            try:
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)

                new_id = max([g['id'] for g in data['grades']], default=0) + 1

                data['grades'].append({
                    'id': new_id,
                    'student': entry_student.get(),
                    'subject': entry_subject.get(),
                    'grade': grade_var.get(),
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'instructor': self.auth.current_user['full_name']
                })

                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                messagebox.showinfo("Успех", "Оценка добавлена")
                dialog.destroy()
                self.set_grades()
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл данных не найден")
        
        tk.Button(dialog, text="Сохранить", command=save, width=15).grid(row=3, column=0, columnspan=2, pady=20)
    
    def mark_attendance(self):
        """Отметка посещаемости"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Отметка посещаемости", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Label(self.content_frame, text="Функция находится в разработке", font=('Arial', 10)).pack(pady=20)
    
    def view_my_students(self):
        """Просмотр учеников инструктора"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои ученики", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'name', 'phone', 'course', 'status'), show='headings', height=15)
        tree.heading('id', text='ID')
        tree.heading('name', text='ФИО')
        tree.heading('phone', text='Телефон')
        tree.heading('course', text='Курс')
        tree.heading('status', text='Статус')

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            instructor_name = self.auth.current_user['full_name']
            for student in data['students']:
                if student['instructor'] == instructor_name:
                    tree.insert('', 'end', values=(student['id'], student['name'], student['phone'], student['course'], student['status']))

            tree.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
    
    # === УЧЕНИК ===
    
    def view_student_schedule(self):
        """Расписание ученика"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мое расписание", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'instructor', 'date', 'time', 'type', 'status'), show='headings', height=15)
        tree.heading('id', text='ID')
        tree.heading('instructor', text='Инструктор')
        tree.heading('date', text='Дата')
        tree.heading('time', text='Время')
        tree.heading('type', text='Тип')
        tree.heading('status', text='Статус')

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            student_name = self.auth.current_user['full_name']
            for lesson in data['lessons']:
                if lesson['student'] == student_name:
                    tree.insert('', 'end', values=(lesson['id'], lesson['instructor'], lesson['date'], lesson['time'], lesson['type'], lesson['status']))

            tree.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
    
    def view_progress(self):
        """Просмотр прогресса"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мой прогресс", font=('Arial', 12, 'bold')).pack(pady=5)

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            student_name = self.auth.current_user['full_name']

            lessons_count = len([l for l in data['lessons'] if l['student'] == student_name])
            grades_count = len([g for g in data['grades'] if g['student'] == student_name])

            avg_grade = 0
            if grades_count > 0:
                grades = [int(g['grade']) for g in data['grades'] if g['student'] == student_name]
                avg_grade = sum(grades) / len(grades)

            progress_text = f"""
            Пройдено занятий: {lessons_count}
            Получено оценок: {grades_count}
            Средний балл: {avg_grade:.2f}
            """

            tk.Label(self.content_frame, text=progress_text, font=('Arial', 11), justify='left').pack(pady=20)
        except FileNotFoundError:
            tk.Label(self.content_frame, text="Файл данных не найден", font=('Arial', 11)).pack(pady=20)
    
    def view_student_grades(self):
        """Просмотр оценок ученика"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Мои оценки", font=('Arial', 12, 'bold')).pack(pady=5)
        
        tree = ttk.Treeview(self.content_frame, columns=('id', 'subject', 'grade', 'date', 'instructor'), show='headings', height=15)
        tree.heading('id', text='ID')
        tree.heading('subject', text='Предмет')
        tree.heading('grade', text='Оценка')
        tree.heading('date', text='Дата')
        tree.heading('instructor', text='Инструктор')

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            student_name = self.auth.current_user['full_name']
            for grade in data['grades']:
                if grade['student'] == student_name:
                    tree.insert('', 'end', values=(grade['id'], grade['subject'], grade['grade'], grade['date'], grade['instructor']))

            tree.pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл данных не найден")
            return
    
    def book_lesson(self):
        """Запись на занятие"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Запись на занятие", font=('Arial', 12, 'bold')).pack(pady=5)
        tk.Label(self.content_frame, text="Свяжитесь с администратором для записи на занятие", font=('Arial', 10)).pack(pady=20)
    
    def view_course_info(self):
        """Информация о курсе"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.content_frame, text="Информация о курсе", font=('Arial', 12, 'bold')).pack(pady=5)

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            student_name = self.auth.current_user['full_name']
            student_info = None

            for student in data['students']:
                if student['name'] == student_name:
                    student_info = student
                    break

            if student_info:
                info_text = f"""
                Курс: {student_info['course']}
                Инструктор: {student_info['instructor']}
                Дата начала: {student_info['start_date']}
                Статус: {student_info['status']}
                """
                tk.Label(self.content_frame, text=info_text, font=('Arial', 11), justify='left').pack(pady=20)
            else:
                tk.Label(self.content_frame, text="Информация не найдена", font=('Arial', 11)).pack(pady=20)
        except FileNotFoundError:
            tk.Label(self.content_frame, text="Файл данных не найден", font=('Arial', 11)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoshkolaApp(root)
    root.mainloop()