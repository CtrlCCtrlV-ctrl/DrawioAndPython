import unittest
import json
import os
import sys
import auth

"""
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                           ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ФОТОСТУДИИ                                 ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝

ТЕСТ 1: Проверка авторизации пользователей
┌─────┬──────────────────────────────────┬───────────────────────────────┬──────────────┐
│ Шаг │ Действие                          │ Ожидаемый результат          │ Результат    │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 1   │ Вход с логином "admin" и         │ Успешная авторизация,        │ PASS         │
│     │ паролем "admin123"               │ роль "administrator"          │              │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 2   │ Вход с логином "photographer" и  │ Успешная авторизация,        │ PASS         │
│     │ паролем "photo123"               │ роль "photographer"           │              │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 3   │ Вход с неверным паролем          │ Ошибка авторизации,          │ PASS         │
│     │                                  │ возврат None                  │              │
└─────┴──────────────────────────────────┴───────────────────────────────┴──────────────┘

ТЕСТ 2: Управление пользователями (администратор)
┌─────┬──────────────────────────────────┬───────────────────────────────┬──────────────┐
│ Шаг │ Действие                          │ Ожидаемый результат          │ Результат    │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 1   │ Создание нового пользователя     │ Пользователь успешно         │ PASS         │
│     │ с логином "test_user"            │ добавлен в систему            │              │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 2   │ Попытка создать пользователя     │ Возврат False, дубликат      │ PASS         │
│     │ с существующим логином           │ не создан                     │              │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 3   │ Удаление пользователя            │ Пользователь удален из       │ PASS         │
│     │ "test_user"                      │ системы                       │              │
└─────┴──────────────────────────────────┴───────────────────────────────┴──────────────┘

ТЕСТ 3: Работа с фотосессиями (CRUD операции)
┌─────┬──────────────────────────────────┬───────────────────────────────┬──────────────┐
│ Шаг │ Действие                          │ Ожидаемый результат          │ Результат    │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 1   │ Чтение данных из data.json       │ Данные успешно загружены,    │ PASS         │
│     │                                  │ структура валидна             │              │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 2   │ Добавление новой фотосессии      │ Сессия добавлена с           │ PASS         │
│     │                                  │ уникальным ID                 │              │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 3   │ Изменение статуса фотосессии     │ Статус успешно изменен       │ PASS         │
│     │ на "Завершена"                   │                              │              │
├─────┼──────────────────────────────────┼───────────────────────────────┼──────────────┤
│ 4   │ Удаление фотосессии              │ Сессия удалена из базы       │ PASS         │
└─────┴──────────────────────────────────┴───────────────────────────────┴──────────────┘
"""

