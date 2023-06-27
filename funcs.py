import csv


def flatten_dict(d):
    """
    Функция разворачивает словарь и возвращает новый словарь со всеми нужными ключами
    :param d: необработанный словарь
    :return: dict
    """
    flat_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            nested_dict = flatten_dict(value)
            for nested_key, nested_value in nested_dict.items():
                if not (nested_key in flat_dict.keys()):
                    flat_dict[nested_key] = nested_value
        else:
            flat_dict[key] = value

    return flat_dict


def write_to_file(csv_file, data_array):
    """
    Функция проверяет, является ли новый массив дубликатом
    :param csv_file: .csv файл
    :param data_array: массив данных
    :return: True/False для добавления/пропуска массива
    """
    rows = []  # все строки

    with open(csv_file, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    for i in range(len(data_array)):
        data_array[i] = str(data_array[i])  # приведение всего ко строке для сравнения

    if data_array not in rows:  # если массива нет в строках, значит его нужно добавить
        return True

    return False
