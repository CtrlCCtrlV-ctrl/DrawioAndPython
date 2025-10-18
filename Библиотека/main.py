import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from auth import AuthManager

class LibrarySystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Библиотечная система")
        self.root.geometry("900x600")
        
        self.auth = AuthManager()
        self.current_user = None

        self.show_login_window()
        
    
    def show_login_window(self):
        """Окно авторизации"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.4, anchor='center')
        
        tk.Label(frame, text="Вход в систему", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(frame, text="Логин:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.login_entry = tk.Entry(frame, width=20)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.password_entry = tk.Entry(frame, width=20, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(frame, text="Войти", command=self.login, width=15).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Подсказка для тестирования
        tk.Label(frame, text="admin/admin123 | librarian/lib123 | reader/read123", 
                font=("Arial", 8), fg="gray").grid(row=4, column=0, columnspan=2)
    
    def login(self):
        """Процесс авторизации"""
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
        
        user = self.auth.authenticate(username, password)
        if user:
            self.current_user = user
            self.show_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_main_window(self):
        """Главное окно в зависимости от роли"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=f"Пользователь: {self.current_user['username']} ({self.current_user['role']})", 
                bg='#2c3e50', fg='white', font=("Arial", 10)).pack(side='left', padx=10, pady=10)
        
        tk.Button(top_frame, text="Выход", command=self.logout).pack(side='right', padx=10, pady=10)
        
        # Основное содержимое
        if self.current_user['role'] == 'administrator':
            self.show_admin_interface()
        elif self.current_user['role'] == 'librarian':
            self.show_librarian_interface()
        else:
            self.show_reader_interface()
    
    def show_admin_interface(self):
        """Интерфейс администратора"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка управления пользователями
        users_tab = ttk.Frame(notebook)
        notebook.add(users_tab, text='Пользователи')
        
        tk.Label(users_tab, text="Управление пользователями", font=("Arial", 14)).pack(pady=10)
        
        # Таблица пользователей
        self.users_tree = ttk.Treeview(users_tab, columns=('Username', 'Role', 'Created'), show='headings', height=10)
        self.users_tree.heading('Username', text='Логин')
        self.users_tree.heading('Role', text='Роль')
        self.users_tree.heading('Created', text='Дата создания')
        self.users_tree.pack(pady=10, padx=10)
        
        # Кнопки управления
        btn_frame = tk.Frame(users_tab)
        btn_frame.pack()
        tk.Button(btn_frame, text="Добавить пользователя", command=self.add_user_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить пользователя", command=self.delete_user).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.load_users).pack(side='left', padx=5)
        
        # Вкладка статистики
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text='Статистика')
        
        tk.Label(stats_tab, text="Статистика системы", font=("Arial", 14)).pack(pady=10)
        self.stats_text = tk.Text(stats_tab, height=15, width=60)
        self.stats_text.pack(pady=10)
        self.load_statistics()
        
        # Вкладка резервного копирования
        backup_tab = ttk.Frame(notebook)
        notebook.add(backup_tab, text='Резервное копирование')
        
        tk.Label(backup_tab, text="Управление резервными копиями", font=("Arial", 14)).pack(pady=20)
        tk.Button(backup_tab, text="Создать резервную копию", command=self.create_backup, width=25).pack(pady=10)
        tk.Button(backup_tab, text="Восстановить из копии", command=self.restore_backup, width=25).pack(pady=10)
        
        self.load_users()
    
    def show_librarian_interface(self):
        """Интерфейс библиотекаря"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка книг
        books_tab = ttk.Frame(notebook)
        notebook.add(books_tab, text='Книги')
        
        tk.Label(books_tab, text="Управление книгами", font=("Arial", 14)).pack(pady=10)
        
        self.books_tree = ttk.Treeview(books_tab, columns=('ID', 'Title', 'Author', 'Year', 'Available'), 
                                      show='headings', height=12)
        self.books_tree.heading('ID', text='ID')
        self.books_tree.heading('Title', text='Название')
        self.books_tree.heading('Author', text='Автор')
        self.books_tree.heading('Year', text='Год')
        self.books_tree.heading('Available', text='Доступна')
        
        self.books_tree.column('ID', width=50)
        self.books_tree.column('Year', width=80)
        self.books_tree.column('Available', width=80)
        
        self.books_tree.pack(pady=10, padx=10)
        
        btn_frame = tk.Frame(books_tab)
        btn_frame.pack()
        tk.Button(btn_frame, text="Добавить книгу", command=self.add_book_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Удалить книгу", command=self.delete_book).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.load_books).pack(side='left', padx=5)
        
        # Вкладка читателей
        readers_tab = ttk.Frame(notebook)
        notebook.add(readers_tab, text='Читатели')
        
        tk.Label(readers_tab, text="Управление читателями", font=("Arial", 14)).pack(pady=10)
        
        self.readers_tree = ttk.Treeview(readers_tab, columns=('ID', 'Name', 'Phone', 'Registered'), 
                                        show='headings', height=12)
        self.readers_tree.heading('ID', text='ID')
        self.readers_tree.heading('Name', text='ФИО')
        self.readers_tree.heading('Phone', text='Телефон')
        self.readers_tree.heading('Registered', text='Дата регистрации')
        
        self.readers_tree.column('ID', width=50)
        self.readers_tree.pack(pady=10, padx=10)
        
        btn_frame2 = tk.Frame(readers_tab)
        btn_frame2.pack()
        tk.Button(btn_frame2, text="Добавить читателя", command=self.add_reader_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame2, text="Удалить читателя", command=self.delete_reader).pack(side='left', padx=5)
        tk.Button(btn_frame2, text="Обновить", command=self.load_readers).pack(side='left', padx=5)
        
        # Вкладка выдачи книг
        issue_tab = ttk.Frame(notebook)
        notebook.add(issue_tab, text='Выдача/Возврат')
        
        tk.Label(issue_tab, text="Выдача и возврат книг", font=("Arial", 14)).pack(pady=10)
        
        self.issues_tree = ttk.Treeview(issue_tab, columns=('ID', 'Book', 'Reader', 'Issue Date', 'Return Date'), 
                                       show='headings', height=10)
        self.issues_tree.heading('ID', text='ID')
        self.issues_tree.heading('Book', text='Книга')
        self.issues_tree.heading('Reader', text='Читатель')
        self.issues_tree.heading('Issue Date', text='Дата выдачи')
        self.issues_tree.heading('Return Date', text='Дата возврата')
        
        self.issues_tree.column('ID', width=50)
        self.issues_tree.pack(pady=10, padx=10)
        
        btn_frame3 = tk.Frame(issue_tab)
        btn_frame3.pack()
        tk.Button(btn_frame3, text="Выдать книгу", command=self.issue_book_dialog).pack(side='left', padx=5)
        tk.Button(btn_frame3, text="Вернуть книгу", command=self.return_book).pack(side='left', padx=5)
        tk.Button(btn_frame3, text="Обновить", command=self.load_issues).pack(side='left', padx=5)
        
        self.load_books()
        self.load_readers()
        self.load_issues()
    
    def show_reader_interface(self):
        """Интерфейс читателя"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка каталога
        catalog_tab = ttk.Frame(notebook)
        notebook.add(catalog_tab, text='Каталог книг')
        
        tk.Label(catalog_tab, text="Каталог библиотеки", font=("Arial", 14)).pack(pady=10)
        
        # Поиск
        search_frame = tk.Frame(catalog_tab)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Поиск:").pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        tk.Button(search_frame, text="Найти", command=self.search_books).pack(side='left', padx=5)
        
        self.catalog_tree = ttk.Treeview(catalog_tab, columns=('Title', 'Author', 'Year', 'Available'), 
                                        show='headings', height=15)
        self.catalog_tree.heading('Title', text='Название')
        self.catalog_tree.heading('Author', text='Автор')
        self.catalog_tree.heading('Year', text='Год')
        self.catalog_tree.heading('Available', text='Доступность')
        
        self.catalog_tree.pack(pady=10, padx=10)
        
        # Вкладка истории
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text='Моя история')
        
        tk.Label(history_tab, text="История выдач", font=("Arial", 14)).pack(pady=10)
        
        self.history_tree = ttk.Treeview(history_tab, columns=('Book', 'Issue Date', 'Return Date', 'Status'), 
                                        show='headings', height=15)
        self.history_tree.heading('Book', text='Книга')
        self.history_tree.heading('Issue Date', text='Дата выдачи')
        self.history_tree.heading('Return Date', text='Дата возврата')
        self.history_tree.heading('Status', text='Статус')
        
        self.history_tree.pack(pady=10, padx=10)
        
        tk.Button(history_tab, text="Продлить срок", command=self.extend_period).pack(pady=10)
        
        self.load_catalog()
        self.load_reader_history()
    
    # Методы для работы с данными
    def load_data(self):
        """Загрузка данных из файла"""
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в файл"""
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_users(self):
        """Загрузка списка пользователей"""
        self.users_tree.delete(*self.users_tree.get_children())
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            for user in users_data['users']:
                self.users_tree.insert('', 'end', values=(
                    user['username'], user['role'], user['created']
                ))
    
    def load_books(self):
        """Загрузка списка книг"""
        self.books_tree.delete(*self.books_tree.get_children())
        data = self.load_data()
        for book in data['books']:
            self.books_tree.insert('', 'end', values=(
                book['id'], book['title'], book['author'], 
                book['year'], 'Да' if book['available'] else 'Нет'
            ))
    
    def load_readers(self):
        """Загрузка списка читателей"""
        self.readers_tree.delete(*self.readers_tree.get_children())
        data = self.load_data()
        for reader in data['readers']:
            self.readers_tree.insert('', 'end', values=(
                reader['id'], reader['name'], reader['phone'], reader['registered']
            ))
    
    def load_issues(self):
        """Загрузка списка выдач"""
        self.issues_tree.delete(*self.issues_tree.get_children())
        data = self.load_data()
        for issue in data['issues']:
            book = next((b for b in data['books'] if b['id'] == issue['book_id']), None)
            reader = next((r for r in data['readers'] if r['id'] == issue['reader_id']), None)
            if book and reader:
                self.issues_tree.insert('', 'end', values=(
                    issue['id'], book['title'], reader['name'],
                    issue['issue_date'], issue['return_date'] or 'Не возвращена'
                ))
    
    def load_catalog(self):
        """Загрузка каталога для читателя"""
        self.catalog_tree.delete(*self.catalog_tree.get_children())
        data = self.load_data()
        for book in data['books']:
            self.catalog_tree.insert('', 'end', values=(
                book['title'], book['author'], book['year'],
                'Доступна' if book['available'] else 'На руках'
            ))
    
    def load_reader_history(self):
        """Загрузка истории читателя"""
        self.history_tree.delete(*self.history_tree.get_children())
        data = self.load_data()
        # Упрощенно показываем все выдачи
        for issue in data['issues']:
            book = next((b for b in data['books'] if b['id'] == issue['book_id']), None)
            if book:
                status = 'Возвращена' if issue['return_date'] else 'На руках'
                self.history_tree.insert('', 'end', values=(
                    book['title'], issue['issue_date'], 
                    issue['return_date'] or '-', status
                ))
    
    def load_statistics(self):
        """Загрузка статистики"""
        data = self.load_data()
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        stats = f"""
        СТАТИСТИКА СИСТЕМЫ
        ==================
        
        Всего книг: {len(data['books'])}
        Доступно книг: {sum(1 for b in data['books'] if b['available'])}
        Выдано книг: {sum(1 for b in data['books'] if not b['available'])}
        
        Всего читателей: {len(data['readers'])}
        Активных выдач: {sum(1 for i in data['issues'] if not i['return_date'])}
        
        Всего пользователей системы: {len(users_data['users'])}
        Администраторов: {sum(1 for u in users_data['users'] if u['role'] == 'administrator')}
        Библиотекарей: {sum(1 for u in users_data['users'] if u['role'] == 'librarian')}
        Читателей: {sum(1 for u in users_data['users'] if u['role'] == 'reader')}
        """
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    # Диалоговые окна
    def add_user_dialog(self):
        """Диалог добавления пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Логин:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Пароль:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        password_entry = tk.Entry(dialog)
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Роль:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        role_var = tk.StringVar(value="reader")
        role_combo = ttk.Combobox(dialog, textvariable=role_var, 
                                 values=['administrator', 'librarian', 'reader'], state='readonly')
        role_combo.grid(row=2, column=1, padx=5, pady=5)
        
        def save_user():
            if username_entry.get() and password_entry.get():
                with open('users.json', 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                
                new_user = {
                    "username": username_entry.get(),
                    "password": password_entry.get(),
                    "role": role_var.get(),
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                
                users_data['users'].append(new_user)
                
                with open('users.json', 'w', encoding='utf-8') as f:
                    json.dump(users_data, f, ensure_ascii=False, indent=2)
                
                self.load_users()
                dialog.destroy()
                messagebox.showinfo("Успех", "Пользователь добавлен")
        
        tk.Button(dialog, text="Сохранить", command=save_user).grid(row=3, column=0, columnspan=2, pady=20)
    
    def add_book_dialog(self):
        """Диалог добавления книги"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить книгу")
        dialog.geometry("350x250")
        
        fields = [("Название:", "title"), ("Автор:", "author"), 
                 ("Год:", "year"), ("ISBN:", "isbn")]
        entries = {}
        
        for i, (label, field) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            entry = tk.Entry(dialog, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry
        
        def save_book():
            if all(entries[field].get() for field in ['title', 'author', 'year']):
                data = self.load_data()
                
                new_id = max([b['id'] for b in data['books']], default=0) + 1
                new_book = {
                    "id": new_id,
                    "title": entries['title'].get(),
                    "author": entries['author'].get(),
                    "year": int(entries['year'].get()),
                    "isbn": entries['isbn'].get(),
                    "available": True
                }
                
                data['books'].append(new_book)
                self.save_data(data)
                self.load_books()
                dialog.destroy()
                messagebox.showinfo("Успех", "Книга добавлена")
        
        tk.Button(dialog, text="Сохранить", command=save_book).grid(row=4, column=0, columnspan=2, pady=20)
    
    def add_reader_dialog(self):
        """Диалог добавления читателя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить читателя")
        dialog.geometry("350x200")
        
        tk.Label(dialog, text="ФИО:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        name_entry = tk.Entry(dialog, width=25)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Телефон:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        phone_entry = tk.Entry(dialog, width=25)
        phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def save_reader():
            if name_entry.get() and phone_entry.get():
                data = self.load_data()
                
                new_id = max([r['id'] for r in data['readers']], default=0) + 1
                new_reader = {
                    "id": new_id,
                    "name": name_entry.get(),
                    "phone": phone_entry.get(),
                    "registered": datetime.now().strftime("%Y-%m-%d")
                }
                
                data['readers'].append(new_reader)
                self.save_data(data)
                self.load_readers()
                dialog.destroy()
                messagebox.showinfo("Успех", "Читатель добавлен")
        
        tk.Button(dialog, text="Сохранить", command=save_reader).grid(row=2, column=0, columnspan=2, pady=20)
    
    def issue_book_dialog(self):
        """Диалог выдачи книги"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Выдать книгу")
        dialog.geometry("400x200")
        
        data = self.load_data()
        available_books = [b for b in data['books'] if b['available']]
        
        tk.Label(dialog, text="Книга:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(dialog, textvariable=book_var, width=30)
        book_combo['values'] = [f"{b['id']}: {b['title']}" for b in available_books]
        book_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Читатель:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        reader_var = tk.StringVar()
        reader_combo = ttk.Combobox(dialog, textvariable=reader_var, width=30)
        reader_combo['values'] = [f"{r['id']}: {r['name']}" for r in data['readers']]
        reader_combo.grid(row=1, column=1, padx=5, pady=5)
        
        def issue():
            if book_var.get() and reader_var.get():
                book_id = int(book_var.get().split(':')[0])
                reader_id = int(reader_var.get().split(':')[0])
                
                new_issue = {
                    "id": max([i['id'] for i in data['issues']], default=0) + 1,
                    "book_id": book_id,
                    "reader_id": reader_id,
                    "issue_date": datetime.now().strftime("%Y-%m-%d"),
                    "return_date": None
                }
                
                data['issues'].append(new_issue)
                
                # Обновляем статус книги
                for book in data['books']:
                    if book['id'] == book_id:
                        book['available'] = False
                        break
                
                self.save_data(data)
                self.load_books()
                self.load_issues()
                dialog.destroy()
                messagebox.showinfo("Успех", "Книга выдана")
        
        tk.Button(dialog, text="Выдать", command=issue).grid(row=2, column=0, columnspan=2, pady=20)
    
    def return_book(self):
        """Возврат книги"""
        selection = self.issues_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите выдачу")
            return
        
        item = self.issues_tree.item(selection[0])
        issue_id = item['values'][0]
        
        if item['values'][4] != 'Не возвращена':
            messagebox.showinfo("Информация", "Книга уже возвращена")
            return
        
        data = self.load_data()
        
        for issue in data['issues']:
            if issue['id'] == issue_id:
                issue['return_date'] = datetime.now().strftime("%Y-%m-%d")
                
                # Обновляем статус книги
                for book in data['books']:
                    if book['id'] == issue['book_id']:
                        book['available'] = True
                        break
                break
        
        self.save_data(data)
        self.load_books()
        self.load_issues()
        messagebox.showinfo("Успех", "Книга возвращена")
    
    def delete_user(self):
        """Удаление пользователя"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите пользователя")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить пользователя?"):
            item = self.users_tree.item(selection[0])
            username = item['values'][0]
            
            with open('users.json', 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            users_data['users'] = [u for u in users_data['users'] if u['username'] != username]
            
            with open('users.json', 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
            
            self.load_users()
            messagebox.showinfo("Успех", "Пользователь удален")
    
    def delete_book(self):
        """Удаление книги"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите книгу")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить книгу?"):
            item = self.books_tree.item(selection[0])
            book_id = item['values'][0]
            
            data = self.load_data()
            data['books'] = [b for b in data['books'] if b['id'] != book_id]
            
            self.save_data(data)
            self.load_books()
            messagebox.showinfo("Успех", "Книга удалена")
    
    def delete_reader(self):
        """Удаление читателя"""
        selection = self.readers_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите читателя")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить читателя?"):
            item = self.readers_tree.item(selection[0])
            reader_id = item['values'][0]
            
            data = self.load_data()
            data['readers'] = [r for r in data['readers'] if r['id'] != reader_id]
            
            self.save_data(data)
            self.load_readers()
            messagebox.showinfo("Успех", "Читатель удален")
    
    def search_books(self):
        """Поиск книг"""
        query = self.search_entry.get().lower()
        if not query:
            self.load_catalog()
            return
        
        self.catalog_tree.delete(*self.catalog_tree.get_children())
        data = self.load_data()
        
        for book in data['books']:
            if (query in book['title'].lower() or 
                query in book['author'].lower()):
                self.catalog_tree.insert('', 'end', values=(
                    book['title'], book['author'], book['year'],
                    'Доступна' if book['available'] else 'На руках'
                ))
    
    def extend_period(self):
        """Продление срока книги"""
        messagebox.showinfo("Информация", "Запрос на продление отправлен библиотекарю")
    
    def create_backup(self):
        """Создание резервной копии"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Копируем data.json
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(f'backup_data_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Копируем users.json
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        with open(f'backup_users_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Успех", f"Резервная копия создана:\nbackup_data_{timestamp}.json\nbackup_users_{timestamp}.json")
    
    def restore_backup(self):
        """Восстановление из резервной копии"""
        messagebox.showinfo("Информация", "Функция восстановления требует выбора файла резервной копии")
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.show_login_window()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LibrarySystem()
    app.run()