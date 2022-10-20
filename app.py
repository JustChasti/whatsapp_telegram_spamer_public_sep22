from unittest import result
from whatsapp.send import send_message as wsend
from time import sleep
from telegram.send import send_message as tsend
from phone.phone_sender import main as psend
import threading
import configparser
from tkinter import *
from tkinter import ttk, Tk
from modules import del_dublicates, deletid_all_string_before_finding_number

config = configparser.ConfigParser()
config.read("settings.ini", encoding='utf-8')
message_text = config['app']['message_text']
input_file = config['app']['input_file']
output_file = config['app']['output_file']


def start_process(table, lable, text, choise):
    f = open(input_file, "r")
    lines = f.readlines()
    f.close()
    input = open(input_file, "w")
    output = open(output_file, "w")
    sended = 0
    notsended = 0
    count = 0
    table.delete(0)
    table.insert(parent='', index='end', iid=0, text='', values=(len(lines), sended, notsended, len(lines) - count))
    for i in lines:
        phone = str(i)
        lable.configure(text=f'Идет отправка на номер {phone}')
        if phone[0] == '8':
            phone = '7' + phone[1:]
        if phone[0] == '+':
            phone = phone[1:]
        if choise == 'wt':
            result = wsend(phone, text)
        elif choise == 'tg':
            result = tsend(phone, text)
        else:
            result = psend(phone, text)
        if result:
            output.write(i)
            sended += 1
        else:
            input.write(i)
            notsended += 1
        count += 1
        table.delete(0)
        table.insert(parent='', index='end', iid=0, text='', values=(len(lines), sended, notsended, len(lines) - count))

    lable.configure(text=f'Отправка завершилась')


def clicked(table, info, choise):
    del_dublicates.delete_duplicates(input_file, input_file, info)
    thread = threading.Thread(target=start_process, args=(table, info, message_text, choise, ))
    thread.start()


def deletion_duplicates(frame):
    info = Label(frame, text="Удалено дубликатов: 0")
    btn = Button(frame, text="Старт", command=lambda: del_dublicates.delete_duplicates(input_file, output_file, info))
    btn.grid(column=0, row=5)
    info.grid(column=0, row=6)
    return frame


def deletion_numbers_before(frame):
    info = Label(frame, text="Осталось номеров: 0")
    number = Entry(frame, width=60)
    info.grid(column=0, row=3)
    number.grid(column=0, row=4)
    btn = Button(frame, text="Старт", command=lambda: deletid_all_string_before_finding_number.find_item(input_file, input_file, number, info))
    btn.grid(column=0, row=5)
    return frame


def draw_window(frame, choise):
    table = ttk.Treeview(frame, height=1)
    table['columns'] = ('all', 'send', 'notsend', 'ost')
    table.column("#0", width=0,  stretch=NO)
    table.column("all", anchor=CENTER, width=150)
    table.column("send", anchor=CENTER, width=150)
    table.column("notsend", anchor=CENTER, width=150)
    table.column("ost", anchor=CENTER, width=150)
    table.heading("all", text="Всего", anchor=CENTER)
    table.heading("send", text="Отправлено", anchor=CENTER)
    table.heading("notsend", text="Не смог отправить", anchor=CENTER)
    table.heading("ost", text="Осталось отправить", anchor=CENTER)
    table.insert(parent='', index='end', iid=0, text='', values=(0, 0, 0, 0))
    table.grid(column=0, row=0)
    info = Label(frame, text="Отправка не идет")
    btn = Button(frame, text="Старт", command=lambda: clicked(table, info, choise))
    btn.grid(column=0, row=5)
    info.grid(column=0, row=6)
    return frame


if __name__ == '__main__':
    window = Tk()
    window.title("Скрипт отправки")
    window.geometry('600x600')
    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=BOTH)
    wt_send = draw_window(ttk.Frame(notebook), 'wt')
    tg_send = draw_window(ttk.Frame(notebook), 'tg')
    ph_send = draw_window(ttk.Frame(notebook), 'ph')
    finds = deletion_numbers_before(ttk.Frame(notebook))
    wt_send.pack(fill=BOTH, expand=True)
    tg_send.pack(fill=BOTH, expand=True)
    ph_send.pack(fill=BOTH, expand=True)
    finds.pack(fill=BOTH, expand=True)

    # добавляем фреймы в качестве вкладок
    notebook.add(wt_send, text="Whatsapp")
    notebook.add(tg_send, text="Telegram")
    notebook.add(ph_send, text="Phone")
    notebook.add(finds, text="Удалить до номера")
    window.mainloop()

    # draw_window()
