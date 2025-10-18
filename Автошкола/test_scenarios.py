"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "АВТОШКОЛА"

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 1: Проверка авторизации пользователей
═══════════════════════════════════════════════════════════════════════════════
|-------|---------------------------|------------------------------|-----------|
| Шаг   | Действие                  | Ожидаемый результат          | Результат |
|-------|---------------------------|------------------------------|-----------|
| 1     | Создать AuthManager       | Файл users.json создан       | PASS      |
| 2     | Войти: admin/admin123     | Авторизация успешна          | PASS      |
| 3     | Проверить роль admin      | Роль = administrator         | PASS      |
| 4     | Войти: admin/wrongpass    | Авторизация неуспешна        | PASS      |
| 5     | Войти: wronguser/wrongpass| Авторизация неуспешна        | PASS      |
|-------|---------------------------|------------------------------|-----------|

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 2: Управление пользователями (CRUD операции)
═══════════════════════════════════════════════════════════════════════════════
|-------|---------------------------|------------------------------|-----------|
| Шаг   | Действие                  | Ожидаемый результат          | Результат |
|-------|---------------------------|------------------------------|-----------|
| 1     | Создать пользователя      | Пользователь добавлен        | PASS      |
|       | test_user/pass123         |                              |           |
| 2     | Получить всех             | test_user в списке           | PASS      |
|       | пользователей             |                              |           |
| 3     | Создать дубликат          | Ошибка: пользователь         | PASS      |
|       | test_user                 | существует                   |           |
| 4     | Удалить test_user         | Пользователь удален          | PASS      |
| 5     | Проверить удаление        | test_user отсутствует        | PASS      |
|-------|---------------------------|------------------------------|-----------|

