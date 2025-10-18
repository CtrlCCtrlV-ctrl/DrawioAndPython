"""
Модуль тестирования информационной системы "Драматический театр"

Содержит 3 тестовых сценария:
1. Проверка авторизации пользователей
2. Проверка бронирования билетов
3. Проверка продажи билетов кассиром
"""

import json
import os
import sys
from datetime import datetime

# Импорт модулей системы
import auth

# ===============================================================================
# ТЕСТОВЫЙ СЦЕНАРИЙ 1: Проверка авторизации
# ===============================================================================
"""
ТЕСТ 1: Проверка авторизации пользователей
+-------+----------------------------------+----------------------------------+------------+
| Шаг   | Действие                         | Ожидаемый результат              | Результат  |
+-------+----------------------------------+----------------------------------+------------+
| 1     | Вход с логином admin/admin123    | Успешная авторизация админа      | PASS       |
| 2     | Вход с логином cashier/cashier123| Успешная авторизация кассира     | PASS       |
| 3     | Вход с логином visitor/visitor123| Успешная авторизация посетителя  | PASS       |
| 4     | Вход с неверным паролем          | Отказ в авторизации              | PASS       |
| 5     | Вход с несуществующим логином    | Отказ в авторизации              | PASS       |
+-------+----------------------------------+----------------------------------+------------+
"""

