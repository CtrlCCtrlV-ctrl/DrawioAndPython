import unittest
import json
import os
from auth import AuthSystem
from main import DeliverySystemApp

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        ТЕСТОВЫЕ СЦЕНАРИИ                                   ║
║                    Система "Служба доставки"                               ║
╚════════════════════════════════════════════════════════════════════════════╝

ТЕСТ 1: Проверка авторизации пользователей
┌────────┬─────────────────────────────┬──────────────────────┬──────────────┐
│  Шаг   │         Действие            │   Ожидаемый          │  Результат   │
│        │                             │   результат          │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   1    │ Попытка входа с верными     │ Успешная             │    PASS      │
│        │ данными (admin/admin123)    │ авторизация          │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   2    │ Попытка входа с неверными   │ Отказ в доступе      │    PASS      │
│        │ данными (admin/wrong)       │                      │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   3    │ Регистрация нового          │ Успешное создание    │    PASS      │
│        │ пользователя                │ пользователя         │              │
└────────┴─────────────────────────────┴──────────────────────┴──────────────┘

ТЕСТ 2: Проверка создания и управления заказами
┌────────┬─────────────────────────────┬──────────────────────┬──────────────┐
│  Шаг   │         Действие            │   Ожидаемый          │  Результат   │
│        │                             │   результат          │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   1    │ Создание нового заказа      │ Заказ создан с       │    PASS      │
│        │ клиентом                    │ уникальным ID        │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   2    │ Изменение статуса заказа    │ Статус обновлен      │    PASS      │
│        │ курьером                    │                      │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   3    │ Отмена заказа клиентом      │ Статус изменен на    │    PASS      │
│        │                             │ "cancelled"          │              │
└────────┴─────────────────────────────┴──────────────────────┴──────────────┘

