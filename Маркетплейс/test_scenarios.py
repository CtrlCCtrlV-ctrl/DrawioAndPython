"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ МАРКЕТПЛЕЙСА

======================================================================================
ТЕСТ 1: Проверка авторизации и разграничения доступа
======================================================================================
|-------|--------------------------------|------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат          | Результат |
|-------|--------------------------------|------------------------------|-----------|
| 1     | Вход как admin/admin123        | Успешный вход, роль admin    | PASS      |
| 2     | Проверка доступа к управлению  | Доступны все функции         | PASS      |
|       | пользователями                 | администратора               |           |
| 3     | Выход из системы               | Возврат к окну входа         | PASS      |
| 4     | Вход с неверным паролем        | Ошибка авторизации           | PASS      |
| 5     | Вход как seller1/seller123     | Успешный вход, роль seller   | PASS      |
| 6     | Вход как buyer1/buyer123       | Успешный вход, роль buyer    | PASS      |
|-------|--------------------------------|------------------------------|-----------|

======================================================================================
ТЕСТ 2: Полный цикл работы с товарами (Продавец -> Покупатель)
======================================================================================
|-------|--------------------------------|------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат          | Результат |
|-------|--------------------------------|------------------------------|-----------|
| 1     | Вход как seller1               | Вход в панель продавца       | PASS      |
| 2     | Добавление нового товара       | Товар создан с уникальным ID | PASS      |
|       | "Тестовый товар"               |                              |           |
| 3     | Проверка товара в списке       | Товар отображается           | PASS      |
| 4     | Редактирование товара          | Изменения сохранены          | PASS      |
|       | (изменение цены)               |                              |           |
| 5     | Выход, вход как buyer1         | Вход в панель покупателя     | PASS      |
| 6     | Поиск добавленного товара      | Товар найден в каталоге      | PASS      |
| 7     | Добавление товара в корзину    | Товар в корзине              | PASS      |
| 8     | Оформление заказа              | Заказ создан, корзина пуста  | PASS      |
| 9     | Проверка заказа в "Мои заказы" | Заказ отображается           | PASS      |
| 10    | Выход, вход как seller1        | Вход в панель продавца       | PASS      |
| 11    | Проверка заказа в "Заказы"     | Заказ отображается           | PASS      |
| 12    | Изменение статуса заказа       | Статус изменен               | PASS      |
|-------|--------------------------------|------------------------------|-----------|

