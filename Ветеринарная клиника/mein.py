import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from pathlib import Path
import auth

DATA_FILE = "data.json"

class VeterinaryClinicApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ветеринарная клиника")
        self.root.geometry("900x600")
        self.current_user = None
        self.data = self.load_data()

        self.show_login_screen()
        
    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"pets": [], "appointments": [], "veterinarians": [], "medical_records": [], "services": []}
    
    def save_data(self, data=None):
        """Сохранение данных в JSON файл"""
        if data is None:
            data = self.data
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Экран входа в систему"""
        self.clear_window()
        
        frame = tk.Frame(self.root, padx=50, pady=50)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Ветеринарная клиника", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        username_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        username_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        password_entry = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
        password_entry.grid(row=2, column=1, pady=5)
        
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
        
        tk.Button(frame, text="Войти", font=("Arial", 12), bg="#4CAF50", fg="white",
                 command=login, width=20, height=2).grid(row=3, column=0, columnspan=2, pady=20)

        password_entry.bind('<Return>', lambda e: login())
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли пользователя"""
        self.clear_window()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text=f"Ветеринарная клиника - {self.current_user['full_name']} ({self.current_user['role']})", 
                bg="#2196F3", fg="white", font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=15)
        
        tk.Button(top_frame, text="Выход", command=self.logout, bg="#f44336", fg="white", 
                 font=("Arial", 10)).pack(side="right", padx=20, pady=15)
        
        # Основной контент
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        role = self.current_user['role']
        
        if role == "client":
            self.show_client_menu(content_frame)
        elif role == "veterinarian":
            self.show_vet_menu(content_frame)
        elif role == "administrator":
            self.show_admin_menu(content_frame)
    
    def show_client_menu(self, parent):
        """Меню для клиента"""
        tk.Label(parent, text="Личный кабинет клиента", font=("Arial", 16, "bold")).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Мои животные", width=25, height=2, bg="#4CAF50", fg="white",
                 font=("Arial", 11), command=self.show_my_pets).grid(row=0, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Зарегистрировать животное", width=25, height=2, bg="#2196F3", fg="white",
                 font=("Arial", 11), command=self.add_pet_dialog).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Записаться на прием", width=25, height=2, bg="#FF9800", fg="white",
                 font=("Arial", 11), command=self.book_appointment_dialog).grid(row=1, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="История приемов", width=25, height=2, bg="#9C27B0", fg="white",
                 font=("Arial", 11), command=self.show_appointment_history).grid(row=1, column=1, padx=10, pady=10)
    
    def show_vet_menu(self, parent):
        """Меню для ветеринара"""
        tk.Label(parent, text="Кабинет ветеринара", font=("Arial", 16, "bold")).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Расписание приемов", width=25, height=2, bg="#4CAF50", fg="white",
                 font=("Arial", 11), command=self.show_appointments).grid(row=0, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Все животные", width=25, height=2, bg="#2196F3", fg="white",
                 font=("Arial", 11), command=self.show_all_pets).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Создать диагноз", width=25, height=2, bg="#FF9800", fg="white",
                 font=("Arial", 11), command=self.create_diagnosis_dialog).grid(row=1, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Медицинские карты", width=25, height=2, bg="#9C27B0", fg="white",
                 font=("Arial", 11), command=self.show_medical_records).grid(row=1, column=1, padx=10, pady=10)
    
    def show_admin_menu(self, parent):
        """Меню для администратора"""
        tk.Label(parent, text="Панель администратора", font=("Arial", 16, "bold")).pack(pady=10)
        
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Управление пользователями", width=25, height=2, bg="#4CAF50", fg="white",
                 font=("Arial", 11), command=self.manage_users).grid(row=0, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Управление ветеринарами", width=25, height=2, bg="#2196F3", fg="white",
                 font=("Arial", 11), command=self.manage_veterinarians).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Управление услугами", width=25, height=2, bg="#FF9800", fg="white",
                 font=("Arial", 11), command=self.manage_services).grid(row=1, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Отчеты", width=25, height=2, bg="#9C27B0", fg="white",
                 font=("Arial", 11), command=self.show_reports).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Все приемы", width=25, height=2, bg="#795548", fg="white",
                 font=("Arial", 11), command=self.show_all_appointments).grid(row=2, column=0, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Резервное копирование", width=25, height=2, bg="#607D8B", fg="white",
                 font=("Arial", 11), command=self.backup_data).grid(row=2, column=1, padx=10, pady=10)
    
    # ФУНКЦИИ ДЛЯ КЛИЕНТА
    
    def show_my_pets(self):
        """Показать животных клиента"""
        window = tk.Toplevel(self.root)
        window.title("Мои животные")
        window.geometry("700x400")
        
        tk.Label(window, text="Мои животные", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Кличка", "Вид", "Порода", "Возраст", "Дата регистрации")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Фильтр по текущему пользователю
        my_pets = [pet for pet in self.data.get("pets", []) 
                  if pet.get("owner") == self.current_user["username"]]
        
        for pet in my_pets:
            tree.insert("", "end", values=(
                pet["id"], pet["name"], pet["species"], 
                pet["breed"], pet["age"], pet["registered_date"]
            ))
        
        tree.pack(fill="both", expand=True)
    
    def add_pet_dialog(self):
        """Диалог добавления животного"""
        window = tk.Toplevel(self.root)
        window.title("Регистрация животного")
        window.geometry("400x350")
        
        tk.Label(window, text="Регистрация животного", font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = tk.Frame(window, padx=20, pady=10)
        form_frame.pack()
        
        tk.Label(form_frame, text="Кличка:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form_frame, text="Вид:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        species_combo = ttk.Combobox(form_frame, values=["Собака", "Кошка", "Птица", "Грызун", "Другое"], width=28)
        species_combo.grid(row=1, column=1, pady=5)
        
        tk.Label(form_frame, text="Порода:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        breed_entry = tk.Entry(form_frame, width=30)
        breed_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(form_frame, text="Возраст (лет):", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        age_entry = tk.Entry(form_frame, width=30)
        age_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(form_frame, text="Вес (кг):", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        weight_entry = tk.Entry(form_frame, width=30)
        weight_entry.grid(row=4, column=1, pady=5)
        
        def save_pet():
            name = name_entry.get().strip()
            species = species_combo.get().strip()
            breed = breed_entry.get().strip()
            age = age_entry.get().strip()
            weight = weight_entry.get().strip()
            
            if not all([name, species, breed, age, weight]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            try:
                age = int(age)
                weight = float(weight)
            except:
                messagebox.showerror("Ошибка", "Неверный формат возраста или веса")
                return
            
            pet_id = f"PET{len(self.data['pets']) + 1:04d}"
            
            new_pet = {
                "id": pet_id,
                "name": name,
                "species": species,
                "breed": breed,
                "age": age,
                "weight": weight,
                "owner": self.current_user["username"],
                "registered_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            self.data["pets"].append(new_pet)
            self.save_data()
            messagebox.showinfo("Успех", f"Животное {name} успешно зарегистрировано!")
            window.destroy()
        
        tk.Button(form_frame, text="Сохранить", bg="#4CAF50", fg="white", 
                 command=save_pet, width=20).grid(row=5, column=0, columnspan=2, pady=20)
    
    def book_appointment_dialog(self):
        """Диалог записи на прием"""
        # Проверка наличия животных
        my_pets = [pet for pet in self.data.get("pets", []) 
                  if pet.get("owner") == self.current_user["username"]]
        
        if not my_pets:
            messagebox.showwarning("Предупреждение", "Сначала зарегистрируйте животное")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Запись на прием")
        window.geometry("450x400")
        
        tk.Label(window, text="Запись на прием", font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = tk.Frame(window, padx=20, pady=10)
        form_frame.pack()
        
        tk.Label(form_frame, text="Животное:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        pet_names = [f"{p['name']} ({p['species']})" for p in my_pets]
        pet_combo = ttk.Combobox(form_frame, values=pet_names, width=30)
        pet_combo.grid(row=0, column=1, pady=5)
        
        tk.Label(form_frame, text="Ветеринар:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        vets = self.data.get("veterinarians", [])
        vet_names = [f"{v['name']} - {v['specialization']}" for v in vets]
        vet_combo = ttk.Combobox(form_frame, values=vet_names, width=30)
        vet_combo.grid(row=1, column=1, pady=5)
        
        tk.Label(form_frame, text="Дата:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        date_entry = tk.Entry(form_frame, width=32)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(form_frame, text="Время:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        time_combo = ttk.Combobox(form_frame, values=["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"], width=30)
        time_combo.grid(row=3, column=1, pady=5)
        
        tk.Label(form_frame, text="Причина:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        reason_text = tk.Text(form_frame, width=32, height=5)
        reason_text.grid(row=4, column=1, pady=5)
        
        def save_appointment():
            if not all([pet_combo.get(), vet_combo.get(), time_combo.get()]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
            
            pet_idx = pet_combo.current()
            vet_idx = vet_combo.current()
            
            appointment_id = f"APP{len(self.data['appointments']) + 1:04d}"
            
            new_appointment = {
                "id": appointment_id,
                "pet_id": my_pets[pet_idx]["id"],
                "pet_name": my_pets[pet_idx]["name"],
                "vet_id": vets[vet_idx]["id"],
                "vet_name": vets[vet_idx]["name"],
                "client": self.current_user["username"],
                "date": date_entry.get(),
                "time": time_combo.get(),
                "reason": reason_text.get("1.0", "end-1c"),
                "status": "Запланирован",
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.data["appointments"].append(new_appointment)
            self.save_data()
            messagebox.showinfo("Успех", "Прием успешно запланирован!")
            window.destroy()
        
        tk.Button(form_frame, text="Записаться", bg="#4CAF50", fg="white", 
                 command=save_appointment, width=20).grid(row=5, column=0, columnspan=2, pady=20)
    
    def show_appointment_history(self):
        """История приемов клиента"""
        window = tk.Toplevel(self.root)
        window.title("История приемов")
        window.geometry("800x400")
        
        tk.Label(window, text="История приемов", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Животное", "Ветеринар", "Дата", "Время", "Статус")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        my_appointments = [app for app in self.data.get("appointments", []) 
                          if app.get("client") == self.current_user["username"]]
        
        for app in my_appointments:
            tree.insert("", "end", values=(
                app["id"], app["pet_name"], app["vet_name"],
                app["date"], app["time"], app["status"]
            ))
        
        tree.pack(fill="both", expand=True)
    
    # ФУНКЦИИ ДЛЯ ВЕТЕРИНАРА
    
    def show_appointments(self):
        """Расписание приемов ветеринара"""
        window = tk.Toplevel(self.root)
        window.title("Расписание приемов")
        window.geometry("900x450")
        
        tk.Label(window, text="Расписание приемов", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Животное", "Владелец", "Дата", "Время", "Причина", "Статус")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Фильтр по текущему ветеринару
        my_appointments = [app for app in self.data.get("appointments", []) 
                          if app.get("vet_id") == self.current_user["username"]]
        
        for app in my_appointments:
            tree.insert("", "end", values=(
                app["id"], app["pet_name"], app["client"],
                app["date"], app["time"], app["reason"][:30], app["status"]
            ))
        
        tree.pack(fill="both", expand=True)
        
        def complete_appointment():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Предупреждение", "Выберите прием")
                return
            
            item = tree.item(selection[0])
            app_id = item['values'][0]
            
            for app in self.data["appointments"]:
                if app["id"] == app_id:
                    app["status"] = "Завершен"
                    break
            
            self.save_data()
            messagebox.showinfo("Успех", "Статус приема обновлен")
            window.destroy()
            self.show_appointments()
        
        tk.Button(window, text="Завершить прием", bg="#4CAF50", fg="white", 
                 command=complete_appointment).pack(pady=5)
    
    def show_all_pets(self):
        """Показать всех животных"""
        window = tk.Toplevel(self.root)
        window.title("Все животные")
        window.geometry("800x450")
        
        tk.Label(window, text="Все животные", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Кличка", "Вид", "Порода", "Возраст", "Владелец")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        
        for pet in self.data.get("pets", []):
            tree.insert("", "end", values=(
                pet["id"], pet["name"], pet["species"],
                pet["breed"], pet["age"], pet["owner"]
            ))
        
        tree.pack(fill="both", expand=True)
    
    def create_diagnosis_dialog(self):
        """Создание диагноза"""
        all_pets = self.data.get("pets", [])
        
        if not all_pets:
            messagebox.showwarning("Предупреждение", "В системе нет зарегистрированных животных")
            return
        
        window = tk.Toplevel(self.root)
        window.title("Создание диагноза")
        window.geometry("500x450")
        
        tk.Label(window, text="Создание диагноза", font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = tk.Frame(window, padx=20, pady=10)
        form_frame.pack()
        
        tk.Label(form_frame, text="Животное:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        pet_names = [f"{p['id']} - {p['name']} ({p['owner']})" for p in all_pets]
        pet_combo = ttk.Combobox(form_frame, values=pet_names, width=40)
        pet_combo.grid(row=0, column=1, pady=5)
        
        tk.Label(form_frame, text="Диагноз:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        diagnosis_entry = tk.Entry(form_frame, width=42)
        diagnosis_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(form_frame, text="Описание:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        description_text = tk.Text(form_frame, width=42, height=5)
        description_text.grid(row=2, column=1, pady=5)
        
        tk.Label(form_frame, text="Лечение:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        treatment_text = tk.Text(form_frame, width=42, height=5)
        treatment_text.grid(row=3, column=1, pady=5)
        
        def save_diagnosis():
            if not pet_combo.get() or not diagnosis_entry.get():
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            pet_idx = pet_combo.current()
            record_id = f"MED{len(self.data['medical_records']) + 1:04d}"
            
            new_record = {
                "id": record_id,
                "pet_id": all_pets[pet_idx]["id"],
                "pet_name": all_pets[pet_idx]["name"],
                "vet_id": self.current_user["username"],
                "vet_name": self.current_user["full_name"],
                "diagnosis": diagnosis_entry.get(),
                "description": description_text.get("1.0", "end-1c"),
                "treatment": treatment_text.get("1.0", "end-1c"),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.data["medical_records"].append(new_record)
            self.save_data()
            messagebox.showinfo("Успех", "Диагноз успешно создан!")
            window.destroy()
        
        tk.Button(form_frame, text="Сохранить", bg="#4CAF50", fg="white", 
                 command=save_diagnosis, width=20).grid(row=4, column=0, columnspan=2, pady=20)
    
    def show_medical_records(self):
        """Медицинские карты"""
        window = tk.Toplevel(self.root)
        window.title("Медицинские карты")
        window.geometry("900x450")
        
        tk.Label(window, text="Медицинские карты", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Животное", "Диагноз", "Ветеринар", "Дата")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=175)
        
        for record in self.data.get("medical_records", []):
            tree.insert("", "end", values=(
                record["id"], record["pet_name"], record["diagnosis"],
                record["vet_name"], record["date"]
            ))
        
        tree.pack(fill="both", expand=True)
    
    # ФУНКЦИИ ДЛЯ АДМИНИСТРАТОРА
    
    def manage_users(self):
        """Управление пользователями"""
        window = tk.Toplevel(self.root)
        window.title("Управление пользователями")
        window.geometry("800x500")
        
        tk.Label(window, text="Управление пользователями", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Логин", "ФИО", "Роль", "Дата создания")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=190)
        
        def refresh_tree():
            tree.delete(*tree.get_children())
            users = auth.get_all_users()
            for user in users:
                tree.insert("", "end", values=(
                    user["username"], user["full_name"], 
                    user["role"], user["created"]
                ))
        
        refresh_tree()
        tree.pack(fill="both", expand=True)
        
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=5)
        
        def add_user_dialog():
            dialog = tk.Toplevel(window)
            dialog.title("Добавить пользователя")
            dialog.geometry("400x300")
            
            tk.Label(dialog, text="Логин:").grid(row=0, column=0, padx=10, pady=5)
            username_entry = tk.Entry(dialog, width=30)
            username_entry.grid(row=0, column=1, pady=5)
            
            tk.Label(dialog, text="Пароль:").grid(row=1, column=0, padx=10, pady=5)
            password_entry = tk.Entry(dialog, width=30, show="*")
            password_entry.grid(row=1, column=1, pady=5)
            
            tk.Label(dialog, text="ФИО:").grid(row=2, column=0, padx=10, pady=5)
            fullname_entry = tk.Entry(dialog, width=30)
            fullname_entry.grid(row=2, column=1, pady=5)
            
            tk.Label(dialog, text="Роль:").grid(row=3, column=0, padx=10, pady=5)
            role_combo = ttk.Combobox(dialog, values=["client", "veterinarian", "administrator"], width=28)
            role_combo.grid(row=3, column=1, pady=5)
            
            def save():
                success, msg = auth.create_user(
                    username_entry.get(),
                    password_entry.get(),
                    role_combo.get(),
                    fullname_entry.get()
                )
                if success:
                    messagebox.showinfo("Успех", msg)
                    refresh_tree()
                    dialog.destroy()
                else:
                    messagebox.showerror("Ошибка", msg)
            
            tk.Button(dialog, text="Создать", command=save, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=20)
        
        def delete_user():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Предупреждение", "Выберите пользователя")
                return
            
            username = tree.item(selection[0])['values'][0]
            if username == "admin":
                messagebox.showerror("Ошибка", "Нельзя удалить администратора")
                return
            
            if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
                auth.delete_user(username)
                refresh_tree()
        
        tk.Button(btn_frame, text="Добавить", command=add_user_dialog, bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=delete_user, bg="#f44336", fg="white", width=15).pack(side="left", padx=5)
    
    def manage_veterinarians(self):
        """Управление ветеринарами"""
        window = tk.Toplevel(self.root)
        window.title("Управление ветеринарами")
        window.geometry("700x450")
        
        tk.Label(window, text="Управление ветеринарами", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "ФИО", "Специализация", "Телефон")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)
        
        def refresh_tree():
            tree.delete(*tree.get_children())
            for vet in self.data.get("veterinarians", []):
                tree.insert("", "end", values=(
                    vet["id"], vet["name"], vet["specialization"], vet["phone"]
                ))
        
        refresh_tree()
        tree.pack(fill="both", expand=True)
        
        def add_vet_dialog():
            dialog = tk.Toplevel(window)
            dialog.title("Добавить ветеринара")
            dialog.geometry("400x250")
            
            tk.Label(dialog, text="ID:").grid(row=0, column=0, padx=10, pady=5)
            id_entry = tk.Entry(dialog, width=30)
            id_entry.grid(row=0, column=1, pady=5)
            
            tk.Label(dialog, text="ФИО:").grid(row=1, column=0, padx=10, pady=5)
            name_entry = tk.Entry(dialog, width=30)
            name_entry.grid(row=1, column=1, pady=5)
            
            tk.Label(dialog, text="Специализация:").grid(row=2, column=0, padx=10, pady=5)
            spec_entry = tk.Entry(dialog, width=30)
            spec_entry.grid(row=2, column=1, pady=5)
            
            tk.Label(dialog, text="Телефон:").grid(row=3, column=0, padx=10, pady=5)
            phone_entry = tk.Entry(dialog, width=30)
            phone_entry.grid(row=3, column=1, pady=5)
            
            def save():
                new_vet = {
                    "id": id_entry.get(),
                    "name": name_entry.get(),
                    "specialization": spec_entry.get(),
                    "phone": phone_entry.get()
                }
                self.data["veterinarians"].append(new_vet)
                self.save_data()
                messagebox.showinfo("Успех", "Ветеринар добавлен")
                refresh_tree()
                dialog.destroy()
            
            tk.Button(dialog, text="Добавить", command=save, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(window, text="Добавить ветеринара", command=add_vet_dialog, bg="#4CAF50", fg="white").pack(pady=5)
    
    def manage_services(self):
        """Управление услугами"""
        window = tk.Toplevel(self.root)
        window.title("Управление услугами")
        window.geometry("600x450")
        
        tk.Label(window, text="Управление услугами", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Название", "Цена")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=190)
        
        def refresh_tree():
            tree.delete(*tree.get_children())
            for service in self.data.get("services", []):
                tree.insert("", "end", values=(
                    service["id"], service["name"], f"{service['price']} руб."
                ))
        
        refresh_tree()
        tree.pack(fill="both", expand=True)
        
        def add_service_dialog():
            dialog = tk.Toplevel(window)
            dialog.title("Добавить услугу")
            dialog.geometry("350x200")
            
            tk.Label(dialog, text="Название:").grid(row=0, column=0, padx=10, pady=5)
            name_entry = tk.Entry(dialog, width=25)
            name_entry.grid(row=0, column=1, pady=5)
            
            tk.Label(dialog, text="Цена:").grid(row=1, column=0, padx=10, pady=5)
            price_entry = tk.Entry(dialog, width=25)
            price_entry.grid(row=1, column=1, pady=5)
            
            def save():
                new_id = max([s["id"] for s in self.data["services"]], default=0) + 1
                new_service = {
                    "id": new_id,
                    "name": name_entry.get(),
                    "price": int(price_entry.get())
                }
                self.data["services"].append(new_service)
                self.save_data()
                messagebox.showinfo("Успех", "Услуга добавлена")
                refresh_tree()
                dialog.destroy()
            
            tk.Button(dialog, text="Добавить", command=save, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=20)
        
        tk.Button(window, text="Добавить услугу", command=add_service_dialog, bg="#4CAF50", fg="white").pack(pady=5)
    
    def show_reports(self):
        """Отчеты"""
        window = tk.Toplevel(self.root)
        window.title("Отчеты")
        window.geometry("500x400")
        
        tk.Label(window, text="Статистика системы", font=("Arial", 14, "bold")).pack(pady=20)
        
        info_frame = tk.Frame(window, padx=30)
        info_frame.pack()
        
        total_pets = len(self.data.get("pets", []))
        total_appointments = len(self.data.get("appointments", []))
        total_records = len(self.data.get("medical_records", []))
        total_users = len(auth.get_all_users())
        total_vets = len(self.data.get("veterinarians", []))
        
        stats = [
            ("Всего пользователей:", total_users),
            ("Всего ветеринаров:", total_vets),
            ("Всего животных:", total_pets),
            ("Всего приемов:", total_appointments),
            ("Медицинских записей:", total_records),
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(info_frame, text=label, font=("Arial", 12), anchor="w", width=25).grid(row=i, column=0, sticky="w", pady=10)
            tk.Label(info_frame, text=str(value), font=("Arial", 12, "bold"), fg="#2196F3", anchor="e", width=10).grid(row=i, column=1, sticky="e", pady=10)
    
    def show_all_appointments(self):
        """Все приемы (для администратора)"""
        window = tk.Toplevel(self.root)
        window.title("Все приемы")
        window.geometry("900x450")
        
        tk.Label(window, text="Все приемы", font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = tk.Frame(window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("ID", "Клиент", "Животное", "Ветеринар", "Дата", "Статус")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=145)
        
        for app in self.data.get("appointments", []):
            tree.insert("", "end", values=(
                app["id"], app["client"], app["pet_name"],
                app["vet_name"], app["date"], app["status"]
            ))
        
        tree.pack(fill="both", expand=True)
    
    def backup_data(self):
        """Резервное копирование"""
        try:
            backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"Резервная копия создана: {backup_filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать резервную копию: {str(e)}")
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.show_login_screen()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VeterinaryClinicApp()
    app.run()