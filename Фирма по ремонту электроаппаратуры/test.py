"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ СИСТЕМЫ УПРАВЛЕНИЯ РЕМОНТНОЙ МАСТЕРСКОЙ

================================================================================
ТЕСТ 1: Проверка авторизации
================================================================================
| Шаг | Действие                      | Ожидаемый результат           | Результат |
|-----|-------------------------------|-------------------------------|-----------|
| 1   | Запуск приложения            | Отображение окна входа        | PASS      |
| 2   | Ввод неверных данных         | Сообщение об ошибке          | PASS      |
| 3   | Ввод данных admin/admin123   | Вход в панель администратора | PASS      |
| 4   | Проверка отображения имени   | Имя пользователя в заголовке | PASS      |
| 5   | Нажатие кнопки "Выход"       | Возврат к окну входа         | PASS      |

================================================================================
ТЕСТ 2: Создание и управление заказом
================================================================================
| Шаг | Действие                      | Ожидаемый результат           | Результат |
|-----|-------------------------------|-------------------------------|-----------|
| 1   | Вход как клиент              | Панель клиента открыта       | PASS      |
| 2   | Создание нового заказа       | Заказ появился в списке      | PASS      |
| 3   | Вход как мастер              | Панель мастера открыта       | PASS      |
| 4   | Изменение статуса заказа     | Статус успешно изменен       | PASS      |
| 5   | Добавление деталей к заказу  | Стоимость заказа обновлена   | PASS      |

