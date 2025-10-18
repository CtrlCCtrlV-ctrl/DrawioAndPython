"""
УПРОЩЕННЫЕ ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "РЫБОЛОВНЫЙ МАГАЗИН"
"""

import json
import sys
from auth import AuthManager

class TestScenarios:
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
        self.auth = AuthManager()

    def run_tests(self):
        """Запуск всех тестов"""
        print("=" * 80)
        print("ЗАПУСК ТЕСТОВ")
        print("=" * 80)

        # Тест авторизации
        self.test_authentication()

        # Тест управления пользователями
        self.test_user_management()

        # Тест загрузки данных
        self.test_data_loading()

        # Вывод результатов
        self.print_results()

    def test_authentication(self):
        """Тест авторизации"""
        print("\n--- ТЕСТ АВТОРИЗАЦИИ ---")

        # Тест 1: Успешный вход admin
        success, role = self.auth.login("admin", "admin123")
        self.assert_true(success and role == "administrator", "Успешный вход администратора")

        # Тест 2: Успешный вход seller
        self.auth.logout()
        success, role = self.auth.login("seller", "seller123")
        self.assert_true(success and role == "seller", "Успешный вход продавца")

        # Тест 3: Успешный вход client
        self.auth.logout()
        success, role = self.auth.login("client", "client123")
        self.assert_true(success and role == "client", "Успешный вход клиента")

        # Тест 4: Неверный пароль
        success, role = self.auth.login("admin", "wrongpass")
        self.assert_false(success, "Неверный пароль отклонен")

        # Тест 5: Неверный логин
        success, role = self.auth.login("wronguser", "admin123")
        self.assert_false(success, "Неверный логин отклонен")

    def test_user_management(self):
        """Тест управления пользователями"""
        print("\n--- ТЕСТ УПРАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯМИ ---")

        # Тест получения списка пользователей
        users = self.auth.get_all_users()
        self.assert_true(len(users) >= 3, "Получен список пользователей")

        # Проверка наличия всех ролей
        roles = [user['role'] for user in users]
        self.assert_true("administrator" in roles, "Есть администратор")
        self.assert_true("seller" in roles, "Есть продавец")
        self.assert_true("client" in roles, "Есть клиент")

    def test_data_loading(self):
        """Тест загрузки данных"""
        print("\n--- ТЕСТ ЗАГРУЗКИ ДАННЫХ ---")

        # Тест загрузки данных из файла
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Проверка структуры данных
            self.assert_true('categories' in data, "Есть категории")
            self.assert_true('products' in data, "Есть товары")
            self.assert_true('customers' in data, "Есть клиенты")
            self.assert_true('orders' in data, "Есть заказы")

            # Проверка наличия данных
            self.assert_true(len(data['categories']) > 0, "Есть категории")
            self.assert_true(len(data['products']) > 0, "Есть товары")
            self.assert_true(len(data['customers']) > 0, "Есть клиенты")

        except Exception as e:
            self.assert_true(False, f"Ошибка загрузки данных: {e}")

    def assert_true(self, condition, message):
        """Проверка условия"""
        if condition:
            self.passed += 1
            print(f"✓ PASS: {message}")
        else:
            self.failed += 1
            print(f"✗ FAIL: {message}")

    def assert_false(self, condition, message):
        """Проверка отрицательного условия"""
        self.assert_true(not condition, message)

    def print_results(self):
        """Вывод результатов тестирования"""
        print("\n" + "=" * 80)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("=" * 80)
        print(f"Пройдено: {self.passed}")
        print(f"Провалено: {self.failed}")
        print(f"Всего: {self.passed + self.failed}")

        if self.failed == 0:
            print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        else:
            print("❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ!")

if __name__ == "__main__":
    tester = TestScenarios()
    tester.run_tests()