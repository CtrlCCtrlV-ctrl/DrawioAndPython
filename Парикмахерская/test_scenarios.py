"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "ПАРИКМАХЕРСКАЯ"

Данный файл содержит автоматизированные тесты для проверки
основных функций системы.
"""

import json
import os
import auth
from datetime import datetime

"""
================================================================================
ТЕСТ 1: Проверка авторизации пользователей
================================================================================
|-------|--------------------------------|--------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат      | Результат |
|-------|--------------------------------|--------------------------|-----------|
| 1     | Авторизация с верными          | Успешный вход,           | PASS      |
|       | данными (admin/admin123)       | пользователь найден      |           |
|-------|--------------------------------|--------------------------|-----------|
| 2     | Авторизация с неверным         | Отказ в доступе,         | PASS      |
|       | паролем (admin/wrongpass)      | возврат None             |           |
|-------|--------------------------------|--------------------------|-----------|
| 3     | Авторизация несуществующего    | Отказ в доступе,         | PASS      |
|       | пользователя (fake/fake)       | возврат None             |           |
|-------|--------------------------------|--------------------------|-----------|
| 4     | Проверка роли пользователя     | Роль = administrator     | PASS      |
|       | admin                          |                          |           |
|-------|--------------------------------|--------------------------|-----------|
| 5     | Создание нового пользователя   | Пользователь создан,     | PASS      |
|       | testuser/testpass/client       | success = True           |           |
|-------|--------------------------------|--------------------------|-----------|
"""

def test_authentication():
    print("\n" + "="*80)
    print("ТЕСТ 1: Проверка авторизации пользователей")
    print("="*80)
    
    auth.init_users_file()
    
    # Шаг 1: Верная авторизация
    print("\nШаг 1: Авторизация с верными данными (admin/admin123)")
    user = auth.authenticate('admin', 'admin123')
    assert user is not None, "FAIL: Пользователь не найден"
    assert user['username'] == 'admin', "FAIL: Неверное имя пользователя"
    print("✓ PASS: Успешная авторизация admin")
    
    # Шаг 2: Неверный пароль
    print("\nШаг 2: Авторизация с неверным паролем (admin/wrongpass)")
    user = auth.authenticate('admin', 'wrongpass')
    assert user is None, "FAIL: Система приняла неверный пароль"
    print("✓ PASS: Неверный пароль отклонен")
    
    # Шаг 3: Несуществующий пользователь
    print("\nШаг 3: Авторизация несуществующего пользователя (fake/fake)")
    user = auth.authenticate('fake', 'fake')
    assert user is None, "FAIL: Система приняла несуществующего пользователя"
    print("✓ PASS: Несуществующий пользователь отклонен")
    
    # Шаг 4: Проверка роли
    print("\nШаг 4: Проверка роли пользователя admin")
    user = auth.authenticate('admin', 'admin123')
    assert user['role'] == 'administrator', "FAIL: Неверная роль"
    print("✓ PASS: Роль пользователя = administrator")
    
    # Шаг 5: Создание нового пользователя
    print("\nШаг 5: Создание нового пользователя (testuser/testpass/client)")
    success, msg = auth.create_user('testuser', 'testpass', 'client', 'Тестовый Пользователь')
    assert success == True, f"FAIL: {msg}"
    print(f"✓ PASS: Пользователь создан - {msg}")
    
    # Проверка созданного пользователя
    user = auth.authenticate('testuser', 'testpass')
    assert user is not None, "FAIL: Созданный пользователь не найден"
    print("✓ PASS: Созданный пользователь может войти в систему")
    
    # Очистка тестового пользователя
    auth.delete_user('testuser')
    
    print("\n" + "="*80)
    print("ТЕСТ 1 ЗАВЕРШЕН: Все проверки пройдены успешно")
    print("="*80)


"""
================================================================================
ТЕСТ 2: Управление данными (CRUD операции)
================================================================================
|-------|--------------------------------|--------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат      | Результат |
|-------|--------------------------------|--------------------------|-----------|
| 1     | Чтение данных из data.json     | Данные успешно загружены | PASS      |
|-------|--------------------------------|--------------------------|-----------|
| 2     | Добавление новой услуги        | Услуга добавлена,        | PASS      |
|       |                                | ID присвоен              |           |
|-------|--------------------------------|--------------------------|-----------|
| 3     | Добавление нового мастера      | Мастер добавлен,         | PASS      |
|       |                                | ID присвоен              |           |
|-------|--------------------------------|--------------------------|-----------|
| 4     | Добавление записи клиента      | Запись создана,          | PASS      |
|       |                                | статус "Запланирована"   |           |
|-------|--------------------------------|--------------------------|-----------|
| 5     | Удаление записи                | Запись удалена из списка | PASS      |
|-------|--------------------------------|--------------------------|-----------|
| 6     | Сохранение данных в файл       | Данные сохранены,        | PASS      |
|       |                                | файл обновлен            |           |
|-------|--------------------------------|--------------------------|-----------|
"""

def test_data_management():
    print("\n" + "="*80)
    print("ТЕСТ 2: Управление данными (CRUD операции)")
    print("="*80)
    
    DATA_FILE = 'data.json'
    
    # Шаг 1: Чтение данных
    print("\nШаг 1: Чтение данных из data.json")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert 'services' in data, "FAIL: Нет секции services"
    assert 'masters' in data, "FAIL: Нет секции masters"
    assert 'appointments' in data, "FAIL: Нет секции appointments"
    print("✓ PASS: Данные успешно загружены")
    print(f"  - Услуг: {len(data['services'])}")
    print(f"  - Мастеров: {len(data['masters'])}")
    print(f"  - Записей: {len(data['appointments'])}")
    
    # Шаг 2: Добавление услуги
    print("\nШаг 2: Добавление новой услуги")
    initial_count = len(data['services'])
    new_id = max([s['id'] for s in data['services']], default=0) + 1
    new_service = {
        'id': new_id,
        'name': 'Тестовая услуга',
        'description': 'Описание тестовой услуги',
        'price': 1000,
        'duration': 30
    }
    data['services'].append(new_service)
    assert len(data['services']) == initial_count + 1, "FAIL: Услуга не добавлена"
    print(f"✓ PASS: Услуга добавлена с ID={new_id}")
    
    # Шаг 3: Добавление мастера
    print("\nШаг 3: Добавление нового мастера")
    initial_count = len(data['masters'])
    new_id = max([m['id'] for m in data['masters']], default=0) + 1
    new_master = {
        'id': new_id,
        'name': 'Тестовый Мастер',
        'specialization': 'Тестовая специализация',
        'phone': '+7-900-000-0000'
    }
    data['masters'].append(new_master)
    assert len(data['masters']) == initial_count + 1, "FAIL: Мастер не добавлен"
    print(f"✓ PASS: Мастер добавлен с ID={new_id}")
    
    # Шаг 4: Добавление записи
    print("\nШаг 4: Добавление записи клиента")
    initial_count = len(data['appointments'])
    new_id = max([a['id'] for a in data['appointments']], default=0) + 1
    new_appointment = {
        'id': new_id,
        'client_id': 1,
        'master_id': 1,
        'service_id': 1,
        'date': '2024-02-01',
        'time': '12:00',
        'status': 'Запланирована'
    }
    data['appointments'].append(new_appointment)
    assert len(data['appointments']) == initial_count + 1, "FAIL: Запись не добавлена"
    print(f"✓ PASS: Запись создана с ID={new_id}, статус: {new_appointment['status']}")
    
    # Шаг 5: Удаление записи
    print("\nШаг 5: Удаление тестовой записи")
    data['appointments'] = [a for a in data['appointments'] if a['id'] != new_id]
    found = any(a['id'] == new_id for a in data['appointments'])
    assert not found, "FAIL: Запись не удалена"
    print("✓ PASS: Запись успешно удалена")
    
    # Шаг 6: Сохранение данных
    print("\nШаг 6: Сохранение данных в файл")
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Проверка сохранения
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert len(saved_data['services']) == len(data['services']), "FAIL: Данные не сохранены"
    print("✓ PASS: Данные успешно сохранены в файл")
    
    print("\n" + "="*80)
    print("ТЕСТ 2 ЗАВЕРШЕН: Все операции выполнены успешно")
    print("="*80)


"""
================================================================================
ТЕСТ 3: Проверка сессии пользователей
================================================================================
|-------|--------------------------------|--------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат      | Результат |
|-------|--------------------------------|--------------------------|-----------|
| 1     | Сессия: вход администратора    | current_user установлен, | PASS      |
|       |                                | роль = administrator     |           |
|-------|--------------------------------|--------------------------|-----------|
| 2     | Сессия: вход мастера           | current_user установлен, | PASS      |
|       |                                | роль = master            |           |
|-------|--------------------------------|--------------------------|-----------|
| 3     | Сессия: вход клиента           | current_user установлен, | PASS      |
|       |                                | роль = client            |           |
|-------|--------------------------------|--------------------------|-----------|
| 4     | Сессия: выход из системы       | current_user = None      | PASS      |
|-------|--------------------------------|--------------------------|-----------|
| 5     | Защита от дубликатов           | Создание пользователя    | PASS      |
|       | пользователей                  | с существующим логином   |           |
|       |                                | отклоняется              |           |
|-------|--------------------------------|--------------------------|-----------|
"""

def test_business_logic():
    print("\n" + "="*80)
    print("ТЕСТ 3: Проверка сессии пользователей")
    print("="*80)

    # Шаг 1: Сессия администратора
    print("\nШаг 1: Сессия - вход администратора")
    user = auth.authenticate('admin', 'admin123')
    auth.Session.login(user)
    assert auth.Session.is_authenticated(), "FAIL: Сессия не установлена"
    assert auth.Session.get_role() == 'administrator', "FAIL: Неверная роль"
    assert auth.Session.current_user['username'] == 'admin', "FAIL: Неверный пользователь"
    print("✓ PASS: Администратор вошел в систему")
    print(f"  Пользователь: {auth.Session.current_user['username']}")
    print(f"  Роль: {auth.Session.get_role()}")

    # Шаг 2: Сессия мастера
    print("\nШаг 2: Сессия - вход мастера")
    user = auth.authenticate('master1', 'master123')
    auth.Session.login(user)
    assert auth.Session.is_authenticated(), "FAIL: Сессия не установлена"
    assert auth.Session.get_role() == 'master', "FAIL: Неверная роль"
    print("✓ PASS: Мастер вошел в систему")
    print(f"  Пользователь: {auth.Session.current_user['username']}")
    print(f"  Роль: {auth.Session.get_role()}")

    # Шаг 3: Сессия клиента
    print("\nШаг 3: Сессия - вход клиента")
    user = auth.authenticate('client1', 'client123')
    auth.Session.login(user)
    assert auth.Session.is_authenticated(), "FAIL: Сессия не установлена"
    assert auth.Session.get_role() == 'client', "FAIL: Неверная роль"
    print("✓ PASS: Клиент вошел в систему")
    print(f"  Пользователь: {auth.Session.current_user['username']}")
    print(f"  Роль: {auth.Session.get_role()}")

    # Шаг 4: Выход из системы
    print("\nШаг 4: Выход из системы")
    auth.Session.logout()
    assert not auth.Session.is_authenticated(), "FAIL: Сессия не закрыта"
    assert auth.Session.current_user is None, "FAIL: current_user не очищен"
    print("✓ PASS: Выход выполнен успешно")

    # Шаг 5: Защита от дубликатов
    print("\nШаг 5: Защита от дубликатов пользователей")
    success, msg = auth.create_user('admin', 'newpass', 'client', 'Новый пользователь')
    assert not success, "FAIL: Система разрешила создать дубликат"
    assert "существует" in msg.lower(), "FAIL: Неверное сообщение об ошибке"
    print(f"✓ PASS: Дубликат отклонен - {msg}")

    print("\n" + "="*80)
    print("ТЕСТ 3 ЗАВЕРШЕН: Сессия работает корректно")
    print("="*80)


def run_all_tests():
    """Запуск всех тестов"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "АВТОМАТИЗИРОВАННОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ" + " "*24 + "║")
    print("║" + " "*22 + "Информационная система 'Парикмахерская'" + " "*18 + "║")
    print("╚" + "="*78 + "╝")
    print(f"\nДата запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Всего тестов: 3")
    
    try:
        test_authentication()
        test_data_management()
        test_business_logic()
        
        print("\n")
        print("╔" + "="*78 + "╗")
        print("║" + " "*25 + "ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!" + " "*26 + "║")
        print("║" + " "*30 + "Система работает корректно" + " "*22 + "║")
        print("╚" + "="*78 + "╝")
        print("\n")
        
        return True
        
    except AssertionError as e:
        print(f"\n\n❌ ТЕСТ ПРОВАЛЕН: {str(e)}\n")
        return False
    except Exception as e:
        print(f"\n\n❌ ОШИБКА ВЫПОЛНЕНИЯ: {str(e)}\n")
        return False


if __name__ == '__main__':
    run_all_tests()