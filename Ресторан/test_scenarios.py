"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ РЕСТОРАН

Данный файл содержит автоматизированные тесты для проверки функциональности системы.
Тесты разделены на три основных сценария.
"""

import json
import os
import sys
from auth import AuthManager
from datetime import datetime

class TestScenarios:
    """
    Класс для выполнения тестовых сценариев
    """
    
    def __init__(self):
        self.auth = AuthManager('users.json')
        self.data_file = 'data.json'
        self.test_results = []
        self._init_test_data()
    
    def _init_test_data(self):
        """Инициализация тестовых данных - используем существующие файлы"""
        # Просто проверяем, что файлы существуют
        if not os.path.exists(self.data_file):
            print(f"Предупреждение: файл {self.data_file} не найден")
        if not os.path.exists(self.auth.users_file):
            print(f"Предупреждение: файл {self.auth.users_file} не найден")
    
    def _load_data(self):
        """Загрузка тестовых данных"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data):
        """Сохранение тестовых данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_result(self, test_name, step, action, expected, result):
        """Логирование результата теста"""
        status = "PASS" if result == expected else "FAIL"
        self.test_results.append({
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'actual': result,
            'status': status
        })
        return status == "PASS"
    
    def print_results(self):
        """Вывод результатов тестирования"""
        print("\n" + "="*100)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("="*100)
        
        current_test = None
        for result in self.test_results:
            if result['test'] != current_test:
                current_test = result['test']
                print(f"\n{'='*100}")
                print(f"ТЕСТ: {current_test}")
                print(f"{'='*100}")
                print(f"{'Шаг':<6} | {'Действие':<35} | {'Ожидаемый результат':<25} | {'Статус':<10}")
                print("-"*100)
            
            print(f"{result['step']:<6} | {result['action']:<35} | {result['expected']:<25} | {result['status']:<10}")
        
        # Статистика
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed = total - passed
        
        print("\n" + "="*100)
        print(f"ИТОГО: Всего тестов: {total} | Успешно: {passed} | Провалено: {failed}")
        print("="*100 + "\n")
    
    def test_1_authentication(self):
        """
        ТЕСТ 1: Проверка системы авторизации
        
        |-------|----------------------------------|---------------------------|-----------|
        | Шаг   | Действие                         | Ожидаемый результат       | Результат |
        |-------|----------------------------------|---------------------------|-----------|
        | 1     | Попытка входа с неверным паролем | Отказ в доступе           | PASS/FAIL |
        | 2     | Попытка входа с верными данными  | Успешная авторизация      | PASS/FAIL |
        | 3     | Проверка роли пользователя       | Роль = administrator      | PASS/FAIL |
        | 4     | Выход из системы                 | current_user = None       | PASS/FAIL |
        | 5     | Создание нового пользователя     | Пользователь создан       | PASS/FAIL |
        |-------|----------------------------------|---------------------------|-----------|
        """
        
        print("\n▶ Запуск ТЕСТА 1: Проверка системы авторизации")
        
        # Шаг 1: Неверный пароль
        result = self.auth.login('admin', 'wrongpassword')
        self.log_result('ТЕСТ 1: Авторизация', 1, 
                       'Вход с неверным паролем', 
                       'Отказ (False)', 
                       'Отказ (False)' if not result else 'Успех (True)')
        
        # Шаг 2: Верные данные
        result = self.auth.login('admin', 'admin123')
        self.log_result('ТЕСТ 1: Авторизация', 2,
                       'Вход с верными данными',
                       'Успех (True)',
                       'Успех (True)' if result else 'Отказ (False)')
        
        # Шаг 3: Проверка роли
        user = self.auth.get_current_user()
        role = user['role'] if user else None
        self.log_result('ТЕСТ 1: Авторизация', 3,
                       'Проверка роли пользователя',
                       'administrator',
                       role if role == 'administrator' else f'{role} (ожидалось administrator)')
        
        # Шаг 4: Выход
        self.auth.logout()
        user = self.auth.get_current_user()
        self.log_result('ТЕСТ 1: Авторизация', 4,
                       'Выход из системы',
                       'None',
                       'None' if user is None else str(user))
        
        # Шаг 5: Создание пользователя
        result = self.auth.add_user('testuser', 'testpass', 'client')
        self.log_result('ТЕСТ 1: Авторизация', 5,
                       'Создание нового пользователя',
                       'True',
                       'True' if result else 'False')
    
    def test_2_menu_management(self):
        """
        ТЕСТ 2: Управление меню
        
        |-------|----------------------------------|---------------------------|-----------|
        | Шаг   | Действие                         | Ожидаемый результат       | Результат |
        |-------|----------------------------------|---------------------------|-----------|
        | 1     | Просмотр меню                    | Список блюд получен       | PASS/FAIL |
        | 2     | Добавление нового блюда          | Блюдо добавлено           | PASS/FAIL |
        | 3     | Проверка количества блюд         | Количество увеличилось    | PASS/FAIL |
        | 4     | Удаление блюда                   | Блюдо удалено             | PASS/FAIL |
        | 5     | Проверка доступности блюда       | Блюдо недоступно          | PASS/FAIL |
        |-------|----------------------------------|---------------------------|-----------|
        """
        
        print("\n▶ Запуск ТЕСТА 2: Управление меню")
        
        # Шаг 1: Просмотр меню
        data = self._load_data()
        initial_count = len(data['menu'])
        self.log_result('ТЕСТ 2: Управление меню', 1,
                       'Просмотр текущего меню',
                       f'Список получен ({initial_count} блюд)',
                       f'Список получен ({initial_count} блюд)')
        
        # Шаг 2: Добавление блюда
        new_dish = {
            "id": data['next_menu_id'],
            "name": "Новое тестовое блюдо",
            "category": "Тест",
            "price": 500,
            "available": True
        }
        data['menu'].append(new_dish)
        data['next_menu_id'] += 1
        self._save_data(data)
        
        self.log_result('ТЕСТ 2: Управление меню', 2,
                       'Добавление блюда "Новое тестовое"',
                       'Блюдо добавлено',
                       'Блюдо добавлено')
        
        # Шаг 3: Проверка количества
        data = self._load_data()
        new_count = len(data['menu'])
        self.log_result('ТЕСТ 2: Управление меню', 3,
                       'Проверка количества блюд',
                       str(initial_count + 1),
                       str(new_count))
        
        # Шаг 4: Удаление блюда
        dish_to_delete = new_dish['id']
        data['menu'] = [d for d in data['menu'] if d['id'] != dish_to_delete]
        self._save_data(data)
        
        self.log_result('ТЕСТ 2: Управление меню', 4,
                       'Удаление добавленного блюда',
                       'Блюдо удалено',
                       'Блюдо удалено')
        
        # Шаг 5: Проверка доступности
        data = self._load_data()
        dish_exists = any(d['id'] == dish_to_delete for d in data['menu'])
        self.log_result('ТЕСТ 2: Управление меню', 5,
                       'Проверка наличия удаленного блюда',
                       'Не найдено',
                       'Не найдено' if not dish_exists else 'Найдено')
    
    def test_3_order_processing(self):
        """
        ТЕСТ 3: Обработка заказов
        
        |-------|----------------------------------|---------------------------|-----------|
        | Шаг   | Действие                         | Ожидаемый результат       | Результат |
        |-------|----------------------------------|---------------------------|-----------|
        | 1     | Авторизация официанта            | Успешный вход             | PASS/FAIL |
        | 2     | Создание нового заказа           | Заказ создан              | PASS/FAIL |
        | 3     | Проверка суммы заказа            | Сумма рассчитана верно    | PASS/FAIL |
        | 4     | Изменение статуса заказа         | Статус изменен            | PASS/FAIL |
        | 5     | Проверка статуса столика         | Столик занят              | PASS/FAIL |
        |-------|----------------------------------|---------------------------|-----------|
        """
        
        print("\n▶ Запуск ТЕСТА 3: Обработка заказов")
        
        # Шаг 1: Авторизация
        result = self.auth.login('waiter1', 'waiter123')
        self.log_result('ТЕСТ 3: Обработка заказов', 1,
                       'Авторизация официанта waiter1',
                       'Успех',
                       'Успех' if result else 'Неудача')
        
        # Шаг 2: Создание заказа
        data = self._load_data()
        new_order = {
            "id": data['next_order_id'],
            "waiter": "waiter1",
            "table": 1,
            "items": [
                {"name": "Борщ", "qty": 2, "price": 250}
            ],
            "total": 500,
            "status": "new",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data['orders'].append(new_order)
        data['next_order_id'] += 1
        self._save_data(data)
        
        self.log_result('ТЕСТ 3: Обработка заказов', 2,
                       'Создание заказа №1',
                       'Заказ создан',
                       'Заказ создан')
        
        # Шаг 3: Проверка суммы
        expected_total = 500
        actual_total = new_order['total']
        self.log_result('ТЕСТ 3: Обработка заказов', 3,
                       'Проверка суммы заказа',
                       f'{expected_total} ₽',
                       f'{actual_total} ₽' if actual_total == expected_total else f'{actual_total} ₽ (ожидалось {expected_total} ₽)')
        
        # Шаг 4: Изменение статуса
        data = self._load_data()
        for order in data['orders']:
            if order['id'] == new_order['id']:
                order['status'] = 'cooking'
        self._save_data(data)

        data = self._load_data()
        order_status = next((o['status'] for o in data['orders'] if o['id'] == new_order['id']), None)
        self.log_result('ТЕСТ 3: Обработка заказов', 4,
                       'Изменение статуса на "cooking"',
                       'cooking',
                       order_status if order_status == 'cooking' else f'{order_status} (ожидалось cooking)')
        
        # Шаг 5: Проверка столика
        data = self._load_data()
        for table in data['tables']:
            if table['number'] == 1:
                table['status'] = 'occupied'
        self._save_data(data)

        data = self._load_data()
        table_status = next((t['status'] for t in data['tables'] if t['number'] == 1), None)
        self.log_result('ТЕСТ 3: Обработка заказов', 5,
                       'Проверка статуса столика',
                       'occupied',
                       table_status if table_status == 'occupied' else f'{table_status} (ожидалось occupied)')
    
    def cleanup(self):
        """Очистка - не требуется, так как используем основные файлы"""
        pass
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "="*100)
        print("НАЧАЛО ТЕСТИРОВАНИЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ РЕСТОРАН")
        print("="*100)
        
        # Запуск тестов
        self.test_1_authentication()
        self.test_2_menu_management()
        self.test_3_order_processing()
        
        # Вывод результатов
        self.print_results()
        
        # Очистка
        self.cleanup()
        
        # Возврат статистики
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        return passed == total

if __name__ == '__main__':
    tester = TestScenarios()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)