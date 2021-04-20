from client_v1 import register,log_in,get_notes,new_note,pass_change
auth_flag =1
reg_flag =0
while auth_flag:
    print("type in user or word 'registration' ")
    user =input()
    if user == 'registration':
        print('You have chosen to register')
        print('type in username')
        user = input()
        reg_flag = 1
    print("type in password")
    password = input()
    if reg_flag:
        response = register(user,password)
        if response.status_code==201:
            print('registration successful')
            auth_flag = 0
            reg_flag=0
        else:
            print('something went wrong, please try again, error'+ str(response.status_code))
            reg_flag =0
    else:
        response = log_in(user,password)
        if response.status_code == 200:
            auth_flag = 0
        else:
            print("error "+ str(response.status_code)+", please try again")
print('Yes, you are in!')
while True:
    print('Type in N for new note, P to change password, G to get your notes, E to exit ')
    in_string = input().upper()
    if in_string not in 'NPGE':
        print('wrong command')
        continue
    if in_string == 'E':
        print('exit successful')
        break
    if in_string == 'N':
        print('Type in your note')
        in_note = input()
        response = new_note(user,password,in_note)
        if response.status_code ==201:
            print("New note added :" + response.json()['text'])
        else:
            print("error "+ str(response.status_code))
    if in_string =="P":
        print('Type in new password')
        new_password = input()
        response = pass_change(user,password,new_password)
        if response.status_code ==200:
            password = new_password #pretty critical
            print("Password successfully changed")
        else:
            print('error '+ str(response.status_code))
    if in_string =='G':
        response = get_notes(user, password)
        if response.status_code ==200:
            for ind in response.json():
                print(ind['text'])
# right here i suppose i'll have to change all data from response.json collection to a collection
        # of no-like objects. They need to be clickable to expand, have to be adjastable on the screen
        # and have to be all in one place. Hopefully, i'll only need to load all notes
        #only once after successfull auth or when we need to hard-update our notes.
        else:
            print('error '+ str(response.status_code))
# we have here: [[uuid, user, ctime, atime, text]]
        #response = response1.json()[0]['text']
        #continue
    #print(response)

