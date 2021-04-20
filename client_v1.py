import requests
headers = {
    'Content-Type': 'application/json',
}
#destination = 'http://127.0.0.1:5000/api/v1'
address = 'http://127.0.0.1:5000'

def log_in(username, password):
    prefix ='/api/v1/auth'
    destination = address+prefix
    response = requests.get(destination, headers=headers, auth=(username, password))
    return response

def register(username,password):
    prefix = '/api/v1/auth'
    destination = address + prefix
    data = '{{"username":"{0}", "password":"{1}"}}'.format(username,password)
    response = requests.put(destination, headers=headers, data=data)
    return response

def pass_change(username,password,new_password):
    prefix = '/api/v1/auth'
    destination = address + prefix
    data = '{{"password":"{0}"}}'.format(new_password)
    response = requests.post(destination, headers=headers,auth=(username, password), data=data)
    return response

def new_note(username,password,text):
    prefix = '/api/v1/note'
    destination = address + prefix
    data = '{{"text":"{0}"}}'.format(text) # may be it is called payload
    response = requests.put(destination, headers=headers,auth=(username, password), data=data)
    return response

def get_notes(username,password):
    prefix = '/api/v1/note'
    destination = address + prefix
    response = requests.get(destination, headers=headers,auth=(username, password))
    return response # this one needs huge parsing. Nevertheless, they all need it

# current users: SS:P,K:P,T:P,L:P
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
            print('something went wrong, please try again')
            reg_flag =0
    else:
        response = log_in(user,password)
        if response.status_code == 200:
            auth_flag = 0
        else:
            print("error, try again")
print('Yes, you are in!')