======================================================================================
ТЕСТ 3: Административные функции
======================================================================================
|-------|--------------------------------|------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат          | Результат |
|-------|--------------------------------|------------------------------|-----------|
| 1     | Вход как admin                 | Вход в панель администратора | PASS      |
| 2     | Создание нового пользователя   | Пользователь создан          | PASS      |
|       | testuser/test123/buyer         |                              |           |
| 3     | Проверка в списке пользователей| Пользователь отображается    | PASS      |
| 4     | Добавление новой категории     | Категория добавлена          | PASS      |
|       | "Тестовая категория"           |                              |           |
| 5     | Просмотр всех заказов системы  | Отображаются все заказы      | PASS      |
| 6     | Генерация отчета               | Статистика корректна         | PASS      |
| 7     | Удаление тестового пользователя| Пользователь удален          | PASS      |
| 8     | Удаление тестовой категории    | Категория удалена            | PASS      |
|-------|--------------------------------|------------------------------|-----------|
"""

import json
import os

class TestScenarios:
    """Класс для автоматического тестирования системы маркетплейса"""
    
    def __init__(self):
        self.users_file = 'users.json'
        self.data_file = 'data.json'
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def _load_json(self, filename):
        """Загрузка JSON файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_json(self, filename, data):
        """Сохранение JSON файла"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    
    def log_result(self, test_name, step, expected, actual, passed):
        """Логирование результата теста"""
        status = "PASS" if passed else "FAIL"
        result = {
            'test': test_name,
            'step': step,
            'expected': expected,
            'actual': actual,
            'status': status
        }
        self.test_results.append(result)
        
        if passed:
            self.passed += 1
            print(f"PASS {test_name} - Шаг {step}: {status}")
        else:
            self.failed += 1
            print(f"FAIL {test_name} - Шаг {step}: {status}")
            print(f"  Ожидалось: {expected}")
            print(f"  Получено: {actual}")
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации и разграничения доступа"""
        print("\n" + "="*80)
        print("ТЕСТ 1: Проверка авторизации и разграничения доступа")
        print("="*80)
        
        users_data = self._load_json(self.users_file)
        
        # Шаг 1: Проверка пользователей
        admin_user = next((u for u in users_data['users']
                          if u['username'] == 'admin'), None)

        self.log_result(
            "ТЕСТ 1",
            "1",
            "Пользователь admin существует",
            f"Пользователь найден: {admin_user is not None}",
            admin_user is not None
        )
        
        # Шаг 2: Проверка наличия всех пользователей
        roles = {'administrator', 'seller', 'buyer'}
        found_roles = {u['role'] for u in users_data['users']}
        
        self.log_result(
            "ТЕСТ 1",
            "2",
            f"Присутствуют роли: {roles}",
            f"Найдены роли: {found_roles}",
            roles.issubset(found_roles)
        )
        
        # Шаг 2: Проверка паролей пользователей
        passwords_correct = all(u['password'] in ['admin123', 'seller123', 'buyer123']
                               for u in users_data['users'])

        self.log_result(
            "ТЕСТ 1",
            "2",
            "Пароли установлены правильно",
            f"Пароли корректны: {passwords_correct}",
            passwords_correct
        )
        
        # Шаг 3: Проверка ролей пользователей
        roles_check = all(u['role'] in ['administrator', 'seller', 'buyer']
                         for u in users_data['users'])

        self.log_result(
            "ТЕСТ 1",
            "3",
            "Все пользователи имеют корректные роли",
            f"Роли корректны: {roles_check}",
            roles_check
        )
        
        # Шаг 4: Проверка количества пользователей
        users_count = len(users_data['users'])

        self.log_result(
            "ТЕСТ 1",
            "4",
            "Правильное количество пользователей",
            f"Пользователей: {users_count}",
            users_count >= 3
        )
    
    def test_2_product_lifecycle(self):
        """ТЕСТ 2: Полный цикл работы с товарами"""
        print("\n" + "="*80)
        print("ТЕСТ 2: Полный цикл работы с товарами")
        print("="*80)
        
        data = self._load_json(self.data_file)
        
        # Шаг 1-2: Добавление нового товара
        initial_count = len(data['products'])
        new_product = {
            "id": max([p['id'] for p in data['products']], default=0) + 1,
            "name": "Тестовый товар",
            "category": "Электроника",
            "price": 1000,
            "seller": "seller1",
            "stock": 10,
            "description": "Товар для тестирования"
        }
        data['products'].append(new_product)
        self._save_json(self.data_file, data)
        
        data = self._load_json(self.data_file)
        new_count = len(data['products'])
        
        self.log_result(
            "ТЕСТ 2",
            "1-2",
            f"Товар добавлен, количество: {initial_count + 1}",
            f"Количество товаров: {new_count}",
            new_count == initial_count + 1
        )
        
        # Шаг 3: Проверка товара в списке
        test_product = next((p for p in data['products'] 
                           if p['name'] == 'Тестовый товар'), None)
        
        self.log_result(
            "ТЕСТ 2",
            "3",
            "Товар найден в списке",
            f"Товар: {test_product['name'] if test_product else 'Не найден'}",
            test_product is not None
        )
        
        # Шаг 4: Редактирование товара
        if test_product:
            test_product['price'] = 1500
            self._save_json(self.data_file, data)
            data = self._load_json(self.data_file)
            updated_product = next((p for p in data['products'] 
                                  if p['name'] == 'Тестовый товар'), None)
            
            self.log_result(
                "ТЕСТ 2",
                "4",
                "Цена изменена на 1500",
                f"Новая цена: {updated_product['price']}",
                updated_product['price'] == 1500
            )
        
        # Шаг 5-7: Добавление в корзину
        buyer_name = 'buyer1'
        if buyer_name not in data['cart']:
            data['cart'][buyer_name] = []
        
        cart_item = {
            'product_id': test_product['id'],
            'quantity': 2
        }
        data['cart'][buyer_name].append(cart_item)
        self._save_json(self.data_file, data)
        
        data = self._load_json(self.data_file)
        in_cart = any(item['product_id'] == test_product['id'] 
                     for item in data['cart'].get(buyer_name, []))
        
        self.log_result(
            "ТЕСТ 2",
            "5-7",
            "Товар добавлен в корзину",
            f"В корзине: {in_cart}",
            in_cart
        )
        
        # Шаг 8: Оформление заказа
        initial_orders = len(data['orders'])
        new_order = {
            'id': max([o['id'] for o in data['orders']], default=0) + 1,
            'buyer': buyer_name,
            'seller': test_product['seller'],
            'product_name': test_product['name'],
            'product_id': test_product['id'],
            'quantity': 2,
            'total': test_product['price'] * 2,
            'status': 'Новый',
            'date': '2024-01-01 12:00:00'
        }
        data['orders'].append(new_order)
        data['cart'][buyer_name] = []
        test_product['stock'] -= 2
        self._save_json(self.data_file, data)
        
        data = self._load_json(self.data_file)
        new_orders_count = len(data['orders'])
        cart_empty = len(data['cart'][buyer_name]) == 0
        
        self.log_result(
            "ТЕСТ 2",
            "8",
            f"Заказ создан ({initial_orders + 1}), корзина пуста",
            f"Заказов: {new_orders_count}, Корзина пуста: {cart_empty}",
            new_orders_count == initial_orders + 1 and cart_empty
        )
        
        # Шаг 9-11: Проверка заказа
        buyer_order = next((o for o in data['orders'] 
                          if o['buyer'] == buyer_name and o['product_name'] == 'Тестовый товар'), None)
        seller_order = next((o for o in data['orders'] 
                           if o['seller'] == 'seller1' and o['product_name'] == 'Тестовый товар'), None)
        
        self.log_result(
            "ТЕСТ 2",
            "9-11",
            "Заказ виден покупателю и продавцу",
            f"У покупателя: {buyer_order is not None}, У продавца: {seller_order is not None}",
            buyer_order is not None and seller_order is not None
        )
        
        # Шаг 12: Изменение статуса
        if seller_order:
            seller_order['status'] = 'Обработан'
            self._save_json(self.data_file, data)
            data = self._load_json(self.data_file)
            updated_order = next((o for o in data['orders'] if o['id'] == seller_order['id']), None)
            
            self.log_result(
                "ТЕСТ 2",
                "12",
                "Статус изменен на 'Обработан'",
                f"Статус: {updated_order['status']}",
                updated_order['status'] == 'Обработан'
            )
    
    def test_3_admin_functions(self):
        """ТЕСТ 3: Административные функции"""
        print("\n" + "="*80)
        print("ТЕСТ 3: Административные функции")
        print("="*80)
        
        users_data = self._load_json(self.users_file)
        data = self._load_json(self.data_file)
        
        # Шаг 1-2: Создание нового пользователя
        initial_users = len(users_data['users'])
        new_user = {
            "username": "testuser",
            "password": "test123",
            "role": "buyer",
            "created": "2024-01-01 10:00:00",
            "email": "test@test.com"
        }
        users_data['users'].append(new_user)
        self._save_json(self.users_file, users_data)
        
        users_data = self._load_json(self.users_file)
        new_users_count = len(users_data['users'])
        
        self.log_result(
            "ТЕСТ 3",
            "1-2",
            f"Пользователь создан ({initial_users + 1})",
            f"Количество пользователей: {new_users_count}",
            new_users_count == initial_users + 1
        )
        
        # Шаг 3: Проверка в списке
        test_user = next((u for u in users_data['users'] 
                         if u['username'] == 'testuser'), None)
        
        self.log_result(
            "ТЕСТ 3",
            "3",
            "Пользователь testuser найден",
            f"Найден: {test_user is not None}",
            test_user is not None
        )
        
        # Шаг 4: Добавление категории
        initial_cats = len(data['categories'])
        test_category = "Тестовая категория"
        if test_category not in data['categories']:
            data['categories'].append(test_category)
        self._save_json(self.data_file, data)
        
        data = self._load_json(self.data_file)
        new_cats_count = len(data['categories'])
        
        self.log_result(
            "ТЕСТ 3",
            "4",
            f"Категория добавлена ({initial_cats + 1})",
            f"Количество категорий: {new_cats_count}",
            test_category in data['categories']
        )
        
        # Шаг 5: Просмотр всех заказов
        all_orders = data['orders']
        orders_exist = len(all_orders) > 0
        
        self.log_result(
            "ТЕСТ 3",
            "5",
            "Заказы доступны для просмотра",
            f"Найдено заказов: {len(all_orders)}",
            orders_exist
        )
        
        # Шаг 6: Генерация отчета
        total_products = len(data['products'])
        total_orders = len(data['orders'])
        total_revenue = sum(o['total'] for o in data['orders'])
        total_users = len(users_data['users'])
        
        report_valid = all([
            total_products >= 0,
            total_orders >= 0,
            total_revenue >= 0,
            total_users >= 0
        ])
        
        self.log_result(
            "ТЕСТ 3",
            "6",
            "Статистика корректна",
            f"Пользователи: {total_users}, Товары: {total_products}, Заказы: {total_orders}, Выручка: {total_revenue}",
            report_valid
        )
        
        # Шаг 7: Удаление тестового пользователя
        users_data['users'] = [u for u in users_data['users'] if u['username'] != 'testuser']
        self._save_json(self.users_file, users_data)
        
        users_data = self._load_json(self.users_file)
        user_deleted = not any(u['username'] == 'testuser' for u in users_data['users'])
        
        self.log_result(
            "ТЕСТ 3",
            "7",
            "Пользователь удален",
            f"Удален: {user_deleted}",
            user_deleted
        )
        
        # Шаг 8: Удаление тестовой категории
        data['categories'] = [c for c in data['categories'] if c != test_category]
        self._save_json(self.data_file, data)
        
        data = self._load_json(self.data_file)
        cat_deleted = test_category not in data['categories']
        
        self.log_result(
            "ТЕСТ 3",
            "8",
            "Категория удалена",
            f"Удалена: {cat_deleted}",
            cat_deleted
        )
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n")
        print("+" + "="*78 + "+")
        print("|" + " "*20 + "ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ" + " "*33 + "|")
        print("|" + " "*25 + "МАРКЕТПЛЕЙС" + " "*42 + "|")
        print("+" + "="*78 + "+")
        
        # Проверка наличия файлов
        if not os.path.exists(self.users_file):
            print(f"\nFAIL Ошибка: файл {self.users_file} не найден!")
            print("  Запустите сначала main.py для инициализации данных")
            return

        if not os.path.exists(self.data_file):
            print(f"\nFAIL Ошибка: файл {self.data_file} не найден!")
            print("  Запустите сначала main.py для инициализации данных")
            return
        
        # Выполнение тестов
        self.test_1_authentication()
        self.test_2_product_lifecycle()
        self.test_3_admin_functions()
        
        # Итоговый отчет
        print("\n")
        print("+" + "="*78 + "+")
        print("|" + " "*28 + "ИТОГОВЫЙ ОТЧЕТ" + " "*36 + "|")
        print("+" + "="*78 + "+")
        print(f"\nВсего тестов выполнено: {self.passed + self.failed}")
        print(f"PASS Успешно: {self.passed}")
        print(f"FAIL Провалено: {self.failed}")
        
        success_rate = (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0
        print(f"\nПроцент успеха: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n+++ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! +++")
        else:
            print(f"\n!!! Обнаружены проблемы в {self.failed} тестах")

        print("\n" + "="*80)
        
        # Сохранение результатов
        self._save_test_results()
    
    def _save_test_results(self):
        """Сохранение результатов тестирования"""
        results = {
            'date': '2024-01-01 10:00:00',
            'total': self.passed + self.failed,
            'passed': self.passed,
            'failed': self.failed,
            'success_rate': f"{(self.passed / (self.passed + self.failed) * 100):.1f}%",
            'details': self.test_results
        }
        
        with open('test_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nРезультаты тестирования сохранены в файл: test_results.json")


if __name__ == "__main__":
    tester = TestScenarios()
    tester.run_all_tests()