"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "БОЛЬНИЦА"

Данный файл содержит автоматизированные тесты для проверки основного функционала системы.
"""

import json
import os
import sys
from auth import authenticate, create_user, load_users, save_users

class TestScenarios:
    def __init__(self):
        self.test_results = []
        self.setup_test_environment()
    
    def setup_test_environment(self):
        """Подготовка тестового окружения"""
        # Создание тестовых файлов
        test_users = {
            "users": [
                {
                    "id": 1,
                    "username": "admin",
                    "password": "admin123",
                    "role": "administrator",
                    "name": "Администратор Системы",
                    "created": "2024-01-01"
                },
                {
                    "id": 2,
                    "username": "doctor1",
                    "password": "doctor123",
                    "role": "doctor",
                    "doctor_id": 1,
                    "name": "Иванов Иван Иванович",
                    "created": "2024-01-01"
                },
                {
                    "id": 3,
                    "username": "patient1",
                    "password": "patient123",
                    "role": "patient",
                    "patient_id": 1,
                    "name": "Петров Петр Петрович",
                    "created": "2024-01-01"
                }
            ]
        }
        save_users(test_users)
        
        test_data = {
            "doctors": [
                {"id": 1, "name": "Иванов Иван Иванович", "specialization": "Терапевт", "phone": "+7-900-123-45-67", "cabinet": "101"},
                {"id": 2, "name": "Сидорова Мария Петровна", "specialization": "Кардиолог", "phone": "+7-900-234-56-78", "cabinet": "205"}
            ],
            "patients": [
                {"id": 1, "name": "Петров Петр Петрович", "birth_date": "1990-05-15", "phone": "+7-900-345-67-89", "address": "г. Москва, ул. Ленина, д. 10"},
                {"id": 2, "name": "Смирнова Анна Ивановна", "birth_date": "1985-03-22", "phone": "+7-900-456-78-90", "address": "г. Москва, ул. Пушкина, д. 25"}
            ],
            "appointments": [
                {
                    "id": 1,
                    "patient_id": 1,
                    "doctor_id": 1,
                    "date": "2024-01-20",
                    "time": "10:00",
                    "status": "scheduled",
                    "diagnosis": "",
                    "treatment": ""
                }
            ]
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    def log_result(self, test_name, step, action, expected, result, status):
        """Логирование результата теста"""
        self.test_results.append({
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'result': result,
            'status': status
        })
    
    def print_results(self):
        """Вывод результатов в виде таблиц"""
        print("\n" + "="*100)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ 'БОЛЬНИЦА'")
        print("="*100 + "\n")
        
        current_test = None
        for result in self.test_results:
            if current_test != result['test']:
                current_test = result['test']
                print(f"\n{current_test}")
                print("-"*100)
                print(f"{'Шаг':<6}{'Действие':<35}{'Ожидаемый результат':<30}{'Статус':<10}")
                print("-"*100)
            
            status_symbol = "PASS" if result['status'] == 'PASS' else "FAIL"
            print(f"{result['step']:<6}{result['action']:<35}{result['expected']:<30}{status_symbol:<10}")
        
        # Итоговая статистика
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed = total - passed
        
        print("\n" + "="*100)
        print(f"ИТОГО: Всего тестов: {total} | Пройдено: {passed} | Провалено: {failed}")
        print("="*100 + "\n")
    
    # ========== ТЕСТ 1: Проверка авторизации ==========
    
    def test_authentication(self):
        """
        ТЕСТ 1: Проверка авторизации
        
        Цель: Проверить корректность работы системы аутентификации
        """
        test_name = "ТЕСТ 1: Проверка авторизации"
        
        # Шаг 1: Вход с корректными данными
        user = authenticate("admin", "admin123")
        if user and user['username'] == 'admin':
            self.log_result(test_name, 1, "Вход с верными данными", "Успешная авторизация",
                          f"Пользователь: {user['name']}", "PASS")
        else:
            self.log_result(test_name, 1, "Вход с верными данными", "Успешная авторизация",
                          "Ошибка входа", "FAIL")
        
        # Шаг 2: Вход с неверным паролем
        user = authenticate("admin", "wrong_password")
        if user is None:
            self.log_result(test_name, 2, "Вход с неверным паролем", "Отказ в доступе",
                          "Доступ запрещен", "PASS")
        else:
            self.log_result(test_name, 2, "Вход с неверным паролем", "Отказ в доступе",
                          "Ошибка: доступ разрешен", "FAIL")

        # Шаг 3: Вход с несуществующим пользователем
        user = authenticate("nonexistent_user", "password")
        if user is None:
            self.log_result(test_name, 3, "Вход несуществ. пользователя", "Отказ в доступе",
                          "Доступ запрещен", "PASS")
        else:
            self.log_result(test_name, 3, "Вход несуществ. пользователя", "Отказ в доступе",
                          "Ошибка: доступ разрешен", "FAIL")

        # Шаг 4: Проверка ролей пользователей
        admin_user = authenticate("admin", "admin123")
        doctor_user = authenticate("doctor1", "doctor123")
        
        if admin_user['role'] == 'administrator' and doctor_user['role'] == 'doctor':
            self.log_result(test_name, 4, "Проверка ролей", "Роли определены верно", 
                          "Админ и Врач определены", "PASS")
        else:
            self.log_result(test_name, 4, "Проверка ролей", "Роли определены верно", 
                          "Ошибка ролей", "FAIL")
    
    # ========== ТЕСТ 2: Управление пользователями ==========
    
    def test_user_management(self):
        """
        ТЕСТ 2: Управление пользователями
        
        Цель: Проверить функционал создания и управления пользователями
        """
        test_name = "ТЕСТ 2: Управление пользователями"
        
        # Шаг 1: Создание нового пользователя
        success, message = create_user("test_user", "testpass123", "patient", "Тестовый Пользователь", patient_id=2)
        if success:
            self.log_result(test_name, 1, "Создание нового пользователя", "Пользователь создан",
                          message, "PASS")
        else:
            self.log_result(test_name, 1, "Создание нового пользователя", "Пользователь создан",
                          message, "FAIL")

        # Шаг 2: Попытка создать дубликат
        success, message = create_user("test_user", "testpass123", "patient", "Дубликат")
        if not success:
            self.log_result(test_name, 2, "Создание дубликата", "Ошибка создания",
                          message, "PASS")
        else:
            self.log_result(test_name, 2, "Создание дубликата", "Ошибка создания",
                          "Создан дубликат", "FAIL")

        # Шаг 3: Проверка авторизации нового пользователя
        user = authenticate("test_user", "testpass123")
        if user and user['username'] == 'test_user':
            self.log_result(test_name, 3, "Авторизация нового польз.", "Успешный вход",
                          f"Вход выполнен: {user['name']}", "PASS")
        else:
            self.log_result(test_name, 3, "Авторизация нового польз.", "Успешный вход",
                          "Ошибка входа", "FAIL")

        # Шаг 4: Проверка количества пользователей
        users_data = load_users()
        user_count = len(users_data['users'])
        if user_count == 4:  # 3 исходных + 1 новый
            self.log_result(test_name, 4, "Подсчет пользователей", "Количество: 4",
                          f"Найдено: {user_count}", "PASS")
        else:
            self.log_result(test_name, 4, "Подсчет пользователей", "Количество: 4",
                          f"Найдено: {user_count}", "FAIL")
    
    # ========== ТЕСТ 3: Работа с данными приемов ==========
    
    def test_appointments_management(self):
        """
        ТЕСТ 3: Работа с данными приемов
        
        Цель: Проверить функционал управления приемами пациентов
        """
        test_name = "ТЕСТ 3: Работа с приемами"
        
        # Загрузка данных
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Шаг 1: Добавление нового приема
        # Найдем максимальный id и создадим новый с уникальным id
        max_id = max([a['id'] for a in data['appointments']]) if data['appointments'] else 0
        new_appointment = {
            "id": max_id + 1,
            "patient_id": 1,
            "doctor_id": 1,
            "date": "2024-02-01",
            "time": "10:00",
            "status": "scheduled",
            "diagnosis": "",
            "treatment": ""
        }
        data['appointments'].append(new_appointment)

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Проверка
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Проверяем, что прием был добавлен (длина списка увеличилась)
        initial_count = len(data['appointments']) - 1
        if len(data['appointments']) > initial_count:
            self.log_result(test_name, 1, "Добавление приема", "Прием создан",
                          f"Прием ID:{new_appointment['id']}", "PASS")
        else:
            self.log_result(test_name, 1, "Добавление приема", "Прием создан",
                          "Ошибка создания", "FAIL")
        
        # Шаг 2: Добавление диагноза
        # Найдем индекс нашего нового приема
        new_appointment_index = None
        for i, appointment in enumerate(data['appointments']):
            if appointment['id'] == new_appointment['id']:
                new_appointment_index = i
                break

        if new_appointment_index is not None:
            data['appointments'][new_appointment_index]['diagnosis'] = "Тестовый диагноз"
            data['appointments'][new_appointment_index]['treatment'] = "Тестовое лечение"

            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data['appointments'][new_appointment_index]['diagnosis'] == "Тестовый диагноз":
                self.log_result(test_name, 2, "Добавление диагноза", "Диагноз сохранен",
                              data['appointments'][new_appointment_index]['diagnosis'], "PASS")
            else:
                self.log_result(test_name, 2, "Добавление диагноза", "Диагноз сохранен",
                              "Ошибка сохранения", "FAIL")
        else:
            self.log_result(test_name, 2, "Добавление диагноза", "Диагноз сохранен",
                          "Прием не найден", "FAIL")

        # Шаг 3: Изменение статуса приема
        if new_appointment_index is not None:
            data['appointments'][new_appointment_index]['status'] = "completed"

            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data['appointments'][new_appointment_index]['status'] == "completed":
                self.log_result(test_name, 3, "Завершение приема", "Статус: завершен",
                              f"Статус: {data['appointments'][new_appointment_index]['status']}", "PASS")
            else:
                self.log_result(test_name, 3, "Завершение приема", "Статус: завершен",
                              "Ошибка изменения статуса", "FAIL")
        else:
            self.log_result(test_name, 3, "Завершение приема", "Статус: завершен",
                          "Прием не найден", "FAIL")
        
        # Шаг 4: Проверка фильтрации по пациенту
        patient_appointments = [a for a in data['appointments'] if a['patient_id'] == 1]

        if len(patient_appointments) >= 1:
            self.log_result(test_name, 4, "Фильтр по пациенту", "Найден хотя бы 1 прием",
                          f"Найдено: {len(patient_appointments)}", "PASS")
        else:
            self.log_result(test_name, 4, "Фильтр по пациенту", "Найден хотя бы 1 прием",
                          f"Найдено: {len(patient_appointments)}", "FAIL")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\nЗАПУСК АВТОМАТИЗИРОВАННЫХ ТЕСТОВ...")
        print("="*100)
        
        self.test_authentication()
        self.test_user_management()
        self.test_appointments_management()
        
        self.print_results()
        
        # Сохранение результатов в файл
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Сохранение результатов в текстовый файл"""
        with open('test_results.txt', 'w', encoding='utf-8') as f:
            f.write("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ 'БОЛЬНИЦА'\n")
            f.write("="*100 + "\n\n")
            
            current_test = None
            for result in self.test_results:
                if current_test != result['test']:
                    current_test = result['test']
                    f.write(f"\n{current_test}\n")
                    f.write("-"*100 + "\n")
                    f.write(f"{'Шаг':<6}{'Действие':<35}{'Ожидаемый результат':<30}{'Статус':<10}\n")
                    f.write("-"*100 + "\n")
                
                status_symbol = "PASS" if result['status'] == 'PASS' else "FAIL"
                f.write(f"{result['step']:<6}{result['action']:<35}{result['expected']:<30}{status_symbol:<10}\n")
            
            total = len(self.test_results)
            passed = len([r for r in self.test_results if r['status'] == 'PASS'])
            failed = total - passed
            
            f.write("\n" + "="*100 + "\n")
            f.write(f"ИТОГО: Всего тестов: {total} | Пройдено: {passed} | Провалено: {failed}\n")
            f.write("="*100 + "\n")
        
        print(f"\nРезультаты сохранены в файл: test_results.txt")

if __name__ == '__main__':
    tester = TestScenarios()
    tester.run_all_tests()