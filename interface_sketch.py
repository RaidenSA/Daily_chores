from tkinter import *
import requests
from client_v1 import register,log_in,get_notes,new_note,pass_change


def auth_click():
    user = user_txt.get()
    password = pass_txt.get()
    response = log_in(user, password)

    if response.status_code == 403:
        auth_lbl.configure(text = "Неверный логин или пароль")
        user_txt.configure(text ="")
        pass_txt.configure(text ="")
    elif response.status_code == 500:
        auth_lbl.configure(text="Внутренняя ошибка сервера")
    elif response.status_code == 200:
        user_txt.configure(state='disabled')
        pass_txt.configure(state='disabled')
        auth_btn.configure(state='disabled')
        reg_btn.configure(state='disabled')
        auth_lbl.configure(text ="Вход выполнен")
    else:
        auth_lbl.configure(text="Ошибка клиента, повторите")
def reg_click():
    user = user_txt.get()
    password = pass_txt.get()
    response = register(user, password)
    if response.status_code == 409:
        auth_lbl.configure(text="Пользователь с таким именем уже существует")
    elif response.status_code == 500:
        auth_lbl.configure(text="Внутренняя ошибка сервера")
    elif response.status_code == 201:
        user_txt.configure(state='disabled')
        pass_txt.configure(state='disabled')
        auth_btn.configure(state='disabled')
        reg_btn.configure(state='disabled')
        auth_lbl.configure(text ="Регистрация успешна")
    else:
        auth_lbl.configure(text="Ошибка клиента, повторите")

window = Tk()
window.title("Daily chores app")
window.geometry('400x250')
user_lbl = Label(window, text="Логин")
user_lbl.grid(column=0, row=0)
user_txt = Entry(window,width=10)
user_txt.grid(column=1, row=0)
pass_lbl = Label(window, text="Пароль")
pass_lbl.grid(column=0, row=1)
pass_txt = Entry(window,width=10)
pass_txt.grid(column=1, row=1)
auth_lbl = Label(window, text="")
auth_lbl.grid(column=0, row=2, columnspan = 4)
auth_btn = Button(window, text="Авторизация", command=auth_click)
auth_btn.grid(column=2, row=0)
reg_btn = Button(window, text="Регистрация", command=reg_click)
reg_btn.grid(column=3, row=0)
window.mainloop()