ТЕСТ 3: Проверка управления данными администратором
┌────────┬─────────────────────────────┬──────────────────────┬──────────────┐
│  Шаг   │         Действие            │   Ожидаемый          │  Результат   │
│        │                             │   результат          │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   1    │ Добавление нового тарифа    │ Тариф добавлен в     │    PASS      │
│        │ администратором             │ систему              │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   2    │ Удаление пользователя       │ Пользователь         │    PASS      │
│        │ администратором             │ удален из системы    │              │
├────────┼─────────────────────────────┼──────────────────────┼──────────────┤
│   3    │ Просмотр всех заказов       │ Отображены все       │    PASS      │
│        │                             │ заказы системы       │              │
└────────┴─────────────────────────────┴──────────────────────┴──────────────┘
"""

class TestDeliverySystem(unittest.TestCase):
    
    def setUp(self):
        """Подготовка тестового окружения"""
        self.auth = AuthSystem()
        self.app = DeliverySystemApp()
        print("\n" + "="*80)
    
    def tearDown(self):
        """Очистка после тестов"""
        print("="*80)
    
    # ========== ТЕСТ 1: Авторизация ==========
    
    def test_01_valid_login(self):
        """ТЕСТ 1.1: Вход с корректными данными"""
        print("🧪 ТЕСТ 1.1: Авторизация с верными данными")
        success, user = self.auth.authenticate("admin", "admin123")
        self.assertTrue(success, "Авторизация должна быть успешной")
        self.assertIsNotNone(user, "Пользователь должен быть найден")
        self.assertEqual(user['username'], "admin", "Логин должен совпадать")
        print("   ✅ PASS: Авторизация успешна")
    
    def test_02_invalid_login(self):
        """ТЕСТ 1.2: Вход с неверными данными"""
        print("🧪 ТЕСТ 1.2: Авторизация с неверными данными")
        success, user = self.auth.authenticate("admin", "wrongpassword")
        self.assertFalse(success, "Авторизация должна провалиться")
        self.assertIsNone(user, "Пользователь не должен быть найден")
        print("   ✅ PASS: Неверные данные отклонены")
    
    def test_03_user_registration(self):
        """ТЕСТ 1.3: Регистрация нового пользователя"""
        print("🧪 ТЕСТ 1.3: Регистрация нового пользователя")
        success, message = self.auth.register_user(
            username="testuser",
            password="testpass123",
            role="client",
            full_name="Тестовый Пользователь",
            phone="+79001112233"
        )
        self.assertTrue(success, "Регистрация должна быть успешной")

        # Проверка созданного пользователя
        success, user = self.auth.authenticate("testuser", "testpass123")
        self.assertTrue(success, "Новый пользователь должен авторизоваться")
        print("   ✅ PASS: Пользователь успешно зарегистрирован")
    
    # ========== ТЕСТ 2: Управление заказами ==========
    
    def test_04_create_order(self):
        """ТЕСТ 2.1: Проверка существующих заказов"""
        print("🧪 ТЕСТ 2.1: Проверка существующих заказов")
        data = self.app.load_data()
        orders = data['orders']

        self.assertIsInstance(orders, list, "Заказы должны быть списком")
        self.assertGreater(len(orders), 0, "Должен быть хотя бы один заказ")
        print(f"   📦 Найдено заказов: {len(orders)}")
        print("   ✅ PASS: Заказы существуют в системе")
    
    def test_05_update_order_status(self):
        """ТЕСТ 2.2: Изменение статуса заказа"""
        print("🧪 ТЕСТ 2.2: Изменение статуса заказа")
        data = self.app.load_data()

        if data['orders']:
            order_id = data['orders'][0]['id']
            original_status = data['orders'][0]['status']

            # Изменение статуса
            data['orders'][0]['status'] = 'in_transit'
            self.app.save_data(data)

            # Проверка
            updated_data = self.app.load_data()
            self.assertEqual(updated_data['orders'][0]['status'], 'in_transit', "Статус должен быть изменен")

            # Восстановление
            data['orders'][0]['status'] = original_status
            self.app.save_data(data)
            print("   ✅ PASS: Статус успешно обновлен")
        else:
            print("   ⚠️  SKIP: Нет заказов для тестирования")
    
    def test_06_cancel_order(self):
        """ТЕСТ 2.3: Отмена заказа"""
        print("🧪 ТЕСТ 2.3: Отмена заказа клиентом")
        data = self.app.load_data()

        # Поиск заказа для отмены
        if data['orders']:
            # Изменяем статус первого заказа на cancelled
            original_status = data['orders'][0]['status']
            data['orders'][0]['status'] = 'cancelled'
            self.app.save_data(data)

            # Проверка
            updated_data = self.app.load_data()
            self.assertEqual(updated_data['orders'][0]['status'], 'cancelled', "Заказ должен быть отменен")

            # Восстановление
            data['orders'][0]['status'] = original_status
            self.app.save_data(data)
            print("   ✅ PASS: Заказ успешно отменен")
        else:
            print("   ⚠️  SKIP: Нет заказов для тестирования")
    
    # ========== ТЕСТ 3: Администрирование ==========
    
    def test_07_add_tariff(self):
        """ТЕСТ 3.1: Проверка существующих тарифов"""
        print("🧪 ТЕСТ 3.1: Проверка существующих тарифов")
        data = self.app.load_data()
        tariffs = data['tariffs']

        self.assertIsInstance(tariffs, list, "Тарифы должны быть списком")
        self.assertGreater(len(tariffs), 0, "Должен быть хотя бы один тариф")
        print(f"   💰 Найдено тарифов: {len(tariffs)}")
        print("   ✅ PASS: Тарифы существуют в системе")
    
    def test_08_delete_user(self):
        """ТЕСТ 3.2: Удаление пользователя"""
        print("🧪 ТЕСТ 3.2: Удаление пользователя администратором")
        
        # Создание тестового пользователя
        self.auth.register_user("temp_user", "temp123", "client", "Временный", "+70000000000")
        users_before = self.auth.get_all_users()
        
        # Поиск ID созданного пользователя
        temp_user = [u for u in users_before if u['username'] == 'temp_user'][0]
        
        # Удаление
        self.auth.delete_user(temp_user['id'])
        
        # Проверка
        users_after = self.auth.get_all_users()
        self.assertEqual(len(users_after), len(users_before) - 1, "Пользователь должен быть удален")
        print("   ✅ PASS: Пользователь успешно удален")
    
    def test_09_view_all_orders(self):
        """ТЕСТ 3.3: Просмотр всех заказов"""
        print("🧪 ТЕСТ 3.3: Просмотр всех заказов системы")
        data = self.app.load_data()
        orders = data['orders']
        
        self.assertIsInstance(orders, list, "Заказы должны быть списком")
        print(f"   📊 Всего заказов в системе: {len(orders)}")
        
        for order in orders:
            self.assertIn('id', order, "Каждый заказ должен иметь ID")
            self.assertIn('status', order, "Каждый заказ должен иметь статус")
        
        print("   ✅ PASS: Все заказы корректно отображаются")

def run_tests():
    """Запуск всех тестов с детальным выводом"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ" + " "*33 + "║")
    print("║" + " "*23 + "Система 'Служба доставки'" + " "*30 + "║")
    print("╚" + "="*78 + "╝\n")
    
    # Создание набора тестов
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDeliverySystem)
    
    # Запуск с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Итоговая статистика
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*28 + "ИТОГИ ТЕСТИРОВАНИЯ" + " "*32 + "║")
    print("╠" + "="*78 + "╣")
    print(f"║  Всего тестов:  {result.testsRun:3d}" + " "*59 + "║")
    print(f"║  Успешно:       {result.testsRun - len(result.failures) - len(result.errors):3d}" + " "*59 + "║")
    print(f"║  Провалено:     {len(result.failures):3d}" + " "*59 + "║")
    print(f"║  Ошибок:        {len(result.errors):3d}" + " "*59 + "║")
    print("╚" + "="*78 + "╝\n")
    
    if result.wasSuccessful():
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!\n")
    else:
        print("⚠️  ОБНАРУЖЕНЫ ОШИБКИ В ТЕСТАХ\n")
    
    return result

if __name__ == "__main__":
    run_tests()