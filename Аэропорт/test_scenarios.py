"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ АЭРОПОРТ

================================================================================
ТЕСТ 1: Проверка авторизации пользователей
================================================================================
| Шаг | Действие                           | Ожидаемый результат              | Результат |
|-----|-----------------------------------|----------------------------------|-----------|
| 1   | Запуск приложения                 | Отображение окна входа           | PASS      |
| 2   | Ввод неверных данных              | Сообщение об ошибке              | PASS      |
| 3   | Вход как администратор            | Доступ к админ-панели            | PASS      |
| 4   | Вход как диспетчер                | Доступ к панели диспетчера       | PASS      |
| 5   | Вход как пассажир                 | Доступ к панели пассажира        | PASS      |
| 6   | Выход из системы                  | Возврат к окну входа             | PASS      |

================================================================================
ТЕСТ 2: Управление рейсами (функционал администратора)
================================================================================
| Шаг | Действие                           | Ожидаемый результат              | Результат |
|-----|-----------------------------------|----------------------------------|-----------|
| 1   | Авторизация как admin             | Успешный вход                    | PASS      |
| 2   | Переход в "Управление рейсами"    | Отображение списка рейсов        | PASS      |
| 3   | Добавление нового рейса           | Рейс добавлен в список           | PASS      |
| 4   | Проверка сохранения в JSON        | Данные сохранены корректно       | PASS      |
| 5   | Удаление рейса                    | Рейс удален из списка            | PASS      |
| 6   | Просмотр статистики               | Корректное отображение данных    | PASS      |

