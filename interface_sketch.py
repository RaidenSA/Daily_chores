from tkinter import *
from tkinter import ttk
import requests
from client_v1 import register,log_in,get_notes,new_note,pass_change
#user =""
#password =""
notes ={}

def load_all():
    response = get_notes(user_txt.get(), pass_txt.get())
    if response.status_code == 200:
        for ind in response.json():
            uuid = ind['uuid']
            text = ind['text']
            #here we need to add title
            note_control.insert(END, uuid)
            notes[uuid]= text
            note_control.focus()
        return notes
    elif response.status_code == 500:
        auth_lbl.configure(text="Внутренняя ошибка сервера")
    else:
        auth_lbl.configure(text="Ошибка клиента, повторите")

def show_note(event):
    selected = note_control.get(note_control.curselection())
    text = notes[selected]
    note_text.delete(1.0, END)
    note_text.insert(1.0,text)

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
        auth_btn.grid_forget()
        reg_btn.configure(state='disabled')
        reg_btn.grid_forget()
        auth_lbl.configure(text ="Вход выполнен")
        note_control.grid()
        note_space.grid()
        note_scroll.grid()
        notes = load_all()  # here we load all our staff
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
        auth_btn.grid_forget()
        reg_btn.configure(state='disabled')
        reg_btn.grid_forget()
        auth_lbl.configure(text ="Регистрация успешна")
        note_control.grid()
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
reg_btn.grid(column=2, row=1)
#note_control = ttk.Notebook(window)
#note_control.grid(column=0, row=3, columnspan =4, sticky=(N, S, E, W))
note_control = Listbox(selectmode=EXTENDED)
note_control.grid(column=0, row=3, columnspan =2, sticky=(N, S, E, W))
note_scroll = Scrollbar(command=note_control.yview)
note_scroll.grid(column = 1, row =3, sticky =(N,S,E))
note_control.config(yscrollcommand=note_scroll.set)
note_control.bind('<<ListboxSelect>>',show_note)
note_space = ttk.Frame(window,borderwidth=5, relief="ridge", width=200, height=100)
note_space.grid(column =3, row =3, sticky=(N, S, E, W))
note_text = Text(note_space)
note_text.grid(sticky = (N,S,E,W))
note_space.grid_columnconfigure(0,weight=1)
note_space.grid_rowconfigure(0,weight=1)
window.grid_columnconfigure(3,weight=1)#grid_remove()
window.grid_rowconfigure(3,weight=1)
note_control.grid_remove()
note_space.grid_remove()
note_scroll.grid_remove()


window.mainloop()

