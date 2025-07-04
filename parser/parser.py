import pandas as pd
from os import path
import sys

# Определение директории запуска скрипта
current_dir = path.dirname(path.abspath(__file__))

# Файл логов DHCP-сервера
LOG_FILE = path.join(current_dir, "dhcpd.log")
# Файл обработанных MAC-адресов
PROCESSED_MACS_FILE = path.join(current_dir, "MACs.csv")
# Файл новых MAC-адресов
NEW_MACS_FILE = path.join(current_dir, "new_macs.txt")
# Список обработанных MAC-адресов из CSV
processed_macs_from_file = []
# Список обработанных MAC-адресов из логов
processed_macs = set()


def read_processed_macs():
    """Читает MAC-адреса из CSV файла и обновляет список обработанных MAC-адресов."""
    global processed_macs_from_file

    try:
        # Считка MAC-адресов из файла
        macs = pd.read_csv(PROCESSED_MACS_FILE)
        # Преобразование в список MAC-адресов
        processed_macs_from_file = set(macs["MACAddress"].tolist())
    except FileNotFoundError:
        print(f"Файл {PROCESSED_MACS_FILE} не найден. Начинаем с пустого списка.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")


def extract_mac_addresses(log_file):
    """Извлечение MAC-адреса из логов DHCP"""
    new_macs = []
    global processed_macs_from_file, processed_macs

    with open(log_file, "r") as file:
        for line in file:
            # Разбираем строку по пробелам
            line_lst = line.split()
            # Формируем строку с датой и временем
            timestamp = f"{line_lst[0]} {line_lst[1]} {line_lst[2]}"
            # Извлекаем MAC-адрес
            mac = line_lst[7].upper()
            # Фильтруем только новые устройства с MAC-адресами из лога
            if (
                "DHCPDISCOVER" in line
                and mac not in processed_macs_from_file
                and mac not in processed_macs
            ):
                # Добавляем MAC-адрес в список обработанных
                processed_macs.add(mac)
                new_macs.append(f"Time: {timestamp}, MAC: {mac}")

    return new_macs


def main():
    """Запуск основного процесса."""
    # Считываем обработанные MAC-адреса
    read_processed_macs()

    # Извлекаем новые MAC-адреса
    new_macs = extract_mac_addresses(LOG_FILE)

    # Сохраняем новые, обработанные MAC-адреса в .txt файл и выводим количество новых MAC-адресов
    if new_macs:
        with open(NEW_MACS_FILE, "w") as file:
            file.write("\n".join(new_macs))
            print(f"Найдено новых MAC-адресов: {len(new_macs)}")


if __name__ == "__main__":
    main()
