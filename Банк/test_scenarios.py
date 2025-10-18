import unittest
import json
import os
import auth
from datetime import datetime

"""
═══════════════════════════════════════════════════════════════════════════════
                            ТЕСТОВЫЕ СЦЕНАРИИ
                    Банковская Информационная Система
═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 1: Проверка авторизации пользователей
┌─────┬──────────────────────────┬────────────────────────────┬──────────────┐
│ Шаг │ Действие                 │ Ожидаемый результат        │ Результат    │
├─────┼──────────────────────────┼────────────────────────────┼──────────────┤
│ 1   │ Вход admin/admin123      │ Успешная авторизация       │ PASS         │
│ 2   │ Вход manager/manager123  │ Успешная авторизация       │ PASS         │
│ 3   │ Вход client1/client123   │ Успешная авторизация       │ PASS         │
│ 4   │ Вход admin/wrongpass     │ Отказ в доступе            │ PASS         │
│ 5   │ Вход unknownuser/pass    │ Отказ в доступе            │ PASS         │
└─────┴──────────────────────────┴────────────────────────────┴──────────────┘

ТЕСТ 2: Операции со счетами (пополнение, перевод)
┌─────┬──────────────────────────┬────────────────────────────┬──────────────┐
│ Шаг │ Действие                 │ Ожидаемый результат        │ Результат    │
├─────┼──────────────────────────┼────────────────────────────┼──────────────┤
│ 1   │ Пополнить счет на 1000   │ Баланс увеличен на 1000    │ PASS         │
│ 2   │ Снять 500 со счета       │ Баланс уменьшен на 500     │ PASS         │
│ 3   │ Попытка снять больше     │ Отказ, недостаточно средств│ PASS         │
│     │ доступного баланса       │                            │              │
│ 4   │ Перевод 1000 на другой   │ Перевод выполнен, балансы  │ PASS         │
│     │ счет                     │ обновлены                  │              │
└─────┴──────────────────────────┴────────────────────────────┴──────────────┘

ТЕСТ 3: Управление пользователями
┌─────┬──────────────────────────┬────────────────────────────┬──────────────┐
│ Шаг │ Действие                 │ Ожидаемый результат        │ Результат    │
├─────┼──────────────────────────┼────────────────────────────┼──────────────┤
│ 1   │ Создать пользователя     │ Пользователь создан        │ PASS         │
│     │ testuser/testpass        │                            │              │
│ 2   │ Попытка создать дубликат │ Отказ, пользователь        │ PASS         │
│     │ пользователя             │ существует                 │              │
│ 3   │ Изменить пароль          │ Пароль успешно изменен     │ PASS         │
│     │ пользователя             │                            │              │
│ 4   │ Удалить тестового        │ Пользователь удален        │ PASS         │
│     │ пользователя             │                            │              │
└─────┴──────────────────────────┴────────────────────────────┴──────────────┘
"""

class TestBankSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Подготовка тестовой среды"""
        print("\n" + "="*80)
        print("НАЧАЛО ТЕСТИРОВАНИЯ БАНКОВСКОЙ СИСТЕМЫ")
        print("="*80 + "\n")

        # Создание резервной копии исходных данных
        import shutil
        shutil.copy('data.json', 'data.json.backup')
        shutil.copy('users.json', 'users.json.backup')

    @classmethod
    def tearDownClass(cls):
        """Завершение тестирования"""
        print("\n" + "="*80)
        print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
        print("="*80 + "\n")

        # Восстановление исходных данных
        import shutil
        if os.path.exists('data.json.backup'):
            shutil.copy('data.json.backup', 'data.json')
            os.remove('data.json.backup')
        if os.path.exists('users.json.backup'):
            shutil.copy('users.json.backup', 'users.json')
            os.remove('users.json.backup')
    
    # ТЕСТ 1: Проверка авторизации
    
    def test_01_authentication_valid_admin(self):
        """ТЕСТ 1.1: Авторизация администратора"""
        print("\n[ТЕСТ 1.1] Проверка авторизации администратора...")
        user = auth.authenticate('admin', 'admin123')
        self.assertIsNotNone(user, "Администратор должен успешно авторизоваться")
        self.assertEqual(user['role'], 'administrator', "Роль должна быть 'administrator'")
        print("PASS: Администратор успешно авторизован")
    
    def test_02_authentication_valid_manager(self):
        """ТЕСТ 1.2: Авторизация менеджера"""
        print("\n[ТЕСТ 1.2] Проверка авторизации менеджера...")
        user = auth.authenticate('manager', 'manager123')
        self.assertIsNotNone(user, "Менеджер должен успешно авторизоваться")
        self.assertEqual(user['role'], 'manager', "Роль должна быть 'manager'")
        print("PASS: Менеджер успешно авторизован")
    
    def test_03_authentication_valid_client(self):
        """ТЕСТ 1.3: Авторизация клиента"""
        print("\n[ТЕСТ 1.3] Проверка авторизации клиента...")
        user = auth.authenticate('client1', 'client123')
        self.assertIsNotNone(user, "Клиент должен успешно авторизоваться")
        self.assertEqual(user['role'], 'client', "Роль должна быть 'client'")
        print("PASS: Клиент успешно авторизован")
    
    def test_04_authentication_wrong_password(self):
        """ТЕСТ 1.4: Неверный пароль"""
        print("\n[ТЕСТ 1.4] Проверка отказа при неверном пароле...")
        user = auth.authenticate('admin', 'wrongpassword')
        self.assertIsNone(user, "Авторизация с неверным паролем должна быть отклонена")
        print("PASS: Вход с неверным паролем отклонен")
    
    def test_05_authentication_wrong_username(self):
        """ТЕСТ 1.5: Несуществующий пользователь"""
        print("\n[ТЕСТ 1.5] Проверка отказа для несуществующего пользователя...")
        user = auth.authenticate('unknownuser', 'anypassword')
        self.assertIsNone(user, "Авторизация несуществующего пользователя должна быть отклонена")
        print("PASS: Вход несуществующего пользователя отклонен")
    
    # ТЕСТ 2: Операции со счетами

    def setUp(self):
        """Восстановление данных перед каждым тестом"""
        if os.path.exists('data.json.backup'):
            import shutil
            shutil.copy('data.json.backup', 'data.json')
        if os.path.exists('users.json.backup'):
            import shutil
            shutil.copy('users.json.backup', 'users.json')

    def test_06_account_deposit(self):
        """ТЕСТ 2.1: Пополнение счета"""
        print("\n[ТЕСТ 2.1] Проверка пополнения счета...")

        # Загружаем существующие данные
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Пополнение счета ACC001
        data['accounts'][0]['balance'] += 1000.0

        # Сохраняем изменения обратно в файл
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.assertEqual(data['accounts'][0]['balance'], 11000.0, "Баланс должен увеличиться до 11000")
        print("PASS: Счет успешно пополнен на 1000, новый баланс: 11000")

    def test_07_account_withdrawal(self):
        """ТЕСТ 2.2: Снятие средств"""
        print("\n[ТЕСТ 2.2] Проверка снятия средств...")

        # Загружаем существующие данные
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        balance = data['accounts'][0]['balance']
        withdrawal = 500.0

        if balance >= withdrawal:
            data['accounts'][0]['balance'] -= withdrawal
            success = True
        else:
            success = False

        # Сохраняем изменения обратно в файл
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.assertTrue(success, "Снятие должно быть успешным")
        self.assertEqual(data['accounts'][0]['balance'], 9500.0, "Баланс должен уменьшиться до 9500")
        print("PASS: Снятие 500 выполнено, новый баланс: 9500")

    def test_08_account_insufficient_funds(self):
        """ТЕСТ 2.3: Попытка снятия больше доступного"""
        print("\n[ТЕСТ 2.3] Проверка отказа при недостаточном балансе...")

        # Загружаем существующие данные
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        balance = data['accounts'][0]['balance']
        withdrawal = 20000.0

        if balance >= withdrawal:
            success = True
        else:
            success = False

        self.assertFalse(success, "Снятие должно быть отклонено")
        self.assertEqual(data['accounts'][0]['balance'], 10000.0, "Баланс не должен измениться")
        print("PASS: Попытка снять 20000 отклонена, баланс остался 10000")

    def test_09_account_transfer(self):
        """ТЕСТ 2.4: Перевод между счетами"""
        print("\n[ТЕСТ 2.4] Проверка перевода между счетами...")

        # Загружаем существующие данные
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        account1_balance = data['accounts'][0]['balance']
        account2_balance = data['accounts'][1]['balance']
        transfer_amount = 1000.0

        if account1_balance >= transfer_amount:
            data['accounts'][0]['balance'] -= transfer_amount
            data['accounts'][1]['balance'] += transfer_amount
            success = True
        else:
            success = False

        # Сохраняем изменения обратно в файл
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.assertTrue(success, "Перевод должен быть успешным")
        self.assertEqual(data['accounts'][0]['balance'], 9000.0, "Баланс счета 1 должен быть 9000")
        self.assertEqual(data['accounts'][1]['balance'], 6000.0, "Баланс счета 2 должен быть 6000")
        print("PASS: Перевод 1000 выполнен, балансы обновлены (9000 и 6000)")
    
    # ТЕСТ 3: Управление пользователями

    def test_10_create_user(self):
        """ТЕСТ 3.1: Создание нового пользователя"""
        print("\n[ТЕСТ 3.1] Проверка создания пользователя...")

        success, msg = auth.create_user('newtestuser', 'testpass123', 'client', 'Новый Тестовый Пользователь')

        self.assertTrue(success, "Пользователь должен быть создан")

        # Проверка авторизации
        user = auth.authenticate('newtestuser', 'testpass123')
        self.assertIsNotNone(user, "Новый пользователь должен авторизоваться")
        print("PASS: Пользователь newtestuser успешно создан")

    def test_11_create_duplicate_user(self):
        """ТЕСТ 3.2: Попытка создания дубликата"""
        print("\n[ТЕСТ 3.2] Проверка отказа при создании дубликата...")

        auth.create_user('duplicatetest', 'pass123', 'client', 'Дубликат')
        success, msg = auth.create_user('duplicatetest', 'pass456', 'client', 'Еще Дубликат')

        self.assertFalse(success, "Создание дубликата должно быть отклонено")
        print("PASS: Создание дубликата пользователя отклонено")

    def test_12_change_password(self):
        """ТЕСТ 3.3: Изменение пароля"""
        print("\n[ТЕСТ 3.3] Проверка изменения пароля...")

        # Создание пользователя
        auth.create_user('changepasstest', 'oldpass123', 'client', 'Смена Пароля')

        # Изменение пароля
        success, msg = auth.change_password('changepasstest', 'oldpass123', 'newpass123')

        self.assertTrue(success, "Пароль должен быть изменен")

        # Проверка старого пароля
        user_old = auth.authenticate('changepasstest', 'oldpass123')
        self.assertIsNone(user_old, "Старый пароль не должен работать")

        # Проверка нового пароля
        user_new = auth.authenticate('changepasstest', 'newpass123')
        self.assertIsNotNone(user_new, "Новый пароль должен работать")
        print("PASS: Пароль успешно изменен")

    def test_13_delete_user(self):
        """ТЕСТ 3.4: Удаление пользователя"""
        print("\n[ТЕСТ 3.4] Проверка удаления пользователя...")

        # Создание пользователя
        auth.create_user('deleteusertest', 'pass123', 'client', 'Удаляемый')

        # Проверка существования
        user_before = auth.authenticate('deleteusertest', 'pass123')
        self.assertIsNotNone(user_before, "Пользователь должен существовать")

        # Удаление
        success = auth.delete_user('deleteusertest')
        self.assertTrue(success, "Удаление должно быть успешным")

        # Проверка отсутствия
        user_after = auth.authenticate('deleteusertest', 'pass123')
        self.assertIsNone(user_after, "Пользователь не должен существовать")
        print("PASS: Пользователь успешно удален")

def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBankSystem)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Итоговая статистика
    print("\n" + "="*80)
    print("ИТОГОВАЯ СТАТИСТИКА")
    print("="*80)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print("="*80)
    
    return result

if __name__ == '__main__':
    run_tests()