═══════════════════════════════════════════════════════════════════════════════
ТЕСТ 3: Работа с данными (студенты, инструкторы, занятия)
═══════════════════════════════════════════════════════════════════════════════
|-------|---------------------------|------------------------------|-----------|
| Шаг   | Действие                  | Ожидаемый результат          | Результат |
|-------|---------------------------|------------------------------|-----------|
| 1     | Загрузить data.json       | Файл успешно загружен        | PASS      |
| 2     | Проверить наличие         | Минимум 1 студент            | PASS      |
|       | студентов                 |                              |           |
| 3     | Проверить наличие         | Минимум 1 инструктор         | PASS      |
|       | инструкторов              |                              |           |
| 4     | Проверить структуру       | Ключи: students, instructors,| PASS      |
|       | данных                    | cars, lessons, grades        |           |
| 5     | Добавить тестовое         | Занятие добавлено            | PASS      |
|       | занятие                   |                              |           |
|-------|---------------------------|------------------------------|-----------|
"""

import json
import os
import sys
from datetime import datetime
from auth import AuthManager

class TestScenarios:
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def test_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        print("\n" + "="*80)
        print("ТЕСТ 1: Проверка авторизации пользователей")
        print("="*80)
        
        try:
            # Шаг 1: Создать AuthManager
            auth = AuthManager()
            print("PASS Шаг 1: AuthManager создан")
            self.passed += 1
            
            # Шаг 2: Войти с правильными данными
            if auth.authenticate('admin', 'admin123'):
                print("PASS Шаг 2: Авторизация admin/admin123 успешна - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 2: Авторизация admin/admin123 неуспешна - FAIL")
                self.failed += 1
            
            # Шаг 3: Проверить роль
            if auth.current_user and auth.current_user['role'] == 'administrator':
                print("PASS Шаг 3: Роль = administrator - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 3: Роль НЕ administrator - FAIL")
                self.failed += 1
            
            # Шаг 4: Войти с неправильным паролем
            if not auth.authenticate('admin', 'wrongpass'):
                print("PASS Шаг 4: Авторизация admin/wrongpass неуспешна - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 4: Авторизация admin/wrongpass успешна (ошибка!) - FAIL")
                self.failed += 1
            
            # Шаг 5: Войти с несуществующим пользователем
            if not auth.authenticate('wronguser', 'wrongpass'):
                print("PASS Шаг 5: Авторизация wronguser/wrongpass неуспешна - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 5: Авторизация wronguser/wrongpass успешна (ошибка!) - FAIL")
                self.failed += 1
            
        except Exception as e:
            print(f"FAIL ТЕСТ 1 ПРОВАЛЕН с ошибкой: {e}")
            self.failed += 5
    
    def test_user_management(self):
        """ТЕСТ 2: Управление пользователями"""
        print("\n" + "="*80)
        print("ТЕСТ 2: Управление пользователями (CRUD операции)")
        print("="*80)
        
        try:
            auth = AuthManager()

            # Шаг 1: Создать пользователя
            if auth.create_user('test_user', 'pass123', 'student', 'Тестовый Пользователь'):
                print("PASS Шаг 1: Пользователь test_user создан - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 1: Пользователь test_user НЕ создан - FAIL")
                self.failed += 1

            # Шаг 2: Получить всех пользователей
            users = auth.get_all_users()
            if any(u['username'] == 'test_user' for u in users):
                print("PASS Шаг 2: test_user найден в списке пользователей - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 2: test_user НЕ найден в списке - FAIL")
                self.failed += 1

            # Шаг 3: Попытка создать дубликат
            if not auth.create_user('test_user', 'pass456', 'student', 'Дубликат'):
                print("PASS Шаг 3: Дубликат test_user НЕ создан (правильно) - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 3: Дубликат test_user создан (ошибка!) - FAIL")
                self.failed += 1

            # Шаг 4: Удалить пользователя
            auth.delete_user('test_user')
            print("PASS Шаг 4: Удаление test_user выполнено - PASS")
            self.passed += 1

            # Шаг 5: Проверить удаление
            users = auth.get_all_users()
            if not any(u['username'] == 'test_user' for u in users):
                print("PASS Шаг 5: test_user отсутствует в списке - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 5: test_user все еще в списке - FAIL")
                self.failed += 1
            
        except Exception as e:
            print(f"FAIL ТЕСТ 2 ПРОВАЛЕН с ошибкой: {e}")
            self.failed += 5
    
    def test_data_operations(self):
        """ТЕСТ 3: Работа с данными"""
        print("\n" + "="*80)
        print("ТЕСТ 3: Работа с данными (студенты, инструкторы, занятия)")
        print("="*80)
        
        try:
            # Шаг 1: Загрузить данные из существующего файла
            try:
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print("PASS Шаг 1: Файл data.json загружен - PASS")
                self.passed += 1
            except FileNotFoundError:
                print("FAIL Шаг 1: Файл data.json НЕ найден - FAIL")
                self.failed += 1
                return

            # Шаг 2: Загрузить и проверить студентов
            if len(data['students']) >= 1:
                print("PASS Шаг 2: Найден минимум 1 студент - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 2: Студенты НЕ найдены - FAIL")
                self.failed += 1

            # Шаг 3: Проверить инструкторов
            if len(data['instructors']) >= 1:
                print("PASS Шаг 3: Найден минимум 1 инструктор - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 3: Инструкторы НЕ найдены - FAIL")
                self.failed += 1

            # Шаг 4: Проверить структуру
            required_keys = {'students', 'instructors', 'cars', 'lessons', 'grades'}
            if required_keys.issubset(data.keys()):
                print("PASS Шаг 4: Структура данных корректна - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 4: Структура данных НЕкорректна - FAIL")
                self.failed += 1

            # Шаг 5: Добавить занятие
            new_lesson = {
                "id": max([l['id'] for l in data['lessons']], default=0) + 1,
                "student": "Тестовый Студент",
                "instructor": "Тестовый Инструктор",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "10:00",
                "type": "Практика",
                "status": "Запланировано"
            }
            data['lessons'].append(new_lesson)

            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            if len(data['lessons']) >= 1:
                print("PASS Шаг 5: Тестовое занятие добавлено - PASS")
                self.passed += 1
            else:
                print("FAIL Шаг 5: Занятие НЕ добавлено - FAIL")
                self.failed += 1
            
        except Exception as e:
            print(f"FAIL ТЕСТ 3 ПРОВАЛЕН с ошибкой: {e}")
            self.failed += 5
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n")
        print("="*80)
        print("ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ")
        print("Информационная система 'Автошкола'")
        print("="*80)
        
        self.test_authentication()
        self.test_user_management()
        self.test_data_operations()

        # Итоги
        print("\n" + "="*80)
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("="*80)
        print(f"PASS Пройдено тестов: {self.passed}")
        print(f"FAIL Провалено тестов: {self.failed}")
        print(f"Всего тестов: {self.passed + self.failed}")

        success_rate = (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0
        print(f"Процент успеха: {success_rate:.1f}%")
        print("="*80)

        if self.failed == 0:
            print("\nPASSPASSPASS ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО PASSPASSPASS\n")
        else:
            print(f"\nFAILFAILFAIL ОБНАРУЖЕНО {self.failed} ОШИБОК FAILFAILFAIL\n")
        
        return self.failed == 0

if __name__ == "__main__":
    tester = TestScenarios()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)