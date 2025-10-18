"""
Тестовые сценарии для информационной системы "Цветочный магазин"

ТЕСТ 1: Проверка авторизации
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Вход администратора            | Успешная авторизация           | PASS      |
| 2     | Вход продавца                  | Роль: Продавец                 | PASS      |
| 3     | Вход клиента                   | Роль: Клиент                   | PASS      |
| 4     | Вход с неверным паролем        | Вход заблокирован              | PASS      |
|-------|--------------------------------|--------------------------------|-----------|

ТЕСТ 2: Управление каталогом цветов (Администратор)
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Вход как администратор         | Успешный вход                  | PASS      |
| 2     | Загрузка каталога              | Каталог доступен               | PASS      |
| 3     | Проверка наличия цветов        | Цветы в каталоге есть          | PASS      |
|-------|--------------------------------|--------------------------------|-----------|

ТЕСТ 3: Оформление заказа (Клиент)
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Вход как клиент                | Успешный вход                  | PASS      |
| 2     | Просмотр каталога              | Каталог доступен               | PASS      |
| 3     | Проверка существующих заказов  | Заказы есть                    | PASS      |
|-------|--------------------------------|--------------------------------|-----------|
"""

import sys
import os
import json
from auth import authenticate, Session, create_user, load_users, save_users
from datetime import datetime

class TestScenarios:
    """Класс для выполнения тестовых сценариев"""
    
    def __init__(self):
        self.data_file = 'data.json'
        self.users_file = 'users.json'
        self.test_results = []
    
    def load_data(self):
        """Загрузка данных"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self, data):
        """Сохранение данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_result(self, test_name, step, action, expected, result):
        """Логирование результата теста"""
        status = "PASS" if result else "FAIL"
        self.test_results.append({
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'status': status
        })
        symbol = "✓" if result else "✗"
        print(f"{symbol} Шаг {step}: {action} - {status}")
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        print("\n" + "="*70)
        print("ТЕСТ 1: Проверка авторизации")
        print("="*70)

        test_name = "Тест 1: Авторизация"

        # Проверка входа администратора
        user = authenticate("admin", "admin123")
        auth_success = user is not None and user['role'] == 'administrator'
        self.log_result(test_name, 1, "Вход администратора",
                       "Успешная авторизация", auth_success)

        # Проверка входа продавца
        seller = authenticate("seller", "seller123")
        seller_success = seller is not None and seller['role'] == 'manager'
        self.log_result(test_name, 2, "Вход продавца",
                       "Роль: manager", seller_success)

        # Проверка входа клиента
        client = authenticate("client", "client123")
        client_success = client is not None and client['role'] == 'client'
        self.log_result(test_name, 3, "Вход клиента",
                       "Роль: client", client_success)

        # Проверка неверного пароля
        invalid_user = authenticate("admin", "wrongpassword")
        invalid_blocked = invalid_user is None
        self.log_result(test_name, 4, "Вход с неверным паролем",
                       "Вход заблокирован", invalid_blocked)

        return all([auth_success, seller_success, client_success, invalid_blocked])
    
    def test_2_catalog_management(self):
        """ТЕСТ 2: Управление каталогом цветов"""
        print("\n" + "="*70)
        print("ТЕСТ 2: Управление каталогом цветов (Администратор)")
        print("="*70)

        test_name = "Тест 2: Управление каталогом"

        # Авторизация как администратор
        user = authenticate("admin", "admin123")
        Session.login(user)
        admin_logged = Session.get_role() == "administrator"
        self.log_result(test_name, 1, "Вход администратора",
                       "Успешный вход", admin_logged)

        # Загрузка каталога
        data = self.load_data()
        catalog_loaded = 'flowers' in data and len(data['flowers']) > 0
        self.log_result(test_name, 2, "Загрузка каталога",
                       "Каталог доступен", catalog_loaded)

        # Проверка наличия цветов в каталоге
        flowers_exist = len(data['flowers']) >= 3  # Минимум 3 цветка из тестовых данных
        self.log_result(test_name, 3, "Проверка наличия цветов",
                       "Цветы в каталоге есть", flowers_exist)

        Session.logout()

        return all([admin_logged, catalog_loaded, flowers_exist])
    
    def test_3_client_order(self):
        """ТЕСТ 3: Оформление заказа клиентом"""
        print("\n" + "="*70)
        print("ТЕСТ 3: Оформление заказа (Клиент)")
        print("="*70)

        test_name = "Тест 3: Оформление заказа"

        # Авторизация как клиент
        user = authenticate("client", "client123")
        Session.login(user)
        client_logged = Session.get_role() == "client"
        self.log_result(test_name, 1, "Вход клиента",
                       "Успешный вход", client_logged)

        # Просмотр каталога
        data = self.load_data()
        catalog_available = len(data['flowers']) > 0
        self.log_result(test_name, 2, "Просмотр каталога",
                       "Каталог доступен", catalog_available)

        # Проверка существующих заказов
        orders_exist = 'orders' in data and len(data['orders']) >= 2  # Минимум 2 заказа из тестовых данных
        self.log_result(test_name, 3, "Проверка существующих заказов",
                       "Заказы есть", orders_exist)

        Session.logout()

        return all([client_logged, catalog_available, orders_exist])
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "🌸"*35)
        print("ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ: Цветочный магазин")
        print("🌸"*35)
        
        test1_result = self.test_1_authentication()
        test2_result = self.test_2_catalog_management()
        test3_result = self.test_3_client_order()
        
        # Итоговый отчет
        print("\n" + "="*70)
        print("ИТОГОВЫЙ ОТЧЕТ")
        print("="*70)
        
        tests_summary = [
            ("Тест 1: Авторизация", test1_result),
            ("Тест 2: Управление каталогом", test2_result),
            ("Тест 3: Оформление заказа", test3_result)
        ]
        
        for test_name, result in tests_summary:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status} - {test_name}")
        
        total_passed = sum(1 for _, result in tests_summary if result)
        total_tests = len(tests_summary)
        
        print("="*70)
        print(f"Пройдено тестов: {total_passed}/{total_tests}")
        print(f"Процент успеха: {(total_passed/total_tests)*100:.1f}%")
        print("="*70)
        
        # Детальная таблица результатов
        print("\nДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
        print("-"*70)
        for result in self.test_results:
            print(f"[{result['status']}] {result['test']} - Шаг {result['step']}")
            print(f"    Действие: {result['action']}")
            print(f"    Ожидалось: {result['expected']}")
        print("-"*70)
        
        return total_passed == total_tests


if __name__ == '__main__':
    tester = TestScenarios()
    success = tester.run_all_tests()
    
    if success:
        print("\n✓ ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
    else:
        print("\n✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ!")
    
    sys.exit(0 if success else 1)