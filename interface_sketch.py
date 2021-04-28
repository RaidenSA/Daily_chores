from tkinter import *
from tkinter import ttk
import requests
import client_v1

#user =""
#password =""
notes ={}
note_control_ind_to_uuid =[]
# need to catch connection troubles
def load_all():
    response = client_v1.get_notes(user_txt.get(), pass_txt.get())
    if response.status_code == 200:
        for ind in response.json():
            uuid = ind['uuid']
            text = ind['text']
            title = ind['title']
            note_control.insert(END, title)
            note_control_ind_to_uuid.append(uuid)
            notes[uuid]= [title, text]
        return notes
    elif response.status_code == 500:
        status_lbl.configure(text="Внутренняя ошибка сервера")
    else:
        status_lbl.configure(text="Ошибка клиента, повторите")

def show_note(event):
    if note_control.curselection():
        #selected = note_control.get(note_control.curselection())
        selected = note_control_ind_to_uuid[note_control.curselection()[0]]
        text = notes[selected][1]
        title = notes[selected][0]
        note_text.delete(1.0, END)
        note_text.insert(1.0,text)
        note_title.delete(0, END)
        note_title.insert(0,title)

def auth_click():
    user = user_txt.get()
    password = pass_txt.get()
    response = client_v1.log_in(user, password)
    if response.status_code == 403:
        status_lbl.configure(text = "Неверный логин или пароль")
        user_txt.configure(text ="")
        pass_txt.configure(text ="")
    elif response.status_code == 500:
        status_lbl.configure(text="Внутренняя ошибка сервера")
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
        status_lbl.configure(text ="Вход выполнен")
        note_control.grid()
        note_space.grid()
        note_scroll.grid()
        new_note_btn.grid()
        save_note_btn.grid()
        del_note_btn.grid()
        note_title.grid()
        title_lbl.grid()
        pass_change_btn.grid()
        notes = load_all()  # here we load all our staff
    else:
        status_lbl.configure(text="Ошибка клиента, повторите")

def reg_click():
    user = user_txt.get()
    password = pass_txt.get()
    response = client_v1.register(user, password)
    if response.status_code == 409:
        status_lbl.configure(text="Пользователь с таким именем уже существует")
    elif response.status_code == 500:
        status_lbl.configure(text="Внутренняя ошибка сервера")
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
        status_lbl.configure(text ="Регистрация успешна")
        note_control.grid()
        note_space.grid()
        note_scroll.grid()
        new_note_btn.grid()
        save_note_btn.grid()
        del_note_btn.grid()
        note_title.grid()
        title_lbl.grid()
        pass_change_btn.grid()
    else:
        status_lbl.configure(text="Ошибка клиента, повторите")

def pass_change_click():
    status_lbl.configure(text="Введите старый и новый пароль")

    note_control.grid_remove()
    note_space.grid_remove()
    note_scroll.grid_remove()
    new_note_btn.grid_remove()
    save_note_btn.grid_remove()
    del_note_btn.grid_remove()
    note_title.grid_remove()
    title_lbl.grid_remove()
    pass_change_btn.grid_remove()

    old_pass_lbl.grid()
    old_pass_txt.grid()
    new_pass_lbl.grid()
    new_pass_txt.grid()
    accept_btn.grid()
    cancel_btn.grid()

def accept_click():
    user = user_txt.get()
    password = old_pass_txt.get()
    new_password = new_pass_txt.get()
    response = client_v1.pass_change(user,password,new_password)
    if response.status_code==200:
        pass_txt.delete(0,END)
        pass_txt.insert(0,new_password)
        status_lbl.configure(text='Пароль изменен успешно')
        old_pass_txt.delete(0, END)
        new_pass_txt.delete(0, END)

        note_control.grid()
        note_space.grid()
        note_scroll.grid()
        new_note_btn.grid()
        save_note_btn.grid()
        del_note_btn.grid()
        note_title.grid()
        title_lbl.grid()
        pass_change_btn.grid()

        old_pass_lbl.grid_remove()
        old_pass_txt.grid_remove()
        new_pass_txt.grid_remove()
        new_pass_lbl.grid_remove()
        accept_btn.grid_remove()
        cancel_btn.grid_remove()
    elif response.status_code == 403:
        status_lbl.configure(text='Неверный пароль')
        old_pass_txt.delete(0, END)
        new_pass_txt.delete(0, END)
    elif response.status_code ==500:
        status_lbl.configure(text='Ошибка сервера')
    else:
        status_lbl.configure(text="Ошибка клиента, повторите")

