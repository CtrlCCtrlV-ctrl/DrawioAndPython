import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import authenticate, session, create_user, get_all_users, delete_user

DATA_FILE = 'data.json'

def load_data():
    """Загрузка данных из JSON"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """Сохранение данных в JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class AudioLibraryApp:
    """Главное приложение аудиобиблиотеки"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Аудиобиблиотека - Вход")
        self.root.geometry("400x300")
        self.data = load_data()
        self.show_login()
    
    def show_login(self):
        """Окно авторизации"""
        self.clear_window()
        self.root.geometry("400x300")
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Аудиобиблиотека", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(frame, text="Логин:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.login_entry = ttk.Entry(frame, width=25)
        self.login_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=25)
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Войти", command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        
        info_text = "Тестовые учетные записи:\nadmin/admin123\nlibrarian/lib123\nreader/read123"
        ttk.Label(frame, text=info_text, font=("Arial", 8), foreground="gray").grid(row=4, column=0, columnspan=2)
        
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Обработка входа"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        user = authenticate(username, password)
        if user:
            session.login(user)
            self.show_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_main_menu(self):
        """Главное меню в зависимости от роли"""
        self.clear_window()
        self.root.geometry("900x600")
        self.root.title(f"Аудиобиблиотека - {session.current_user['full_name']}")
        
        # Верхняя панель
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(top_frame, text=f"Пользователь: {session.current_user['full_name']}", 
                 font=("Arial", 10)).pack(side="left")
        ttk.Label(top_frame, text=f"Роль: {self.get_role_name()}", 
                 font=("Arial", 10)).pack(side="left", padx=20)
        ttk.Button(top_frame, text="Выход", command=self.logout).pack(side="right")
        
        # Меню
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill="x", padx=10, pady=5)
        
        role = session.get_role()
        
        if role == "administrator":
            ttk.Button(menu_frame, text="Управление пользователями", 
                      command=self.show_users_management).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Управление книгами", 
                      command=self.show_books_management).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Управление авторами", 
                      command=self.show_authors_management).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Статистика", 
                      command=self.show_statistics).pack(side="left", padx=2)
        
        elif role == "librarian":
            ttk.Button(menu_frame, text="Каталог книг", 
                      command=self.show_books_catalog).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Добавить книгу", 
                      command=self.show_add_book).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Авторы", 
                      command=self.show_authors_management).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Выдача книг", 
                      command=self.show_issue_books).pack(side="left", padx=2)
        
        elif role == "reader":
            ttk.Button(menu_frame, text="Каталог", 
                      command=self.show_reader_catalog).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Мои бронирования", 
                      command=self.show_my_reservations).pack(side="left", padx=2)
            ttk.Button(menu_frame, text="Поиск", 
                      command=self.show_search).pack(side="left", padx=2)
        
        # Рабочая область
        self.work_area = ttk.Frame(self.root)
        self.work_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Показываем начальный экран
        if role == "administrator":
            self.show_statistics()
        elif role == "librarian":
            self.show_books_catalog()
        else:
            self.show_reader_catalog()
    
    def get_role_name(self):
        """Получение названия роли на русском"""
        roles = {
            "administrator": "Администратор",
            "librarian": "Библиотекарь",
            "reader": "Читатель"
        }
        return roles.get(session.get_role(), "Неизвестно")
    
    # ФУНКЦИИ АДМИНИСТРАТОРА
    
    def show_users_management(self):
        """Управление пользователями"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Управление пользователями", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Кнопки действий
        btn_frame = ttk.Frame(self.work_area)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Добавить пользователя", 
                  command=self.add_user_dialog).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить выбранного", 
                  command=self.delete_selected_user).pack(side="left", padx=5)
        
        # Таблица пользователей
        columns = ("Логин", "ФИО", "Роль", "Дата создания")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        users = get_all_users()
        for user in users:
            tree.insert("", "end", values=(
                user['username'],
                user['full_name'],
                self.translate_role(user['role']),
                user['created']
            ))
        
        tree.pack(fill="both", expand=True, pady=5)
        self.users_tree = tree
    
    def translate_role(self, role):
        """Перевод роли на русский"""
        roles = {
            "administrator": "Администратор",
            "librarian": "Библиотекарь",
            "reader": "Читатель"
        }
        return roles.get(role, role)
    
    def add_user_dialog(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("350x250")
        
        ttk.Label(dialog, text="Логин:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        username_entry = ttk.Entry(dialog, width=25)
        username_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(dialog, text="Пароль:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        password_entry = ttk.Entry(dialog, show="*", width=25)
        password_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(dialog, text="ФИО:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        fullname_entry = ttk.Entry(dialog, width=25)
        fullname_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(dialog, text="Роль:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        role_var = tk.StringVar(value="reader")
        role_combo = ttk.Combobox(dialog, textvariable=role_var, width=23, state="readonly")
        role_combo['values'] = ("administrator", "librarian", "reader")
        role_combo.grid(row=3, column=1, pady=5)
        
        def save_user():
            success, msg = create_user(
                username_entry.get(),
                password_entry.get(),
                role_var.get(),
                fullname_entry.get()
            )
            if success:
                messagebox.showinfo("Успех", msg)
                dialog.destroy()
                self.show_users_management()
            else:
                messagebox.showerror("Ошибка", msg)
        
        ttk.Button(dialog, text="Сохранить", command=save_user).grid(row=4, column=0, columnspan=2, pady=20)
    
    def delete_selected_user(self):
        """Удаление выбранного пользователя"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя")
            return
        
        item = self.users_tree.item(selected[0])
        username = item['values'][0]
        
        if username == session.current_user['username']:
            messagebox.showerror("Ошибка", "Нельзя удалить текущего пользователя")
            return
        
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя {username}?"):
            delete_user(username)
            self.show_users_management()
    
    def show_books_management(self):
        """Управление книгами (администратор)"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Управление аудиокнигами", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        btn_frame = ttk.Frame(self.work_area)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Добавить книгу", 
                  command=self.show_add_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Редактировать", 
                  command=self.edit_selected_book).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить", 
                  command=self.delete_selected_book).pack(side="left", padx=5)
        
        columns = ("ID", "Название", "Автор", "Жанр", "Длительность", "Диктор", "Год", "Доступна")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=15)
        
        widths = [40, 200, 150, 100, 100, 150, 60, 80]
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=widths[i])
        
        for book in self.data['audiobooks']:
            tree.insert("", "end", values=(
                book['id'],
                book['title'],
                book['author'],
                book['genre'],
                book['duration'],
                book['narrator'],
                book['year'],
                "Да" if book['available'] else "Нет"
            ))
        
        tree.pack(fill="both", expand=True, pady=5)
        self.books_tree = tree
    
    def show_authors_management(self):
        """Управление авторами"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Управление авторами", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        btn_frame = ttk.Frame(self.work_area)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Добавить автора", 
                  command=self.add_author_dialog).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить", 
                  command=self.delete_selected_author).pack(side="left", padx=5)
        
        columns = ("ID", "Имя", "Страна", "Год рождения")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        for author in self.data['authors']:
            tree.insert("", "end", values=(
                author['id'],
                author['name'],
                author['country'],
                author['birth_year']
            ))
        
        tree.pack(fill="both", expand=True, pady=5)
        self.authors_tree = tree
    
    def add_author_dialog(self):
        """Диалог добавления автора"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить автора")
        dialog.geometry("350x200")
        
        ttk.Label(dialog, text="Имя автора:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        name_entry = ttk.Entry(dialog, width=25)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(dialog, text="Страна:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        country_entry = ttk.Entry(dialog, width=25)
        country_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(dialog, text="Год рождения:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        year_entry = ttk.Entry(dialog, width=25)
        year_entry.grid(row=2, column=1, pady=5)
        
        def save_author():
            new_id = max([a['id'] for a in self.data['authors']], default=0) + 1
            self.data['authors'].append({
                'id': new_id,
                'name': name_entry.get(),
                'country': country_entry.get(),
                'birth_year': int(year_entry.get()) if year_entry.get().isdigit() else 0
            })
            save_data(self.data)
            messagebox.showinfo("Успех", "Автор добавлен")
            dialog.destroy()
            self.show_authors_management()
        
        ttk.Button(dialog, text="Сохранить", command=save_author).grid(row=3, column=0, columnspan=2, pady=20)
    
    def delete_selected_author(self):
        """Удаление автора"""
        selected = self.authors_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите автора")
            return
        
        item = self.authors_tree.item(selected[0])
        author_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить автора?"):
            self.data['authors'] = [a for a in self.data['authors'] if a['id'] != author_id]
            save_data(self.data)
            self.show_authors_management()
    
    def show_statistics(self):
        """Показ статистики"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Статистика системы", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        stats_frame = ttk.Frame(self.work_area)
        stats_frame.pack(pady=20)
        
        total_books = len(self.data['audiobooks'])
        available_books = sum(1 for b in self.data['audiobooks'] if b['available'])
        total_authors = len(self.data['authors'])
        total_users = len(get_all_users())
        total_reservations = len(self.data['reservations'])
        
        stats = [
            ("Всего аудиокниг:", total_books),
            ("Доступно для выдачи:", available_books),
            ("Авторов в базе:", total_authors),
            ("Зарегистрировано пользователей:", total_users),
            ("Активных бронирований:", total_reservations)
        ]
        
        for i, (label, value) in enumerate(stats):
            ttk.Label(stats_frame, text=label, font=("Arial", 11)).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            ttk.Label(stats_frame, text=str(value), font=("Arial", 11, "bold")).grid(row=i, column=1, sticky="w", padx=10, pady=5)
    
    # ФУНКЦИИ БИБЛИОТЕКАРЯ
    
    def show_books_catalog(self):
        """Каталог книг для библиотекаря"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Каталог аудиокниг", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        btn_frame = ttk.Frame(self.work_area)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Label(btn_frame, text="Поиск:").pack(side="left", padx=5)
        search_entry = ttk.Entry(btn_frame, width=30)
        search_entry.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Найти", 
                  command=lambda: self.search_books(search_entry.get())).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Показать все", 
                  command=self.show_books_catalog).pack(side="left", padx=5)
        
        columns = ("ID", "Название", "Автор", "Жанр", "Длительность", "Доступна")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=15)
        
        widths = [40, 250, 200, 120, 100, 80]
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=widths[i])
        
        for book in self.data['audiobooks']:
            tree.insert("", "end", values=(
                book['id'],
                book['title'],
                book['author'],
                book['genre'],
                book['duration'],
                "Да" if book['available'] else "Нет"
            ))
        
        tree.pack(fill="both", expand=True, pady=5)
        self.catalog_tree = tree
    
    def search_books(self, query):
        """Поиск книг"""
        if not query:
            return
        
        self.clear_work_area()
        
        ttk.Label(self.work_area, text=f"Результаты поиска: '{query}'", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        ttk.Button(self.work_area, text="← Назад к каталогу", 
                  command=self.show_books_catalog).pack(anchor="w", pady=5)
        
        columns = ("ID", "Название", "Автор", "Жанр", "Доступна")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        query_lower = query.lower()
        found = False
        
        for book in self.data['audiobooks']:
            if (query_lower in book['title'].lower() or 
                query_lower in book['author'].lower() or 
                query_lower in book['genre'].lower()):
                tree.insert("", "end", values=(
                    book['id'],
                    book['title'],
                    book['author'],
                    book['genre'],
                    "Да" if book['available'] else "Нет"
                ))
                found = True
        
        if not found:
            ttk.Label(self.work_area, text="Ничего не найдено", 
                     font=("Arial", 11), foreground="red").pack(pady=20)
        
        tree.pack(fill="both", expand=True, pady=5)
    
    def show_add_book(self):
        """Форма добавления книги"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить аудиокнигу")
        dialog.geometry("400x400")
        
        fields = [
            ("Название:", "title"),
            ("Автор:", "author"),
            ("Жанр:", "genre"),
            ("Длительность (чч:мм:сс):", "duration"),
            ("Диктор:", "narrator"),
            ("Год:", "year")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries[key] = entry
        
        ttk.Label(dialog, text="Доступна:").grid(row=len(fields), column=0, sticky="e", padx=5, pady=5)
        available_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(dialog, variable=available_var).grid(row=len(fields), column=1, sticky="w", pady=5)
        
        def save_book():
            new_id = max([b['id'] for b in self.data['audiobooks']], default=0) + 1
            new_book = {
                'id': new_id,
                'title': entries['title'].get(),
                'author': entries['author'].get(),
                'genre': entries['genre'].get(),
                'duration': entries['duration'].get(),
                'narrator': entries['narrator'].get(),
                'year': int(entries['year'].get()) if entries['year'].get().isdigit() else 0,
                'available': available_var.get()
            }
            self.data['audiobooks'].append(new_book)
            save_data(self.data)
            messagebox.showinfo("Успех", "Книга добавлена")
            dialog.destroy()
        
        ttk.Button(dialog, text="Сохранить", command=save_book).grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
    
    def edit_selected_book(self):
        """Редактирование выбранной книги"""
        if not hasattr(self, 'books_tree'):
            return
        
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу")
            return
        
        item = self.books_tree.item(selected[0])
        book_id = item['values'][0]
        book = next((b for b in self.data['audiobooks'] if b['id'] == book_id), None)
        
        if not book:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать аудиокнигу")
        dialog.geometry("400x400")
        
        fields = [
            ("Название:", "title", book['title']),
            ("Автор:", "author", book['author']),
            ("Жанр:", "genre", book['genre']),
            ("Длительность:", "duration", book['duration']),
            ("Диктор:", "narrator", book['narrator']),
            ("Год:", "year", str(book['year']))
        ]
        
        entries = {}
        for i, (label, key, value) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(dialog, width=30)
            entry.insert(0, value)
            entry.grid(row=i, column=1, pady=5, padx=5)
            entries[key] = entry
        
        ttk.Label(dialog, text="Доступна:").grid(row=len(fields), column=0, sticky="e", padx=5, pady=5)
        available_var = tk.BooleanVar(value=book['available'])
        ttk.Checkbutton(dialog, variable=available_var).grid(row=len(fields), column=1, sticky="w", pady=5)
        
        def update_book():
            book['title'] = entries['title'].get()
            book['author'] = entries['author'].get()
            book['genre'] = entries['genre'].get()
            book['duration'] = entries['duration'].get()
            book['narrator'] = entries['narrator'].get()
            book['year'] = int(entries['year'].get()) if entries['year'].get().isdigit() else 0
            book['available'] = available_var.get()
            save_data(self.data)
            messagebox.showinfo("Успех", "Книга обновлена")
            dialog.destroy()
            self.show_books_management()
        
        ttk.Button(dialog, text="Сохранить", command=update_book).grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
    
    def delete_selected_book(self):
        """Удаление книги"""
        if not hasattr(self, 'books_tree'):
            return
        
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу")
            return
        
        item = self.books_tree.item(selected[0])
        book_id = item['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Удалить книгу?"):
            self.data['audiobooks'] = [b for b in self.data['audiobooks'] if b['id'] != book_id]
            save_data(self.data)
            self.show_books_management()
    
    def show_issue_books(self):
        """Выдача книг читателям"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Выдача аудиокниг", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(self.work_area)
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Читатель:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        reader_var = tk.StringVar()
        readers = [u['username'] for u in get_all_users() if u['role'] == 'reader']
        reader_combo = ttk.Combobox(form_frame, textvariable=reader_var, values=readers, width=25, state="readonly")
        reader_combo.grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Книга:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        book_var = tk.StringVar()
        books = [f"{b['id']}: {b['title']}" for b in self.data['audiobooks'] if b['available']]
        book_combo = ttk.Combobox(form_frame, textvariable=book_var, values=books, width=40, state="readonly")
        book_combo.grid(row=1, column=1, pady=5)
        
        def issue_book():
            if not reader_var.get() or not book_var.get():
                messagebox.showwarning("Внимание", "Заполните все поля")
                return
            
            book_id = int(book_var.get().split(':')[0])
            reservation = {
                'id': len(self.data['reservations']) + 1,
                'reader': reader_var.get(),
                'book_id': book_id,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'status': 'active'
            }
            self.data['reservations'].append(reservation)
            
            # Делаем книгу недоступной
            for book in self.data['audiobooks']:
                if book['id'] == book_id:
                    book['available'] = False
                    break
            
            save_data(self.data)
            messagebox.showinfo("Успех", "Книга выдана")
            self.show_issue_books()
        
        ttk.Button(form_frame, text="Выдать книгу", command=issue_book).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Список текущих выдач
        ttk.Label(self.work_area, text="Текущие выдачи:", font=("Arial", 11, "bold")).pack(pady=10)
        
        columns = ("ID", "Читатель", "Книга", "Дата", "Статус")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for res in self.data['reservations']:
            book = next((b for b in self.data['audiobooks'] if b['id'] == res['book_id']), None)
            book_title = book['title'] if book else "Неизвестно"
            tree.insert("", "end", values=(
                res['id'],
                res['reader'],
                book_title,
                res['date'],
                res['status']
            ))
        
        tree.pack(fill="both", expand=True, pady=5)
    
    # ФУНКЦИИ ЧИТАТЕЛЯ
    
    def show_reader_catalog(self):
        """Каталог для читателя"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Каталог аудиокниг", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        btn_frame = ttk.Frame(self.work_area)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="Забронировать выбранную", 
                  command=self.reserve_selected_book).pack(side="left", padx=5)
        
        columns = ("ID", "Название", "Автор", "Жанр", "Длительность", "Диктор", "Доступна")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=15)
        
        widths = [40, 200, 150, 100, 100, 150, 80]
        for i, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=widths[i])
        
        for book in self.data['audiobooks']:
            tree.insert("", "end", values=(
                book['id'],
                book['title'],
                book['author'],
                book['genre'],
                book['duration'],
                book['narrator'],
                "Да" if book['available'] else "Нет"
            ))
        
        tree.pack(fill="both", expand=True, pady=5)
        self.reader_catalog_tree = tree
    
    def reserve_selected_book(self):
        """Бронирование книги"""
        if not hasattr(self, 'reader_catalog_tree'):
            return
        
        selected = self.reader_catalog_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу")
            return
        
        item = self.reader_catalog_tree.item(selected[0])
        book_id = item['values'][0]
        available = item['values'][6] == "Да"
        
        if not available:
            messagebox.showwarning("Внимание", "Книга недоступна")
            return
        
        reservation = {
            'id': len(self.data['reservations']) + 1,
            'reader': session.current_user['username'],
            'book_id': book_id,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'status': 'active'
        }
        self.data['reservations'].append(reservation)
        
        for book in self.data['audiobooks']:
            if book['id'] == book_id:
                book['available'] = False
                break
        
        save_data(self.data)
        messagebox.showinfo("Успех", "Книга забронирована")
        self.show_reader_catalog()
    
    def show_my_reservations(self):
        """Мои бронирования"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Мои бронирования", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        columns = ("ID", "Название книги", "Автор", "Дата бронирования", "Статус")
        tree = ttk.Treeview(self.work_area, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        my_reservations = [r for r in self.data['reservations'] 
                          if r['reader'] == session.current_user['username']]
        
        for res in my_reservations:
            book = next((b for b in self.data['audiobooks'] if b['id'] == res['book_id']), None)
            if book:
                tree.insert("", "end", values=(
                    res['id'],
                    book['title'],
                    book['author'],
                    res['date'],
                    res['status']
                ))
        
        tree.pack(fill="both", expand=True, pady=5)
        
        if not my_reservations:
            ttk.Label(self.work_area, text="У вас нет бронирований", 
                     font=("Arial", 11), foreground="gray").pack(pady=20)
    
    def show_search(self):
        """Поиск для читателя"""
        self.clear_work_area()
        
        ttk.Label(self.work_area, text="Поиск аудиокниг", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        search_frame = ttk.Frame(self.work_area)
        search_frame.pack(pady=20)
        
        ttk.Label(search_frame, text="Поиск по названию, автору или жанру:").grid(row=0, column=0, padx=5, pady=5)
        search_entry = ttk.Entry(search_frame, width=40)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Найти", 
                  command=lambda: self.perform_reader_search(search_entry.get())).grid(row=0, column=2, padx=5)
        
        self.search_results_frame = ttk.Frame(self.work_area)
        self.search_results_frame.pack(fill="both", expand=True, pady=10)
    
    def perform_reader_search(self, query):
        """Выполнение поиска"""
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        if not query:
            return
        
        columns = ("Название", "Автор", "Жанр", "Доступна")
        tree = ttk.Treeview(self.search_results_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        
        query_lower = query.lower()
        found = False
        
        for book in self.data['audiobooks']:
            if (query_lower in book['title'].lower() or 
                query_lower in book['author'].lower() or 
                query_lower in book['genre'].lower()):
                tree.insert("", "end", values=(
                    book['title'],
                    book['author'],
                    book['genre'],
                    "Да" if book['available'] else "Нет"
                ))
                found = True
        
        if found:
            tree.pack(fill="both", expand=True)
        else:
            ttk.Label(self.search_results_frame, text="Ничего не найдено", 
                     font=("Arial", 11), foreground="red").pack(pady=20)
    
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_work_area(self):
        """Очистка рабочей области"""
        if hasattr(self, 'work_area'):
            for widget in self.work_area.winfo_children():
                widget.destroy()
    
    def logout(self):
        """Выход из системы"""
        session.logout()
        self.show_login()

def main():
    root = tk.Tk()
    app = AudioLibraryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()