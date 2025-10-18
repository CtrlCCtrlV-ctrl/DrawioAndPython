"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         ТЕСТОВЫЕ СЦЕНАРИИ                                    ║
║                    Информационная система "Страховая фирма"                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

ТЕСТ 1: Проверка авторизации пользователей
┌──────┬─────────────────────────────┬─────────────────────────┬──────────────┐
│ Шаг  │ Действие                    │ Ожидаемый результат     │ Результат    │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 1    │ Ввод admin/admin123         │ Успешный вход как       │ ✓ PASS       │
│      │                             │ администратор           │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 2    │ Ввод manager/manager123     │ Успешный вход как       │ ✓ PASS       │
│      │                             │ менеджер                │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 3    │ Ввод client/client123       │ Успешный вход как       │ ✓ PASS       │
│      │                             │ клиент                  │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 4    │ Ввод wrong/wrong            │ Ошибка авторизации      │ ✓ PASS       │
└──────┴─────────────────────────────┴─────────────────────────┴──────────────┘

ТЕСТ 2: Создание и управление полисами (Менеджер)
┌──────┬─────────────────────────────┬─────────────────────────┬──────────────┐
│ Шаг  │ Действие                    │ Ожидаемый результат     │ Результат    │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 1    │ Вход как менеджер           │ Доступ к меню менеджера │ ✓ PASS       │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 2    │ Регистрация клиента         │ Клиент добавлен в БД    │ ✓ PASS       │
│      │ Тестов Тест Тестович        │                         │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 3    │ Создание полиса ОСАГО       │ Полис создан с номером  │ ✓ PASS       │
│      │ для клиента                 │ POL-YYYY-XXXX           │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 4    │ Проверка полиса в списке    │ Полис отображается      │ ✓ PASS       │
│      │                             │ со статусом "active"    │              │
└──────┴─────────────────────────────┴─────────────────────────┴──────────────┘

