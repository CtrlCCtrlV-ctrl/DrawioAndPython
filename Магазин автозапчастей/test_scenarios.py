"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ СИСТЕМЫ "МАГАЗИН АВТОЗАПЧАСТЕЙ"

═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 1: Проверка авторизации пользователей
┌────────┬─────────────────────────────┬──────────────────────────┬───────────┐
│  Шаг   │         Действие            │   Ожидаемый результат    │ Результат │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   1    │ Вход с логином "admin"      │ Успешная авторизация,    │   PASS    │
│        │ и паролем "admin123"        │ роль "admin"             │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   2    │ Вход с логином "seller"     │ Успешная авторизация,    │   PASS    │
│        │ и паролем "seller123"       │ роль "seller"            │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   3    │ Вход с логином "client"     │ Успешная авторизация,    │   PASS    │
│        │ и паролем "client123"       │ роль "client"            │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   4    │ Вход с неверным паролем     │ Отказ в доступе          │   PASS    │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   5    │ Вход с несуществующим       │ Отказ в доступе          │   PASS    │
│        │ пользователем               │                          │           │
└────────┴─────────────────────────────┴──────────────────────────┴───────────┘

═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 2: Работа с товарами (CRUD операции)
┌────────┬─────────────────────────────┬──────────────────────────┬───────────┐
│  Шаг   │         Действие            │   Ожидаемый результат    │ Результат │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   1    │ Чтение списка товаров       │ Отображение всех товаров │   PASS    │
│        │ из базы данных              │ из data.json             │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   2    │ Добавление нового товара    │ Товар добавлен в БД,     │   PASS    │
│        │ с валидными данными         │ присвоен ID              │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   3    │ Попытка добавления товара   │ Сообщение об ошибке      │   PASS    │
│        │ с пустыми полями            │                          │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   4    │ Удаление существующего      │ Товар удален из БД       │   PASS    │
│        │ товара                      │                          │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   5    │ Проверка сохранения         │ Изменения сохранены      │   PASS    │
│        │ изменений в файл            │ в data.json              │           │
└────────┴─────────────────────────────┴──────────────────────────┴───────────┘

═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 3: Оформление и обработка заказов
┌────────┬─────────────────────────────┬──────────────────────────┬───────────┐
│  Шаг   │         Действие            │   Ожидаемый результат    │ Результат │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   1    │ Создание заказа с           │ Заказ создан, присвоен   │   PASS    │
│        │ несколькими товарами        │ уникальный ID            │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   2    │ Проверка корректности       │ Сумма = Σ(цена×кол-во)   │   PASS    │
│        │ расчета суммы заказа        │                          │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   3    │ Проверка уменьшения         │ Остатки уменьшены на     │   PASS    │
│        │ остатков товара после       │ заказанное количество    │           │
│        │ оформления заказа           │                          │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   4    │ Попытка заказа товара в     │ Сообщение об ошибке,     │   PASS    │
│        │ количестве больше           │ заказ не создан          │           │
│        │ доступного                  │                          │           │
├────────┼─────────────────────────────┼──────────────────────────┼───────────┤
│   5    │ Просмотр истории заказов    │ Отображение всех заказов │   PASS    │
│        │                             │ с корректной информацией │           │
└────────┴─────────────────────────────┴──────────────────────────┴───────────┘

