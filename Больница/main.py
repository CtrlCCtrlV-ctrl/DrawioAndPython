import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import auth

class HospitalSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Информационная система 'Больница'")
        self.root.geometry("900x600")
        self.current_user = None
        self.data = self.load_data()
        
        self.show_login()
        
    def load_data(self):
        """Загрузка данных из файла"""
        if not os.path.exists('data.json'):
            default_data = {
                "doctors": [
                    {
                        "id": 1,
                        "name": "Иванов Иван Иванович",
                        "specialization": "Терапевт",
                        "phone": "+7-900-123-45-67",
                        "cabinet": "101"
                    },
                    {
                        "id": 2,
                        "name": "Сидорова Мария Петровна",
                        "specialization": "Кардиолог",
                        "phone": "+7-900-234-56-78",
                        "cabinet": "205"
                    }
                ],
                "patients": [
                    {
                        "id": 1,
                        "name": "Петров Петр Петрович",
                        "birth_date": "1990-05-15",
                        "phone": "+7-900-345-67-89",
                        "address": "г. Москва, ул. Ленина, д. 10"
                    }
                ],
                "appointments": [
                    {
                        "id": 1,
                        "patient_id": 1,
                        "doctor_id": 1,
                        "date": "2024-01-20",
                        "time": "10:00",
                        "status": "scheduled",
                        "diagnosis": "",
                        "treatment": ""
                    }
                ]
            }
            self.save_data(default_data)
            return default_data
        
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data=None):
        """Сохранение данных в файл"""
        if data is not None:
            self.data = data
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Окно авторизации"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(frame, text="Вход в систему", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', pady=10)
        username_entry = tk.Entry(frame, font=('Arial', 12), width=20)
        username_entry.grid(row=1, column=1, pady=10)
        
        tk.Label(frame, text="Пароль:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', pady=10)
        password_entry = tk.Entry(frame, font=('Arial', 12), width=20, show='*')
        password_entry.grid(row=2, column=1, pady=10)
        
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            user = auth.authenticate(username, password)
            if user:
                self.current_user = user
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        
        tk.Button(frame, text="Войти", font=('Arial', 12), width=15, command=login).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка
        hint_text = "Демо-доступы:\nadmin/admin123\ndoctor1/doctor123\npatient1/patient123"
        tk.Label(frame, text=hint_text, font=('Arial', 9), fg='gray', justify='left').grid(row=4, column=0, columnspan=2)
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"Пользователь: {self.current_user['name']}", 
                bg='#2c3e50', fg='white', font=('Arial', 12)).pack(side='left', padx=20, pady=15)
        
        tk.Label(top_frame, text=f"Роль: {self.get_role_name()}", 
                bg='#2c3e50', fg='white', font=('Arial', 12)).pack(side='left', pady=15)
        
        tk.Button(top_frame, text="Выход", command=self.logout, bg='#e74c3c', fg='white').pack(side='right', padx=20, pady=15)
        
        # Контент в зависимости от роли
        if self.current_user['role'] == 'administrator':
            self.show_admin_panel()
        elif self.current_user['role'] == 'doctor':
            self.show_doctor_panel()
        elif self.current_user['role'] == 'patient':
            self.show_patient_panel()
    
    def get_role_name(self):
        """Получение названия роли на русском"""
        roles = {
            'administrator': 'Администратор',
            'doctor': 'Врач',
            'patient': 'Пациент'
        }
        return roles.get(self.current_user['role'], 'Неизвестно')
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.show_login()
    
    # ========== ПАНЕЛЬ АДМИНИСТРАТОРА ==========
    
    def show_admin_panel(self):
        """Панель администратора"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладки
        tab_users = tk.Frame(notebook)
        tab_doctors = tk.Frame(notebook)
        tab_patients = tk.Frame(notebook)
        tab_appointments = tk.Frame(notebook)
        tab_stats = tk.Frame(notebook)
        
        notebook.add(tab_users, text='Пользователи')
        notebook.add(tab_doctors, text='Врачи')
        notebook.add(tab_patients, text='Пациенты')
        notebook.add(tab_appointments, text='Приемы')
        notebook.add(tab_stats, text='Статистика')
        
        self.show_users_tab(tab_users)
        self.show_doctors_tab(tab_doctors)
        self.show_patients_tab(tab_patients)
        self.show_appointments_tab(tab_appointments)
        self.show_stats_tab(tab_stats)
    
    def show_users_tab(self, parent):
        """Вкладка управления пользователями"""
        # Кнопки управления
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Добавить пользователя", command=self.add_user_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_users_table(tree)).pack(side='left', padx=5)
        
        # Таблица пользователей
        columns = ('ID', 'Логин', 'Имя', 'Роль', 'Дата создания')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_users_table(tree)
    
    def refresh_users_table(self, tree):
        """Обновление таблицы пользователей"""
        for item in tree.get_children():
            tree.delete(item)
        
        users_data = auth.load_users()
        for user in users_data['users']:
            tree.insert('', 'end', values=(
                user['id'],
                user['username'],
                user.get('name', 'N/A'),
                self.get_role_name_by_code(user['role']),
                user['created']
            ))
    
    def get_role_name_by_code(self, code):
        """Получение названия роли"""
        roles = {
            'administrator': 'Администратор',
            'doctor': 'Врач',
            'patient': 'Пациент'
        }
        return roles.get(code, code)
    
    def add_user_dialog(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление пользователя")
        dialog.geometry("400x350")
        
        tk.Label(dialog, text="Логин:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        username_entry = tk.Entry(dialog, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        password_entry = tk.Entry(dialog, width=30, show='*')
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Имя:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Роль:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        role_var = tk.StringVar(value='patient')
        roles = [('Администратор', 'administrator'), ('Врач', 'doctor'), ('Пациент', 'patient')]
        for i, (text, value) in enumerate(roles):
            tk.Radiobutton(dialog, text=text, variable=role_var, value=value).grid(row=3+i, column=1, sticky='w', padx=10)
        
        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            name = name_entry.get()
            role = role_var.get()
            
            if not all([username, password, name]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            success, message = auth.create_user(username, password, role, name)
            if success:
                messagebox.showinfo("Успех", message)
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", message)
        
        tk.Button(dialog, text="Сохранить", command=save_user).grid(row=7, column=0, columnspan=2, pady=20)
    
    def show_doctors_tab(self, parent):
        """Вкладка управления врачами"""
        # Кнопки управления
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Добавить врача", command=self.add_doctor_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_doctor(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_doctors_table(tree)).pack(side='left', padx=5)
        
        # Таблица врачей
        columns = ('ID', 'ФИО', 'Специализация', 'Телефон', 'Кабинет')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_doctors_table(tree)
    
    def refresh_doctors_table(self, tree):
        """Обновление таблицы врачей"""
        for item in tree.get_children():
            tree.delete(item)
        
        for doctor in self.data['doctors']:
            tree.insert('', 'end', values=(
                doctor['id'],
                doctor['name'],
                doctor['specialization'],
                doctor['phone'],
                doctor.get('cabinet', 'N/A')
            ))
    
    def add_doctor_dialog(self):
        """Диалог добавления врача"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление врача")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="ФИО:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Специализация:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        spec_entry = tk.Entry(dialog, width=30)
        spec_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Телефон:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        phone_entry = tk.Entry(dialog, width=30)
        phone_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Кабинет:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        cabinet_entry = tk.Entry(dialog, width=30)
        cabinet_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save_doctor():
            name = name_entry.get()
            spec = spec_entry.get()
            phone = phone_entry.get()
            cabinet = cabinet_entry.get()
            
            if not all([name, spec, phone, cabinet]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            new_doctor = {
                "id": max([d['id'] for d in self.data['doctors']]) + 1 if self.data['doctors'] else 1,
                "name": name,
                "specialization": spec,
                "phone": phone,
                "cabinet": cabinet
            }
            
            self.data['doctors'].append(new_doctor)
            self.save_data()
            messagebox.showinfo("Успех", "Врач добавлен")
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_doctor).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_doctor(self, tree):
        """Удаление врача"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите врача для удаления")
            return
        
        item = tree.item(selected[0])
        doctor_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранного врача?"):
            self.data['doctors'] = [d for d in self.data['doctors'] if d['id'] != doctor_id]
            self.save_data()
            self.refresh_doctors_table(tree)
    
    def show_patients_tab(self, parent):
        """Вкладка управления пациентами"""
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Добавить пациента", command=self.add_patient_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_patient(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_patients_table(tree)).pack(side='left', padx=5)
        
        columns = ('ID', 'ФИО', 'Дата рождения', 'Телефон', 'Адрес')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_patients_table(tree)
    
    def refresh_patients_table(self, tree):
        """Обновление таблицы пациентов"""
        for item in tree.get_children():
            tree.delete(item)
        
        for patient in self.data['patients']:
            tree.insert('', 'end', values=(
                patient['id'],
                patient['name'],
                patient['birth_date'],
                patient['phone'],
                patient.get('address', 'N/A')
            ))
    
    def add_patient_dialog(self):
        """Диалог добавления пациента"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление пациента")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="ФИО:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Дата рождения:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        birth_entry = tk.Entry(dialog, width=30)
        birth_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Label(dialog, text="(ГГГГ-ММ-ДД)", font=('Arial', 8)).grid(row=1, column=2, sticky='w')
        
        tk.Label(dialog, text="Телефон:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        phone_entry = tk.Entry(dialog, width=30)
        phone_entry.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Адрес:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        address_entry = tk.Entry(dialog, width=30)
        address_entry.grid(row=3, column=1, padx=10, pady=10)
        
        def save_patient():
            name = name_entry.get()
            birth = birth_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()
            
            if not all([name, birth, phone, address]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            new_patient = {
                "id": max([p['id'] for p in self.data['patients']]) + 1 if self.data['patients'] else 1,
                "name": name,
                "birth_date": birth,
                "phone": phone,
                "address": address
            }
            
            self.data['patients'].append(new_patient)
            self.save_data()
            messagebox.showinfo("Успех", "Пациент добавлен")
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_patient).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_patient(self, tree):
        """Удаление пациента"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пациента для удаления")
            return
        
        item = tree.item(selected[0])
        patient_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранного пациента?"):
            self.data['patients'] = [p for p in self.data['patients'] if p['id'] != patient_id]
            self.save_data()
            self.refresh_patients_table(tree)
    
    def show_appointments_tab(self, parent):
        """Вкладка управления приемами"""
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(btn_frame, text="Добавить прием", command=self.add_appointment_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_appointment(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_appointments_table(tree)).pack(side='left', padx=5)
        
        columns = ('ID', 'Пациент', 'Врач', 'Дата', 'Время', 'Статус')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_appointments_table(tree)
    
    def refresh_appointments_table(self, tree):
        """Обновление таблицы приемов"""
        for item in tree.get_children():
            tree.delete(item)
        
        for appointment in self.data['appointments']:
            patient_name = self.get_patient_name(appointment['patient_id'])
            doctor_name = self.get_doctor_name(appointment['doctor_id'])
            
            tree.insert('', 'end', values=(
                appointment['id'],
                patient_name,
                doctor_name,
                appointment['date'],
                appointment['time'],
                self.get_status_name(appointment['status'])
            ))
    
    def get_patient_name(self, patient_id):
        """Получение имени пациента по ID"""
        for patient in self.data['patients']:
            if patient['id'] == patient_id:
                return patient['name']
        return 'N/A'
    
    def get_doctor_name(self, doctor_id):
        """Получение имени врача по ID"""
        for doctor in self.data['doctors']:
            if doctor['id'] == doctor_id:
                return doctor['name']
        return 'N/A'
    
    def get_status_name(self, status):
        """Получение названия статуса"""
        statuses = {
            'scheduled': 'Запланирован',
            'completed': 'Завершен',
            'cancelled': 'Отменен'
        }
        return statuses.get(status, status)
    
    def add_appointment_dialog(self):
        """Диалог добавления приема"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление приема")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Пациент:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(dialog, textvariable=patient_var, width=28, state='readonly')
        patient_combo['values'] = [f"{p['id']} - {p['name']}" for p in self.data['patients']]
        patient_combo.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Врач:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(dialog, textvariable=doctor_var, width=28, state='readonly')
        doctor_combo['values'] = [f"{d['id']} - {d['name']}" for d in self.data['doctors']]
        doctor_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Дата:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        date_entry = tk.Entry(dialog, width=30)
        date_entry.grid(row=2, column=1, padx=10, pady=10)
        tk.Label(dialog, text="(ГГГГ-ММ-ДД)", font=('Arial', 8)).grid(row=2, column=2, sticky='w')
        
        tk.Label(dialog, text="Время:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        time_entry = tk.Entry(dialog, width=30)
        time_entry.grid(row=3, column=1, padx=10, pady=10)
        tk.Label(dialog, text="(ЧЧ:ММ)", font=('Arial', 8)).grid(row=3, column=2, sticky='w')
        
        def save_appointment():
            patient = patient_var.get()
            doctor = doctor_var.get()
            date = date_entry.get()
            time = time_entry.get()
            
            if not all([patient, doctor, date, time]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            patient_id = int(patient.split(' - ')[0])
            doctor_id = int(doctor.split(' - ')[0])
            
            new_appointment = {
                "id": max([a['id'] for a in self.data['appointments']]) + 1 if self.data['appointments'] else 1,
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "date": date,
                "time": time,
                "status": "scheduled",
                "diagnosis": "",
                "treatment": ""
            }
            
            self.data['appointments'].append(new_appointment)
            self.save_data()
            messagebox.showinfo("Успех", "Прием добавлен")
            dialog.destroy()
        
        tk.Button(dialog, text="Сохранить", command=save_appointment).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_appointment(self, tree):
        """Удаление приема"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите прием для удаления")
            return
        
        item = tree.item(selected[0])
        appointment_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный прием?"):
            self.data['appointments'] = [a for a in self.data['appointments'] if a['id'] != appointment_id]
            self.save_data()
            self.refresh_appointments_table(tree)
    
    def show_stats_tab(self, parent):
        """Вкладка статистики"""
        stats_frame = tk.Frame(parent, padx=20, pady=20)
        stats_frame.pack(fill='both', expand=True)
        
        tk.Label(stats_frame, text="Статистика системы", font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Подсчет статистики
        total_doctors = len(self.data['doctors'])
        total_patients = len(self.data['patients'])
        total_appointments = len(self.data['appointments'])
        scheduled = len([a for a in self.data['appointments'] if a['status'] == 'scheduled'])
        completed = len([a for a in self.data['appointments'] if a['status'] == 'completed'])
        
        stats_text = f"""
        Всего врачей: {total_doctors}
        Всего пациентов: {total_patients}
        Всего приемов: {total_appointments}
        
        Запланировано приемов: {scheduled}
        Завершено приемов: {completed}
        """
        
        tk.Label(stats_frame, text=stats_text, font=('Arial', 14), justify='left').pack(pady=20)
    
    # ========== ПАНЕЛЬ ВРАЧА ==========
    
    def show_doctor_panel(self):
        """Панель врача"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        tab_schedule = tk.Frame(notebook)
        tab_patients = tk.Frame(notebook)
        tab_appointments = tk.Frame(notebook)
        
        notebook.add(tab_schedule, text='Мое расписание')
        notebook.add(tab_patients, text='Пациенты')
        notebook.add(tab_appointments, text='Работа с приемами')
        
        self.show_doctor_schedule_tab(tab_schedule)
        self.show_doctor_patients_tab(tab_patients)
        self.show_doctor_appointments_tab(tab_appointments)
    
    def show_doctor_schedule_tab(self, parent):
        """Расписание врача"""
        doctor_id = self.current_user.get('doctor_id')
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(btn_frame, text="Мои приемы", font=('Arial', 14, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_doctor_schedule(tree, doctor_id)).pack(side='right', padx=5)
        
        columns = ('ID', 'Пациент', 'Дата', 'Время', 'Статус')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_doctor_schedule(tree, doctor_id)
    
    def refresh_doctor_schedule(self, tree, doctor_id):
        """Обновление расписания врача"""
        for item in tree.get_children():
            tree.delete(item)
        
        doctor_appointments = [a for a in self.data['appointments'] if a['doctor_id'] == doctor_id]
        
        for appointment in doctor_appointments:
            patient_name = self.get_patient_name(appointment['patient_id'])
            
            tree.insert('', 'end', values=(
                appointment['id'],
                patient_name,
                appointment['date'],
                appointment['time'],
                self.get_status_name(appointment['status'])
            ))
    
    def show_doctor_patients_tab(self, parent):
        """Список всех пациентов для врача"""
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(btn_frame, text="Список пациентов", font=('Arial', 14, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=lambda: self.refresh_patients_table(tree)).pack(side='right', padx=5)
        
        columns = ('ID', 'ФИО', 'Дата рождения', 'Телефон')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_patients_table(tree)
    
    def show_doctor_appointments_tab(self, parent):
        """Работа с приемами (диагноз, лечение)"""
        doctor_id = self.current_user.get('doctor_id')
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(btn_frame, text="Мои приемы", font=('Arial', 14, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Добавить диагноз/лечение", 
                 command=lambda: self.add_diagnosis_dialog(tree, doctor_id)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Завершить прием", 
                 command=lambda: self.complete_appointment(tree)).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", 
                 command=lambda: self.refresh_doctor_appointments(tree, doctor_id)).pack(side='right', padx=5)
        
        columns = ('ID', 'Пациент', 'Дата', 'Время', 'Диагноз', 'Лечение', 'Статус')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_doctor_appointments(tree, doctor_id)
    
    def refresh_doctor_appointments(self, tree, doctor_id):
        """Обновление приемов врача"""
        for item in tree.get_children():
            tree.delete(item)
        
        doctor_appointments = [a for a in self.data['appointments'] if a['doctor_id'] == doctor_id]
        
        for appointment in doctor_appointments:
            patient_name = self.get_patient_name(appointment['patient_id'])
            
            tree.insert('', 'end', values=(
                appointment['id'],
                patient_name,
                appointment['date'],
                appointment['time'],
                appointment.get('diagnosis', ''),
                appointment.get('treatment', ''),
                self.get_status_name(appointment['status'])
            ))
    
    def add_diagnosis_dialog(self, tree, doctor_id):
        """Диалог добавления диагноза и лечения"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите прием")
            return
        
        item = tree.item(selected[0])
        appointment_id = item['values'][0]
        
        # Найти прием
        appointment = None
        for a in self.data['appointments']:
            if a['id'] == appointment_id:
                appointment = a
                break
        
        if not appointment:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление диагноза и лечения")
        dialog.geometry("500x300")
        
        tk.Label(dialog, text="Диагноз:").grid(row=0, column=0, padx=10, pady=10, sticky='ne')
        diagnosis_text = tk.Text(dialog, width=40, height=5)
        diagnosis_text.grid(row=0, column=1, padx=10, pady=10)
        diagnosis_text.insert('1.0', appointment.get('diagnosis', ''))
        
        tk.Label(dialog, text="Лечение:").grid(row=1, column=0, padx=10, pady=10, sticky='ne')
        treatment_text = tk.Text(dialog, width=40, height=5)
        treatment_text.grid(row=1, column=1, padx=10, pady=10)
        treatment_text.insert('1.0', appointment.get('treatment', ''))
        
        def save_diagnosis():
            diagnosis = diagnosis_text.get('1.0', 'end-1c')
            treatment = treatment_text.get('1.0', 'end-1c')
            
            appointment['diagnosis'] = diagnosis
            appointment['treatment'] = treatment
            
            self.save_data()
            messagebox.showinfo("Успех", "Данные сохранены")
            dialog.destroy()
            self.refresh_doctor_appointments(tree, doctor_id)
        
        tk.Button(dialog, text="Сохранить", command=save_diagnosis).grid(row=2, column=0, columnspan=2, pady=20)
    
    def complete_appointment(self, tree):
        """Завершение приема"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите прием")
            return
        
        item = tree.item(selected[0])
        appointment_id = item['values'][0]
        
        for appointment in self.data['appointments']:
            if appointment['id'] == appointment_id:
                appointment['status'] = 'completed'
                self.save_data()
                messagebox.showinfo("Успех", "Прием завершен")
                break
    
    # ========== ПАНЕЛЬ ПАЦИЕНТА ==========
    
    def show_patient_panel(self):
        """Панель пациента"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        tab_info = tk.Frame(notebook)
        tab_appointments = tk.Frame(notebook)
        tab_history = tk.Frame(notebook)
        tab_new = tk.Frame(notebook)
        
        notebook.add(tab_info, text='Мои данные')
        notebook.add(tab_appointments, text='Мои приемы')
        notebook.add(tab_history, text='История визитов')
        notebook.add(tab_new, text='Записаться на прием')
        
        self.show_patient_info_tab(tab_info)
        self.show_patient_appointments_tab(tab_appointments)
        self.show_patient_history_tab(tab_history)
        self.show_patient_new_appointment_tab(tab_new)
    
    def show_patient_info_tab(self, parent):
        """Информация о пациенте"""
        patient_id = self.current_user.get('patient_id')
        patient = None
        
        for p in self.data['patients']:
            if p['id'] == patient_id:
                patient = p
                break
        
        if not patient:
            tk.Label(parent, text="Данные пациента не найдены").pack(pady=20)
            return
        
        info_frame = tk.Frame(parent, padx=30, pady=30)
        info_frame.pack(fill='both', expand=True)
        
        tk.Label(info_frame, text="Мои данные", font=('Arial', 16, 'bold')).pack(pady=20)
        
        info_text = f"""
        ФИО: {patient['name']}
        Дата рождения: {patient['birth_date']}
        Телефон: {patient['phone']}
        Адрес: {patient.get('address', 'N/A')}
        """
        
        tk.Label(info_frame, text=info_text, font=('Arial', 12), justify='left').pack(pady=10)
    
    def show_patient_appointments_tab(self, parent):
        """Текущие приемы пациента"""
        patient_id = self.current_user.get('patient_id')
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(btn_frame, text="Мои предстоящие приемы", font=('Arial', 14, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", 
                 command=lambda: self.refresh_patient_appointments(tree, patient_id)).pack(side='right', padx=5)
        
        columns = ('ID', 'Врач', 'Специализация', 'Дата', 'Время', 'Статус')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_patient_appointments(tree, patient_id)
    
    def refresh_patient_appointments(self, tree, patient_id):
        """Обновление приемов пациента"""
        for item in tree.get_children():
            tree.delete(item)
        
        patient_appointments = [a for a in self.data['appointments'] 
                              if a['patient_id'] == patient_id and a['status'] == 'scheduled']
        
        for appointment in patient_appointments:
            doctor = None
            for d in self.data['doctors']:
                if d['id'] == appointment['doctor_id']:
                    doctor = d
                    break
            
            tree.insert('', 'end', values=(
                appointment['id'],
                doctor['name'] if doctor else 'N/A',
                doctor['specialization'] if doctor else 'N/A',
                appointment['date'],
                appointment['time'],
                self.get_status_name(appointment['status'])
            ))
    
    def show_patient_history_tab(self, parent):
        """История визитов пациента"""
        patient_id = self.current_user.get('patient_id')
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(btn_frame, text="История моих визитов", font=('Arial', 14, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", 
                 command=lambda: self.refresh_patient_history(tree, patient_id)).pack(side='right', padx=5)
        
        columns = ('Дата', 'Врач', 'Диагноз', 'Лечение')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.refresh_patient_history(tree, patient_id)
    
    def refresh_patient_history(self, tree, patient_id):
        """Обновление истории визитов"""
        for item in tree.get_children():
            tree.delete(item)
        
        completed_appointments = [a for a in self.data['appointments'] 
                                if a['patient_id'] == patient_id and a['status'] == 'completed']
        
        for appointment in completed_appointments:
            doctor_name = self.get_doctor_name(appointment['doctor_id'])
            
            tree.insert('', 'end', values=(
                f"{appointment['date']} {appointment['time']}",
                doctor_name,
                appointment.get('diagnosis', 'Нет данных'),
                appointment.get('treatment', 'Нет данных')
            ))
    
    def show_patient_new_appointment_tab(self, parent):
        """Запись на новый прием"""
        patient_id = self.current_user.get('patient_id')
        
        form_frame = tk.Frame(parent, padx=30, pady=30)
        form_frame.pack(fill='both', expand=True)
        
        tk.Label(form_frame, text="Записаться на прием", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(form_frame, text="Выберите врача:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        doctor_var = tk.StringVar()
        doctor_combo = ttk.Combobox(form_frame, textvariable=doctor_var, width=40, state='readonly')
        doctor_combo['values'] = [f"{d['id']} - {d['name']} ({d['specialization']})" for d in self.data['doctors']]
        doctor_combo.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(form_frame, text="Дата:", font=('Arial', 12)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        date_entry = tk.Entry(form_frame, width=42, font=('Arial', 10))
        date_entry.grid(row=2, column=1, padx=10, pady=10)
        tk.Label(form_frame, text="Формат: ГГГГ-ММ-ДД", font=('Arial', 8), fg='gray').grid(row=2, column=2, sticky='w')
        
        tk.Label(form_frame, text="Время:", font=('Arial', 12)).grid(row=3, column=0, sticky='e', padx=10, pady=10)
        time_entry = tk.Entry(form_frame, width=42, font=('Arial', 10))
        time_entry.grid(row=3, column=1, padx=10, pady=10)
        tk.Label(form_frame, text="Формат: ЧЧ:ММ", font=('Arial', 8), fg='gray').grid(row=3, column=2, sticky='w')
        
        def create_appointment():
            doctor = doctor_var.get()
            date = date_entry.get()
            time = time_entry.get()
            
            if not all([doctor, date, time]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            doctor_id = int(doctor.split(' - ')[0])
            
            new_appointment = {
                "id": max([a['id'] for a in self.data['appointments']]) + 1 if self.data['appointments'] else 1,
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "date": date,
                "time": time,
                "status": "scheduled",
                "diagnosis": "",
                "treatment": ""
            }
            
            self.data['appointments'].append(new_appointment)
            self.save_data()
            messagebox.showinfo("Успех", "Вы успешно записаны на прием!")
            
            # Очистить форму
            doctor_var.set('')
            date_entry.delete(0, 'end')
            time_entry.delete(0, 'end')
        
        tk.Button(form_frame, text="Записаться", font=('Arial', 12), width=20, 
                 command=create_appointment, bg='#27ae60', fg='white').grid(row=4, column=0, columnspan=2, pady=30)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == '__main__':
    app = HospitalSystem()
    app.run()