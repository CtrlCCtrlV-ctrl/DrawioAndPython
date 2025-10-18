"""
УПРОЩЕННЫЕ ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ СИСТЕМЫ ГИБДД

Дата: 2024
Версия: 1.1
"""

import json
from datetime import datetime
from auth import AuthManager

class TestScenarios:
    """
    Упрощенный класс для тестирования системы ГИБДД
    """

    def __init__(self):
        self.auth_manager = AuthManager()
        self.test_results = []

    def run_all_tests(self):
        """
        Запуск всех тестовых сценариев
        """
        print("=" * 60)
        print("ЗАПУСК УПРОЩЕННЫХ ТЕСТОВ СИСТЕМЫ ГИБДД")
        print("=" * 60)
        print(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Тест 1: Проверка авторизации
        self.test_authentication()

        # Тест 2: Проверка работы с данными
        self.test_data_operations()

        # Вывод итоговых результатов
        self.print_summary()
        
    def test_authentication(self):
        """
        ТЕСТ 1: Проверка авторизации в системе
        """
        print("\n" + "=" * 60)
        print("ТЕСТ 1: ПРОВЕРКА АВТОРИЗАЦИИ")
        print("=" * 60)

        # Проверка авторизации администратора
        result1 = self.auth_manager.authenticate('admin', 'admin123')
        status1 = "PASS" if result1 else "FAIL"
        print(f"Администратор: {'PASS' if result1 else 'FAIL'}")

        # Проверка авторизации инспектора
        result2 = self.auth_manager.authenticate('inspector', 'inspector123')
        status2 = "PASS" if result2 else "FAIL"
        print(f"Инспектор: {'PASS' if result2 else 'FAIL'}")

        # Проверка авторизации водителя
        result3 = self.auth_manager.authenticate('driver', 'driver123')
        status3 = "PASS" if result3 else "FAIL"
        print(f"Водитель: {'PASS' if result3 else 'FAIL'}")

        # Проверка неверного пароля
        result4 = self.auth_manager.authenticate('admin', 'wrong')
        status4 = "PASS" if not result4 else "FAIL"
        print(f"Неверный пароль: {'PASS' if not result4 else 'FAIL'}")

        self.test_results.extend([
            {'test': 'Авторизация', 'step': 1, 'status': status1},
            {'test': 'Авторизация', 'step': 2, 'status': status2},
            {'test': 'Авторизация', 'step': 3, 'status': status3},
            {'test': 'Авторизация', 'step': 4, 'status': status4}
        ])
            
    def test_data_operations(self):
        """
        ТЕСТ 2: Проверка работы с данными
        """
        print("\n" + "=" * 60)
        print("ТЕСТ 2: ПРОВЕРКА РАБОТЫ С ДАННЫМИ")
        print("=" * 60)

        # Проверка чтения данных из файлов
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            with open('users.json', 'r', encoding='utf-8') as f:
                users = json.load(f)

            print(f"Файлы данных загружены успешно")
            print(f"Найдено нарушений: {len(data['violations'])}")
            print(f"Найдено штрафов: {len(data['fines'])}")
            print(f"Найдено пользователей: {len(users['users'])}")

            status1 = "PASS"
        except Exception as e:
            print(f"Ошибка загрузки данных: {str(e)}")
            status1 = "FAIL"

        self.test_results.append({
            'test': 'Работа с данными',
            'step': 1,
            'status': status1
        })

        # Проверка структуры данных
        try:
            required_keys_data = ['violations', 'fines', 'drivers']
            required_keys_users = ['users']

            data_ok = all(key in data for key in required_keys_data)
            users_ok = all(key in users for key in required_keys_users)

            if data_ok and users_ok:
                print("Структура данных корректна")
                status2 = "PASS"
            else:
                print("Структура данных некорректна")
                status2 = "FAIL"
        except Exception as e:
            print(f"Ошибка проверки структуры: {str(e)}")
            status2 = "FAIL"

        self.test_results.append({
            'test': 'Работа с данными',
            'step': 2,
            'status': status2
        })
        
    def print_summary(self):
        """
        Вывод итоговой таблицы результатов тестирования
        """
        print("\n" + "=" * 60)
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("=" * 60)

        # Подсчет статистики
        total_tests = len(self.test_results)
        passed = len([t for t in self.test_results if t['status'] == 'PASS'])
        failed = len([t for t in self.test_results if t['status'] == 'FAIL'])

        print(f"\nВсего тестов: {total_tests}")
        print(f"Успешно: {passed}")
        print(f"Провалено: {failed}")

        # Таблица результатов
        print("\n" + "-" * 40)
        print(f"{'Тест':<20} {'Шаг':<5} {'Результат':<8}")
        print("-" * 40)

        for result in self.test_results:
            print(f"{result['test']:<20} {result['step']:<5} {result['status']:<8}")

        print("-" * 40)
        print("=" * 60)

def main():
    """
    Главная функция запуска тестов
    """
    tester = TestScenarios()
    tester.run_all_tests()
    print("\nТЕСТИРОВАНИЕ ЗАВЕРШЕНО")

if __name__ == "__main__":
    main()