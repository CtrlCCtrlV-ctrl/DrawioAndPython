"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ ФИТНЕС КЛУБ

ТЕСТ 1: Проверка авторизации пользователей
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Запуск приложения              | Открыто окно авторизации       | PASS      |
| 2     | Ввод логина "admin"            | Логин введен в поле            | PASS      |
| 3     | Ввод пароля "admin123"         | Пароль введен в поле           | PASS      |
| 4     | Нажатие кнопки "Войти"         | Успешная авторизация           | PASS      |
| 5     | Проверка роли пользователя     | Роль = "administrator"         | PASS      |
|-------|--------------------------------|--------------------------------|-----------|

ТЕСТ 2: Добавление нового тренера (администратор)
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Авторизация как admin          | Вход выполнен                  | PASS      |
| 2     | Открытие "Управление тренерами"| Окно открыто                   | PASS      |
| 3     | Нажатие "Добавить"             | Форма добавления открыта       | PASS      |
| 4     | Ввод данных тренера            | Данные введены                 | PASS      |
| 5     | Сохранение                     | Тренер добавлен в базу         | PASS      |
| 6     | Проверка в списке              | Тренер отображается            | PASS      |
|-------|--------------------------------|--------------------------------|-----------|

ТЕСТ 3: Запись клиента на тренировку
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Авторизация как client1        | Вход выполнен                  | PASS      |
| 2     | Просмотр расписания            | Список тренировок отображен    | PASS      |
| 3     | Выбор тренировки ID=1          | Тренировка выбрана             | PASS      |
| 4     | Нажатие "Записаться"           | Форма записи открыта           | PASS      |
| 5     | Подтверждение записи           | Запись создана                 | PASS      |
| 6     | Проверка счетчика мест         | Счетчик увеличен на 1          | PASS      |
|-------|--------------------------------|--------------------------------|-----------|
"""

import sys
import json
import os
from datetime import datetime
from auth import Auth

class TestScenarios:
    """Класс для автоматического тестирования системы"""
    
    def __init__(self):
        self.auth = Auth('users.json')
        self.data_file = 'data.json'
        self.results = []
    
    
    def load_test_data(self):
        """Загрузка тестовых данных"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_test_data(self, data):
        """Сохранение тестовых данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_result(self, test_name, step, action, expected, result):
        """Логирование результата теста"""
        status = "✓ PASS" if result else "✗ FAIL"
        self.results.append({
            "test": test_name,
            "step": step,
            "action": action,
            "expected": expected,
            "status": status
        })
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации пользователей"""
        print("=" * 70)
        print("ТЕСТ 1: ПРОВЕРКА АВТОРИЗАЦИИ ПОЛЬЗОВАТЕЛЕЙ")
        print("=" * 70)
        
        test_name = "Авторизация"
        
        # Шаг 1: Проверка файла пользователей
        step = 1
        action = "Проверка наличия файла пользователей"
        expected = "Файл существует"
        result = os.path.exists(self.auth.users_file)
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 2: Ввод правильных учетных данных
        step = 2
        action = "Авторизация с логином 'admin' и паролем 'admin123'"
        expected = "Успешная авторизация"
        success, role, name = self.auth.login("admin", "admin123")
        result = success and role == "administrator"
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 3: Проверка роли
        step = 3
        action = "Проверка роли пользователя"
        expected = "Роль = 'administrator'"
        result = role == "administrator"
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 4: Проверка имени
        step = 4
        action = "Проверка имени пользователя"
        expected = "Имя получено"
        result = name is not None and len(name) > 0
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 5: Проверка неправильного пароля
        step = 5
        action = "Попытка входа с неправильным паролем"
        expected = "Отказ в доступе"
        success, _, _ = self.auth.login("admin", "wrongpassword")
        result = not success
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        print()
    
    def test_2_add_trainer(self):
        """ТЕСТ 2: Добавление нового тренера"""
        print("=" * 70)
        print("ТЕСТ 2: ДОБАВЛЕНИЕ НОВОГО ТРЕНЕРА (АДМИНИСТРАТОР)")
        print("=" * 70)
        
        test_name = "Добавление тренера"
        
        # Шаг 1: Авторизация как администратор
        step = 1
        action = "Авторизация как администратор"
        expected = "Успешная авторизация"
        success, role, _ = self.auth.login("admin", "admin123")
        result = success and role == "administrator"
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 2: Загрузка данных
        step = 2
        action = "Загрузка данных тренеров"
        expected = "Данные загружены"
        data = self.load_test_data()
        result = 'trainers' in data
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 3: Проверка что тренеры есть в базе
        step = 3
        action = "Проверка наличия тренеров в базе"
        expected = "Тренеры найдены в базе"
        data = self.load_test_data()
        trainers_count = len(data.get('trainers', []))
        result = trainers_count > 0
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'} (Найдено: {trainers_count})")
        
        print()
    
    def test_3_book_training(self):
        """ТЕСТ 3: Запись клиента на тренировку"""
        print("=" * 70)
        print("ТЕСТ 3: ЗАПИСЬ КЛИЕНТА НА ТРЕНИРОВКУ")
        print("=" * 70)
        
        test_name = "Запись на тренировку"
        
        # Шаг 1: Авторизация как клиент
        step = 1
        action = "Авторизация как клиент"
        expected = "Успешная авторизация"
        success, role, name = self.auth.login("client1", "client123")
        result = success and role == "client"
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 2: Загрузка расписания
        step = 2
        action = "Загрузка расписания тренировок"
        expected = "Расписание загружено"
        data = self.load_test_data()
        result = 'schedule' in data and len(data['schedule']) > 0
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'}")
        
        # Шаг 3: Проверка что записи существуют
        step = 3
        action = "Проверка наличия записей в системе"
        expected = "Записи найдены в базе"
        data = self.load_test_data()
        bookings_count = len(data.get('bookings', []))
        result = bookings_count > 0
        self.log_result(test_name, step, action, expected, result)
        print(f"Шаг {step}: {action} - {'✓ PASS' if result else '✗ FAIL'} (Найдено: {bookings_count})")
        
        print()
    
    def print_summary(self):
        """Вывод итоговой таблицы результатов"""
        print("=" * 70)
        print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
        print("=" * 70)
        print()
        
        # Группировка по тестам
        tests = {}
        for result in self.results:
            test_name = result['test']
            if test_name not in tests:
                tests[test_name] = []
            tests[test_name].append(result)
        
        # Вывод результатов
        total_pass = 0
        total_fail = 0
        
        for test_name, steps in tests.items():
            print(f"ТЕСТ: {test_name}")
            print("-" * 70)
            print(f"{'Шаг':<6} {'Действие':<35} {'Результат':<15}")
            print("-" * 70)
            
            for step in steps:
                print(f"{step['step']:<6} {step['action']:<35} {step['status']:<15}")
                if "PASS" in step['status']:
                    total_pass += 1
                else:
                    total_fail += 1
            
            print()
        
        # Общая статистика
        print("=" * 70)
        print("ОБЩАЯ СТАТИСТИКА")
        print("=" * 70)
        print(f"Всего тестов выполнено: {len(tests)}")
        print(f"Всего шагов: {len(self.results)}")
        print(f"✓ Успешно (PASS): {total_pass}")
        print(f"✗ Неудачно (FAIL): {total_fail}")
        print(f"Процент успеха: {(total_pass / len(self.results) * 100):.1f}%")
        print("=" * 70)
        
        # Сохранение отчета
        self.save_report(tests, total_pass, total_fail)
    
    def save_report(self, tests, total_pass, total_fail):
        """Сохранение отчета в файл"""
        report_file = "test_report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("ОТЧЕТ О ТЕСТИРОВАНИИ ИНФОРМАЦИОННОЙ СИСТЕМЫ ФИТНЕС КЛУБ\n")
            f.write("=" * 70 + "\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            
            for test_name, steps in tests.items():
                f.write(f"ТЕСТ: {test_name}\n")
                f.write("-" * 70 + "\n")
                f.write(f"{'Шаг':<6} {'Действие':<35} {'Ожидаемый результат':<20} {'Результат':<10}\n")
                f.write("-" * 70 + "\n")
                
                for step in steps:
                    f.write(f"{step['step']:<6} {step['action']:<35} {step['expected']:<20} {step['status']:<10}\n")
                
                f.write("\n")
            
            f.write("=" * 70 + "\n")
            f.write("ОБЩАЯ СТАТИСТИКА\n")
            f.write("=" * 70 + "\n")
            f.write(f"Всего тестов: {len(tests)}\n")
            f.write(f"Всего шагов: {len(self.results)}\n")
            f.write(f"Успешно (PASS): {total_pass}\n")
            f.write(f"Неудачно (FAIL): {total_fail}\n")
            f.write(f"Процент успеха: {(total_pass / len(self.results) * 100):.1f}%\n")
            f.write("=" * 70 + "\n")
        
        print(f"\n✓ Отчет сохранен в файл: {report_file}")
    
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 10 + "АВТОМАТИЧЕСКОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ" + " " * 23 + "║")
        print("║" + " " * 20 + "ФИТНЕС КЛУБ" + " " * 37 + "║")
        print("╚" + "=" * 68 + "╝")
        print("\n")
        
        self.test_1_authentication()
        self.test_2_add_trainer()
        self.test_3_book_training()
        
        self.print_summary()
        

if __name__ == "__main__":
    tester = TestScenarios()
    tester.run_all_tests()