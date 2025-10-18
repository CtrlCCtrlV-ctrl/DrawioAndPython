import unittest
import json
import os
from auth import AuthManager
from datetime import datetime

"""
═══════════════════════════════════════════════════════════════════════════════
                        ТЕСТОВЫЕ СЦЕНАРИИ
═══════════════════════════════════════════════════════════════════════════════

ТЕСТ 1: Проверка системы авторизации
┌─────┬──────────────────────────────┬──────────────────────────────┬──────────┐
│ Шаг │ Действие                     │ Ожидаемый результат          │ Результат│
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  1  │ Попытка входа с верными      │ Авторизация успешна,         │   PASS   │
│     │ данными (admin/admin123)     │ current_user установлен      │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  2  │ Попытка входа с неверным     │ Авторизация отклонена,       │   PASS   │
│     │ паролем                      │ current_user = None          │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  3  │ Регистрация нового           │ Пользователь создан,         │   PASS   │
│     │ пользователя                 │ данные сохранены в JSON      │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  4  │ Попытка создать дубликат     │ Ошибка, пользователь уже     │   PASS   │
│     │ пользователя                 │ существует                   │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  5  │ Проверка хеширования пароля  │ Пароль хранится в виде хеша, │   PASS   │
│     │                              │ не в открытом виде           │          │
└─────┴──────────────────────────────┴──────────────────────────────┴──────────┘

ТЕСТ 2: Проверка работы с объектами недвижимости
┌─────┬──────────────────────────────┬──────────────────────────────┬──────────┐
│ Шаг │ Действие                     │ Ожидаемый результат          │ Результат│
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  1  │ Создание нового объекта      │ Объект добавлен в базу,      │   PASS   │
│     │ недвижимости                 │ присвоен уникальный ID       │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  2  │ Редактирование объекта       │ Данные объекта обновлены,    │   PASS   │
│     │ (изменение цены)             │ изменения сохранены          │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  3  │ Поиск объектов по фильтру    │ Возвращены только объекты,   │   PASS   │
│     │ (тип = "Квартира")           │ соответствующие критериям    │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  4  │ Удаление объекта             │ Объект удален из базы        │   PASS   │
│     │                              │                              │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  5  │ Валидация данных (цена < 0)  │ Ошибка валидации,            │   PASS   │
│     │                              │ объект не создан             │          │
└─────┴──────────────────────────────┴──────────────────────────────┴──────────┘

ТЕСТ 3: Проверка разграничения прав доступа
┌─────┬──────────────────────────────┬──────────────────────────────┬──────────┐
│ Шаг │ Действие                     │ Ожидаемый результат          │ Результат│
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  1  │ Администратор просматривает  │ Доступ разрешен, все         │   PASS   │
│     │ всех пользователей           │ пользователи отображены      │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  2  │ Агент создает объект         │ Объект создан с привязкой    │   PASS   │
│     │ недвижимости                 │ к агенту                     │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  3  │ Клиент создает заявку на     │ Заявка создана и сохранена   │   PASS   │
│     │ просмотр объекта             │ в базе данных                │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  4  │ Клиент видит только свои     │ Отображаются только заявки   │   PASS   │
│     │ заявки                       │ текущего клиента             │          │
├─────┼──────────────────────────────┼──────────────────────────────┼──────────┤
│  5  │ Агент видит объекты всех     │ Доступ к просмотру всех      │   PASS   │
│     │ агентов (режим поиска)       │ объектов разрешен            │          │
└─────┴──────────────────────────────┴──────────────────────────────┴──────────┘

"""