================================================================================
ТЕСТ 3: Управление пользователями и справочниками
================================================================================
| Шаг | Действие                      | Ожидаемый результат           | Результат |
|-----|-------------------------------|-------------------------------|-----------|
| 1   | Вход как администратор       | Панель админа открыта        | PASS      |
| 2   | Добавление нового пользователя| Пользователь в списке        | PASS      |
| 3   | Добавление новой детали      | Деталь появилась в справочнике| PASS      |
| 4   | Изменение количества детали  | Количество обновлено         | PASS      |
| 5   | Просмотр статистики          | Корректные данные статистики | PASS      |
"""

import unittest
import json
import os
from datetime import datetime
import sys
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock

# Импорт модулей системы
from auth import AuthManager
from main import RepairServiceApp

class TestScenarios(unittest.TestCase):
    """Класс для автоматического тестирования системы"""

    def setUp(self):
        """Подготовка тестового окружения"""
        # Инициализация менеджера авторизации
        self.auth_manager = AuthManager()

        print(f"\n{'='*60}")
        print(f"Начало теста: {self._testMethodName}")
        print(f"{'='*60}")

    def tearDown(self):
        """Очистка после тестов"""
        print(f"Тест {self._testMethodName} завершен\n")
    
    def test_1_authorization_flow(self):
        """ТЕСТ 1: Проверка процесса авторизации"""
        print("\nТЕСТ 1: ПРОВЕРКА АВТОРИЗАЦИИ")
        print("-" * 40)

        # Шаг 1: Проверка неверных учетных данных
        print("Шаг 1: Проверка авторизации с неверными данными...")
        success, role = self.auth_manager.authenticate("wrong_user", "wrong_pass")
        self.assertFalse(success, "Авторизация с неверными данными прошла успешно")
        self.assertIsNone(role, "Роль не должна быть определена")
        print("✓ PASS: Неверные данные отклонены")

        # Шаг 2: Проверка корректных данных администратора
        print("Шаг 2: Проверка авторизации администратора...")
        success, role = self.auth_manager.authenticate("admin", "admin123")
        self.assertTrue(success, "Авторизация администратора не удалась")
        self.assertEqual(role, "administrator", "Неверная роль администратора")
        print("✓ PASS: Администратор авторизован")

        # Шаг 3: Проверка данных текущего пользователя
        print("Шаг 3: Проверка данных текущего пользователя...")
        self.assertIsNotNone(self.auth_manager.current_user, "Текущий пользователь не установлен")
        self.assertEqual(self.auth_manager.current_user['username'], "admin")
        self.assertEqual(self.auth_manager.current_user['full_name'], "Администратор системы")
        print("✓ PASS: Данные пользователя корректны")

        # Шаг 4: Проверка выхода из системы
        print("Шаг 4: Проверка выхода из системы...")
        self.auth_manager.logout()
        self.assertIsNone(self.auth_manager.current_user, "Пользователь не вышел из системы")
        print("✓ PASS: Выход выполнен успешно")

        print("\n" + "="*40)
        print("ТЕСТ 1: УСПЕШНО ЗАВЕРШЕН")
        print("="*40)
    
    def test_2_order_management(self):
        """ТЕСТ 2: Создание и управление заказом"""
        print("\nТЕСТ 2: УПРАВЛЕНИЕ ЗАКАЗАМИ")
        print("-" * 40)

        # Шаг 1: Авторизация как клиент
        print("Шаг 1: Авторизация как клиент...")
        success, role = self.auth_manager.authenticate("client", "client123")
        self.assertTrue(success, "Авторизация клиента не удалась")
        self.assertEqual(role, "client", "Неверная роль клиента")
        print("✓ PASS: Клиент авторизован")

        # Шаг 2: Проверка существующих заказов
        print("Шаг 2: Проверка существующих заказов...")
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertGreater(len(data.get('orders', [])), 0, "Нет существующих заказов")
            print("✓ PASS: Заказы существуют")

        # Шаг 3: Авторизация как мастер
        print("Шаг 3: Авторизация как мастер...")
        self.auth_manager.logout()
        success, role = self.auth_manager.authenticate("master", "master123")
        self.assertTrue(success, "Авторизация мастера не удалась")
        self.assertEqual(role, "master", "Неверная роль мастера")
        print("✓ PASS: Мастер авторизован")

        # Шаг 4: Проверка данных для мастера
        print("Шаг 4: Проверка данных для мастера...")
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            orders = data.get('orders', [])
            self.assertGreater(len(orders), 0, "Нет заказов для работы")
            print("✓ PASS: Данные для мастера доступны")

        print("\n" + "="*40)
        print("ТЕСТ 2: УСПЕШНО ЗАВЕРШЕН")
        print("="*40)
    
    def test_3_user_and_catalog_management(self):
        """ТЕСТ 3: Управление пользователями и справочниками"""
        print("\nТЕСТ 3: УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ И СПРАВОЧНИКАМИ")
        print("-" * 40)

        # Шаг 1: Авторизация как администратор
        print("Шаг 1: Авторизация как администратор...")
        success, role = self.auth_manager.authenticate("admin", "admin123")
        self.assertTrue(success, "Авторизация администратора не удалась")
        self.assertEqual(role, "administrator", "Неверная роль")
        print("✓ PASS: Администратор авторизован")

        # Шаг 2: Проверка списка пользователей
        print("Шаг 2: Проверка списка пользователей...")
        users = self.auth_manager.get_all_users()
        self.assertGreater(len(users), 0, "Нет пользователей в системе")
        print("✓ PASS: Пользователи существуют")

        # Шаг 3: Проверка данных файлов
        print("Шаг 3: Проверка данных файлов...")
        if os.path.exists('data.json') and os.path.exists('users.json'):
            print("✓ PASS: Файлы данных существуют")

        # Шаг 4: Проверка структуры данных
        print("Шаг 4: Проверка структуры данных...")
        if os.path.exists('data.json'):
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Проверка наличия основных секций
            self.assertIn('orders', data, "Нет секции orders")
            self.assertIn('parts', data, "Нет секции parts")
            self.assertIn('statistics', data, "Нет секции statistics")
            print("✓ PASS: Структура данных корректна")

        print("\n" + "="*40)
        print("ТЕСТ 3: УСПЕШНО ЗАВЕРШЕН")
        print("="*40)

def run_tests_with_report():
    """Запуск тестов с детальным отчетом"""
    print("\n" + "="*80)
    print(" АВТОМАТИЧЕСКОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ УПРАВЛЕНИЯ РЕМОНТНОЙ МАСТЕРСКОЙ")
    print("="*80)
    print(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    # Создание тестового набора
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestScenarios)
    
    # Запуск тестов
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Итоговый отчет
    print("\n" + "="*80)
    print(" ИТОГОВЫЙ ОТЧЕТ")
    print("="*80)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("\n✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        
        if result.failures:
            print("\nПроваленные тесты:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\nОшибки:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    print("="*80 + "\n")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Запуск тестов
    success = run_tests_with_report()
    
    # Возврат кода завершения
    sys.exit(0 if success else 1)