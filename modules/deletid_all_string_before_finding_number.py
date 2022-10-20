from loguru import logger


def find_item(input, output, number, info):
    # удаляем все строки, пока не находим искомый номер, после чего все остальное сохраняем
    finding_number = number.get()
    fi = open(input, 'rt')
    flag = 1
    list_sms = []  # сначала пустой список
    counter_sms = 0
    # 7. Реализовать обход файла по строкам и считать числа.
    # Для чтения строк используется итератор файла.
    for s in fi:
        # Убрать последний символ '\n' из s
        s = s.rstrip()
        # Вывести s для контроля
        # print("s = ", s)
        if flag == 1:
            # нашли искомый тел номер, сохраняем его в новый файл
            if s == finding_number:
                flag = 0
            #            fo.write(s + '\n')
            #            counter_sms += 1
            elif s != finding_number:
                pass
                # print("s = ", s)
        if flag == 0:
            list_sms.append(s + '\n')
            counter_sms += 1
    fi.close()
    fo = open(output, 'wt')
    for i in list_sms:
        fo.write(i)
        # Добавить строку s в список list_sms
    #    list_sms = list_sms + [s]
    #    counter_sms = counter_sms + 1
    # 8. Вывести список list_sms для контроля
    # print("list_sms = ", list_sms)
    # 9. Закрыть файл - необязательно
    fo.close()
    logger.info(f"counter_sms = {counter_sms}")
    info.configure(text=f'Осталось номеров: {counter_sms}')