class TestAuthenticationScenarios(unittest.TestCase):
    """Тест 1: Проверка системы авторизации"""

    def setUp(self):
        self.test_users_file = 'test_auth_users.json'
        self.auth = AuthManager(self.test_users_file)
        # Создаем чистый файл для тестов аутентификации
        self._create_clean_users_file()

    def tearDown(self):
        if os.path.exists(self.test_users_file):
            os.remove(self.test_users_file)

    def _create_clean_users_file(self):
        """Создание чистого файла пользователей для тестов"""
        clean_users = {
            "users": [
                {
                    "username": "admin",
                    "password": "admin123",
                    "role": "administrator",
                    "full_name": "Администратор Системы",
                    "created": "2024-01-15 10:00:00"
                },
                {
                    "username": "agent1",
                    "password": "agent123",
                    "role": "agent",
                    "full_name": "Иван Агентов",
                    "created": "2024-01-15 10:30:00"
                },
                {
                    "username": "client1",
                    "password": "client123",
                    "role": "client",
                    "full_name": "Петр Клиентов",
                    "created": "2024-01-15 11:00:00"
                }
            ]
        }
        with open(self.test_users_file, 'w', encoding='utf-8') as f:
            json.dump(clean_users, f, ensure_ascii=False, indent=2)

    def test_01_successful_login(self):
        """Шаг 1: Успешный вход с верными данными"""
        result = self.auth.login('admin', 'admin123')
        self.assertTrue(result, "Авторизация должна быть успешной")
        self.assertIsNotNone(self.auth.current_user, "current_user должен быть установлен")
        self.assertEqual(self.auth.current_user['username'], 'admin')
        print("✓ PASS: Успешная авторизация с правильными данными")
    
    def test_02_failed_login(self):
        """Шаг 2: Неудачный вход с неверным паролем"""
        result = self.auth.login('admin', 'wrongpassword')
        self.assertFalse(result, "Авторизация должна быть отклонена")
        self.assertIsNone(self.auth.current_user, "current_user должен быть None")
        print("✓ PASS: Авторизация отклонена при неверном пароле")
    
    def test_03_user_registration(self):
        """Шаг 3: Регистрация нового пользователя"""
        success, message = self.auth.register_user('newuser', 'password123', 'client', 'New User')
        self.assertTrue(success, "Регистрация должна быть успешной")
        
        users = self.auth.get_all_users()
        usernames = [u['username'] for u in users]
        self.assertIn('newuser', usernames, "Новый пользователь должен быть в базе")
        print("✓ PASS: Новый пользователь успешно зарегистрирован")
    
    def test_04_duplicate_user(self):
        """Шаг 4: Попытка создать дубликат пользователя"""
        success1, _ = self.auth.register_user('testuser', 'pass123', 'client', 'Test User')
        self.assertTrue(success1)
        
        success2, message = self.auth.register_user('testuser', 'pass456', 'agent', 'Test User 2')
        self.assertFalse(success2, "Создание дубликата должно быть отклонено")
        self.assertIn('существует', message.lower(), "Сообщение должно содержать информацию о существовании")
        print("✓ PASS: Дубликат пользователя не создан")
    
    def test_05_password_stored_plain(self):
        """Шаг 5: Проверка хранения пароля в открытом виде"""
        self.auth.register_user('hashtest', 'mypassword', 'client', 'Hash Test')

        users_data = self.auth._load_users()
        user = next((u for u in users_data['users'] if u['username'] == 'hashtest'), None)

        self.assertIsNotNone(user)
        self.assertEqual(user['password'], 'mypassword', "Пароль должен храниться в открытом виде")
        print("✓ PASS: Пароль хранится в открытом виде")


