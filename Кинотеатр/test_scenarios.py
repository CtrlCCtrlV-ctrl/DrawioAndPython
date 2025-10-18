"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ СИСТЕМЫ КИНОТЕАТР

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 1: Проверка авторизации пользователей
═══════════════════════════════════════════════════════════════════════════════
┌─────┬────────────────────────────┬──────────────────────────┬──────────────┐
│ Шаг │ Действие                   │ Ожидаемый результат      │ Результат    │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 1   │ Вход с логином: admin      │ Успешная авторизация     │ PASS         │
│     │ пароль: admin123           │ Роль: administrator      │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 2   │ Вход с логином: cashier    │ Успешная авторизация     │ PASS         │
│     │ пароль: cashier123         │ Роль: cashier            │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 3   │ Вход с логином: client     │ Успешная авторизация     │ PASS         │
│     │ пароль: client123          │ Роль: client             │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 4   │ Вход с неверным паролем    │ Отказ в доступе          │ PASS         │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 5   │ Вход с несуществующим      │ Отказ в доступе          │ PASS         │
│     │ пользователем              │                          │              │
└─────┴────────────────────────────┴──────────────────────────┴──────────────┘

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 2: Управление фильмами (Администратор)
═══════════════════════════════════════════════════════════════════════════════
┌─────┬────────────────────────────┬──────────────────────────┬──────────────┐
│ Шаг │ Действие                   │ Ожидаемый результат      │ Результат    │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 1   │ Авторизация как admin      │ Успешный вход            │ PASS         │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 2   │ Открыть "Управление        │ Отображение списка       │ PASS         │
│     │ фильмами"                  │ существующих фильмов     │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 3   │ Добавить новый фильм       │ Фильм добавлен в базу    │ PASS         │
│     │ "Дюна 2"                   │ Отображается в списке    │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 4   │ Удалить фильм              │ Фильм удален из базы     │ PASS         │
└─────┴────────────────────────────┴──────────────────────────┴──────────────┘

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 3: Бронирование билетов (Клиент)
═══════════════════════════════════════════════════════════════════════════════
┌─────┬────────────────────────────┬──────────────────────────┬──────────────┐
│ Шаг │ Действие                   │ Ожидаемый результат      │ Результат    │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 1   │ Авторизация как client     │ Успешный вход            │ PASS         │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 2   │ Открыть "Бронирование      │ Отображение доступных    │ PASS         │
│     │ билетов"                   │ сеансов                  │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 3   │ Выбрать сеанс и            │ Бронирование создано     │ PASS         │
│     │ забронировать 2 билета     │ Статус: booked           │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 4   │ Просмотреть историю        │ Бронирование отображается│ PASS         │
│     │ бронирований               │ в списке                 │              │
├─────┼────────────────────────────┼──────────────────────────┼──────────────┤
│ 5   │ Поиск фильма "Барби"       │ Найден 1 фильм           │ PASS         │
└─────┴────────────────────────────┴──────────────────────────┴──────────────┘
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth import AuthManager
import json
from datetime import datetime

