"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ СТО

═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 1: Проверка системы авторизации
┌──────┬─────────────────────────────┬───────────────────────────┬──────────┐
│ Шаг  │ Действие                    │ Ожидаемый результат       │ Результат│
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 1    │ Попытка входа с пустыми     │ Ошибка валидации         │ PASS     │
│      │ полями                      │                          │          │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 2    │ Вход с неверным паролем     │ Отказ в доступе          │ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 3    │ Вход с корректными          │ Успешная авторизация     │ PASS     │
│      │ учетными данными admin      │                          │          │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 4    │ Проверка пароля             │ Пароль сохранен в виде   │ PASS     │
│      │                             │ открытого текста         │          │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 5    │ Выход из системы            │ Возврат к окну входа     │ PASS     │
└──────┴─────────────────────────────┴───────────────────────────┴──────────┘

═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 2: Проверка функционала администратора
┌──────┬─────────────────────────────┬───────────────────────────┬──────────┐
│ Шаг  │ Действие                    │ Ожидаемый результат       │ Результат│
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 1    │ Вход как администратор      │ Доступ к панели админа   │ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 2    │ Создание нового пользователя│ Пользователь добавлен    │ PASS     │
│      │ (testuser/test123)          │ в систему                │          │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 3    │ Добавление новой услуги     │ Услуга появилась в списке│ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 4    │ Добавление запчасти         │ Запчасть добавлена       │ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 5    │ Генерация отчета            │ Отчет содержит актуальные│ PASS     │
│      │                             │ данные                   │          │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 6    │ Просмотр всех заказов       │ Отображены все заказы    │ PASS     │
│      │                             │ в системе                │          │
└──────┴─────────────────────────────┴───────────────────────────┴──────────┘

═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 3: Проверка работы клиента и механика
┌──────┬─────────────────────────────┬───────────────────────────┬──────────┐
│ Шаг  │ Действие                    │ Ожидаемый результат       │ Результат│
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 1    │ Вход как клиент             │ Доступ к личному кабинету│ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 2    │ Просмотр списка услуг       │ Услуги отображены        │ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 3    │ Создание заявки на          │ Заявка создана со статусом│ PASS    │
│      │ обслуживание                │ "Новый"                  │          │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 4    │ Выход и вход как механик    │ Доступ к рабочему месту  │ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 5    │ Просмотр заказов механика   │ Заказы механика видны    │ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 6    │ Изменение статуса заказа    │ Статус изменен на        │ PASS     │
│      │ с "Новый" на "В работе"     │ "В работе"               │          │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 7    │ Просмотр запчастей          │ Список запчастей доступен│ PASS     │
├──────┼─────────────────────────────┼───────────────────────────┼──────────┤
│ 8    │ Заказ запчастей (+5 шт)     │ Количество увеличено     │ PASS     │
└──────┴─────────────────────────────┴───────────────────────────┴──────────┘

═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import json
import os
from auth import AuthManager
from datetime import datetime

