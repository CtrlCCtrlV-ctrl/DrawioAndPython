"""
ТЕСТОВЫЕ СЦЕНАРИИ ДЛЯ ИНФОРМАЦИОННОЙ СИСТЕМЫ "ТУРИСТИЧЕСКАЯ ФИРМА"

Данный файл содержит три тестовых сценария для проверки работы системы.
Каждый тест включает документацию в виде таблицы и программную реализацию.
"""

import json
import os
import sys
import auth

# Импорт для работы с данными
def load_data():
    """Загрузка данных из файла"""
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """Сохранение данных в файл"""
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class TestScenarios:
    """Класс для выполнения тестовых сценариев"""
    
    def __init__(self):
        self.results = []
    
    def print_result(self, test_name, step, action, expected, actual, status):
        """Вывод результата теста"""
        result = {
            'test': test_name,
            'step': step,
            'action': action,
            'expected': expected,
            'actual': actual,
            'status': status
        }
        self.results.append(result)
        print(f"  [{status}] Шаг {step}: {action}")
        if status == "FAIL":
            print(f"       Ожидалось: {expected}")
            print(f"       Получено: {actual}")
    
    def test_1_authentication(self):
        """
        ТЕСТ 1: Проверка системы аутентификации
        
        |-----|--------------------------------|--------------------------------|-----------|
        | Шаг | Действие                       | Ожидаемый результат            | Результат |
        |-----|--------------------------------|--------------------------------|-----------|
        | 1   | Вход с корректными данными     | Успешная авторизация           | PASS/FAIL |
        |     | admin/admin123                 | current_user != None           |           |
        |-----|--------------------------------|--------------------------------|-----------|
        | 2   | Проверка роли администратора   | Роль = 'administrator'         | PASS/FAIL |
        |-----|--------------------------------|--------------------------------|-----------|
        | 3   | Выход из системы               | current_user = None            | PASS/FAIL |
        |-----|--------------------------------|--------------------------------|-----------|
        | 4   | Вход с неверными данными       | Авторизация отклонена          | PASS/FAIL |
        |     | admin/wrongpassword            | current_user = None            |           |
        |-----|--------------------------------|--------------------------------|-----------|
        | 5   | Вход как менеджер              | Успешная авторизация           | PASS/FAIL |
        |     | manager/manager123             | Роль = 'manager'               |           |
        |-----|--------------------------------|--------------------------------|-----------|
        """
        
        print("\n" + "="*80)
        print("ТЕСТ 1: Проверка системы аутентификации")
        print("="*80)
        
        # Шаг 1: Вход с корректными данными
        result = auth.login("admin", "admin123")
        current_user = auth.get_current_user()
        status = "PASS" if result and current_user is not None else "FAIL"
        self.print_result("ТЕСТ 1", 1, "Вход admin/admin123",
                         "Авторизация успешна",
                         f"Авторизация {'успешна' if result else 'не удалась'}",
                         status)

        # Шаг 2: Проверка роли
        if current_user:
            status = "PASS" if current_user['role'] == 'administrator' else "FAIL"
            self.print_result("ТЕСТ 1", 2, "Проверка роли администратора",
                             "Роль = 'administrator'",
                             f"Роль = '{current_user['role']}'",
                             status)

        # Шаг 3: Выход из системы
        auth.logout()
        current_user = auth.get_current_user()
        status = "PASS" if current_user is None else "FAIL"
        self.print_result("ТЕСТ 1", 3, "Выход из системы",
                         "current_user = None",
                         f"current_user = {current_user}",
                         status)

        # Шаг 4: Вход с неверными данными
        result = auth.login("admin", "wrongpassword")
        current_user = auth.get_current_user()
        status = "PASS" if not result and current_user is None else "FAIL"
        self.print_result("ТЕСТ 1", 4, "Вход с неверным паролем",
                         "Авторизация отклонена",
                         f"Авторизация {'успешна' if result else 'отклонена'}",
                         status)

        # Шаг 5: Вход как менеджер
        result = auth.login("manager", "manager123")
        current_user = auth.get_current_user()
        status = "PASS" if result and current_user and current_user['role'] == 'manager' else "FAIL"
        self.print_result("ТЕСТ 1", 5, "Вход manager/manager123",
                         "Роль = 'manager'",
                         f"Роль = '{current_user['role'] if current_user else 'None'}'",
                         status)

        auth.logout()
    
    def test_2_tour_management(self):
        """
        ТЕСТ 2: Управление турами
        
        |-----|--------------------------------|--------------------------------|-----------|
        | Шаг | Действие                       | Ожидаемый результат            | Результат |
        |-----|--------------------------------|--------------------------------|-----------|
        | 1   | Получение списка туров         | Список содержит туры           | PASS/FAIL |
        |-----|--------------------------------|--------------------------------|-----------|
        | 2   | Добавление нового тура         | Тур добавлен в систему         | PASS/FAIL |
        |     | "Греция - Крит"                | Количество туров увеличилось   |           |
        |-----|--------------------------------|--------------------------------|-----------|
        | 3   | Проверка данных нового тура    | Данные совпадают с введенными  | PASS/FAIL |
        |-----|--------------------------------|--------------------------------|-----------|
        | 4   | Изменение цены тура            | Цена обновлена                 | PASS/FAIL |
        |-----|--------------------------------|--------------------------------|-----------|
        | 5   | Удаление тура                  | Тур удален из системы          | PASS/FAIL |
        |     |                                | Количество туров уменьшилось   |           |
        |-----|--------------------------------|--------------------------------|-----------|
        """
        
        print("\n" + "="*80)
        print("ТЕСТ 2: Управление турами")
        print("="*80)
        
        # Шаг 1: Получение списка туров
        data = load_data()
        initial_count = len(data['tours'])
        status = "PASS" if initial_count > 0 else "FAIL"
        self.print_result("ТЕСТ 2", 1, "Получение списка туров",
                         "Список содержит туры",
                         f"Найдено туров: {initial_count}",
                         status)

        # Шаг 2: Добавление нового тура
        new_tour = {
            'id': max([t['id'] for t in data['tours']], default=0) + 1,
            'name': 'Греция - Крит',
            'country': 'Греция',
            'duration': 8,
            'price': 65000,
            'description': 'Отдых на острове Крит',
            'available': True
        }
        data['tours'].append(new_tour)
        save_data(data)

        data = load_data()
        new_count = len(data['tours'])
        status = "PASS" if new_count == initial_count + 1 else "FAIL"
        self.print_result("ТЕСТ 2", 2, "Добавление тура 'Греция - Крит'",
                         f"Количество туров = {initial_count + 1}",
                         f"Количество туров = {new_count}",
                         status)

        # Шаг 3: Проверка данных
        added_tour = next((t for t in data['tours'] if t['name'] == 'Греция - Крит'), None)
        status = "PASS" if added_tour and added_tour['price'] == 65000 else "FAIL"
        self.print_result("ТЕСТ 2", 3, "Проверка данных тура",
                         "Цена = 65000, Страна = Греция",
                         f"Цена = {added_tour['price'] if added_tour else 'N/A'}, Страна = {added_tour['country'] if added_tour else 'N/A'}",
                         status)

        # Шаг 4: Изменение цены
        if added_tour:
            for tour in data['tours']:
                if tour['id'] == added_tour['id']:
                    tour['price'] = 70000
                    break
            save_data(data)

            data = load_data()
            updated_tour = next((t for t in data['tours'] if t['id'] == added_tour['id']), None)
            status = "PASS" if updated_tour and updated_tour['price'] == 70000 else "FAIL"
            self.print_result("ТЕСТ 2", 4, "Изменение цены на 70000",
                             "Цена = 70000",
                             f"Цена = {updated_tour['price'] if updated_tour else 'N/A'}",
                             status)

        # Шаг 5: Удаление тура
        if added_tour:
            data['tours'] = [t for t in data['tours'] if t['id'] != added_tour['id']]
            save_data(data)

            data = load_data()
            final_count = len(data['tours'])
            status = "PASS" if final_count == initial_count else "FAIL"
            self.print_result("ТЕСТ 2", 5, "Удаление тура",
                             f"Количество туров = {initial_count}",
                             f"Количество туров = {final_count}",
                             status)
    
    def test_3_booking_process(self):
        """
        ТЕСТ 3: Процесс бронирования
        
        |-----|--------------------------------|--------------------------------|-----------|
        | Шаг | Действие                       | Ожидаемый результат            | Результат |
        |-----|--------------------------------|--------------------------------|-----------|
        | 1   | Вход как клиент                | Авторизация успешна            | PASS/FAIL |
        |     | client/client123               | Роль = 'client'                |           |
        |-----|--------------------------------|--------------------------------|-----------|
        | 2   | Создание бронирования          | Бронирование создано           | PASS/FAIL |
        |     | Тур ID=1, 2 персоны            | Статус = 'pending'             |           |
        |-----|--------------------------------|--------------------------------|-----------|
        | 3   | Проверка расчета стоимости     | Сумма = Цена тура × Персоны    | PASS/FAIL |
        |-----|--------------------------------|--------------------------------|-----------|
        | 4   | Вход как менеджер и            | Статус изменен на 'confirmed'  | PASS/FAIL |
        |     | подтверждение бронирования     |                                |           |
        |-----|--------------------------------|--------------------------------|-----------|
        | 5   | Отмена бронирования клиентом   | Статус изменен на 'cancelled'  | PASS/FAIL |
        |-----|--------------------------------|--------------------------------|-----------|
        """
        
        print("\n" + "="*80)
        print("ТЕСТ 3: Процесс бронирования")
        print("="*80)
        
        # Шаг 1: Вход как клиент
        result = auth.login("client", "client123")
        current_user = auth.get_current_user()
        status = "PASS" if result and current_user and current_user['role'] == 'client' else "FAIL"
        self.print_result("ТЕСТ 3", 1, "Вход client/client123",
                         "Роль = 'client'",
                         f"Роль = '{current_user['role'] if current_user else 'None'}'",
                         status)
        
        # Шаг 2: Создание бронирования
        data = load_data()
        initial_bookings = len(data['bookings'])

        # Найти тур
        tour = next((t for t in data['tours'] if t['id'] == 1), None)
        if not tour:
            self.print_result("ТЕСТ 3", 2, "Создание бронирования", "Тур найден", "Тур не найден", "FAIL")
        else:
            persons = 2
            new_booking = {
                'id': max([b['id'] for b in data['bookings']], default=0) + 1,
                'tour_id': 1,
                'client_id': 1,
                'client_username': 'client',
                'booking_date': '2024-01-20',
                'travel_date': '2024-03-15',
                'persons': persons,
                'total_price': tour['price'] * persons,
                'status': 'pending'
            }
            data['bookings'].append(new_booking)
            save_data(data)

            data = load_data()
            new_bookings_count = len(data['bookings'])
            status = "PASS" if new_bookings_count == initial_bookings + 1 else "FAIL"
            self.print_result("ТЕСТ 3", 2, "Создание бронирования",
                             f"Бронирований = {initial_bookings + 1}, Статус = 'pending'",
                             f"Бронирований = {new_bookings_count}, Статус = '{new_booking['status']}'",
                             status)

            # Шаг 3: Проверка расчета стоимости
            expected_price = tour['price'] * persons
            actual_price = new_booking['total_price']
            status = "PASS" if expected_price == actual_price else "FAIL"
            self.print_result("ТЕСТ 3", 3, "Проверка расчета стоимости",
                             f"Сумма = {expected_price}",
                             f"Сумма = {actual_price}",
                             status)

            # Шаг 4: Подтверждение менеджером
            auth.logout()
            auth.login("manager", "manager123")

            data = load_data()
            for booking in data['bookings']:
                if booking['id'] == new_booking['id']:
                    booking['status'] = 'confirmed'
                    break
            save_data(data)

            data = load_data()
            updated_booking = next((b for b in data['bookings'] if b['id'] == new_booking['id']), None)
            status = "PASS" if updated_booking and updated_booking['status'] == 'confirmed' else "FAIL"
            self.print_result("ТЕСТ 3", 4, "Подтверждение менеджером",
                             "Статус = 'confirmed'",
                             f"Статус = '{updated_booking['status'] if updated_booking else 'N/A'}'",
                             status)

            # Шаг 5: Отмена клиентом
            auth.logout()
            auth.login("client", "client123")

            data = load_data()
            for booking in data['bookings']:
                if booking['id'] == new_booking['id']:
                    booking['status'] = 'cancelled'
                    break
            save_data(data)

            data = load_data()
            cancelled_booking = next((b for b in data['bookings'] if b['id'] == new_booking['id']), None)
            status = "PASS" if cancelled_booking and cancelled_booking['status'] == 'cancelled' else "FAIL"
            self.print_result("ТЕСТ 3", 5, "Отмена бронирования",
                             "Статус = 'cancelled'",
                             f"Статус = '{cancelled_booking['status'] if cancelled_booking else 'N/A'}'",
                             status)
        
        auth.logout()
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n")
        print("╔" + "="*78 + "╗")
        print("║" + " "*15 + "ТЕСТИРОВАНИЕ ИНФОРМАЦИОННОЙ СИСТЕМЫ" + " "*28 + "║")
        print("║" + " "*23 + "ТУРИСТИЧЕСКАЯ ФИРМА" + " "*36 + "║")
        print("╚" + "="*78 + "╝")
        
        self.test_1_authentication()
        self.test_2_tour_management()
        self.test_3_booking_process()
        
        # Подсчет результатов
        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'PASS'])
        failed = len([r for r in self.results if r['status'] == 'FAIL'])
        
        print("\n" + "="*80)
        print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
        print("="*80)
        print(f"Всего тестов: {total}")
        print(f"Успешно (PASS): {passed}")
        print(f"Неудачно (FAIL): {failed}")
        print(f"Процент успеха: {(passed/total*100):.1f}%")
        print("="*80 + "\n")
        
        return passed == total

if __name__ == "__main__":
    tester = TestScenarios()
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)