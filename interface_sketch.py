from tkinter import *
from tkinter import ttk
import requests
import client_v1

#user =""
#password =""
notes ={}
# need to catch connection troubles
def load_all():
    response = client_v1.get_notes(user_txt.get(), pass_txt.get())
    if response.status_code == 200:
        for ind in response.json():
            uuid = ind['uuid']
            text = ind['text']
            #here we need to add title
            note_control.insert(END, uuid)
            notes[uuid]= text
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
    response = client_v1.log_in(user, password)
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
        auth_btn.grid_remove()
        reg_btn.configure(state='disabled')
        reg_btn.grid_remove()
        user_lbl.grid_remove()
        user_txt.grid_remove()
        pass_lbl.grid_remove()
        pass_txt.grid_remove()
        auth_lbl.configure(text ="Вход выполнен")
        note_control.grid()
        note_space.grid()
        note_scroll.grid()
        new_note_btn.grid()
        save_note_btn.grid()
        del_note_btn.grid()
        notes = load_all()  # here we load all our staff
    else:
        auth_lbl.configure(text="Ошибка клиента, повторите")

def reg_click():
    user = user_txt.get()
    password = pass_txt.get()
    response = client_v1.register(user, password)
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
        user_lbl.grid_remove()
        user_txt.grid_remove()
        pass_lbl.grid_remove()
        pass_txt.grid_remove()
        auth_lbl.configure(text ="Регистрация успешна")
        note_control.grid()
        note_space.grid()
        note_scroll.grid()
        new_note_btn.grid()
        save_note_btn.grid()
        del_note_btn.grid()
    else:
        auth_lbl.configure(text="Ошибка клиента, повторите")

def new_note_click():
    user = user_txt.get()
    password = pass_txt.get()
    response = client_v1.new_note(user,password,"")
    if response.status_code == 201:
        uuid = response.json()['uuid']
        text = response.json()['text']
        note_control.insert(END, uuid)
        notes[uuid] = text
    #and i need to show it somehow

def save_changes_click():
    user = user_txt.get()
    password = pass_txt.get()
    index = note_control.curselection()
    if not index:
        index = 0
    selected = note_control.get(index) #cause of uuid
    text = note_text.get(1.0, 'end-1c') # it doesn't like end of line at all
    #print(text)
    response = client_v1.update_note(user,password,selected,text)
    if response.status_code == 200:
        notes[selected] = text
    #status code chek

def delete_click():
    user = user_txt.get()
    password = pass_txt.get()
    index = note_control.curselection()
    if not index:
        index = 0
    selected = note_control.get(index)
    response = client_v1.delete_note(user,password,selected)
    if response.status_code == 204:
        del notes[selected]
        note_text.delete(1.0, END)
        note_control.delete(index)


window = Tk()
window.title("Daily chores app")
window.geometry('400x250')
user_lbl = Label(window, text="Логин")
user_lbl.grid(column=0, row=0)
user_txt = Entry(window,width=10)
user_txt.grid(column=1, row=0)
user_txt.focus()
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
note_control = Listbox(selectmode=EXTENDED, exportselection=False)
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
new_note_btn = Button(window, text="Создать новую", command=new_note_click)
new_note_btn.grid(column=0, row=0)
save_note_btn = Button(window, text="Сохранить", command=save_changes_click)
save_note_btn.grid(column=0, row=1)
del_note_btn = Button(window, text="Удалить", command=delete_click)
del_note_btn.grid(column=1, row=0)
#password_change_btn = Button(window, text="", command=save_changes_click)
#password_change_btn.grid(column=1, row=1)
note_control.grid_remove()
note_space.grid_remove()
note_scroll.grid_remove()
new_note_btn.grid_remove()
save_note_btn.grid_remove()
del_note_btn.grid_remove()


window.mainloop()