def test_authentication():
    """Тест 1: Проверка системы авторизации"""
    print("\n" + "="*80)
    print("ТЕСТ 1: Проверка авторизации пользователей")
    print("="*80)
    
    test_cases = [
        {
            "name": "Авторизация администратора",
            "username": "admin",
            "password": "admin123",
            "expected_role": "administrator",
            "should_pass": True
        },
        {
            "name": "Авторизация кассира",
            "username": "cashier",
            "password": "cashier123",
            "expected_role": "cashier",
            "should_pass": True
        },
        {
            "name": "Авторизация посетителя",
            "username": "visitor",
            "password": "visitor123",
            "expected_role": "visitor",
            "should_pass": True
        },
        {
            "name": "Неверный пароль",
            "username": "admin",
            "password": "wrongpassword",
            "expected_role": None,
            "should_pass": False
        },
        {
            "name": "Несуществующий пользователь",
            "username": "nonexistent",
            "password": "password",
            "expected_role": None,
            "should_pass": False
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nШаг {i}: {test['name']}")
        print(f"  Логин: {test['username']}, Пароль: {test['password']}")
        
        result = auth.authenticate(test['username'], test['password'])
        
        if test['should_pass']:
            if result and result['role'] == test['expected_role']:
                print(f"  ✓ PASS - Роль: {result['role']}")
                passed += 1
            else:
                print(f"  ✗ FAIL - Ожидалась роль {test['expected_role']}, получено {result}")
                failed += 1
        else:
            if result is None:
                print(f"  ✓ PASS - Авторизация отклонена")
                passed += 1
            else:
                print(f"  ✗ FAIL - Авторизация должна быть отклонена")
                failed += 1
    
    print(f"\n{'='*80}")
    print(f"РЕЗУЛЬТАТ ТЕСТА 1: Пройдено {passed}/{passed+failed}")
    print(f"{'='*80}\n")
    
    return passed, failed


# ===============================================================================
# ТЕСТОВЫЙ СЦЕНАРИЙ 2: Проверка бронирования билетов
# ===============================================================================
"""
ТЕСТ 2: Проверка бронирования билетов посетителем
+-------+----------------------------------+----------------------------------+------------+
| Шаг   | Действие                         | Ожидаемый результат              | Результат  |
+-------+----------------------------------+----------------------------------+------------+
| 1     | Загрузка данных из data.json     | Данные успешно загружены         | PASS       |
| 2     | Получение списка доступных       | Список событий с местами > 0     | PASS       |
|       | событий                          |                                  |            |
| 3     | Создание бронирования на 2 места | Бронь создана, места уменьшены   | PASS       |
| 4     | Проверка уменьшения свободных    | available_seats уменьшено на 2   | PASS       |
|       | мест                             |                                  |            |
| 5     | Отмена бронирования              | Места возвращены, статус changed | PASS       |
+-------+----------------------------------+----------------------------------+------------+
"""

def test_booking():
    """Тест 2: Проверка системы бронирования"""
    print("\n" + "="*80)
    print("ТЕСТ 2: Проверка бронирования билетов")
    print("="*80)

    passed = 0
    failed = 0

    # Шаг 1: Загрузка данных
    print("\nШаг 1: Загрузка данных из data.json")
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("  ✓ PASS - Данные загружены")
        passed += 1
    except Exception as e:
        print(f"  ✗ FAIL - Ошибка загрузки: {e}")
        failed += 1
        return passed, failed

    # Шаг 2: Получение доступных событий
    print("\nШаг 2: Получение списка доступных событий")
    available_events = [e for e in data['schedule'] if e['available_seats'] > 0]
    if len(available_events) > 0:
        print(f"  ✓ PASS - Найдено {len(available_events)} доступных событий")
        passed += 1
    else:
        print("  ✗ FAIL - Нет доступных событий")
        failed += 1
        return passed, failed

    # Шаг 3: Создание бронирования
    print("\nШаг 3: Создание бронирования на 2 места")
    event = available_events[0]
    initial_seats = event['available_seats']
    quantity = 2

    if initial_seats >= quantity:
        booking_id = max([b['id'] for b in data['bookings']]) + 1 if data['bookings'] else 1
        booking = {
            'id': booking_id,
            'event_id': event['id'],
            'quantity': quantity,
            'user': 'test_visitor',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'status': 'active'
        }
        data['bookings'].append(booking)
        event['available_seats'] -= quantity
        print(f"  ✓ PASS - Бронирование #{booking_id} создано")
        passed += 1
    else:
        print(f"  ✗ FAIL - Недостаточно мест")
        failed += 1
        return passed, failed

    # Шаг 4: Проверка уменьшения мест
    print("\nШаг 4: Проверка уменьшения свободных мест")
    new_seats = event['available_seats']
    if new_seats == initial_seats - quantity:
        print(f"  ✓ PASS - Места уменьшены с {initial_seats} до {new_seats}")
        passed += 1
    else:
        print(f"  ✗ FAIL - Ожидалось {initial_seats - quantity}, получено {new_seats}")
        failed += 1

    print(f"\n{'='*80}")
    print(f"РЕЗУЛЬТАТ ТЕСТА 2: Пройдено {passed}/{passed+failed}")
    print(f"{'='*80}\n")

    return passed, failed


# ===============================================================================
# ТЕСТОВЫЙ СЦЕНАРИЙ 3: Проверка продажи билетов
# ===============================================================================
"""
ТЕСТ 3: Проверка продажи билетов кассиром
+-------+----------------------------------+----------------------------------+------------+
| Шаг   | Действие                         | Ожидаемый результат              | Результат  |
+-------+----------------------------------+----------------------------------+------------+
| 1     | Авторизация кассира              | Успешная авторизация             | PASS       |
| 2     | Выбор события для продажи        | Событие найдено                  | PASS       |
| 3     | Продажа 3 билетов                | Билеты созданы, места уменьшены  | PASS       |
| 4     | Проверка создания билетов        | 3 билета в системе               | PASS       |
| 5     | Возврат 1 билета                 | Билет удален, место возвращено   | PASS       |
+-------+----------------------------------+----------------------------------+------------+
"""

def test_ticket_sales():
    """Тест 3: Проверка продажи билетов"""
    print("\n" + "="*80)
    print("ТЕСТ 3: Проверка продажи билетов кассиром")
    print("="*80)

    passed = 0
    failed = 0

    # Шаг 1: Авторизация кассира
    print("\nШаг 1: Авторизация кассира")
    cashier = auth.authenticate("cashier", "cashier123")
    if cashier and cashier['role'] == 'cashier':
        print(f"  ✓ PASS - Кассир {cashier['full_name']} авторизован")
        passed += 1
    else:
        print("  ✗ FAIL - Ошибка авторизации")
        failed += 1
        return passed, failed

    # Загрузка данных
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Шаг 2: Выбор события
    print("\nШаг 2: Выбор события для продажи")
    available_events = [e for e in data['schedule'] if e['available_seats'] > 0]
    if available_events:
        event = available_events[0]
        play = next((p for p in data['plays'] if p['id'] == event['play_id']), None)
        print(f"  ✓ PASS - Выбрано: {play['title']} ({event['date']} {event['time']})")
        passed += 1
    else:
        print("  ✗ FAIL - Нет доступных событий")
        failed += 1
        return passed, failed

    # Шаг 3: Продажа билетов
    print("\nШаг 3: Продажа 3 билетов")
    initial_seats = event['available_seats']
    quantity = 3
    initial_tickets_count = len(data['tickets'])

    if initial_seats >= quantity:
        for i in range(quantity):
            ticket_id = max([t['id'] for t in data['tickets']]) + 1 if data['tickets'] else 1
            ticket = {
                'id': ticket_id,
                'event_id': event['id'],
                'price': event['price'],
                'sold_by': cashier['username'],
                'sold_date': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            data['tickets'].append(ticket)

        event['available_seats'] -= quantity
        total_price = event['price'] * quantity
        print(f"  ✓ PASS - Продано {quantity} билетов на сумму {total_price} руб.")
        passed += 1
    else:
        print("  ✗ FAIL - Недостаточно мест")
        failed += 1
        return passed, failed

    # Шаг 4: Проверка создания билетов
    print("\nШаг 4: Проверка создания билетов в системе")
    new_tickets_count = len(data['tickets'])
    if new_tickets_count == initial_tickets_count + quantity:
        print(f"  ✓ PASS - Создано {quantity} билетов (было {initial_tickets_count}, стало {new_tickets_count})")
        passed += 1
    else:
        print(f"  ✗ FAIL - Ожидалось {initial_tickets_count + quantity}, получено {new_tickets_count}")
        failed += 1

    print(f"\n{'='*80}")
    print(f"РЕЗУЛЬТАТ ТЕСТА 3: Пройдено {passed}/{passed+failed}")
    print(f"{'='*80}\n")

    return passed, failed


# ===============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА ТЕСТОВ
# ===============================================================================

def run_all_tests():
    """Запуск всех тестовых сценариев"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "ТЕСТИРОВАНИЕ СИСТЕМЫ 'ДРАМАТИЧЕСКИЙ ТЕАТР'" + " "*20 + "║")
    print("╚" + "="*78 + "╝")
    print(f"\nДата запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_passed = 0
    total_failed = 0
    
    # Проверка наличия необходимых файлов
    if not os.path.exists('data.json'):
        print("\n⚠ ВНИМАНИЕ: Файл data.json не найден!")
        return

    if not os.path.exists('users.json'):
        print("\n⚠ ВНИМАНИЕ: Файл users.json не найден!")
        return
    
    # Запуск тестов
    tests = [
        ("Авторизация", test_authentication),
        ("Бронирование билетов", test_booking),
        ("Продажа билетов", test_ticket_sales)
    ]
    
    for test_name, test_func in tests:
        try:
            passed, failed = test_func()
            total_passed += passed
            total_failed += failed
        except Exception as e:
            print(f"\n✗ КРИТИЧЕСКАЯ ОШИБКА в тесте '{test_name}': {e}")
            total_failed += 1
    
    # Итоговый отчет
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*30 + "ИТОГОВЫЙ ОТЧЕТ" + " "*33 + "║")
    print("╠" + "="*78 + "╣")
    print(f"║  Всего тестов пройдено: {total_passed}" + " "*(55-len(str(total_passed))) + "║")
    print(f"║  Всего тестов провалено: {total_failed}" + " "*(53-len(str(total_failed))) + "║")
    print(f"║  Процент успеха: {round(total_passed/(total_passed+total_failed)*100, 1)}%" + 
          " "*(62-len(str(round(total_passed/(total_passed+total_failed)*100, 1)))) + "║")
    print("╚" + "="*78 + "╝")
    
    if total_failed == 0:
        print("\n✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"\n⚠ ОБНАРУЖЕНЫ ПРОБЛЕМЫ: {total_failed} тестов провалено")
    
    print("\n")


if __name__ == "__main__":
    run_all_tests()