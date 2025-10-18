"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "АВТОСАЛОН"

Этот файл содержит три тестовых сценария для проверки основной функциональности системы.
"""

import json
import os
import sys
import random
import string
import auth
from datetime import datetime

# Путь к файлам данных
USERS_FILE = "users.json"
DATA_FILE = "data.json"

class TestScenarios:
    """Класс для выполнения тестовых сценариев"""
    
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_result(self, test_name, step, action, expected, result, status):
        """Логирование результата теста"""
        self.results.append({
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'result': result,
            'status': status
        })
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
    
    def print_results(self):
        """Вывод результатов тестирования"""
        print("\n" + "="*100)
        print(" "*35 + "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("="*100)

        current_test = None
        for r in self.results:
            if r['test'] != current_test:
                current_test = r['test']
                print(f"\n{current_test}")
                print("-"*100)
                print(f"{'Шаг':<6}{'Действие':<35}{'Ожидаемый результат':<30}{'Фактический результат':<20}{'Статус':<10}")
                print("-"*100)

            status_symbol = "PASS" if r['status'] == "PASS" else "FAIL"
            print(f"{r['step']:<6}{r['action']:<35}{r['expected']:<30}{r['result']:<20}{status_symbol}")

        print("\n" + "="*100)
        print(f"ИТОГО: {self.passed_tests}/{self.total_tests} тестов пройдено ({self.passed_tests/self.total_tests*100:.1f}%)")
        print("="*100 + "\n")
    
    def test_scenario_1_authentication(self):
        """
        ТЕСТ 1: Проверка системы авторизации

        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        | Шаг   | Действие                         | Ожидаемый результат              | Фактический результат    | Статус    |
        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        | 1     | Вход с логином admin/admin123    | Успешная авторизация             | Данные пользователя      | PASS/FAIL |
        | 2     | Вход с неверным паролем          | Авторизация отклонена            | None                     | PASS/FAIL |
        | 3     | Создание нового пользователя     | Пользователь создан              | True                     | PASS/FAIL |
        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        """
        test_name = "ТЕСТ 1: Проверка системы авторизации"
        print(f"\nВыполнение: {test_name}")

        # Шаг 1: Вход с правильными данными
        user = auth.authenticate("admin", "admin123")
        self.log_result(test_name, 1, "Вход admin/admin123",
                       "Успешная авторизация",
                       f"User: {user['username']}" if user else "None",
                       "PASS" if user and user['username'] == 'admin' else "FAIL")

        # Шаг 2: Вход с неверным паролем
        user_wrong = auth.authenticate("admin", "wrongpassword")
        self.log_result(test_name, 2, "Вход с неверным паролем",
                       "Отклонено",
                       "None" if not user_wrong else "Accepted",
                       "PASS" if not user_wrong else "FAIL")

        # Шаг 3: Создание нового пользователя
        random_username = "testuser" + ''.join(random.choices(string.digits, k=3))
        success, msg = auth.create_user(random_username, "test123", "manager", "Тестовый Пользователь")
        self.log_result(test_name, 3, f"Создание пользователя {random_username}",
                       "Создан",
                       "True" if success else "False",
                       "PASS" if success else "FAIL")
    
    def test_scenario_2_car_management(self):
        """
        ТЕСТ 2: Управление автомобилями

        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        | Шаг   | Действие                         | Ожидаемый результат              | Фактический результат    | Статус    |
        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        | 1     | Проверка наличия автомобилей     | Автомобили присутствуют          | Количество > 0           | PASS/FAIL |
        | 2     | Добавление нового автомобиля     | Автомобиль добавлен              | Новый ID                 | PASS/FAIL |
        | 3     | Проверка статуса автомобиля      | Статус 'available'               | available                | PASS/FAIL |
        | 4     | Изменение статуса на 'sold'      | Статус изменен                   | sold                     | PASS/FAIL |
        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        """
        test_name = "ТЕСТ 2: Управление автомобилями"
        print(f"\nВыполнение: {test_name}")

        # Шаг 1: Загрузка данных
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.log_result(test_name, 1, "Загрузка данных",
                           "Данные загружены", f"Ошибка: {e}", "FAIL")
            return

        # Шаг 2: Проверка автомобилей
        cars_count = len(data['cars'])
        self.log_result(test_name, 1, "Проверка автомобилей в БД",
                       "Количество > 0",
                       f"Найдено: {cars_count}",
                       "PASS" if cars_count > 0 else "FAIL")

        # Шаг 3: Добавление автомобиля
        initial_count = len(data['cars'])
        new_car = {
            "id": max([c['id'] for c in data['cars']], default=0) + 1,
            "brand": "Audi",
            "model": "A6",
            "year": 2024,
            "price": 3800000,
            "vin": "WAU12345678901234",
            "status": "available",
            "color": "Синий"
        }
        data['cars'].append(new_car)

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Перезагрузка для проверки
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data_check = json.load(f)

        added = len(data_check['cars']) == initial_count + 1
        self.log_result(test_name, 2, "Добавление Audi A6",
                       "Добавлен",
                       f"ID {new_car['id']}" if added else "Не добавлен",
                       "PASS" if added else "FAIL")

        # Шаг 4: Проверка статуса
        last_car = data_check['cars'][-1]
        status_ok = last_car['status'] == 'available'
        self.log_result(test_name, 3, "Проверка статуса нового авто",
                       "available",
                       last_car['status'],
                       "PASS" if status_ok else "FAIL")

        # Шаг 5: Изменение статуса
        data_check['cars'][-1]['status'] = 'sold'
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_check, f, ensure_ascii=False, indent=2)

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data_final = json.load(f)

        status_changed = data_final['cars'][-1]['status'] == 'sold'
        self.log_result(test_name, 4, "Изменение статуса на 'sold'",
                       "sold",
                       data_final['cars'][-1]['status'],
                       "PASS" if status_changed else "FAIL")
    
    def test_scenario_3_sales_process(self):
        """
        ТЕСТ 3: Процесс оформления продажи

        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        | Шаг   | Действие                         | Ожидаемый результат              | Фактический результат    | Статус    |
        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        | 1     | Проверка наличия клиентов        | Клиенты присутствуют             | Количество > 0           | PASS/FAIL |
        | 2     | Создание новой продажи           | Продажа добавлена                | Новый ID продажи         | PASS/FAIL |
        | 3     | Проверка данных продажи          | Все поля заполнены               | Проверка полей           | PASS/FAIL |
        | 4     | Подсчет общей выручки            | Сумма рассчитана                 | Сумма > 0                | PASS/FAIL |
        |-------|----------------------------------|----------------------------------|--------------------------|-----------|
        """
        test_name = "ТЕСТ 3: Процесс оформления продажи"
        print(f"\nВыполнение: {test_name}")

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Шаг 1: Проверка клиентов
        clients_count = len(data['clients'])
        self.log_result(test_name, 1, "Проверка клиентов в БД",
                       "Количество > 0",
                       f"Найдено: {clients_count}",
                       "PASS" if clients_count > 0 else "FAIL")

        # Шаг 2: Создание продажи
        initial_sales = len(data['sales'])
        available_car = next((c for c in data['cars'] if c['status'] == 'available'), None)

        if available_car and data['clients']:
            new_sale = {
                "id": len(data['sales']) + 1,
                "car": f"{available_car['brand']} {available_car['model']} ({available_car['year']})",
                "car_id": available_car['id'],
                "client": data['clients'][0]['name'],
                "manager": "Тестовый Менеджер",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "price": available_car['price']
            }
            data['sales'].append(new_sale)

            # Обновление статуса автомобиля
            for car in data['cars']:
                if car['id'] == available_car['id']:
                    car['status'] = 'sold'

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            sale_added = len(data['sales']) == initial_sales + 1
            self.log_result(test_name, 2, "Создание новой продажи",
                           "Добавлена",
                           f"ID {new_sale['id']}" if sale_added else "Не добавлена",
                           "PASS" if sale_added else "FAIL")

            # Шаг 3: Проверка данных продажи
            all_fields_filled = all([
                new_sale.get('car'),
                new_sale.get('client'),
                new_sale.get('manager'),
                new_sale.get('date'),
                new_sale.get('price')
            ])
            self.log_result(test_name, 3, "Проверка полноты данных продажи",
                           "Все поля заполнены",
                           "Да" if all_fields_filled else "Нет",
                           "PASS" if all_fields_filled else "FAIL")
        else:
            self.log_result(test_name, 2, "Создание новой продажи",
                           "Добавлена", "Нет доступных авто", "FAIL")
            self.log_result(test_name, 3, "Проверка данных продажи",
                           "Все поля заполнены", "Пропущено", "FAIL")

        # Шаг 4: Подсчет выручки
        total_revenue = sum([s['price'] for s in data['sales']])
        revenue_ok = total_revenue > 0
        self.log_result(test_name, 4, "Подсчет общей выручки",
                       "Сумма > 0",
                       f"{total_revenue:,} руб.",
                       "PASS" if revenue_ok else "FAIL")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "="*100)
        print(" "*30 + "ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ")
        print(" "*25 + "Информационная система 'Автосалон'")
        print("="*100)
        
        self.test_scenario_1_authentication()
        self.test_scenario_2_car_management()
        self.test_scenario_3_sales_process()
        
        self.print_results()
        
        # Сохранение результатов в файл
        with open('test_results.txt', 'w', encoding='utf-8') as f:
            f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ\n")
            f.write("="*100 + "\n\n")
            for r in self.results:
                f.write(f"Тест: {r['test']}\n")
                f.write(f"Шаг {r['step']}: {r['action']}\n")
                f.write(f"Ожидалось: {r['expected']}\n")
                f.write(f"Получено: {r['result']}\n")
                f.write(f"Статус: {r['status']}\n")
                f.write("-"*100 + "\n")
            f.write(f"\nИТОГО: {self.passed_tests}/{self.total_tests} ({self.passed_tests/self.total_tests*100:.1f}%)\n")
        
        print("Результаты сохранены в файл: test_results.txt\n")

if __name__ == "__main__":
    tester = TestScenarios()
    tester.run_all_tests()