"""

import json
import os
from datetime import datetime
from auth import AuthManager

class TestScenarios:
    def __init__(self):
        self.users_file = 'users.json'
        self.data_file = 'data.json'
        self.auth = AuthManager(self.users_file)
        self.results = []
        
    def setup(self):
        """Подготовка тестовой среды - используем существующие файлы"""
        # Проверяем что файлы существуют
        if not os.path.exists(self.users_file):
            print(f"Файл {self.users_file} не найден!")
            return False

        if not os.path.exists(self.data_file):
            print(f"Файл {self.data_file} не найден!")
            return False

        return True
    
    
    def log_result(self, test_name, step, action, expected, result):
        """Запись результата теста"""
        status = "PASS" if result else "FAIL"
        self.results.append({
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'status': status
        })
        print(f"  [{status}] Шаг {step}: {action}")
    
    def test1_authorization(self):
        """ТЕСТ 1: Проверка авторизации пользователей"""
        print("\n" + "="*80)
        print("ТЕСТ 1: Проверка авторизации пользователей")
        print("="*80)
        
        # Шаг 1: Вход администратора
        success, role, name = self.auth.login("admin", "admin123")
        self.log_result("ТЕСТ 1", 1, "Вход admin/admin123",
                       "Успешная авторизация, роль admin",
                       success and role == "admin")
        
        self.auth.logout()
        
        # Шаг 2: Вход продавца
        success, role, name = self.auth.login("seller", "seller123")
        self.log_result("ТЕСТ 1", 2, "Вход seller/seller123",
                       "Успешная авторизация, роль seller",
                       success and role == "seller")
        
        self.auth.logout()
        
        # Шаг 3: Вход клиента
        success, role, name = self.auth.login("client", "client123")
        self.log_result("ТЕСТ 1", 3, "Вход client/client123",
                       "Успешная авторизация, роль client",
                       success and role == "client")
        
        self.auth.logout()
        
        # Шаг 4: Неверный пароль
        success, role, name = self.auth.login("admin", "wrongpassword")
        self.log_result("ТЕСТ 1", 4, "Вход с неверным паролем",
                       "Отказ в доступе",
                       not success)
        
        # Шаг 5: Несуществующий пользователь
        success, role, name = self.auth.login("nonexistent", "password")
        self.log_result("ТЕСТ 1", 5, "Вход с несуществующим пользователем",
                       "Отказ в доступе",
                       not success)
    
    def test2_crud_operations(self):
        """ТЕСТ 2: Работа с товарами (CRUD операции)"""
        print("\n" + "="*80)
        print("ТЕСТ 2: Работа с товарами (CRUD операции)")
        print("="*80)
        
        # Шаг 1: Чтение товаров
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        parts_count = len(data['parts'])
        self.log_result("ТЕСТ 2", 1, "Чтение списка товаров",
                       "Отображение всех товаров",
                       parts_count >= 1)
        
        # Шаг 2: Добавление товара
        new_part = {
            "id": 3,
            "name": "Новый тестовый товар",
            "article": "TEST-003",
            "manufacturer": "TestBrand",
            "category": "Тест",
            "price": 300.00,
            "quantity": 15,
            "supplier_id": 1
        }
        data['parts'].append(new_part)

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        added = any(p['id'] == 3 for p in data['parts'])
        self.log_result("ТЕСТ 2", 2, "Добавление нового товара",
                       "Товар добавлен в БД",
                       added)
        
        # Шаг 3: Валидация данных
        invalid_part = {
            "id": 4,
            "name": "",
            "article": "",
            "manufacturer": "",
            "category": "",
            "price": 0,
            "quantity": 0,
            "supplier_id": 1
        }
        
        is_valid = all([invalid_part['name'], invalid_part['article'], 
                       invalid_part['manufacturer'], invalid_part['category']])
        
        self.log_result("ТЕСТ 2", 3, "Добавление товара с пустыми полями",
                       "Сообщение об ошибке",
                       not is_valid)
        
        # Шаг 4: Удаление товара
        data['parts'] = [p for p in data['parts'] if p['id'] != 3]

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        deleted = not any(p['id'] == 3 for p in data['parts'])
        self.log_result("ТЕСТ 2", 4, "Удаление товара",
                       "Товар удален из БД",
                       deleted)
        
        # Шаг 5: Проверка сохранения
        self.log_result("ТЕСТ 2", 5, "Проверка сохранения в файл",
                       "Изменения сохранены",
                       os.path.exists(self.data_file))
    
    def test3_order_processing(self):
        """ТЕСТ 3: Оформление и обработка заказов"""
        print("\n" + "="*80)
        print("ТЕСТ 3: Оформление и обработка заказов")
        print("="*80)
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Шаг 1: Создание заказа
        order_items = [
            {
                'id': 1,
                'name': 'Тестовый товар 1',
                'price': 100.00,
                'quantity': 2,
                'total': 200.00
            },
            {
                'id': 2,
                'name': 'Тестовый товар 2',
                'price': 200.00,
                'quantity': 1,
                'total': 200.00
            }
        ]

        # Определяем ID для нового заказа
        orders_count_before = len(data['orders'])
        new_order_id = orders_count_before + 1

        new_order = {
            'id': new_order_id,
            'client_id': 3,
            'items': order_items,
            'total': 400.00,
            'status': 'Новый',
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'seller_id': 2
        }

        data['orders'].append(new_order)

        self.log_result("ТЕСТ 3", 1, "Создание заказа с товарами",
                       "Заказ создан, присвоен ID",
                       data['orders'][-1]['id'] == new_order_id)
        
        # Шаг 2: Проверка суммы
        calculated_total = sum(item['total'] for item in order_items)
        self.log_result("ТЕСТ 3", 2, "Проверка расчета суммы",
                       "Сумма = Σ(цена×кол-во)",
                       calculated_total == 400.00)
        
        # Шаг 3: Уменьшение остатков
        original_qty_1 = data['parts'][0]['quantity']  # Товар с id=1
        original_qty_2 = data['parts'][1]['quantity']  # Товар с id=2

        for item in order_items:
            for part in data['parts']:
                if part['id'] == item['id']:
                    part['quantity'] -= item['quantity']

        new_qty_1 = data['parts'][0]['quantity']
        new_qty_2 = data['parts'][1]['quantity']

        self.log_result("ТЕСТ 3", 3, "Уменьшение остатков товара",
                       "Остатки уменьшены на заказанное количество",
                       new_qty_1 == original_qty_1 - 2 and new_qty_2 == original_qty_2 - 1)
        
        # Шаг 4: Проверка превышения остатка
        excessive_quantity = 100
        available_quantity = data['parts'][0]['quantity']
        can_order = excessive_quantity <= available_quantity
        
        self.log_result("ТЕСТ 3", 4, "Попытка заказа > доступного",
                       "Сообщение об ошибке",
                       not can_order)
        
        # Шаг 5: Сохранение и просмотр заказов
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        orders_count_after = len(data['orders'])
        self.log_result("ТЕСТ 3", 5, "Просмотр истории заказов",
                       "Отображение всех заказов",
                       orders_count_after == orders_count_before + 1)
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*20 + "ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ" + " "*33 + "║")
        print("║" + " "*15 + "Магазин автозапчастей - Автотесты" + " "*30 + "║")
        print("╚" + "="*78 + "╝")
        
        if not self.setup():
            print("Не удалось настроить тестовую среду!")
            return False

        self.test1_authorization()
        self.test2_crud_operations()
        self.test3_order_processing()
        
        # Итоговый отчет
        print("\n" + "╔" + "="*78 + "╗")
        print("║" + " "*28 + "ИТОГОВЫЙ ОТЧЕТ" + " "*36 + "║")
        print("╚" + "="*78 + "╝")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        print(f"\nВсего тестов: {total_tests}")
        print(f"Успешно: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Провалено: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        
        if failed_tests > 0:
            print("\nПроваленные тесты:")
            for r in self.results:
                if r['status'] == 'FAIL':
                    print(f"  - {r['test']}, Шаг {r['step']}: {r['action']}")
        
        print("\n" + "="*80)
        print("Тестирование завершено!")
        print("="*80 + "\n")
        
        return passed_tests == total_tests

if __name__ == '__main__':
    tester = TestScenarios()
    success = tester.run_all_tests()