class TestPhotoStudio(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Подготовка тестового окружения"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Очистка после тестов"""
        pass
    
    def test_01_authentication_admin(self):
        """ТЕСТ 1.1: Авторизация администратора"""
        print("\n" + "="*80)
        print("ТЕСТ 1.1: Проверка авторизации администратора")
        print("="*80)

        user = auth.authenticate('admin', 'admin123')

        self.assertIsNotNone(user, "Авторизация не должна возвращать None")
        self.assertEqual(user['username'], 'admin', "Логин должен быть 'admin'")

        print("✓ Администратор успешно авторизован")
        print(f"  Логин: {user['username']}")

    def test_02_authentication_photographer(self):
        """ТЕСТ 1.2: Авторизация фотографа"""
        print("\n" + "="*80)
        print("ТЕСТ 1.2: Проверка авторизации фотографа")
        print("="*80)

        user = auth.authenticate('photographer', 'photo123')

        self.assertIsNotNone(user, "Авторизация не должна возвращать None")
        self.assertEqual(user['role'], 'photographer', "Роль должна быть 'photographer'")

        print("✓ Фотограф успешно авторизован")

    def test_03_authentication_failure(self):
        """ТЕСТ 1.3: Отказ в авторизации с неверным паролем"""
        print("\n" + "="*80)
        print("ТЕСТ 1.3: Проверка отказа в авторизации")
        print("="*80)

        user = auth.authenticate('admin', 'wrong_password')

        self.assertIsNone(user, "Неверный пароль должен вернуть None")

        print("✓ Авторизация корректно отклонена для неверного пароля")
    
    def test_04_create_user(self):
        """ТЕСТ 2.1: Создание нового пользователя"""
        print("\n" + "="*80)
        print("ТЕСТ 2.1: Создание нового пользователя")
        print("="*80)

        result = auth.create_user('test_user', 'password123', 'client', 'Тестовый Пользователь')

        self.assertTrue(result, "Пользователь должен быть успешно создан")

        print("✓ Пользователь успешно создан")

    def test_05_duplicate_user(self):
        """ТЕСТ 2.2: Попытка создания дубликата пользователя"""
        print("\n" + "="*80)
        print("ТЕСТ 2.2: Попытка создания дубликата пользователя")
        print("="*80)

        result = auth.create_user('admin', 'password', 'client', 'Дубликат')

        self.assertFalse(result, "Создание дубликата должно вернуть False")

        print("✓ Система корректно предотвратила создание дубликата")

    def test_06_delete_user(self):
        """ТЕСТ 2.3: Удаление пользователя"""
        print("\n" + "="*80)
        print("ТЕСТ 2.3: Удаление пользователя")
        print("="*80)

        auth.delete_user('test_user')

        user = auth.authenticate('test_user', 'password123')
        self.assertIsNone(user, "Удаленный пользователь не должен авторизоваться")

        print("✓ Пользователь успешно удален из системы")
    
    def test_07_load_data(self):
        """ТЕСТ 3.1: Загрузка данных из JSON"""
        print("\n" + "="*80)
        print("ТЕСТ 3.1: Проверка загрузки данных")
        print("="*80)

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn('studios', data, "Данные должны содержать ключ 'studios'")
        self.assertIn('sessions', data, "Данные должны содержать ключ 'sessions'")

        print("✓ Данные успешно загружены")
        print(f"  Студий: {len(data['studios'])}")
        print(f"  Сессий: {len(data['sessions'])}")

    def test_08_add_session(self):
        """ТЕСТ 3.2: Добавление новой фотосессии"""
        print("\n" + "="*80)
        print("ТЕСТ 3.2: Добавление новой фотосессии")
        print("="*80)

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        new_session = {
            'id': 2,
            'client': 'client',
            'photographer': 'photographer',
            'studio_id': 1,
            'date': '2024-03-01',
            'time': '15:00',
            'duration': 2,
            'status': 'Запланирована',
            'paid': False
        }

        data['sessions'].append(new_session)

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data['sessions']), 2, "Должно быть две сессии")

        print("✓ Фотосессия успешно добавлена")

    def test_09_update_session_status(self):
        """ТЕСТ 3.3: Изменение статуса фотосессии"""
        print("\n" + "="*80)
        print("ТЕСТ 3.3: Изменение статуса фотосессии")
        print("="*80)

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        data['sessions'][0]['status'] = 'Завершена'

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data['sessions'][0]['status'], 'Завершена', "Статус должен быть 'Завершена'")

        print("✓ Статус фотосессии успешно изменен")

    def test_10_delete_session(self):
        """ТЕСТ 3.4: Удаление фотосессии"""
        print("\n" + "="*80)
        print("ТЕСТ 3.4: Удаление фотосессии")
        print("="*80)

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        data['sessions'] = [s for s in data['sessions'] if s['id'] != 2]

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data['sessions']), 1, "Должна остаться одна сессия")

        print("✓ Фотосессия успешно удалена из базы")

def run_tests():
    """Запуск тестов с подробным выводом"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "ТЕСТИРОВАНИЕ СИСТЕМЫ ФОТОСТУДИЯ" + " "*27 + "║")
    print("╚" + "="*78 + "╝")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPhotoStudio)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*80)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*80)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Ошибок: {len(result.failures)}")
    print(f"Критических ошибок: {len(result.errors)}")
    print("="*80)
    
    if result.wasSuccessful():
        print("\n✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("\n✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
    
    return result

if __name__ == '__main__':
    run_tests()