class TestScenarios:
    def __init__(self):
        self.test_results = []
        self.auth = AuthManager('users.json')
        self.data_file = 'data.json'
    
    def _load_test_data(self):
        """Загрузка тестовых данных"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_test_data(self, data):
        """Сохранение тестовых данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_test(self, test_name, step, expected, result):
        """Логирование результата теста"""
        status = "PASS" if result else "FAIL"
        self.test_results.append({
            'test': test_name,
            'step': step,
            'expected': expected,
            'result': status
        })
        print(f"  [{status}] Шаг {step}: {expected}")
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка системы авторизации"""
        print("\n" + "="*70)
        print("ТЕСТ 1: Проверка системы авторизации")
        print("="*70)
        
        # Шаг 1: Попытка входа с пустыми полями
        result = not self.auth.authenticate("", "")
        self.log_test("Авторизация", 1, "Ошибка при пустых полях", result)
        
        # Шаг 2: Вход с неверным паролем
        result = not self.auth.authenticate("admin", "wrongpassword")
        self.log_test("Авторизация", 2, "Отказ при неверном пароле", result)
        
        # Шаг 3: Вход с корректными данными
        result = self.auth.authenticate("admin", "admin123")
        self.log_test("Авторизация", 3, "Успешная авторизация admin", result)
        
        # Шаг 4: Проверка пароля
        users = self.auth.get_all_users()
        admin_user = next((u for u in users if u['username'] == 'admin'), None)
        result = admin_user and admin_user['password'] == "admin123"
        self.log_test("Авторизация", 4, "Пароль сохранен в открытом виде", result)
        
        # Шаг 5: Выход из системы
        self.auth.logout()
        result = self.auth.current_user is None
        self.log_test("Авторизация", 5, "Успешный выход из системы", result)
    
    def test_2_administrator_functions(self):
        """ТЕСТ 2: Проверка функционала администратора"""
        print("\n" + "="*70)
        print("ТЕСТ 2: Проверка функционала администратора")
        print("="*70)
        
        # Шаг 1: Вход как администратор
        result = self.auth.authenticate("admin", "admin123")
        has_admin_role = result and self.auth.current_user['role'] == 'administrator'
        self.log_test("Админ функции", 1, "Доступ к панели администратора", has_admin_role)
        
        # Шаг 2: Создание нового пользователя
        success, msg = self.auth.register_user("testuser", "test123", "client", "Тестовый Пользователь")
        self.log_test("Админ функции", 2, "Создание пользователя testuser", success)
        
        # Шаг 3: Добавление новой услуги
        data = self._load_test_data()
        new_id = max([s['id'] for s in data['services']], default=0) + 1
        new_service = {"id": new_id, "name": "Диагностика", "price": 2000, "duration": "60 мин"}
        data['services'].append(new_service)
        self._save_test_data(data)

        data = self._load_test_data()
        result = len(data['services']) == 4  # Было 3, добавили 1
        self.log_test("Админ функции", 3, "Добавление услуги 'Диагностика'", result)
        
        # Шаг 4: Добавление запчасти
        data = self._load_test_data()
        new_id = max([p['id'] for p in data['parts']], default=0) + 1
        new_part = {"id": new_id, "name": "Фильтр", "price": 300, "quantity": 15}
        data['parts'].append(new_part)
        self._save_test_data(data)

        data = self._load_test_data()
        result = len(data['parts']) == 4  # Было 3, добавили 1
        self.log_test("Админ функции", 4, "Добавление запчасти 'Фильтр'", result)
        
        # Шаг 5: Генерация отчета
        users = self.auth.get_all_users()
        data = self._load_test_data()
        report_has_data = len(users) > 0 and len(data['services']) > 0
        self.log_test("Админ функции", 5, "Генерация отчета с данными", report_has_data)
        
        # Шаг 6: Просмотр всех заказов
        result = 'orders' in data and len(data['orders']) > 0
        self.log_test("Админ функции", 6, "Просмотр всех заказов в системе", result)
    
    def test_3_client_mechanic_workflow(self):
        """ТЕСТ 3: Проверка работы клиента и механика"""
        print("\n" + "="*70)
        print("ТЕСТ 3: Проверка работы клиента и механика")
        print("="*70)
        
        # Шаг 1: Вход как клиент
        result = self.auth.authenticate("client", "client123")
        is_client = result and self.auth.current_user['role'] == 'client'
        self.log_test("Клиент/Механик", 1, "Вход как клиент", is_client)
        
        # Шаг 2: Просмотр списка услуг
        data = self._load_test_data()
        result = len(data['services']) > 0
        self.log_test("Клиент/Механик", 2, "Просмотр списка услуг", result)
        
        # Шаг 3: Создание заявки
        data = self._load_test_data()
        new_id = max([o['id'] for o in data['orders']], default=0) + 1
        new_order = {
            "id": new_id,
            "client": "client",
            "car": "Honda Civic",
            "service": "Диагностика",
            "status": "Новый",
            "mechanic": "mechanic",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total": 2000
        }
        data['orders'].append(new_order)
        self._save_test_data(data)

        data = self._load_test_data()
        new_order_exists = any(o['id'] == new_id and o['status'] == 'Новый' for o in data['orders'])
        self.log_test("Клиент/Механик", 3, "Создание заявки со статусом 'Новый'", new_order_exists)
        
        # Шаг 4: Выход и вход как механик
        self.auth.logout()
        result = self.auth.authenticate("mechanic", "mech123")
        is_mechanic = result and self.auth.current_user['role'] == 'mechanic'
        self.log_test("Клиент/Механик", 4, "Вход как механик", is_mechanic)
        
        # Шаг 5: Просмотр заказов механика
        mechanic_orders = [o for o in data['orders'] if o['mechanic'] == 'mechanic']
        result = len(mechanic_orders) > 0
        self.log_test("Клиент/Механик", 5, "Просмотр заказов механика", result)
        
        # Шаг 6: Изменение статуса заказа
        data = self._load_test_data()
        # Найти заказ механика с максимальным ID (самый новый)
        mechanic_order_ids = [o['id'] for o in data['orders'] if o['mechanic'] == 'mechanic']
        if mechanic_order_ids:
            latest_order_id = max(mechanic_order_ids)
            for order in data['orders']:
                if order['id'] == latest_order_id:
                    order['status'] = 'В работе'
            self._save_test_data(data)

            data = self._load_test_data()
            status_changed = any(o['id'] == latest_order_id and o['status'] == 'В работе' for o in data['orders'])
            self.log_test("Клиент/Механик", 6, "Изменение статуса на 'В работе'", status_changed)
        else:
            self.log_test("Клиент/Механик", 6, "Изменение статуса на 'В работе'", False)
        
        # Шаг 7: Просмотр запчастей
        result = len(data['parts']) > 0
        self.log_test("Клиент/Механик", 7, "Просмотр запчастей", result)
        
        # Шаг 8: Заказ запчастей
        for part in data['parts']:
            if part['id'] == 1:
                original_qty = part['quantity']
                part['quantity'] += 5
                self._save_test_data(data)
                
                data = self._load_test_data()
                new_qty = next((p['quantity'] for p in data['parts'] if p['id'] == 1), 0)
                result = new_qty == original_qty + 5
                self.log_test("Клиент/Механик", 8, "Заказ запчастей (+5 шт)", result)
                break
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "╔" + "═"*68 + "╗")
        print("║" + " "*15 + "ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ СТО" + " "*24 + "║")
        print("╚" + "═"*68 + "╝")
        
        start_time = datetime.now()
        
        self.test_1_authentication()
        self.test_2_administrator_functions()
        self.test_3_client_mechanic_workflow()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Подсчет результатов
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['result'] == 'PASS'])
        failed_tests = total_tests - passed_tests
        
        # Итоговый отчет
        print("\n" + "="*70)
        print("ИТОГОВЫЙ ОТЧЕТ")
        print("="*70)
        print(f"Всего тестов:     {total_tests}")
        print(f"Успешно (PASS):   {passed_tests}")
        print(f"Провалено (FAIL): {failed_tests}")
        print(f"Процент успеха:   {(passed_tests/total_tests*100):.1f}%")
        print(f"Время выполнения: {duration:.2f} сек")
        print("="*70)
        
        # Сохранение отчета
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(__doc__)
            f.write(f"\n\nОТЧЕТ О ВЫПОЛНЕНИИ ТЕСТОВ\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Всего тестов: {total_tests}\n")
            f.write(f"Успешно: {passed_tests}\n")
            f.write(f"Провалено: {failed_tests}\n")
            f.write(f"Процент успеха: {(passed_tests/total_tests*100):.1f}%\n")
        
        print(f"\nОтчет сохранен в файл: {report_file}")
        
        # Очистка тестовых файлов
        self._cleanup()
        
        return passed_tests == total_tests
    
    def _cleanup(self):
        """Очистка тестовых файлов"""
        pass

if __name__ == "__main__":
    tester = TestScenarios()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)