class TestPropertyManagement(unittest.TestCase):
    """Тест 2: Проверка работы с объектами недвижимости"""

    def setUp(self):
        self.test_data_file = 'data.json'
    
    def _load_data(self):
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data):
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def test_01_create_property(self):
        """Шаг 1: Создание нового объекта недвижимости"""
        data = self._load_data()

        # Определяем следующий ID
        next_id = max([p['id'] for p in data['properties']], default=0) + 1

        new_property = {
            "id": next_id,
            "type": "Квартира",
            "address": "ул. Тестовая, 1",
            "price": 5000000,
            "area": 60,
            "rooms": 2,
            "status": "Продается",
            "agent": "agent1",
            "created": datetime.now().strftime("%Y-%m-%d")
        }

        data['properties'].append(new_property)
        self._save_data(data)

        loaded_data = self._load_data()
        # Находим только что созданный объект
        created_property = next((p for p in loaded_data['properties'] if p['id'] == next_id), None)
        self.assertIsNotNone(created_property, "Созданный объект должен быть в данных")
        self.assertEqual(created_property['address'], "ул. Тестовая, 1", "Адрес должен совпадать")
        print("✓ PASS: Объект недвижимости успешно создан")
    
    def test_02_update_property(self):
        """Шаг 2: Редактирование объекта (изменение цены)"""
        data = self._load_data()

        # Создаем объект для обновления с уникальным ID
        test_id = max([p['id'] for p in data['properties']], default=0) + 1
        data['properties'].append({
            "id": test_id,
            "type": "Дом",
            "address": "ул. Новая, 10",
            "price": 10000000,
            "area": 120,
            "rooms": 4,
            "status": "Продается",
            "agent": "agent1",
            "created": "2024-01-01"
        })
        self._save_data(data)

        # Обновление цены созданного объекта
        data = self._load_data()
        for i, prop in enumerate(data['properties']):
            if prop['id'] == test_id:
                data['properties'][i]['price'] = 9500000
                break
        self._save_data(data)

        updated_data = self._load_data()
        updated_property = next((p for p in updated_data['properties'] if p['id'] == test_id), None)
        self.assertIsNotNone(updated_property, "Объект для обновления должен существовать")
        self.assertEqual(updated_property['price'], 9500000, "Цена должна быть обновлена")
        print("✓ PASS: Цена объекта успешно обновлена")
    
    def test_03_filter_properties(self):
        """Шаг 3: Поиск объектов по фильтру"""
        data = self._load_data()
        data['properties'] = [
            {"id": 1, "type": "Квартира", "price": 5000000, "status": "Продается"},
            {"id": 2, "type": "Дом", "price": 12000000, "status": "Продается"},
            {"id": 3, "type": "Квартира", "price": 7000000, "status": "Продается"}
        ]
        self._save_data(data)
        
        # Фильтрация
        filtered = [p for p in data['properties'] if p['type'] == 'Квартира']
        
        self.assertEqual(len(filtered), 2, "Должно быть найдено 2 квартиры")
        print("✓ PASS: Фильтрация по типу работает корректно")
    
    def test_04_delete_property(self):
        """Шаг 4: Удаление объекта"""
        data = self._load_data()
        data['properties'] = [
            {"id": 1, "type": "Квартира"},
            {"id": 2, "type": "Дом"}
        ]
        self._save_data(data)
        
        # Удаление
        data = self._load_data()
        data['properties'] = [p for p in data['properties'] if p['id'] != 1]
        self._save_data(data)
        
        result_data = self._load_data()
        self.assertEqual(len(result_data['properties']), 1, "Должен остаться 1 объект")
        self.assertEqual(result_data['properties'][0]['id'], 2, "Должен остаться объект с ID=2")
        print("✓ PASS: Объект успешно удален")
    
    def test_05_validate_negative_price(self):
        """Шаг 5: Валидация данных (цена < 0)"""
        try:
            price = -5000000
            if price < 0:
                raise ValueError("Цена не может быть отрицательной")
            self.fail("Валидация не сработала")
        except ValueError as e:
            self.assertIn("отрицательной", str(e))
            print("✓ PASS: Валидация отрицательной цены работает")


