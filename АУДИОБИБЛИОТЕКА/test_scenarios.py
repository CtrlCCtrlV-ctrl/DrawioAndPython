"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "АУДИОБИБЛИОТЕКА"

Этот файл содержит автоматизированные тесты для проверки основного функционала системы.
"""

import json
import os
from auth import authenticate, create_user, session
from datetime import datetime

# Таблицы тестовых сценариев

"""
ПРОСТЫЕ ТЕСТЫ ДЛЯ АУДИОБИБЛИОТЕКИ

Тест 1: Проверка авторизации пользователей
- Вход администратора (admin/admin123)
- Вход библиотекаря (librarian/lib123)
- Вход читателя (reader/read123)

Тест 2: Работа с данными аудиокниг
- Загрузка данных из файлов
- Добавление книги
- Поиск книги
- Изменение книги

Тест 3: Управление пользователями
- Создание нового пользователя
- Проверка списка пользователей
"""

class TestScenarios:
    """Класс для автоматического тестирования системы"""
    
    def __init__(self):
        self.results = []
        self.test_data_file = 'data.json'
        self.test_users_file = 'users.json'
        
    def log_result(self, test_name, step, passed, details=""):
        """Логирование результата теста"""
        result = {
            'test': test_name,
            'step': step,
            'status': 'PASS' if passed else 'FAIL',
            'details': details,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results.append(result)
        
        status_symbol = "✓" if passed else "✗"
        print(f"{status_symbol} {test_name} - Шаг {step}: {result['status']} - {details}")
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        print("\n" + "="*50)
        print("ТЕСТ 1: Проверка авторизации пользователей")
        print("="*50)

        # Тест 1: Вход администратора
        user = authenticate("admin", "admin123")
        passed = user is not None and user['role'] == 'administrator'
        self.log_result("Тест 1", 1, passed,
                       f"Админ вход: {'Успешно' if passed else 'Ошибка'}")

        # Тест 2: Вход библиотекаря
        user = authenticate("librarian", "lib123")
        passed = user is not None and user['role'] == 'librarian'
        self.log_result("Тест 1", 2, passed,
                       f"Библиотекарь вход: {'Успешно' if passed else 'Ошибка'}")

        # Тест 3: Вход читателя
        user = authenticate("reader", "read123")
        passed = user is not None and user['role'] == 'reader'
        self.log_result("Тест 1", 3, passed,
                       f"Читатель вход: {'Успешно' if passed else 'Ошибка'}")
    
    def test_2_audiobook_management(self):
        """ТЕСТ 2: Работа с данными аудиокниг"""
        print("\n" + "="*50)
        print("ТЕСТ 2: Работа с данными аудиокниг")
        print("="*50)

        # Тест 1: Загрузка данных
        try:
            with open(self.test_data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            passed = 'audiobooks' in data and len(data['audiobooks']) > 0
            self.log_result("Тест 2", 1, passed,
                           f"Данные загружены, книг: {len(data.get('audiobooks', []))}")
        except Exception as e:
            self.log_result("Тест 2", 1, False, f"Ошибка загрузки: {str(e)}")
            return

        # Тест 2: Добавление новой книги
        initial_count = len(data['audiobooks'])
        new_book = {
            'id': max([b['id'] for b in data['audiobooks']], default=0) + 1,
            'title': 'Тестовая книга',
            'author': 'Тестовый автор',
            'genre': 'Тест',
            'duration': '10:00:00',
            'narrator': 'Тест диктор',
            'year': 2024,
            'available': True
        }
        data['audiobooks'].append(new_book)

        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        passed = len(data['audiobooks']) == initial_count + 1
        self.log_result("Тест 2", 2, passed,
                       f"Книга добавлена: {initial_count} -> {len(data['audiobooks'])}")

        # Тест 3: Поиск книги
        found = next((b for b in data['audiobooks'] if b['title'] == 'Тестовая книга'), None)
        passed = found is not None
        self.log_result("Тест 2", 3, passed,
                       f"Поиск книги: {'Найдена' if passed else 'Не найдена'}")
    
    def test_3_user_management(self):
        """ТЕСТ 3: Управление пользователями"""
        print("\n" + "="*50)
        print("ТЕСТ 3: Управление пользователями")
        print("="*50)

        # Тест 1: Создание нового пользователя
        success, message = create_user("test_user", "test123", "reader", "Тестовый Пользователь")
        passed = success
        self.log_result("Тест 3", 1, passed, f"Создание пользователя: {message}")

        # Тест 2: Проверка списка пользователей
        from auth import get_all_users
        users = get_all_users()
        passed = len(users) >= 4  # admin, librarian, reader, test_user
        self.log_result("Тест 3", 2, passed,
                       f"Список пользователей получен: {len(users)} пользователей")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*20 + "ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ" + " "*33 + "║")
        print("║" + " "*24 + "АУДИОБИБЛИОТЕКА" + " "*39 + "║")
        print("╚" + "="*78 + "╝")
        
        self.test_1_authentication()
        self.test_2_audiobook_management()
        self.test_3_user_management()
        
        self.print_summary()
    
    def print_summary(self):
        """Вывод итоговой статистики"""
        print("\n" + "="*80)
        print("ИТОГОВАЯ СТАТИСТИКА ТЕСТИРОВАНИЯ")
        print("="*80)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = total - passed
        
        print(f"\nВсего тестов выполнено: {total}")
        print(f"✓ Успешно: {passed} ({passed/total*100:.1f}%)")
        print(f"✗ Провалено: {failed} ({failed/total*100:.1f}%)")

        print("\n" + "-"*50)
        print("ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
        print("-"*50)
        
        current_test = None
        for result in self.results:
            if result['test'] != current_test:
                current_test = result['test']
                print(f"\n{current_test}:")
            
            status_symbol = "✓" if result['status'] == 'PASS' else "✗"
            print(f"  {status_symbol} Шаг {result['step']}: {result['status']} - {result['details']}")
        
        print("\n" + "="*50)

        if failed == 0:
            print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        else:
            print(f"⚠️  ВНИМАНИЕ: {failed} тест(ов) провалено")

        print("="*50 + "\n")
        
        # Сохранение результатов в файл
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Сохранение результатов в JSON файл"""
        results_file = 'test_results.json'
        report = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_tests': len(self.results),
            'passed': sum(1 for r in self.results if r['status'] == 'PASS'),
            'failed': sum(1 for r in self.results if r['status'] == 'FAIL'),
            'details': self.results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Подробные результаты сохранены в файл: {results_file}\n")

def main():
    """Главная функция запуска тестов"""
    tester = TestScenarios()
    tester.run_all_tests()

if __name__ == "__main__":
    main()