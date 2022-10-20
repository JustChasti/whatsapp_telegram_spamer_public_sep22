from loguru import logger


def delete_duplicates(input, output, info):
    f = open(input, 'rt')
    list_sms_with_dubles = []  # сначала пустой список
    counter_sms_with_dubles = 0
    # 7. Реализовать обход файла по строкам и считать числа.
    # Для чтения строк используется итератор файла.
    for s in f:
        # Убрать последний символ '\n' из s
        s = s.rstrip()
        # Вывести s для контроля
        # print("s = ", s)
        # Добавить строку s в список list_sms_with_dubles
        list_sms_with_dubles = list_sms_with_dubles + [s]
        counter_sms_with_dubles = counter_sms_with_dubles + 1
    # 8. Вывести список list_sms_with_dubles для контроля
    # print("list_sms_with_dubles = ", list_sms_with_dubles)
    # print("counter_sms_with_dubles = ", counter_sms_with_dubles)
    f.close()
    list_sms_without_dubles = list(set(list_sms_with_dubles))
    # print(list_sms_without_dubles)
    counter_sms_without_dubles = 0
    f = open(output, 'wt')
    for item in list_sms_without_dubles:
        # 2.3.1. Конвертировать item в строку
        s = str(item)
        # 2.3.2. Записать строку + символ ' ' пробел
        f.write(s + '\n')
        counter_sms_without_dubles = counter_sms_without_dubles + 1
        # 2.4. Закрыть файл
    f.close()
    logger.info(f"counter_sms_without_dubles = {counter_sms_without_dubles}")
    info.configure(text=f'Удалено дубликатов {counter_sms_with_dubles - counter_sms_without_dubles}')