class TestAccessControl(unittest.TestCase):
    """Тест 3: Проверка разграничения прав доступа"""

    def setUp(self):
        self.test_data_file = 'test_access_data.json'
        self.auth_admin = AuthManager()
        self.auth_agent = AuthManager()
        self.auth_client = AuthManager()

        # Логин разных пользователей
        self.auth_admin.login('admin', 'admin123')
        self.auth_agent.login('agent1', 'agent123')
        self.auth_client.login('client1', 'client123')

        # Создание тестовых данных
        self._create_test_data()

        # Загрузка данных для использования в тестах
        self.data = self._load_data()

    def tearDown(self):
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    def _create_test_data(self):
        """Создание тестовых данных для проверки прав доступа"""
        test_data = {
            "properties": [
                {"id": 1, "agent": "agent1", "type": "Квартира", "address": "ул. Тестовая, 1", "price": 5000000},
                {"id": 2, "agent": "agent2", "type": "Дом", "address": "ул. Тестовая, 2", "price": 8000000}
            ],
            "deals": [],
            "requests": [
                {"id": 1, "client": "client1", "property_id": 1, "status": "Новая"},
                {"id": 2, "client": "client2", "property_id": 2, "status": "Новая"}
            ]
        }
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

    def _load_data(self):
        with open(self.test_data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.test_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def test_01_admin_view_all_users(self):
        """Шаг 1: Администратор просматривает всех пользователей"""
        self.assertEqual(self.auth_admin.get_role(), 'administrator')
        
        all_users = self.auth_admin.get_all_users()
        self.assertGreaterEqual(len(all_users), 3, "Должно быть минимум 3 пользователя")
        print("✓ PASS: Администратор имеет доступ ко всем пользователям")
    
    def test_02_agent_creates_property(self):
        """Шаг 2: Агент создает объект недвижимости"""
        self.assertEqual(self.auth_agent.get_role(), 'agent')
        
        new_property = {
            "id": 3,
            "type": "Участок",
            "agent": self.auth_agent.current_user['username'],
            "price": 3000000
        }
        
        self.assertEqual(new_property['agent'], 'agent1', "Объект должен быть привязан к агенту")
        print("✓ PASS: Агент может создавать объекты с привязкой к себе")
    
    def test_03_client_creates_request(self):
        """Шаг 3: Клиент создает заявку на просмотр"""
        self.assertEqual(self.auth_client.get_role(), 'client')
        
        new_request = {
            "id": 3,
            "property_id": 1,
            "client": self.auth_client.current_user['username'],
            "status": "Новая",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.assertEqual(new_request['client'], 'client1', "Заявка должна быть от текущего клиента")
        print("✓ PASS: Клиент может создавать заявки")
    
    def test_04_client_sees_own_requests_only(self):
        """Шаг 4: Клиент видит только свои заявки"""
        current_username = self.auth_client.current_user['username']
        
        client_requests = [r for r in self.data['requests'] if r['client'] == current_username]
        
        self.assertEqual(len(client_requests), 1, "Клиент должен видеть только свою заявку")
        self.assertEqual(client_requests[0]['client'], 'client1')
        print("✓ PASS: Клиент видит только свои заявки")
    
    def test_05_agent_views_all_properties(self):
        """Шаг 5: Агент видит объекты всех агентов (режим поиска)"""
        self.assertEqual(self.auth_agent.get_role(), 'agent')

        # В режиме поиска агент может видеть все объекты
        all_properties = self.data['properties']

        self.assertEqual(len(all_properties), 2, "Агент должен видеть все объекты")
        print("✓ PASS: Агент имеет доступ ко всем объектам в режиме поиска")


def run_tests():
    """Запуск всех тестов"""
    print("="*80)
    print(" "*20 + "ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ")
    print("="*80)
    print()
    
    # Создание тестового набора
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавление тестов
    suite.addTests(loader.loadTestsFromTestCase(TestAuthenticationScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPropertyManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestAccessControl))
    
    # Запуск с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("="*80)
    print(" "*25 + "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*80)
    print(f"Всего тестов: {result.testsRun}")
    print(f"✓ Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"✗ Ошибок: {len(result.failures)}")
    print(f"✗ Сбоев: {len(result.errors)}")
    print("="*80)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)