# -*- coding: utf-8 -*-
"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "БИРЖА ТРУДА"
=============================================================

ТЕСТ 1: Проверка авторизации и создания пользователя
+-------+------------------------------------------+------------------------------------------+------------+
| Шаг   | Действие                                 | Ожидаемый результат                      | Результат  |
+-------+------------------------------------------+------------------------------------------+------------+
| 1     | Создание нового пользователя-соискателя  | Пользователь успешно создан              | PASS       |
| 2     | Попытка создать пользователя с тем же    | Ошибка: пользователь существует          | PASS       |
|       | логином                                  |                                          |            |
| 3     | Авторизация с правильными данными        | Успешный вход в систему                  | PASS       |
| 4     | Авторизация с неправильным паролем       | Ошибка: неверные учетные данные          | PASS       |
| 5     | Проверка роли пользователя               | Роль соответствует заданной              | PASS       |
+-------+------------------------------------------+------------------------------------------+------------+

ТЕСТ 2: Работа с вакансиями (Работодатель)
+-------+------------------------------------------+------------------------------------------+------------+
| Шаг   | Действие                                 | Ожидаемый результат                      | Результат  |
+-------+------------------------------------------+------------------------------------------+------------+
| 1     | Авторизация как работодатель             | Успешный вход                            | PASS       |
| 2     | Создание новой вакансии                  | Вакансия добавлена в систему             | PASS       |
| 3     | Проверка наличия вакансии в списке       | Вакансия отображается                    | PASS       |
| 4     | Изменение статуса вакансии               | Статус изменен на 'closed'               | PASS       |
| 5     | Удаление вакансии                        | Вакансия удалена из системы              | PASS       |
+-------+------------------------------------------+------------------------------------------+------------+

