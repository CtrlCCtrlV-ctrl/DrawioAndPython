import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

import auth

"""
ПРОСТЫЕ ТЕСТЫ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "КОМПЬЮТЕРНЫЙ МАГАЗИН"
"""

class TestScenarios:
    """Класс для выполнения тестовых сценариев"""

    def __init__(self):
        self.data_file = 'data.json'
        self.users_file = 'users.json'
        self.results = []

    def log_result(self, test_name, expected, actual, status):
        """Логирование результата теста"""
        result = {
            'test': test_name,
            'expected': expected,
            'actual': actual,
            'status': status
        }
        self.results.append(result)

        status_symbol = "✓" if status == "PASS" else "✗"
        print(f"{status_symbol} {test_name}: {status}")
        print(f"  Ожидалось: {expected}")
        print(f"  Получено: {actual}")
        print()
    
    def test1_authentication(self):
        """ТЕСТ 1: Проверка авторизации пользователей"""
        print("="*50)
        print("ТЕСТ 1: ПРОВЕРКА АВТОРИЗАЦИИ")
        print("="*50)

        # Тест администратора
        user = auth.authenticate('admin', 'admin123')
        expected = "Успешная авторизация администратора"
        actual = f"Роль: {user['role']}" if user else "Ошибка авторизации"
        status = "PASS" if user and user['role'] == 'administrator' else "FAIL"
        self.log_result("Администратор", expected, actual, status)

        # Тест продавца
        user = auth.authenticate('seller', 'seller123')
        expected = "Успешная авторизация продавца"
        actual = f"Роль: {user['role']}" if user else "Ошибка авторизации"
        status = "PASS" if user and user['role'] == 'seller' else "FAIL"
        self.log_result("Продавец", expected, actual, status)

        # Тест клиента
        user = auth.authenticate('client', 'client123')
        expected = "Успешная авторизация клиента"
        actual = f"Роль: {user['role']}" if user else "Ошибка авторизации"
        status = "PASS" if user and user['role'] == 'client' else "FAIL"
        self.log_result("Клиент", expected, actual, status)

        # Тест неверного пароля
        user = auth.authenticate('admin', 'wrongpassword')
        expected = "Ошибка авторизации с неверным паролем"
        actual = "Ошибка авторизации" if user is None else "Авторизация прошла"
        status = "PASS" if user is None else "FAIL"
        self.log_result("Неверный пароль", expected, actual, status)
    
    def test2_data_loading(self):
        """ТЕСТ 2: Загрузка данных"""
        print("="*50)
        print("ТЕСТ 2: ЗАГРУЗКА ДАННЫХ")
        print("="*50)

        # Тест загрузки товаров
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            expected = "Файл загружен успешно"
            actual = f"Загружено товаров: {len(data['products'])}, заказов: {len(data['orders'])}"
            status = "PASS"
        except Exception as e:
            expected = "Файл загружен успешно"
            actual = f"Ошибка загрузки: {e}"
            status = "FAIL"

        self.log_result("Загрузка данных", expected, actual, status)

        # Тест загрузки пользователей
        try:
            users = auth.get_all_users()
            expected = "Пользователи загружены успешно"
            actual = f"Загружено пользователей: {len(users)}"
            status = "PASS"
        except Exception as e:
            expected = "Пользователи загружены успешно"
            actual = f"Ошибка загрузки пользователей: {e}"
            status = "FAIL"

        self.log_result("Загрузка пользователей", expected, actual, status)
    
    def test3_order_processing(self):
        """ТЕСТ 3: Обработка заказов"""
        print("="*50)
        print("ТЕСТ 3: ОБРАБОТКА ЗАКАЗОВ")
        print("="*50)

        # Загружаем данные
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Проверяем, что есть заказы
        orders_count = len(data['orders'])
        expected = "Есть заказы для обработки"
        actual = f"Найдено заказов: {orders_count}"
        status = "PASS" if orders_count > 0 else "FAIL"
        self.log_result("Проверка заказов", expected, actual, status)

        # Проверяем товары в наличии
        products_count = len(data['products'])
        expected = "Есть товары в каталоге"
        actual = f"Найдено товаров: {products_count}"
        status = "PASS" if products_count > 0 else "FAIL"
        self.log_result("Проверка товаров", expected, actual, status)
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("ЗАПУСК ПРОСТЫХ ТЕСТОВ")
        print("="*50)

        self.test1_authentication()
        self.test2_data_loading()
        self.test3_order_processing()

        self.print_summary()

    def print_summary(self):
        """Вывод итоговой таблицы результатов"""
        print("\n" + "="*50)
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("="*50)

        passed = len([r for r in self.results if r['status'] == 'PASS'])
        failed = len([r for r in self.results if r['status'] == 'FAIL'])
        total = len(self.results)

        print(f"Всего тестов: {total}")
        print(f"✓ Успешно: {passed}")
        print(f"✗ Ошибок: {failed}")
        print(f"Процент успеха: {(passed/total*100):.1f}%")

if __name__ == "__main__":
    # Запуск тестов
    tester = TestScenarios()
    tester.run_all_tests()
    