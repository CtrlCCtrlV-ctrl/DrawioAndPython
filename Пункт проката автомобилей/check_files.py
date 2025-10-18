#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка созданных файлов и основных функций
"""

import json
import os

def check_files():
    """Проверка файлов данных"""
    print("Проверка файлов данных...")

    # Проверка users.json
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        print(f"✓ Файл users.json найден, пользователей: {len(users_data['users'])}")

        for user in users_data['users']:
            print(f"  - {user['username']}: {user['password']} ({user['role']})")
    else:
        print("❌ Файл users.json не найден")

    # Проверка data.json
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Файл data.json найден")
        print(f"  Автомобилей: {len(data['cars'])}")
        print(f"  Клиентов: {len(data['clients'])}")
        print(f"  Аренд: {len(data['rentals'])}")
        print(f"  Бронирований: {len(data['bookings'])}")

        print("\nАвтомобили:")
        for car in data['cars']:
            print(f"  - {car['brand']} {car['model']} ({car['year']}) - {car['price_per_day']} руб/день - {car['status']}")

        print("\nКлиенты:")
        for client in data['clients']:
            print(f"  - {client['name']} - {client['phone']}")

        print("\nАренды:")
        for rental in data['rentals']:
            print(f"  - ID {rental['id']}: Авто {rental['car_id']}, Клиент {rental['client_id']} - {rental['status']}")
    else:
        print("❌ Файл data.json не найден")

    # Проверка кода auth.py
    print("\nПроверка auth.py...")
    if os.path.exists('auth.py'):
        with open('auth.py', 'r', encoding='utf-8') as f:
            content = f.read()
        if 'hashlib' in content:
            print("❌ Найден hashlib в auth.py - шифрование не удалено")
        else:
            print("✓ Шифрование паролей удалено из auth.py")

        if 'hash_password' in content:
            print("❌ Найдена функция hash_password - шифрование не удалено")
        else:
            print("✓ Функция hash_password удалена")

    # Проверка кода main.py
    print("\nПроверка main.py...")
    if os.path.exists('main.py'):
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        if 'init_database' in content:
            print("❌ Найден метод init_database - инициализация файлов не удалена")
        else:
            print("✓ Метод init_database удален")

        if 'os.path.exists' in content:
            print("❌ Найдены проверки существования файлов - инициализация не удалена")
        else:
            print("✓ Проверки существования файлов удалены")

    print("\n" + "="*50)
    print("ПРОВЕРКА ЗАВЕРШЕНА")
    print("="*50)

if __name__ == "__main__":
    check_files()