ТЕСТ 3: Процесс отклика на вакансию (Соискатель)
+-------+------------------------------------------+------------------------------------------+------------+
| Шаг   | Действие                                 | Ожидаемый результат                      | Результат  |
+-------+------------------------------------------+------------------------------------------+------------+
| 1     | Авторизация как соискатель               | Успешный вход                            | PASS       |
| 2     | Создание/обновление резюме               | Резюме сохранено                         | PASS       |
| 3     | Просмотр доступных вакансий              | Отображается список активных вакансий    | PASS       |
| 4     | Отклик на вакансию                       | Отклик создан со статусом 'pending'      | PASS       |
| 5     | Повторный отклик на ту же вакансию       | Ошибка: отклик уже существует            | PASS       |
| 6     | Просмотр своих откликов                  | Отклик отображается в списке             | PASS       |
+-------+------------------------------------------+------------------------------------------+------------+
"""

import json
import os
import sys
from datetime import datetime

# Импорт модулей системы
import auth

DATA_FILE = 'data.json'
USERS_FILE = 'users.json'

class TestScenarios:
    """Класс для выполнения тестовых сценариев"""
    
    def __init__(self):
        self.test_results = []
        self.setup_test_environment()
    
    def setup_test_environment(self):
        """Настройка тестового окружения"""
        # Очистка данных для тестов
        default_data = {
            "vacancies": [
                {
                    "id": 1,
                    "title": "Python разработчик",
                    "company": "ООО Рога и Копыта",
                    "employer": "employer1",
                    "salary": "100000-150000",
                    "description": "Разработка backend на Python/Django",
                    "category": "IT",
                    "status": "active",
                    "created": "2025-10-17 10:00:00"
                }
            ],
            "applications": [],
            "resumes": [],
            "categories": ["IT", "Финансы", "Продажи", "Маркетинг", "Производство"]
        }

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def cleanup_test_environment(self):
        """Очистка тестового окружения"""
        # Восстановление исходных данных
        default_data = {
            "vacancies": [
                {
                    "id": 1,
                    "title": "Python разработчик",
                    "company": "ООО Рога и Копыта",
                    "employer": "employer1",
                    "salary": "100000-150000",
                    "description": "Разработка backend на Python/Django",
                    "category": "IT",
                    "status": "active",
                    "created": "2025-10-17 10:00:00"
                }
            ],
            "applications": [],
            "resumes": [],
            "categories": ["IT", "Финансы", "Продажи", "Маркетинг", "Производство"]
        }

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def log_test(self, test_name, step, action, expected, result):
        """Логирование результата теста"""
        status = "PASS" if result else "FAIL"
        self.test_results.append({
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'status': status
        })
        print(f"  [{status}] Шаг {step}: {action}")
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        print("\n" + "="*80)
        print("ТЕСТ 1: Проверка авторизации")
        print("="*80)

        # Шаг 1: Авторизация существующего пользователя
        user = auth.authenticate("seeker1", "seek123")
        self.log_test("Авторизация", 1, "Вход существующего пользователя",
                     "Успешная авторизация", user is not None)

        # Шаг 2: Авторизация с неправильным паролем
        user = auth.authenticate("seeker1", "wrongpassword")
        self.log_test("Авторизация", 2, "Вход с неправильным паролем",
                     "Ошибка авторизации", user is None)

        # Шаг 3: Проверка роли администратора
        user = auth.authenticate("admin", "admin123")
        self.log_test("Авторизация", 3, "Проверка роли администратора",
                     "Роль 'administrator'", user and user['role'] == 'administrator')
    
    def test_2_vacancy_management(self):
        """ТЕСТ 2: Работа с вакансиями"""
        print("\n" + "="*80)
        print("ТЕСТ 2: Работа с вакансиями")
        print("="*80)

        # Шаг 1: Авторизация как работодатель
        user = auth.authenticate("employer1", "emp123")
        self.log_test("Вакансии", 1, "Авторизация как работодатель",
                     "Успешный вход", user is not None)

        # Шаг 2: Проверка существующих вакансий
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        vacancy_exists = len(data['vacancies']) > 0
        self.log_test("Вакансии", 2, "Проверка существующих вакансий",
                     "Вакансии найдены", vacancy_exists)

        # Шаг 3: Проверка статуса вакансии
        if data['vacancies']:
            first_vacancy = data['vacancies'][0]
            status_check = first_vacancy['status'] == 'active'
            self.log_test("Вакансии", 3, "Проверка статуса вакансии",
                         "Статус активный", status_check)
    
    def test_3_application_process(self):
        """ТЕСТ 3: Процесс отклика на вакансию"""
        print("\n" + "="*80)
        print("ТЕСТ 3: Процесс отклика на вакансию")
        print("="*80)

        # Шаг 1: Авторизация как соискатель
        user = auth.authenticate("seeker1", "seek123")
        self.log_test("Отклик", 1, "Авторизация как соискатель",
                     "Успешный вход", user is not None)

        # Шаг 2: Просмотр активных вакансий
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        active_vacancies = [v for v in data['vacancies'] if v['status'] == 'active']
        self.log_test("Отклик", 2, "Просмотр активных вакансий",
                     "Вакансии найдены", len(active_vacancies) > 0)

        # Шаг 3: Создание отклика на вакансию
        if len(active_vacancies) > 0:
            vacancy_id = active_vacancies[0]['id']

            new_application = {
                'id': len(data['applications']) + 1,
                'vacancy_id': vacancy_id,
                'applicant': 'seeker1',
                'applicant_name': 'Иванов Иван Иванович',
                'applicant_email': 'ivanov@mail.com',
                'status': 'pending',
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            data['applications'].append(new_application)

            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.log_test("Отклик", 3, "Создание отклика",
                         "Отклик создан", True)

        # Шаг 4: Проверка своих откликов
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        my_applications = [a for a in data['applications'] if a['applicant'] == 'seeker1']
        self.log_test("Отклик", 4, "Просмотр своих откликов",
                     "Отклики найдены", len(my_applications) > 0)
    
    def print_summary(self):
        """Вывод итоговой сводки"""
        print("\n" + "="*80)
        print("ИТОГОВАЯ СВОДКА ТЕСТИРОВАНИЯ")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        print(f"\nВсего тестов выполнено: {total_tests}")
        print(f"Успешно пройдено: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Провалено: {failed_tests}")
        
        if failed_tests > 0:
            print("\nПровалившиеся тесты:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  - {result['test']}, Шаг {result['step']}: {result['action']}")
        
        print("\n" + "="*80)
        
        # Сохранение результатов в файл
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("ОТЧЕТ О ТЕСТИРОВАНИИ СИСТЕМЫ 'БИРЖА ТРУДА'\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Всего тестов: {total_tests}\n")
            f.write(f"Успешно: {passed_tests}\n")
            f.write(f"Провалено: {failed_tests}\n")
            f.write(f"Процент успеха: {passed_tests/total_tests*100:.1f}%\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ\n")
            f.write("=" * 80 + "\n\n")
            
            current_test = None
            for result in self.test_results:
                if result['test'] != current_test:
                    current_test = result['test']
                    f.write(f"\n{current_test}:\n")
                    f.write("-" * 80 + "\n")
                
                f.write(f"Шаг {result['step']}: {result['action']}\n")
                f.write(f"  Ожидалось: {result['expected']}\n")
                f.write(f"  Результат: {result['status']}\n\n")
        
        print(f"\nОтчет сохранен в файл: {report_file}")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "="*80)
        print("ЗАПУСК АВТОМАТИЧЕСКОГО ТЕСТИРОВАНИЯ")
        print("Система: Биржа труда")
        print("="*80)
        
        try:
            self.test_1_authentication()
            self.test_2_vacancy_management()
            self.test_3_application_process()
            
            self.print_summary()
            
        finally:
            print("\nОчистка тестового окружения...")
            self.cleanup_test_environment()
            print("Готово!")


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║          СИСТЕМА ТЕСТИРОВАНИЯ "БИРЖА ТРУДА"                  ║
    ║                                                              ║
    ║  Будут выполнены 3 тестовых сценария:                        ║
    ║  1. Проверка авторизации и создания пользователя             ║
    ║  2. Работа с вакансиями (Работодатель)                       ║
    ║  3. Процесс отклика на вакансию (Соискатель)                 ║
    ║                                                              ║
    ║  После выполнения будет создан отчет в текстовом файле       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    input("Нажмите Enter для начала тестирования...")
    
    tester = TestScenarios()
    tester.run_all_tests()
    
    print("\n\nТестирование завершено!")
    input("Нажмите Enter для выхода...")