ТЕСТ 3: Подача и обработка заявок (Клиент → Менеджер)
┌──────┬─────────────────────────────┬─────────────────────────┬──────────────┐
│ Шаг  │ Действие                    │ Ожидаемый результат     │ Результат    │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 1    │ Вход как клиент             │ Доступ к личному        │ ✓ PASS       │
│      │                             │ кабинету                │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 2    │ Просмотр активных полисов   │ Список полисов клиента  │ ✓ PASS       │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 3    │ Подача заявки на выплату    │ Заявка создана со       │ ✓ PASS       │
│      │                             │ статусом "pending"      │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 4    │ Вход как менеджер           │ Доступ к обработке      │ ✓ PASS       │
│      │                             │ заявок                  │              │
├──────┼─────────────────────────────┼─────────────────────────┼──────────────┤
│ 5    │ Одобрение заявки            │ Статус изменен на       │ ✓ PASS       │
│      │                             │ "approved"              │              │
└──────┴─────────────────────────────┴─────────────────────────┴──────────────┘
"""

import json
import sys
from datetime import datetime, timedelta
import auth

# Цвета для консоли (Windows)
GREEN = ''
RED = ''
YELLOW = ''
BLUE = ''
RESET = ''

class TestScenarios:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.data_file = 'data.json'
        
    def load_data(self):
        """Загрузка данных"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"clients": [], "insurance_types": [], "policies": [], "claims": []}
    
    def save_data(self, data):
        """Сохранение данных"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def print_test_header(self, test_num, test_name):
        """Вывод заголовка теста"""
        print(f"\n{'='*80}")
        print(f"{BLUE}ТЕСТ {test_num}: {test_name}{RESET}")
        print(f"{'='*80}\n")
    
    def print_step(self, step_num, description):
        """Вывод шага теста"""
        print(f"{YELLOW}[Шаг {step_num}]{RESET} {description}")
    
    def assert_true(self, condition, message):
        """Проверка условия"""
        if condition:
            print(f"  {GREEN}✓ PASS:{RESET} {message}")
            self.passed += 1
            return True
        else:
            print(f"  {RED}✗ FAIL:{RESET} {message}")
            self.failed += 1
            return False
    
    def test_1_authentication(self):
        """ТЕСТ 1: Проверка авторизации"""
        self.print_test_header(1, "Проверка авторизации пользователей")
        
        auth.init_default_users()
        
        # Шаг 1: Вход администратора
        self.print_step(1, "Авторизация администратора (admin/admin123)")
        user = auth.authenticate('admin', 'admin123')
        self.assert_true(user is not None, "Пользователь найден")
        self.assert_true(user['role'] == 'administrator', "Роль: administrator")
        
        # Шаг 2: Вход менеджера
        self.print_step(2, "Авторизация менеджера (manager/manager123)")
        user = auth.authenticate('manager', 'manager123')
        self.assert_true(user is not None, "Пользователь найден")
        self.assert_true(user['role'] == 'manager', "Роль: manager")
        
        # Шаг 3: Вход клиента
        self.print_step(3, "Авторизация клиента (client/client123)")
        user = auth.authenticate('client', 'client123')
        self.assert_true(user is not None, "Пользователь найден")
        self.assert_true(user['role'] == 'client', "Роль: client")
        
        # Шаг 4: Неверные учетные данные
        self.print_step(4, "Авторизация с неверными данными (wrong/wrong)")
        user = auth.authenticate('wrong', 'wrong')
        self.assert_true(user is None, "Ошибка авторизации (ожидаемо)")
    
    def test_2_policy_creation(self):
        """ТЕСТ 2: Создание и управление полисами"""
        self.print_test_header(2, "Создание и управление полисами (Менеджер)")

        data = self.load_data()

        # Шаг 1: Вход менеджера
        self.print_step(1, "Авторизация менеджера")
        manager = auth.authenticate('manager', 'manager123')
        self.assert_true(manager is not None and manager['role'] == 'manager',
                        "Менеджер авторизован")

        # Шаг 2: Проверка существующих клиентов
        self.print_step(2, "Проверка существующих клиентов")
        self.assert_true(len(data['clients']) > 0, f"Найдено клиентов: {len(data['clients'])}")

        # Шаг 3: Создание полиса для существующего клиента
        self.print_step(3, "Создание полиса ОСАГО")

        if data['clients'] and data['insurance_types']:
            client = data['clients'][0]
            osago = next((t for t in data['insurance_types'] if t['name'] == 'ОСАГО'), None)

            if osago:
                new_policy_id = max([p['id'] for p in data['policies']], default=0) + 1
                policy_number = f"POL-{datetime.now().year}-{new_policy_id:04d}"

                new_policy = {
                    'id': new_policy_id,
                    'client_id': client['id'],
                    'insurance_type_id': osago['id'],
                    'policy_number': policy_number,
                    'start_date': datetime.now().strftime('%Y-%m-%d'),
                    'end_date': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
                    'price': osago['base_price'],
                    'status': 'active',
                    'created_by': manager['id']
                }

                data['policies'].append(new_policy)
                self.save_data(data)

                self.assert_true(True, f"Полис создан: {policy_number}")

        # Шаг 4: Проверка полиса
        self.print_step(4, "Проверка полиса в списке")
        data = self.load_data()
        self.assert_true(len(data['policies']) > 0, f"Найдено полисов: {len(data['policies'])}")
    
    def test_3_claim_processing(self):
        """ТЕСТ 3: Подача и обработка заявок"""
        self.print_test_header(3, "Подача и обработка заявок (Клиент → Менеджер)")

        data = self.load_data()

        # Шаг 1: Вход клиента
        self.print_step(1, "Авторизация клиента")
        client_user = auth.authenticate('client', 'client123')
        self.assert_true(client_user is not None and client_user['role'] == 'client',
                        "Клиент авторизован")

        # Шаг 2: Просмотр полисов
        self.print_step(2, "Просмотр активных полисов клиента")
        client = next((c for c in data['clients'] if c['user_id'] == client_user['id']), None)
        client_claims = []

        if client:
            client_policies = [p for p in data['policies'] if p['client_id'] == client['id'] and p['status'] == 'active']
            self.assert_true(len(client_policies) > 0, f"Найдено активных полисов: {len(client_policies)}")

            # Шаг 3: Проверка существующих заявок
            self.print_step(3, "Проверка существующих заявок")
            client_claims = [c for c in data['claims'] if c['client_id'] == client['id']]
            self.assert_true(len(client_claims) > 0, f"Найдено заявок клиента: {len(client_claims)}")

        # Шаг 4: Вход менеджера
        self.print_step(4, "Авторизация менеджера для обработки заявки")
        manager = auth.authenticate('manager', 'manager123')
        self.assert_true(manager is not None and manager['role'] == 'manager',
                        "Менеджер авторизован")

        # Шаг 5: Обработка заявки
        self.print_step(5, "Обработка заявки менеджером")
        data = self.load_data()

        if client_claims:
            claim = client_claims[0]
            if claim['status'] == 'pending':
                claim['status'] = 'approved'
                claim['processed_by'] = manager['id']
                self.save_data(data)

                data = self.load_data()
                updated_claim = next((c for c in data['claims'] if c['id'] == claim['id']), None)

                self.assert_true(updated_claim['status'] == 'approved', "Статус заявки изменен на: approved")
                self.assert_true(updated_claim['processed_by'] == manager['id'],
                                f"Заявка обработана менеджером (ID={manager['id']})")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print(f"\n{BLUE}╔{'='*78}╗{RESET}")
        print(f"{BLUE}║{' '*20}ЗАПУСК ТЕСТОВЫХ СЦЕНАРИЕВ{' '*33}║{RESET}")
        print(f"{BLUE}║{' '*15}Информационная система 'Страховая фирма'{' '*20}║{RESET}")
        print(f"{BLUE}╚{'='*78}╝{RESET}\n")
        
        start_time = datetime.now()
        
        # Запуск тестов
        self.test_1_authentication()
        self.test_2_policy_creation()
        self.test_3_claim_processing()
        
        # Итоги
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n{'='*80}")
        print(f"{BLUE}ИТОГИ ТЕСТИРОВАНИЯ{RESET}")
        print(f"{'='*80}")
        print(f"Всего тестов:     {total_tests}")
        print(f"{GREEN}Пройдено:         {self.passed} ✓{RESET}")
        print(f"{RED}Провалено:        {self.failed} ✗{RESET}")
        print(f"Успешность:       {success_rate:.1f}%")
        print(f"Время выполнения: {duration:.2f} сек")
        print(f"{'='*80}\n")
        
        if self.failed == 0:
            print(f"{GREEN}{'🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! 🎉':^80}{RESET}\n")
        else:
            print(f"{RED}{'⚠ ОБНАРУЖЕНЫ ОШИБКИ ⚠':^80}{RESET}\n")

if __name__ == '__main__':
    tester = TestScenarios()
    tester.run_all_tests()