def cancel_click():
    note_control.grid()
    note_space.grid()
    note_scroll.grid()
    new_note_btn.grid()
    save_note_btn.grid()
    del_note_btn.grid()
    note_title.grid()
    title_lbl.grid()
    pass_change_btn.grid()

    old_pass_txt.delete(0,END)
    new_pass_txt.delete(0,END)
    old_pass_lbl.grid_remove()
    old_pass_txt.grid_remove()
    new_pass_txt.grid_remove()
    new_pass_lbl.grid_remove()
    accept_btn.grid_remove()
    cancel_btn.grid_remove()


def new_note_click():
    user = user_txt.get()
    password = pass_txt.get()
    response = client_v1.new_note(user,password,"New note","New note")
    if response.status_code == 201:
        uuid = response.json()['uuid']
        text = response.json()['text']
        title = response.json()['title']
        note_control.insert(END, title)
        note_control_ind_to_uuid.append(uuid)
        notes[uuid] = [title, text]
        status_lbl.configure(text="Успешно создана")
    elif response.status_code ==500:
        status_lbl.configure(text='Ошибка сервера')
    else:
        status_lbl.configure(text="Ошибка клиента, повторите")

def save_changes_click():
    user = user_txt.get()
    password = pass_txt.get()
    index = note_control.curselection()
    if not index:
        return
    selected = note_control_ind_to_uuid[index[0]] #cause of uuid
    text = note_text.get(1.0, 'end-1c') # it doesn't like end of line at all
    #print(text)
    title =note_title.get()
    response = client_v1.update_note(user,password,selected,title,text)
    if response.status_code == 200:
        note_control.delete(index[0])
        note_control.insert(index[0],title)
        notes[selected] = [title,text]
        status_lbl.configure(text="Изменения сохранены")
    elif response.status_code == 500:
        status_lbl.configure(text='Ошибка сервера')
    else:
        status_lbl.configure(text="Ошибка клиента, повторите")

def delete_click():
    user = user_txt.get()
    password = pass_txt.get()
    index = note_control.curselection()
    if not index:
        return
    selected = note_control_ind_to_uuid[index[0]]
    response = client_v1.delete_note(user,password,selected)
    if response.status_code == 204:
        del notes[selected]
        note_text.delete(1.0, END)
        note_title.delete(0, END)
        note_control.delete(index[0])
        note_control_ind_to_uuid.pop(index[0])
        status_lbl.configure(text="Заметка удалена")
    elif response.status_code == 500:
        status_lbl.configure(text='Ошибка сервера')
    else:
        status_lbl.configure(text="Ошибка клиента, повторите")


window = Tk()
window.title("Daily chores app")
window.geometry('450x250')
user_lbl = Label(window, text="Логин")
user_lbl.grid(column=0, row=0)
user_txt = Entry(window,width=10)
user_txt.grid(column=1, row=0)
user_txt.focus()
pass_lbl = Label(window, text="Пароль")
pass_lbl.grid(column=0, row=1)
pass_txt = Entry(window,width=10)
pass_txt.grid(column=1, row=1)
status_lbl = Label(window, text="")
status_lbl.grid(column=3, row=1, columnspan =2) #here
auth_btn = Button(window, text="Авторизация", command=auth_click)
auth_btn.grid(column=2, row=0)
reg_btn = Button(window, text="Регистрация", command=reg_click)
reg_btn.grid(column=2, row=1)

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
note_title = Entry(window,width=10)
#note_title.grid(column=3, row=1, sticky=(N,S,E,W))
note_title.grid(column=3, row=2, sticky=(N,S,E,W))
title_lbl=Label(window, text="Заголовок")
title_lbl.grid(column=0, row=2,columnspan = 2)
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
note_title.grid_remove()
title_lbl.grid_remove()

#for pass change
old_pass_lbl = Label(window, text="Старый пароль")
old_pass_lbl.grid(column=0, row=0)
old_pass_txt = Entry(window,width=10)
old_pass_txt.grid(column=1, row=0)
old_pass_txt.focus()
new_pass_lbl = Label(window, text="Новый пароль")
new_pass_lbl.grid(column=0, row=1)
new_pass_txt = Entry(window,width=10)
new_pass_txt.grid(column=1, row=1)
pass_change_btn=Button(window, text="Изменить пароль", command=pass_change_click)
pass_change_btn.grid(column=3, row=0)
accept_btn = Button(window, text="Потдвердить", command=accept_click)
accept_btn.grid(column=2, row=0)
cancel_btn = Button(window, text="Отмена", command=cancel_click)
cancel_btn.grid(column=2, row=1)

pass_change_btn.grid_remove()
old_pass_lbl.grid_remove()
old_pass_txt.grid_remove()
new_pass_txt.grid_remove()
new_pass_lbl.grid_remove()
accept_btn.grid_remove()
cancel_btn.grid_remove()

window.mainloop()

