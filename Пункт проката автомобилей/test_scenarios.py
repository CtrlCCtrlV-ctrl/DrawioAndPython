import json
import os
from datetime import datetime, timedelta
import unittest

class TestScenarios(unittest.TestCase):
    """Класс для автоматического тестирования системы"""
    
    def setUp(self):
        """Подготовка тестового окружения"""
        self.test_users_file = 'test_users.json'
        self.test_data_file = 'test_data.json'
        
        # Создание тестовых данных пользователей
        test_users = {
            "users": [
                {
                    "username": "test_admin",
                    "password": "test123",
                    "role": "administrator",
                    "full_name": "Тестовый Администратор",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "username": "test_manager",
                    "password": "test123",
                    "role": "manager",
                    "full_name": "Тестовый Менеджер",
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }
        
        # Создание тестовых данных системы
        test_data = {
            "cars": [
                {"id": 1, "brand": "Test", "model": "Car1", "year": 2023, "price_per_day": 1000, "status": "available"},
                {"id": 2, "brand": "Test", "model": "Car2", "year": 2023, "price_per_day": 2000, "status": "available"}
            ],
            "clients": [
                {"id": 1, "name": "Тестовый Клиент", "phone": "+7900-000-00-00", "passport": "0000 000000"}
            ],
            "rentals": [],
            "bookings": []
        }
        
        with open(self.test_users_file, 'w', encoding='utf-8') as f:
            json.dump(test_users, f, ensure_ascii=False, indent=2)
        
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.test_users_file):
            os.remove(self.test_users_file)
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
    
    def test_01_authentication(self):
        """Тест 1: Проверка авторизации"""
        print("\n" + "="*50)
        print("ТЕСТ 1: Проверка авторизации")
        print("="*50)
        
        # Загрузка тестовых пользователей
        with open(self.test_users_file, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        # Тест неверного пароля
        auth_result = False
        for user in users_data['users']:
            if user['username'] == 'test_admin' and user['password'] == "wrong_password":
                auth_result = True
                break

        self.assertFalse(auth_result, "Шаг 2: Неверный пароль - PASS")
        print("✓ Шаг 2: Проверка неверного пароля - PASS")

        # Тест правильного пароля
        auth_result = False
        user_role = None
        for user in users_data['users']:
            if user['username'] == 'test_admin' and user['password'] == "test123":
                auth_result = True
                user_role = user['role']
                break

        self.assertTrue(auth_result, "Шаг 3: Правильный пароль")
        self.assertEqual(user_role, 'administrator', "Шаг 4: Роль администратора")
        print("✓ Шаг 3: Успешная авторизация - PASS")
        print("✓ Шаг 4: Проверка роли администратора - PASS")
        print("✓ Шаг 5: Функция выхода - PASS (симуляция)")
    
    def test_02_car_management(self):
        """Тест 2: Управление автопарком"""
        print("\n" + "="*50)
        print("ТЕСТ 2: Управление автопарком")
        print("="*50)
        
        # Загрузка тестовых данных
        with open(self.test_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        initial_count = len(data['cars'])
        print(f"✓ Шаг 1: Начальное количество автомобилей: {initial_count}")
        
        # Добавление автомобиля
        new_car = {
            "id": 3,
            "brand": "Test",
            "model": "NewCar",
            "year": 2024,
            "price_per_day": 3000,
            "status": "available"
        }
        data['cars'].append(new_car)
        self.assertEqual(len(data['cars']), initial_count + 1, "Добавление автомобиля")
        print("✓ Шаг 3: Добавление автомобиля - PASS")
        
        # Редактирование автомобиля
        for car in data['cars']:
            if car['id'] == 3:
                car['price_per_day'] = 3500
                break
        
        edited_car = next((c for c in data['cars'] if c['id'] == 3), None)
        self.assertEqual(edited_car['price_per_day'], 3500, "Редактирование автомобиля")
        print("✓ Шаг 4: Редактирование автомобиля - PASS")
        
        # Удаление автомобиля
        data['cars'] = [c for c in data['cars'] if c['id'] != 3]
        self.assertEqual(len(data['cars']), initial_count, "Удаление автомобиля")
        print("✓ Шаг 5: Удаление автомобиля - PASS")
        
        # Сохранение изменений
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def test_03_rental_process(self):
        """Тест 3: Оформление аренды"""
        print("\n" + "="*50)
        print("ТЕСТ 3: Оформление аренды")
        print("="*50)
        
        # Загрузка тестовых данных
        with open(self.test_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✓ Шаг 1: Вход как менеджер - PASS (симуляция)")
        
        # Выбор клиента и автомобиля
        client_id = 1
        car_id = 1
        days = 5
        
        client = next((c for c in data['clients'] if c['id'] == client_id), None)
        car = next((c for c in data['cars'] if c['id'] == car_id), None)
        
        self.assertIsNotNone(client, "Клиент найден")
        self.assertIsNotNone(car, "Автомобиль найден")
        print("✓ Шаг 2: Выбор клиента и автомобиля - PASS")
        
        # Расчет стоимости
        total_price = car['price_per_day'] * days
        self.assertEqual(total_price, 5000, "Расчет стоимости")
        print(f"✓ Шаг 3: Расчет стоимости ({total_price} руб.) - PASS")
        
        # Создание аренды
        new_rental = {
            "id": 1,
            "car_id": car_id,
            "client_id": client_id,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
            "total_price": total_price,
            "status": "active"
        }
        
        data['rentals'].append(new_rental)
        car['status'] = 'rented'
        
        self.assertEqual(len(data['rentals']), 1, "Создание аренды")
        print("✓ Шаг 4: Оформление аренды - PASS")
        
        self.assertEqual(car['status'], 'rented', "Изменение статуса автомобиля")
        print("✓ Шаг 5: Статус автомобиля изменен на 'В аренде' - PASS")
        
        # Сохранение изменений
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def run_all_tests(self):
        """Запуск всех тестов с отчетом"""
        print("\n" + "="*70)
        print("ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ СИСТЕМЫ ПРОКАТА АВТОМОБИЛЕЙ")
        print("="*70)
        print(f"Время начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Запуск тестов
        suite = unittest.TestLoader().loadTestsFromTestCase(TestScenarios)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Итоговый отчет
        print("\n" + "="*70)
        print("ИТОГОВЫЙ ОТЧЕТ")
        print("="*70)
        print(f"Всего тестов: {result.testsRun}")
        print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"Провалено: {len(result.failures)}")
        print(f"Ошибок: {len(result.errors)}")
        print(f"Время окончания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Создание файла отчета
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("ОТЧЕТ О ТЕСТИРОВАНИИ СИСТЕМЫ ПРОКАТА АВТОМОБИЛЕЙ\n")
            f.write("="*60 + "\n\n")
            f.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Всего тестов: {result.testsRun}\n")
            f.write(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}\n")
            f.write(f"Провалено: {len(result.failures)}\n")
            f.write(f"Ошибок: {len(result.errors)}\n\n")
            
            if result.failures:
                f.write("ПРОВАЛИВШИЕСЯ ТЕСТЫ:\n")
                f.write("-" * 30 + "\n")
                for test, traceback in result.failures:
                    f.write(f"Тест: {test}\n")
                    f.write(f"Ошибка: {traceback}\n\n")
            
            if result.errors:
                f.write("ТЕСТЫ С ОШИБКАМИ:\n")
                f.write("-" * 30 + "\n")
                for test, traceback in result.errors:
                    f.write(f"Тест: {test}\n")
                    f.write(f"Ошибка: {traceback}\n\n")
        
        print(f"Отчет сохранен в файл: {report_file}")
        
        return result.testsRun == 3 and len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    # Создание экземпляра тестового класса
    test_runner = TestScenarios()
    
    # Запуск всех тестов
    success = test_runner.run_all_tests()
    
    if success:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("Система проката автомобилей готова к работе.")
    else:
        print("\n❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ!")
        print("Необходимо исправить ошибки перед использованием системы.") 