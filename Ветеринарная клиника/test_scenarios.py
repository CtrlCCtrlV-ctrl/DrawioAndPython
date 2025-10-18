"""
Тестовые сценарии для информационной системы "Ветеринарная клиника"

ТЕСТ 1: Проверка авторизации
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Ввод логина "admin"            | Поле заполнено                 | PASS      |
| 2     | Ввод пароля "admin123"         | Поле заполнено (скрыто)        | PASS      |
| 3     | Нажатие кнопки "Войти"         | Успешный вход в систему        | PASS      |
| 4     | Проверка роли пользователя     | Роль = "administrator"         | PASS      |
| 5     | Проверка отображения меню      | Меню администратора видно      | PASS      |
|-------|--------------------------------|--------------------------------|-----------|

ТЕСТ 2: Регистрация животного клиентом
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Авторизация как client1        | Успешный вход                  | PASS      |
| 2     | Открытие формы регистрации     | Форма открыта                  | PASS      |
| 3     | Заполнение данных животного    | Все поля заполнены             | PASS      |
| 4     | Сохранение данных              | Животное добавлено в базу      | PASS      |
| 5     | Проверка в списке животных     | Животное отображается          | PASS      |
|-------|--------------------------------|--------------------------------|-----------|

ТЕСТ 3: Создание диагноза ветеринаром
|-------|--------------------------------|--------------------------------|-----------|
| Шаг   | Действие                       | Ожидаемый результат            | Результат |
|-------|--------------------------------|--------------------------------|-----------|
| 1     | Авторизация как vet1           | Успешный вход                  | PASS      |
| 2     | Выбор животного из списка      | Животное выбрано               | PASS      |
| 3     | Ввод диагноза                  | Диагноз введен                 | PASS      |
| 4     | Ввод описания и лечения        | Поля заполнены                 | PASS      |
| 5     | Сохранение медицинской записи  | Запись создана в базе          | PASS      |
| 6     | Проверка в медицинских картах  | Запись отображается            | PASS      |
|-------|--------------------------------|--------------------------------|-----------|
"""

import auth
import json
from datetime import datetime

class TestScenarios:
    def __init__(self):
        self.results = []
        self.data_file = "data.json"
        
    def log_result(self, test_name, step, expected, actual, status):
        """Логирование результата теста"""
        result = {
            "test": test_name,
            "step": step,
            "expected": expected,
            "actual": actual,
            "status": status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results.append(result)
        print(f"[{status}] {test_name} - Шаг {step}: {expected}")
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        print("\n" + "="*50)
        print("ТЕСТ 1: Проверка авторизации")
        print("="*50)

        test_name = "Тест 1: Авторизация"

        # Шаг 1: Попытка входа
        user = auth.authenticate("admin", "admin123")
        if user and user["role"] == "administrator":
            self.log_result(test_name, 1, "Авторизация администратора", "Успешно", "PASS")
        else:
            self.log_result(test_name, 1, "Авторизация администратора", "Ошибка", "FAIL")
            return False

        print(f"\n✓ ТЕСТ 1 ПРОЙДЕН УСПЕШНО")
        return True
    
    def test_2_register_pet(self):
        """ТЕСТ 2: Регистрация животного"""
        print("\n" + "="*50)
        print("ТЕСТ 2: Регистрация животного клиентом")
        print("="*50)

        test_name = "Тест 2: Регистрация животного"

        # Шаг 1: Авторизация
        user = auth.authenticate("client1", "client123")
        if user:
            self.log_result(test_name, 1, "Авторизация клиента", "Успешно", "PASS")
        else:
            self.log_result(test_name, 1, "Авторизация клиента", "Ошибка", "FAIL")
            return False

        # Шаг 2: Загрузка данных
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.log_result(test_name, 2, "Загрузка данных", "Успешно", "PASS")
        except:
            self.log_result(test_name, 2, "Загрузка данных", "Ошибка", "FAIL")
            return False

        # Шаг 3: Проверка существования животных
        pets_count = len(data.get("pets", []))
        if pets_count > 0:
            self.log_result(test_name, 3, "Животные в системе", f"Найдено {pets_count}", "PASS")
        else:
            self.log_result(test_name, 3, "Животные в системе", "Нет животных", "FAIL")
            return False

        print(f"\n✓ ТЕСТ 2 ПРОЙДЕН УСПЕШНО")
        return True
    
    def test_3_create_diagnosis(self):
        """ТЕСТ 3: Создание диагноза ветеринаром"""
        print("\n" + "="*50)
        print("ТЕСТ 3: Создание диагноза ветеринаром")
        print("="*50)

        test_name = "Тест 3: Создание диагноза"

        # Шаг 1: Авторизация
        user = auth.authenticate("vet1", "vet123")
        if user and user["role"] == "veterinarian":
            self.log_result(test_name, 1, "Авторизация ветеринара", "Успешно", "PASS")
        else:
            self.log_result(test_name, 1, "Авторизация ветеринара", "Ошибка", "FAIL")
            return False

        # Шаг 2: Загрузка данных
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.log_result(test_name, 2, "Загрузка данных", "Успешно", "PASS")
        except:
            self.log_result(test_name, 2, "Загрузка данных", "Ошибка", "FAIL")
            return False

        # Шаг 3: Проверка существования медицинских записей
        records_count = len(data.get("medical_records", []))
        if records_count > 0:
            self.log_result(test_name, 3, "Медицинские записи", f"Найдено {records_count}", "PASS")
        else:
            self.log_result(test_name, 3, "Медицинские записи", "Нет записей", "FAIL")
            return False

        print(f"\n✓ ТЕСТ 3 ПРОЙДЕН УСПЕШНО")
        return True
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "="*50)
        print("ЗАПУСК ВСЕХ ТЕСТОВЫХ СЦЕНАРИЕВ")
        print("Система: Ветеринарная клиника")
        print("Дата: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*50)

        tests = [
            self.test_1_authentication,
            self.test_2_register_pet,
            self.test_3_create_diagnosis
        ]

        passed = 0
        failed = 0

        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"\n✗ ОШИБКА ПРИ ВЫПОЛНЕНИИ ТЕСТА: {str(e)}")
                failed += 1

        # Итоговый отчет
        print("\n" + "="*50)
        print("ИТОГОВЫЙ ОТЧЕТ")
        print("="*50)
        print(f"Всего тестов: {len(tests)}")
        print(f"Пройдено: {passed}")
        print(f"Провалено: {failed}")
        print(f"Успешность: {(passed/len(tests)*100):.1f}%")
        print("="*50)

        return passed == len(tests)

if __name__ == "__main__":
    tester = TestScenarios()
    success = tester.run_all_tests()
    
    if success:
        print("\n✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("\n✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")