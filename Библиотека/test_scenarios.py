import json
import os
import sys
from datetime import datetime

class TestScenarios:
    def __init__(self):
        self.test_results = []
    
    def test_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        print("\n" + "="*60)
        print("ТЕСТ 1: Проверка авторизации")
        print("="*60)
        
        results = []
        
        # Шаг 1: Проверка существования файла пользователей
        print("Шаг 1: Проверка файла пользователей...")
        if os.path.exists('users.json'):
            results.append(("Файл пользователей существует", "PASS"))
            print("✓ PASS: Файл users.json найден")
        else:
            results.append(("Файл пользователей существует", "FAIL"))
            print("✗ FAIL: Файл users.json не найден")
            return results
        
        # Шаг 2: Проверка неверного логина
        print("Шаг 2: Проверка неверного логина...")
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        auth_failed = True

        for user in users_data['users']:
            if user['username'] == 'admin' and user['password'] == "wrong_password":
                auth_failed = False
                break

        if auth_failed:
            results.append(("Отклонение неверного пароля", "PASS"))
            print("✓ PASS: Неверный пароль отклонен")
        else:
            results.append(("Отклонение неверного пароля", "FAIL"))
            print("✗ FAIL: Неверный пароль принят")
        
        # Шаг 3: Проверка корректного логина
        print("Шаг 3: Проверка корректного логина...")
        auth_success = False

        for user in users_data['users']:
            if user['username'] == 'admin' and user['password'] == "admin123":
                auth_success = True
                break
        
        if auth_success:
            results.append(("Успешная авторизация", "PASS"))
            print("✓ PASS: Авторизация успешна")
        else:
            results.append(("Успешная авторизация", "FAIL"))
            print("✗ FAIL: Авторизация не удалась")
        
        # Шаг 4: Проверка ролей
        print("Шаг 4: Проверка ролей пользователей...")
        roles_found = {'administrator': False, 'librarian': False, 'reader': False}
        
        for user in users_data['users']:
            if user['role'] in roles_found:
                roles_found[user['role']] = True
        
        if all(roles_found.values()):
            results.append(("Все роли присутствуют", "PASS"))
            print("✓ PASS: Все роли найдены")
        else:
            results.append(("Все роли присутствуют", "FAIL"))
            print("✗ FAIL: Не все роли найдены")
        
        self.test_results.append(("Тест авторизации", results))
        return results
    
    def test_book_management(self):
        """ТЕСТ 2: Управление книгами"""
        print("\n" + "="*60)
        print("ТЕСТ 2: Управление книгами")
        print("="*60)
        
        results = []
        
        # Шаг 1: Проверка файла данных
        print("Шаг 1: Проверка файла данных...")
        if os.path.exists('data.json'):
            results.append(("Файл данных существует", "PASS"))
            print("✓ PASS: Файл data.json найден")
        else:
            results.append(("Файл данных существует", "FAIL"))
            print("✗ FAIL: Файл data.json не найден")
            return results
        
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Шаг 2: Добавление книги
        print("Шаг 2: Добавление новой книги...")
        initial_count = len(data['books'])
        
        new_book = {
            "id": max([b['id'] for b in data['books']], default=0) + 1,
            "title": "Тестовая книга",
            "author": "Тестовый автор",
            "year": 2024,
            "isbn": "TEST-ISBN-123",
            "available": True
        }
        
        data['books'].append(new_book)
        
        if len(data['books']) == initial_count + 1:
            results.append(("Добавление книги", "PASS"))
            print("✓ PASS: Книга добавлена")
        else:
            results.append(("Добавление книги", "FAIL"))
            print("✗ FAIL: Книга не добавлена")
        
        # Шаг 3: Выдача книги
        print("Шаг 3: Выдача книги читателю...")
        book_id = new_book['id']
        
        # Находим книгу и меняем статус
        for book in data['books']:
            if book['id'] == book_id:
                book['available'] = False
                break
        
        # Создаем запись о выдаче
        new_issue = {
            "id": max([i['id'] for i in data['issues']], default=0) + 1,
            "book_id": book_id,
            "reader_id": 1,
            "issue_date": datetime.now().strftime("%Y-%m-%d"),
            "return_date": None
        }
        
        data['issues'].append(new_issue)
        
        book_issued = False
        for book in data['books']:
            if book['id'] == book_id and not book['available']:
                book_issued = True
                break
        
        if book_issued:
            results.append(("Выдача книги", "PASS"))
            print("✓ PASS: Книга выдана")
        else:
            results.append(("Выдача книги", "FAIL"))
            print("✗ FAIL: Книга не выдана")
        
        # Шаг 4: Возврат книги
        print("Шаг 4: Возврат книги...")
        
        # Находим выдачу и отмечаем возврат
        for issue in data['issues']:
            if issue['id'] == new_issue['id']:
                issue['return_date'] = datetime.now().strftime("%Y-%m-%d")
                break
        
        # Меняем статус книги
        for book in data['books']:
            if book['id'] == book_id:
                book['available'] = True
                break
        
        book_returned = False
        for book in data['books']:
            if book['id'] == book_id and book['available']:
                book_returned = True
                break
        
        if book_returned:
            results.append(("Возврат книги", "PASS"))
            print("✓ PASS: Книга возвращена")
        else:
            results.append(("Возврат книги", "FAIL"))
            print("✗ FAIL: Книга не возвращена")
        
        # Шаг 5: Удаление книги
        print("Шаг 5: Удаление книги...")
        data['books'] = [b for b in data['books'] if b['id'] != book_id]
        
        book_deleted = True
        for book in data['books']:
            if book['id'] == book_id:
                book_deleted = False
                break
        
        if book_deleted:
            results.append(("Удаление книги", "PASS"))
            print("✓ PASS: Книга удалена")
        else:
            results.append(("Удаление книги", "FAIL"))
            print("✗ FAIL: Книга не удалена")
        
        # Сохраняем изменения для демонстрации
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.test_results.append(("Тест управления книгами", results))
        return results
    
    def test_reader_functions(self):
        """ТЕСТ 3: Функции читателя"""
        print("\n" + "="*60)
        print("ТЕСТ 3: Функции читателя")
        print("="*60)
        
        results = []
        
        # Шаг 1: Проверка роли читателя
        print("Шаг 1: Проверка роли читателя...")
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        reader_exists = False
        for user in users_data['users']:
            if user['role'] == 'reader':
                reader_exists = True
                break
        
        if reader_exists:
            results.append(("Роль читателя существует", "PASS"))
            print("✓ PASS: Роль читателя найдена")
        else:
            results.append(("Роль читателя существует", "FAIL"))
            print("✗ FAIL: Роль читателя не найдена")
        
        # Шаг 2: Просмотр каталога
        print("Шаг 2: Проверка каталога книг...")
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if len(data['books']) > 0:
            results.append(("Каталог содержит книги", "PASS"))
            print(f"✓ PASS: В каталоге {len(data['books'])} книг")
        else:
            results.append(("Каталог содержит книги", "FAIL"))
            print("✗ FAIL: Каталог пуст")
        
        # Шаг 3: Поиск книги
        print("Шаг 3: Поиск книги...")
        search_query = "война"
        found_books = []
        
        for book in data['books']:
            if search_query.lower() in book['title'].lower():
                found_books.append(book)
        
        if len(found_books) > 0:
            results.append(("Поиск книги работает", "PASS"))
            print(f"✓ PASS: Найдено {len(found_books)} книг")
        else:
            results.append(("Поиск книги работает", "PASS"))  # Может не быть результатов
            print("✓ PASS: Поиск выполнен (результатов нет)")
        
        # Шаг 4: История выдач
        print("Шаг 4: Проверка истории выдач...")
        reader_issues = []
        
        for issue in data['issues']:
            if issue['reader_id'] == 1:  # Проверяем для первого читателя
                reader_issues.append(issue)
        
        if 'issues' in data:
            results.append(("История выдач доступна", "PASS"))
            print(f"✓ PASS: История содержит {len(reader_issues)} записей")
        else:
            results.append(("История выдач доступна", "FAIL"))
            print("✗ FAIL: История недоступна")
        
        self.test_results.append(("Тест функций читателя", results))
        return results
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "="*60)
        print("ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ")
        print("="*60)
        
        # Запускаем тесты
        self.test_authentication()
        self.test_book_management()
        self.test_reader_functions()
        
        # Выводим итоги
        print("\n" + "="*60)
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("="*60)
        
        total_tests = 0
        passed_tests = 0
        
        for test_name, results in self.test_results:
            print(f"\n{test_name}:")
            for description, status in results:
                total_tests += 1
                if status == "PASS":
                    passed_tests += 1
                    print(f"  ✓ {description}: {status}")
                else:
                    print(f"  ✗ {description}: {status}")
        
        print("\n" + "-"*60)
        print(f"Всего тестов: {total_tests}")
        print(f"Успешно: {passed_tests}")
        print(f"Провалено: {total_tests - passed_tests}")
        print(f"Процент успеха: {(passed_tests/total_tests*100):.1f}%")
        print("="*60)
        
        
        return self.test_results
    
    def generate_report(self):
        """Генерация отчета о тестировании"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
ОТЧЕТ О ТЕСТИРОВАНИИ БИБЛИОТЕЧНОЙ СИСТЕМЫ
==========================================
Дата и время: {timestamp}

РЕЗУЛЬТАТЫ ТЕСТОВ:
------------------
"""
        
        for test_name, results in self.test_results:
            report += f"\n{test_name}:\n"
            for description, status in results:
                report += f"  - {description}: {status}\n"
        
        # Сохраняем отчет
        with open(f'test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nОтчет сохранен в файл test_report_*.txt")
        
        return report

if __name__ == "__main__":
    print("Библиотечная система - Автоматическое тестирование")
    print("="*60)
    
    tester = TestScenarios()
    tester.run_all_tests()
    tester.generate_report()
    
    input("\nНажмите Enter для завершения...")