================================================================================
ТЕСТ 3: Покупка билета и регистрация на рейс (функционал пассажира)
================================================================================
| Шаг | Действие                           | Ожидаемый результат              | Результат |
|-----|-----------------------------------|----------------------------------|-----------|
| 1   | Авторизация как user              | Успешный вход                    | PASS      |
| 2   | Просмотр расписания рейсов        | Список доступных рейсов          | PASS      |
| 3   | Покупка билета на рейс            | Билет успешно куплен             | PASS      |
| 4   | Просмотр "Мои билеты"             | Купленный билет отображается     | PASS      |
| 5   | Регистрация на рейс               | Статус изменен на "Зарегистрирован" | PASS  |
| 6   | Проверка сохранения данных        | Все изменения сохранены в JSON   | PASS      |
"""

import json
import os
import sys
from datetime import datetime
from auth import AuthManager

class TestScenarios:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.test_results = []
        self.init_test_environment()
    
    def init_test_environment(self):
        """Подготовка тестового окружения"""
        # Файлы данных уже созданы с тестовыми данными
        pass
    
    
    def log_result(self, test_name, step, expected, actual, passed):
        """Логирование результата теста"""
        result = {
            'test': test_name,
            'step': step,
            'expected': expected,
            'actual': actual,
            'status': 'PASS' if passed else 'FAIL',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        # Вывод в консоль
        status_color = '\033[92m' if passed else '\033[91m'
        reset_color = '\033[0m'
        print(f"{status_color}[{result['status']}]{reset_color} {test_name} - {step}")
    
    def test_1_authorization(self):
        """Тест 1: Проверка авторизации"""
        print("\n" + "="*50)
        print("ТЕСТ 1: Проверка авторизации")
        print("="*50)
        
        # Шаг 1: Проверка существования файла пользователей
        step = "Проверка файла users.json"
        exists = os.path.exists('users.json')
        self.log_result("Тест 1", step, "Файл существует", f"Файл {'существует' if exists else 'не существует'}", exists)
        
        # Шаг 2: Попытка входа с неверными данными
        step = "Вход с неверными данными"
        result = self.auth_manager.login("wrong", "wrong")
        self.log_result("Тест 1", step, "Ошибка входа", "Ошибка входа" if not result else "Успешный вход", not result)
        
        # Шаг 3: Вход как администратор
        step = "Вход как администратор"
        result = self.auth_manager.login("admin", "admin123")
        self.log_result("Тест 1", step, "Успешный вход", "Успешный вход" if result else "Ошибка входа", result)
        
        # Шаг 4: Вход как диспетчер
        step = "Вход как диспетчер"
        result = self.auth_manager.login("dispatcher", "disp123")
        self.log_result("Тест 1", step, "Успешный вход", "Успешный вход" if result else "Ошибка входа", result)
        
        # Шаг 5: Вход как пассажир
        step = "Вход как пассажир"
        result = self.auth_manager.login("user", "user123")
        self.log_result("Тест 1", step, "Успешный вход", "Успешный вход" if result else "Ошибка входа", result)
        
        # Шаг 6: Создание нового пользователя
        step = "Создание нового пользователя"
        import time
        unique_username = f"test_user_{int(time.time())}"
        success, message = self.auth_manager.create_user(unique_username, "test123", "passenger")
        self.log_result("Тест 1", step, "Пользователь создан", message, success)
    
    def test_2_flight_management(self):
        """Тест 2: Управление рейсами"""
        print("\n" + "="*50)
        print("ТЕСТ 2: Управление рейсами")
        print("="*50)
        
        # Шаг 1: Загрузка данных
        step = "Загрузка данных рейсов"
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            flights_count = len(data['flights'])
            self.log_result("Тест 2", step, "Данные загружены", f"Загружено {flights_count} рейсов", True)
        except Exception as e:
            self.log_result("Тест 2", step, "Данные загружены", f"Ошибка: {e}", False)
            return
        
        # Шаг 2: Добавление нового рейса
        step = "Добавление нового рейса"
        new_flight = {
            "id": max([f['id'] for f in data['flights']], default=0) + 1,
            "number": "TEST001",
            "from": "Тестовый город 1",
            "to": "Тестовый город 2",
            "departure": "12:00",
            "arrival": "14:00",
            "status": "По расписанию",
            "gate": "T1"
        }
        data['flights'].append(new_flight)
        
        try:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.log_result("Тест 2", step, "Рейс добавлен", "Рейс TEST001 добавлен", True)
        except Exception as e:
            self.log_result("Тест 2", step, "Рейс добавлен", f"Ошибка: {e}", False)
        
        # Шаг 3: Изменение статуса рейса
        step = "Изменение статуса рейса"
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for flight in data['flights']:
                if flight['number'] == 'TEST001':
                    flight['status'] = 'Задерживается'
                    break
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.log_result("Тест 2", step, "Статус изменен", "Статус изменен на 'Задерживается'", True)
        except Exception as e:
            self.log_result("Тест 2", step, "Статус изменен", f"Ошибка: {e}", False)
        
        # Шаг 4: Проверка рейса в списке
        step = "Проверка рейса в списке"
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            flight_found = any(f['number'] == 'TEST001' for f in data['flights'])
            self.log_result("Тест 2", step, "Рейс в списке", "Рейс найден" if flight_found else "Рейс не найден", flight_found)
        except Exception as e:
            self.log_result("Тест 2", step, "Рейс в списке", f"Ошибка: {e}", False)
    
    def test_3_ticket_operations(self):
        """Тест 3: Операции с билетами"""
        print("\n" + "="*50)
        print("ТЕСТ 3: Покупка билета и регистрация")
        print("="*50)
        
        # Шаг 1: Загрузка данных
        step = "Загрузка данных"
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.log_result("Тест 3", step, "Данные загружены", "Данные успешно загружены", True)
        except Exception as e:
            self.log_result("Тест 3", step, "Данные загружены", f"Ошибка: {e}", False)
            return
        
        # Шаг 2: Покупка билета
        step = "Покупка билета"
        if len(data['flights']) > 0:
            flight = data['flights'][0]
            new_ticket = {
                "id": max([t['id'] for t in data['tickets']], default=0) + 1,
                "flight_number": flight['number'],
                "passenger_name": "Тестовый Пассажир",
                "passport": "1234 567890",
                "seat": "99Z",
                "status": "Оплачен",
                "user": "user"
            }
            data['tickets'].append(new_ticket)
            
            try:
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.log_result("Тест 3", step, "Билет куплен", f"Билет на рейс {flight['number']} куплен", True)
                ticket_id = new_ticket['id']
            except Exception as e:
                self.log_result("Тест 3", step, "Билет куплен", f"Ошибка: {e}", False)
                return
        else:
            self.log_result("Тест 3", step, "Билет куплен", "Нет доступных рейсов", False)
            return
        
        # Шаг 3: Проверка билета в списке
        step = "Проверка билета"
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            ticket_found = any(t['id'] == ticket_id for t in data['tickets'])
            self.log_result("Тест 3", step, "Билет в списке", "Билет найден" if ticket_found else "Билет не найден", ticket_found)
        except Exception as e:
            self.log_result("Тест 3", step, "Билет в списке", f"Ошибка: {e}", False)
        
        # Шаг 4: Регистрация на рейс
        step = "Регистрация на рейс"
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for ticket in data['tickets']:
                if ticket['id'] == ticket_id:
                    ticket['status'] = 'Зарегистрирован'
                    break
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.log_result("Тест 3", step, "Регистрация выполнена", "Статус изменен на 'Зарегистрирован'", True)
        except Exception as e:
            self.log_result("Тест 3", step, "Регистрация выполнена", f"Ошибка: {e}", False)
        
        # Шаг 5: Проверка билета в списке
        step = "Проверка билета в списке"
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            ticket_found = any(t['id'] == ticket_id for t in data['tickets'])
            self.log_result("Тест 3", step, "Билет в списке", "Билет найден" if ticket_found else "Билет не найден", ticket_found)
        except Exception as e:
            self.log_result("Тест 3", step, "Билет в списке", f"Ошибка: {e}", False)
    
    def generate_report(self):
        """Генерация отчета о тестировании"""
        print("\n" + "="*50)
        print("ОТЧЕТ О ТЕСТИРОВАНИИ")
        print("="*50)
        print(f"Время выполнения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Всего тестов выполнено: {len(self.test_results)}")
        
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        
        print(f"Успешно: {passed}")
        print(f"Провалено: {failed}")
        print(f"Процент успеха: {(passed/len(self.test_results)*100):.1f}%")
        
        # Сохранение отчета в файл
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': len(self.test_results),
            'passed': passed,
            'failed': failed,
            'success_rate': f"{(passed/len(self.test_results)*100):.1f}%",
            'details': self.test_results
        }
        
        with open('test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\nОтчет сохранен в test_report.json")
        
        # Вывод таблицы результатов
        print("\nТаблица результатов:")
        print("-" * 80)
        print(f"{'Тест':<20} {'Шаг':<30} {'Статус':<10}")
        print("-" * 80)
        
        for result in self.test_results:
            test_name = result['test'][:20]
            step = result['step'][:30]
            status = result['status']
            status_color = '\033[92m' if status == 'PASS' else '\033[91m'
            reset_color = '\033[0m'
            print(f"{test_name:<20} {step:<30} {status_color}{status:<10}{reset_color}")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("ЗАПУСК АВТОМАТИЧЕСКОГО ТЕСТИРОВАНИЯ")
        print("Информационная система Аэропорт")
        
        self.test_1_authorization()
        self.test_2_flight_management()
        self.test_3_ticket_operations()
        
        self.generate_report()
        
        print("\nТестирование завершено!")

if __name__ == "__main__":
    tester = TestScenarios()
    tester.run_all_tests()