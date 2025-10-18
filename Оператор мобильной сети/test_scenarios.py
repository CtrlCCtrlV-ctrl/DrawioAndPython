"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ СИСТЕМЫ ОПЕРАТОРА МОБИЛЬНОЙ СВЯЗИ

Данный файл содержит автоматизированные тесты для проверки основных функций системы.
"""

import json
import os
from auth import AuthManager

class TestScenarios:
    def __init__(self):
        self.users_file = 'users.json'
        self.data_file = 'data.json'
        self.results = []
    
    
    def log_result(self, test_name, step, action, expected, result):
        """Логирование результата теста"""
        self.results.append({
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'result': result
        })
    
    def test_1_authentication(self):
        """
        ТЕСТ 1: Проверка авторизации
        |-------|--------------------------------|--------------------------------|-----------|
        | Шаг   | Действие                       | Ожидаемый результат            | Результат |
        |-------|--------------------------------|--------------------------------|-----------|
        | 1     | Вход с верными данными admin   | Авторизация успешна            | PASS      |
        | 2     | Проверка роли администратора   | Роль = administrator           | PASS      |
        | 3     | Выход из системы               | current_user = None            | PASS      |
        | 4     | Вход с неверным паролем        | Авторизация отклонена          | PASS      |
        | 5     | Вход как клиент                | Авторизация успешна, роль=client| PASS      |
        |-------|--------------------------------|--------------------------------|-----------|
        """
        print("\n" + "="*80)
        print("ТЕСТ 1: ПРОВЕРКА АВТОРИЗАЦИИ")
        print("="*80)
        
        auth = AuthManager(self.users_file)

        # Шаг 1: Вход с верными данными
        step1 = auth.login('admin', 'admin')
        self.log_result('ТЕСТ 1', 1, 'Вход с верными данными admin', 'True', 'PASS' if step1 else 'FAIL')
        print(f"Шаг 1: Вход admin - {'✓ PASS' if step1 else '✗ FAIL'}")

        # Шаг 2: Проверка роли
        step2 = auth.get_role() == 'administrator'
        self.log_result('ТЕСТ 1', 2, 'Проверка роли администратора', 'administrator', 'PASS' if step2 else 'FAIL')
        print(f"Шаг 2: Роль администратора - {'✓ PASS' if step2 else '✗ FAIL'}")

        # Шаг 3: Выход
        auth.logout()
        step3 = auth.get_current_user() is None
        self.log_result('ТЕСТ 1', 3, 'Выход из системы', 'None', 'PASS' if step3 else 'FAIL')
        print(f"Шаг 3: Выход из системы - {'✓ PASS' if step3 else '✗ FAIL'}")

        # Шаг 4: Неверный пароль
        step4 = not auth.login('admin', 'wrong_password')
        self.log_result('ТЕСТ 1', 4, 'Вход с неверным паролем', 'False', 'PASS' if step4 else 'FAIL')
        print(f"Шаг 4: Неверный пароль - {'✓ PASS' if step4 else '✗ FAIL'}")

        # Шаг 5: Вход как клиент
        step5 = auth.login('client1', '1234') and auth.get_role() == 'client'
        self.log_result('ТЕСТ 1', 5, 'Вход как клиент', 'client', 'PASS' if step5 else 'FAIL')
        print(f"Шаг 5: Вход клиента - {'✓ PASS' if step5 else '✗ FAIL'}")
        
        test_passed = all([step1, step2, step3, step4, step5])
        print(f"\nРезультат теста 1: {'✓ УСПЕШНО' if test_passed else '✗ ПРОВАЛ'}")
        return test_passed
    
    def test_2_user_management(self):
        """
        ТЕСТ 2: Управление пользователями
        |-------|--------------------------------|--------------------------------|-----------|
        | Шаг   | Действие                       | Ожидаемый результат            | Результат |
        |-------|--------------------------------|--------------------------------|-----------|
        | 1     | Создание нового пользователя   | Пользователь создан            | PASS      |
        | 2     | Проверка существования         | Пользователь найден в списке   | PASS      |
        | 3     | Попытка создать дубликат       | Ошибка, пользователь существует| PASS      |
        | 4     | Обновление данных пользователя | Данные обновлены               | PASS      |
        | 5     | Удаление пользователя          | Пользователь удален            | PASS      |
        |-------|--------------------------------|--------------------------------|-----------|
        """
        print("\n" + "="*80)
        print("ТЕСТ 2: УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
        print("="*80)
        
        auth = AuthManager(self.users_file)

        # Шаг 1: Создание пользователя
        step1 = auth.create_user('new_operator', 'password123', 'operator', '+79002222222')
        self.log_result('ТЕСТ 2', 1, 'Создание пользователя', 'True', 'PASS' if step1 else 'FAIL')
        print(f"Шаг 1: Создание пользователя - {'✓ PASS' if step1 else '✗ FAIL'}")

        # Шаг 2: Проверка существования
        step2 = auth.user_exists('new_operator')
        self.log_result('ТЕСТ 2', 2, 'Проверка существования', 'True', 'PASS' if step2 else 'FAIL')
        print(f"Шаг 2: Пользователь существует - {'✓ PASS' if step2 else '✗ FAIL'}")

        # Шаг 3: Попытка дубликата
        step3 = not auth.create_user('new_operator', 'password', 'client')
        self.log_result('ТЕСТ 2', 3, 'Создание дубликата', 'False', 'PASS' if step3 else 'FAIL')
        print(f"Шаг 3: Предотвращение дубликата - {'✓ PASS' if step3 else '✗ FAIL'}")

        # Шаг 4: Обновление данных
        step4 = auth.update_user('new_operator', phone='+79003333333')
        updated_user = next((u for u in auth.get_all_users() if u['username'] == 'new_operator'), None)
        step4 = step4 and updated_user and updated_user['phone'] == '+79003333333'
        self.log_result('ТЕСТ 2', 4, 'Обновление данных', 'True', 'PASS' if step4 else 'FAIL')
        print(f"Шаг 4: Обновление данных - {'✓ PASS' if step4 else '✗ FAIL'}")

        # Шаг 5: Удаление
        auth.delete_user('new_operator')
        step5 = not auth.user_exists('new_operator')
        self.log_result('ТЕСТ 2', 5, 'Удаление пользователя', 'True', 'PASS' if step5 else 'FAIL')
        print(f"Шаг 5: Удаление пользователя - {'✓ PASS' if step5 else '✗ FAIL'}")
        
        test_passed = all([step1, step2, step3, step4, step5])
        print(f"\nРезультат теста 2: {'✓ УСПЕШНО' if test_passed else '✗ ПРОВАЛ'}")
        return test_passed
    
    def test_3_data_operations(self):
        """
        ТЕСТ 3: Операции с данными (клиенты, тарифы)
        |-------|--------------------------------|--------------------------------|-----------|
        | Шаг   | Действие                       | Ожидаемый результат            | Результат |
        |-------|--------------------------------|--------------------------------|-----------|
        | 1     | Загрузка тестовых данных       | Данные загружены               | PASS      |
        | 2     | Добавление нового клиента      | Клиент добавлен в список       | PASS      |
        | 3     | Изменение баланса клиента      | Баланс обновлен                | PASS      |
        | 4     | Добавление нового тарифа       | Тариф добавлен                 | PASS      |
        | 5     | Сохранение изменений в файл    | Данные сохранены корректно     | PASS      |
        |-------|--------------------------------|--------------------------------|-----------|
        """
        print("\n" + "="*80)
        print("ТЕСТ 3: ОПЕРАЦИИ С ДАННЫМИ")
        print("="*80)
        
        # Шаг 1: Загрузка данных
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            step1 = True
        except:
            step1 = False
        self.log_result('ТЕСТ 3', 1, 'Загрузка данных', 'True', 'PASS' if step1 else 'FAIL')
        print(f"Шаг 1: Загрузка данных - {'✓ PASS' if step1 else '✗ FAIL'}")

        # Шаг 2: Добавление клиента
        new_client = {
            "id": 4,
            "phone": "+79005555555",
            "name": "Новый Клиент",
            "tariff_id": 1,
            "balance": 1000.0,
            "status": "active",
            "registered": "2024-03-01"
        }
        data['clients'].append(new_client)
        step2 = len(data['clients']) == 4
        self.log_result('ТЕСТ 3', 2, 'Добавление клиента', '4 клиента', 'PASS' if step2 else 'FAIL')
        print(f"Шаг 2: Добавление клиента - {'✓ PASS' if step2 else '✗ FAIL'}")

        # Шаг 3: Изменение баланса
        data['clients'][0]['balance'] += 100
        step3 = data['clients'][0]['balance'] == 250.50
        self.log_result('ТЕСТ 3', 3, 'Изменение баланса', '250.50', 'PASS' if step3 else 'FAIL')
        print(f"Шаг 3: Изменение баланса - {'✓ PASS' if step3 else '✗ FAIL'}")

        # Шаг 4: Добавление тарифа
        new_tariff = {
            "id": 4,
            "name": "Супер тариф",
            "price": 500,
            "minutes": 1000,
            "internet": 50,
            "sms": 500,
            "description": "Тестовый тариф"
        }
        data['tariffs'].append(new_tariff)
        step4 = len(data['tariffs']) == 4
        self.log_result('ТЕСТ 3', 4, 'Добавление тарифа', '4 тарифа', 'PASS' if step4 else 'FAIL')
        print(f"Шаг 4: Добавление тарифа - {'✓ PASS' if step4 else '✗ FAIL'}")

        # Шаг 5: Сохранение
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            with open(self.data_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

            step5 = (len(loaded_data['clients']) == 4 and
                    len(loaded_data['tariffs']) == 4 and
                    loaded_data['clients'][0]['balance'] == 250.50)
        except:
            step5 = False

        self.log_result('ТЕСТ 3', 5, 'Сохранение данных', 'True', 'PASS' if step5 else 'FAIL')
        print(f"Шаг 5: Сохранение данных - {'✓ PASS' if step5 else '✗ FAIL'}")
        
        test_passed = all([step1, step2, step3, step4, step5])
        print(f"\nРезультат теста 3: {'✓ УСПЕШНО' if test_passed else '✗ ПРОВАЛ'}")
        return test_passed
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " "*20 + "АВТОМАТИЗИРОВАННОЕ ТЕСТИРОВАНИЕ" + " "*27 + "█")
        print("█" + " "*15 + "Система оператора мобильной связи" + " "*30 + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")
        
        test_results = []
        
        # Запуск тестов
        test_results.append(('Тест 1: Авторизация', self.test_1_authentication()))
        test_results.append(('Тест 2: Управление пользователями', self.test_2_user_management()))
        test_results.append(('Тест 3: Операции с данными', self.test_3_data_operations()))
        
        # Итоговая таблица
        print("\n" + "="*80)
        print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
        print("="*80)
        print(f"{'Тест':<45} | {'Результат':^10}")
        print("-"*80)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = '✓ PASS' if result else '✗ FAIL'
            print(f"{test_name:<45} | {status:^10}")
            if result:
                passed += 1
        
        print("="*80)
        print(f"Пройдено тестов: {passed}/{total} ({passed*100//total}%)")
        print("="*80 + "\n")

        return all(result for _, result in test_results)

if __name__ == '__main__':
    tester = TestScenarios()
    all_passed = tester.run_all_tests()
    
    if all_passed:
        print("✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")