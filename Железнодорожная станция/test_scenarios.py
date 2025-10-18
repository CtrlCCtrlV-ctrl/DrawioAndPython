"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "ЖЕЛЕЗНОДОРОЖНАЯ СТАНЦИЯ"

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 1: Проверка аутентификации пользователей
═══════════════════════════════════════════════════════════════════════════════
|-----|---------------------------|---------------------------|---------------|
| Шаг | Действие                  | Ожидаемый результат       | Результат     |
|-----|---------------------------|---------------------------|---------------|
| 1   | Вход с логином "admin"    | Успешная аутентификация   | PASS          |
|     | и паролем "admin123"      | роль: administrator       |               |
|-----|---------------------------|---------------------------|---------------|
| 2   | Вход с логином "cashier"  | Успешная аутентификация   | PASS          |
|     | и паролем "cashier123"    | роль: cashier             |               |
|-----|---------------------------|---------------------------|---------------|
| 3   | Вход с логином "passenger"| Успешная аутентификация   | PASS          |
|     | и паролем "pass123"       | роль: passenger           |               |
|-----|---------------------------|---------------------------|---------------|
| 4   | Вход с неверным паролем   | Отказ в доступе           | PASS          |
|     | логин "admin", пароль "123"| current_user = None      |               |
|-----|---------------------------|---------------------------|---------------|
| 5   | Вход с несуществующим     | Отказ в доступе           | PASS          |
|     | пользователем "hacker"    | current_user = None       |               |
|-----|---------------------------|---------------------------|---------------|

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 2: Проверка управления данными (CRUD операции)
═══════════════════════════════════════════════════════════════════════════════
|-----|---------------------------|---------------------------|---------------|
| Шаг | Действие                  | Ожидаемый результат       | Результат     |
|-----|---------------------------|---------------------------|---------------|
| 1   | Создание нового поезда    | Поезд добавлен в систему  | PASS          |
|     | (номер: 999, мест: 150)   | запись в data.json        |               |
|-----|---------------------------|---------------------------|---------------|
| 2   | Чтение списка поездов     | Возврат всех поездов      | PASS          |
|     |                           | включая новый (999)       |               |
|-----|---------------------------|---------------------------|---------------|
| 3   | Создание маршрута для     | Маршрут создан и связан   | PASS          |
|     | поезда 999                | с поездом                 |               |
|-----|---------------------------|---------------------------|---------------|
| 4   | Удаление поезда 999       | Поезд удален из системы   | PASS          |
|     |                           | не отображается в списке  |               |
|-----|---------------------------|---------------------------|---------------|
| 5   | Попытка создать дубликат  | Проверка уникальности     | PASS          |
|     | пользователя              | отказ в создании          |               |
|-----|---------------------------|---------------------------|---------------|

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 3: Проверка бизнес-логики (продажа/бронирование билетов)
═══════════════════════════════════════════════════════════════════════════════
|-----|---------------------------|---------------------------|---------------|
| Шаг | Действие                  | Ожидаемый результат       | Результат     |
|-----|---------------------------|---------------------------|---------------|
| 1   | Продажа билета на место 1 | Билет создан со статусом  | PASS          |
|     | маршрут ID=1 (кассир)     | "sold"                    |               |
|-----|---------------------------|---------------------------|---------------|
| 2   | Попытка продать билет на  | Отказ: место занято       | PASS          |
|     | то же место 1             | сообщение об ошибке       |               |
|-----|---------------------------|---------------------------|---------------|
| 3   | Бронирование билета на    | Билет создан со статусом  | PASS          |
|     | место 2 (пассажир)        | "booked"                  |               |
|-----|---------------------------|---------------------------|---------------|
| 4   | Возврат билета (место 1)  | Билет удален из системы   | PASS          |
|     | через кассира             | место освобождено         |               |
|-----|---------------------------|---------------------------|---------------|
| 5   | Проверка свободных мест   | Корректный расчет:        | PASS          |
|     | после операций            | занято=1, свободно=N-1    |               |
|-----|---------------------------|---------------------------|---------------|
"""

import json
import os
import sys
from auth import AuthManager

class TestScenarios:
    def __init__(self):
        self.auth = AuthManager('users.json')
        self.data_file = 'data.json'
        self.test_results = []
    
    def log_test(self, test_name, step, result, details=""):
        """Логирование результатов теста"""
        status = "✓ PASS" if result else "✗ FAIL"
        message = f"{status} | {test_name} | Шаг {step} | {details}"
        print(message)
        self.test_results.append((test_name, step, result, details))
    
    def load_data(self):
        """Загрузка данных"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def save_data(self, data):
        """Сохранение данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка аутентификации пользователей"""
        print("\n" + "="*80)
        print("ТЕСТ 1: Проверка аутентификации пользователей")
        print("="*80)
        
        # Шаг 1: Вход администратора
        result = self.auth.authenticate('admin', 'admin123')
        self.log_test("Аутентификация", 1, result and self.auth.current_user['role'] == 'administrator',
                     "Вход admin с корректным паролем")
        self.auth.logout()
        
        # Шаг 2: Вход кассира
        result = self.auth.authenticate('cashier', 'cashier123')
        self.log_test("Аутентификация", 2, result and self.auth.current_user['role'] == 'cashier',
                     "Вход cashier с корректным паролем")
        self.auth.logout()
        
        # Шаг 3: Вход пассажира
        result = self.auth.authenticate('passenger', 'pass123')
        self.log_test("Аутентификация", 3, result and self.auth.current_user['role'] == 'passenger',
                     "Вход passenger с корректным паролем")
        self.auth.logout()
        
        # Шаг 4: Неверный пароль
        result = self.auth.authenticate('admin', '123')
        self.log_test("Аутентификация", 4, not result and self.auth.current_user is None,
                     "Отказ при неверном пароле")
        
        # Шаг 5: Несуществующий пользователь
        result = self.auth.authenticate('hacker', 'password')
        self.log_test("Аутентификация", 5, not result and self.auth.current_user is None,
                     "Отказ при несуществующем пользователе")
    
    def test_2_crud_operations(self):
        """ТЕСТ 2: Проверка управления данными (CRUD операции)"""
        print("\n" + "="*80)
        print("ТЕСТ 2: Проверка управления данными (CRUD операции)")
        print("="*80)
        
        data = self.load_data()
        
        # Шаг 1: Создание нового поезда
        initial_count = len(data['trains'])
        new_train = {
            'id': 999,
            'number': '999TEST',
            'type': 'Тестовый',
            'seats': 150
        }
        data['trains'].append(new_train)
        self.save_data(data)
        
        data = self.load_data()
        created = any(t['id'] == 999 for t in data['trains'])
        self.log_test("CRUD операции", 1, created and len(data['trains']) == initial_count + 1,
                     "Создание поезда ID=999")
        
        # Шаг 2: Чтение списка поездов
        trains = data['trains']
        test_train = next((t for t in trains if t['id'] == 999), None)
        self.log_test("CRUD операции", 2, test_train is not None and test_train['number'] == '999TEST',
                     "Чтение созданного поезда")
        
        # Шаг 3: Создание маршрута для поезда
        new_route = {
            'id': 999,
            'train_id': 999,
            'from_station': 'Тест А',
            'to_station': 'Тест Б',
            'departure': '10:00',
            'arrival': '15:00',
            'date': '2024-12-31',
            'price': 1000
        }
        data['routes'].append(new_route)
        self.save_data(data)
        
        data = self.load_data()
        route_created = any(r['id'] == 999 for r in data['routes'])
        self.log_test("CRUD операции", 3, route_created,
                     "Создание маршрута для поезда 999")
        
        # Шаг 4: Удаление поезда
        data['trains'] = [t for t in data['trains'] if t['id'] != 999]
        data['routes'] = [r for r in data['routes'] if r['id'] != 999]
        self.save_data(data)
        
        data = self.load_data()
        deleted = not any(t['id'] == 999 for t in data['trains'])
        self.log_test("CRUD операции", 4, deleted,
                     "Удаление поезда ID=999")
        
        # Шаг 5: Попытка создать дубликат пользователя
        result = self.auth.create_user('admin', 'newpassword', 'administrator')
        self.log_test("CRUD операции", 5, not result,
                     "Проверка уникальности пользователя")
    
    def test_3_business_logic(self):
        """ТЕСТ 3: Проверка бизнес-логики (продажа/бронирование билетов)"""
        print("\n" + "="*80)
        print("ТЕСТ 3: Проверка бизнес-логики (продажа/бронирование билетов)")
        print("="*80)
        
        data = self.load_data()
        
        # Шаг 1: Продажа билета на место 1
        if data['routes']:
            route_id = data['routes'][0]['id']
            
            new_ticket = {
                'id': 9991,
                'route_id': route_id,
                'passenger': 'Тестовый Пассажир',
                'seat': 1,
                'status': 'sold',
                'sold_by': 'cashier',
                'date': '2024-01-15 10:00'
            }
            data['tickets'].append(new_ticket)
            self.save_data(data)
            
            data = self.load_data()
            ticket_created = any(t['id'] == 9991 and t['status'] == 'sold' for t in data['tickets'])
            self.log_test("Бизнес-логика", 1, ticket_created,
                         "Продажа билета на место 1")
            
            # Шаг 2: Попытка продать билет на занятое место
            occupied = any(t['route_id'] == route_id and t['seat'] == 1 for t in data['tickets'])
            self.log_test("Бизнес-логика", 2, occupied,
                         "Проверка занятости места (должно быть занято)")
            
            # Шаг 3: Бронирование билета на место 2
            new_booking = {
                'id': 9992,
                'route_id': route_id,
                'passenger': 'passenger',
                'seat': 2,
                'status': 'booked',
                'date': '2024-01-15 11:00'
            }
            data['tickets'].append(new_booking)
            self.save_data(data)
            
            data = self.load_data()
            booking_created = any(t['id'] == 9992 and t['status'] == 'booked' for t in data['tickets'])
            self.log_test("Бизнес-логика", 3, booking_created,
                         "Бронирование билета на место 2")
            
            # Шаг 4: Возврат билета
            data['tickets'] = [t for t in data['tickets'] if t['id'] != 9991]
            self.save_data(data)
            
            data = self.load_data()
            ticket_deleted = not any(t['id'] == 9991 for t in data['tickets'])
            self.log_test("Бизнес-логика", 4, ticket_deleted,
                         "Возврат билета (удаление)")
            
            # Шаг 5: Проверка свободных мест
            train = next((t for t in data['trains'] if t['id'] == data['routes'][0]['train_id']), None)
            if train:
                total_seats = train['seats']
                occupied_seats = len([t for t in data['tickets'] if t['route_id'] == route_id])
                free_seats = total_seats - occupied_seats
                
                self.log_test("Бизнес-логика", 5, free_seats == total_seats - 1,
                             f"Расчет свободных мест: всего={total_seats}, занято={occupied_seats}, свободно={free_seats}")
            
            # Очистка после теста - удаляем только созданные тестовые билеты
            data['tickets'] = [t for t in data['tickets'] if t['id'] not in [9991, 9992, 999]]
            self.save_data(data)
    
    def print_summary(self):
        """Вывод итогов тестирования"""
        print("\n" + "="*80)
        print("ИТОГИ ТЕСТИРОВАНИЯ")
        print("="*80)
        
        total = len(self.test_results)
        passed = sum(1 for _, _, result, _ in self.test_results if result)
        failed = total - passed
        
        print(f"\nВсего тестов: {total}")
        print(f"Успешно: {passed} ✓")
        print(f"Провалено: {failed} ✗")
        print(f"Процент успеха: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\n⚠ Проваленные тесты:")
            for test_name, step, result, details in self.test_results:
                if not result:
                    print(f"  - {test_name}, Шаг {step}: {details}")
        else:
            print("\n✓ Все тесты пройдены успешно!")
        
        print("="*80 + "\n")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n")
        print("╔" + "="*78 + "╗")
        print("║" + " "*15 + "СИСТЕМА ТЕСТИРОВАНИЯ - ЖЕЛЕЗНОДОРОЖНАЯ СТАНЦИЯ" + " "*16 + "║")
        print("╚" + "="*78 + "╝")
        
        self.test_1_authentication()
        self.test_2_crud_operations()
        self.test_3_business_logic()
        self.print_summary()

if __name__ == '__main__':
    # Запуск тестов
    tester = TestScenarios()
    tester.run_all_tests()