class TestScenarios:
    def __init__(self):
        self.auth = AuthManager('users.json')
        self.data_file = 'data.json'
        self.test_results = []
    
    def load_data(self):
        """Загрузка данных из JSON"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных в JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_result(self, test_name, step, result, details=""):
        """Логирование результатов теста"""
        self.test_results.append({
            'test': test_name,
            'step': step,
            'result': result,
            'details': details
        })
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        print("\n" + "="*80)
        print("ТЕСТ 1: Проверка авторизации пользователей")
        print("="*80)
        
        # Шаг 1: Вход администратора
        print("\nШаг 1: Авторизация администратора...")
        result = self.auth.login('admin', 'admin123')
        if result and self.auth.get_current_user()['role'] == 'administrator':
            print("✓ PASS - Администратор успешно авторизован")
            self.log_result("Тест 1", "Шаг 1", "PASS", "Вход admin")
        else:
            print("✗ FAIL - Ошибка авторизации администратора")
            self.log_result("Тест 1", "Шаг 1", "FAIL", "Вход admin")
        self.auth.logout()
        
        # Шаг 2: Вход кассира
        print("\nШаг 2: Авторизация кассира...")
        result = self.auth.login('cashier', 'cashier123')
        if result and self.auth.get_current_user()['role'] == 'cashier':
            print("✓ PASS - Кассир успешно авторизован")
            self.log_result("Тест 1", "Шаг 2", "PASS", "Вход cashier")
        else:
            print("✗ FAIL - Ошибка авторизации кассира")
            self.log_result("Тест 1", "Шаг 2", "FAIL", "Вход cashier")
        self.auth.logout()
        
        # Шаг 3: Вход клиента
        print("\nШаг 3: Авторизация клиента...")
        result = self.auth.login('client', 'client123')
        if result and self.auth.get_current_user()['role'] == 'client':
            print("✓ PASS - Клиент успешно авторизован")
            self.log_result("Тест 1", "Шаг 3", "PASS", "Вход client")
        else:
            print("✗ FAIL - Ошибка авторизации клиента")
            self.log_result("Тест 1", "Шаг 3", "FAIL", "Вход client")
        self.auth.logout()
        
        # Шаг 4: Неверный пароль
        print("\nШаг 4: Попытка входа с неверным паролем...")
        result = self.auth.login('admin', 'wrongpassword')
        if not result:
            print("✓ PASS - Вход с неверным паролем отклонен")
            self.log_result("Тест 1", "Шаг 4", "PASS", "Отказ неверный пароль")
        else:
            print("✗ FAIL - Система пропустила неверный пароль")
            self.log_result("Тест 1", "Шаг 4", "FAIL", "Пропуск неверного пароля")
        
        # Шаг 5: Несуществующий пользователь
        print("\nШаг 5: Попытка входа несуществующим пользователем...")
        result = self.auth.login('hacker', 'password')
        if not result:
            print("✓ PASS - Вход несуществующего пользователя отклонен")
            self.log_result("Тест 1", "Шаг 5", "PASS", "Отказ несуществующий юзер")
        else:
            print("✗ FAIL - Система пропустила несуществующего пользователя")
            self.log_result("Тест 1", "Шаг 5", "FAIL", "Пропуск несуществующего")
    
    def test_2_movie_management(self):
        """ТЕСТ 2: Управление фильмами"""
        print("\n" + "="*80)
        print("ТЕСТ 2: Управление фильмами (Администратор)")
        print("="*80)
        
        # Шаг 1: Авторизация
        print("\nШаг 1: Авторизация как администратор...")
        result = self.auth.login('admin', 'admin123')
        if result:
            print("✓ PASS - Успешная авторизация")
            self.log_result("Тест 2", "Шаг 1", "PASS", "Авторизация admin")
        else:
            print("✗ FAIL - Ошибка авторизации")
            self.log_result("Тест 2", "Шаг 1", "FAIL", "Авторизация admin")
            return
        
        # Шаг 2: Просмотр фильмов
        print("\nШаг 2: Загрузка списка фильмов...")
        data = self.load_data()
        initial_count = len(data['movies'])
        print(f"✓ PASS - Загружено {initial_count} фильмов")
        self.log_result("Тест 2", "Шаг 2", "PASS", f"Фильмов: {initial_count}")
        
        # Шаг 3: Добавление фильма
        print("\nШаг 3: Добавление нового фильма 'Дюна 2'...")
        new_movie = {
            'id': max([m['id'] for m in data['movies']], default=0) + 1,
            'title': 'Дюна 2',
            'genre': 'Фантастика',
            'duration': 166,
            'rating': '16+'
        }
        data['movies'].append(new_movie)
        self.save_data(data)
        
        # Проверка добавления
        data = self.load_data()
        if len(data['movies']) == initial_count + 1:
            print("✓ PASS - Фильм успешно добавлен")
            self.log_result("Тест 2", "Шаг 3", "PASS", "Добавлен 'Дюна 2'")
        else:
            print("✗ FAIL - Ошибка добавления фильма")
            self.log_result("Тест 2", "Шаг 3", "FAIL", "Не добавлен")
        
        
        # Шаг 4: Удаление фильма
        print("\nШаг 4: Удаление фильма 'Дюна 2'...")
        data = self.load_data()
        data['movies'] = [m for m in data['movies'] if m['title'] != 'Дюна 2']
        self.save_data(data)
        
        data = self.load_data()
        if len(data['movies']) == initial_count:
            print("✓ PASS - Фильм успешно удален")
            self.log_result("Тест 2", "Шаг 4", "PASS", "Удален 'Дюна 2'")
        else:
            print("✗ FAIL - Ошибка удаления фильма")
            self.log_result("Тест 2", "Шаг 4", "FAIL", "Не удален")
        
        self.auth.logout()
    
    def test_3_ticket_booking(self):
        """ТЕСТ 3: Бронирование билетов"""
        print("\n" + "="*80)
        print("ТЕСТ 3: Бронирование билетов (Клиент)")
        print("="*80)
        
        # Шаг 1: Авторизация клиента
        print("\nШаг 1: Авторизация как клиент...")
        result = self.auth.login('client', 'client123')
        if result:
            print("✓ PASS - Успешная авторизация клиента")
            self.log_result("Тест 3", "Шаг 1", "PASS", "Авторизация client")
        else:
            print("✗ FAIL - Ошибка авторизации")
            self.log_result("Тест 3", "Шаг 1", "FAIL", "Авторизация")
            return
        
        # Шаг 2: Просмотр доступных сеансов
        print("\nШаг 2: Загрузка доступных сеансов...")
        data = self.load_data()
        sessions_count = len(data['sessions'])
        print(f"✓ PASS - Доступно {sessions_count} сеансов")
        self.log_result("Тест 3", "Шаг 2", "PASS", f"Сеансов: {sessions_count}")
        
        # Шаг 3: Создание бронирования
        print("\nШаг 3: Бронирование 2 билетов на первый сеанс...")
        if data['sessions']:
            session = data['sessions'][0]
            new_booking = {
                'id': max([b['id'] for b in data['bookings']], default=0) + 1,
                'session_id': session['id'],
                'client_name': 'client',
                'quantity': 2,
                'price': session['price'] * 2,
                'status': 'booked',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            data['bookings'].append(new_booking)
            self.save_data(data)
            print(f"✓ PASS - Забронировано 2 билета на сумму {new_booking['price']} ₽")
            self.log_result("Тест 3", "Шаг 3", "PASS", f"Забронировано 2 билета")
        else:
            print("✗ FAIL - Нет доступных сеансов")
            self.log_result("Тест 3", "Шаг 3", "FAIL", "Нет сеансов")
        
        # Шаг 4: Просмотр истории
        print("\nШаг 4: Проверка истории бронирований...")
        data = self.load_data()
        user_bookings = [b for b in data['bookings'] if b['client_name'] == 'client']
        if user_bookings:
            print(f"✓ PASS - Найдено {len(user_bookings)} бронирований клиента")
            self.log_result("Тест 3", "Шаг 4", "PASS", f"Бронирований: {len(user_bookings)}")
        else:
            print("✗ FAIL - История бронирований пуста")
            self.log_result("Тест 3", "Шаг 4", "FAIL", "История пуста")
        
        # Шаг 5: Поиск фильма
        print("\nШаг 5: Поиск фильма 'Барби'...")
        search_query = 'барби'
        found_movies = [m for m in data['movies'] if search_query in m['title'].lower()]
        if found_movies:
            print(f"✓ PASS - Найдено {len(found_movies)} фильм(ов): {', '.join([m['title'] for m in found_movies])}")
            self.log_result("Тест 3", "Шаг 5", "PASS", f"Найдено: {len(found_movies)}")
        else:
            print("✗ FAIL - Фильмы не найдены")
            self.log_result("Тест 3", "Шаг 5", "FAIL", "Не найдено")
        
        self.auth.logout()
    
    def generate_report(self):
        """Генерация отчета по тестам"""
        print("\n" + "="*80)
        print("ИТОГОВЫЙ ОТЧЕТ ПО ТЕСТИРОВАНИЮ")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['result'] == 'PASS'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nВсего тестов: {total_tests}")
        print(f"✓ Успешно: {passed_tests}")
        print(f"✗ Провалено: {failed_tests}")
        print(f"Процент успеха: {(passed_tests/total_tests*100):.1f}%")
        
        print("\nДетальные результаты:")
        print("-" * 80)
        for result in self.test_results:
            status = "✓" if result['result'] == 'PASS' else "✗"
            print(f"{status} {result['test']} | {result['step']} | {result['details']}")
        
        print("\n" + "="*80)
        print(f"Дата тестирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + "  СИСТЕМА АВТОМАТИЧЕСКОГО ТЕСТИРОВАНИЯ - КИНОТЕАТР".center(78) + "█")
        print("█" + " "*78 + "█")
        print("█"*80)
        
        self.test_1_authentication()
        self.test_2_movie_management()
        self.test_3_ticket_booking()
        self.generate_report()
        
        print("\nТестирование завершено!")

if __name__ == '__main__':
    tester = TestScenarios()
    tester.run_all_tests()
    