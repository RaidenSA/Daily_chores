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

def get_notes(username, password):
    prefix = '/api/v1/note'
    destination = address + prefix
    response = requests.get(destination, headers=headers,auth=(username, password))
    return response # this one needs huge parsing. Nevertheless, they all need it

def update_note(username, password, id, text):
    prefix = '/api/v1/note'
    destination = address + prefix + '/' + str(id)
    #print(data)# may be it is called payload
    response = requests.post(destination, headers=headers, auth=(username, password), json={'text':text})
    return response
#print(requests.put('http://127.0.0.1:5000/api/v1/note', json={'text':a}, auth = ("max", "123"), headers = {}).json()["text"])

def get_note(username, password, id):
    prefix = '/api/v1/note'
    destination = address + prefix + '/' + str(id)
    response = requests.get(destination, headers=headers, auth=(username, password))
    return response

def delete_note(username, password, id):
    prefix = '/api/v1/note'
    destination = address + prefix + '/' + str(id)
    response = requests.delete(destination, headers=headers, auth=(username, password))
    return response
#returns empty + code
# current users: SS:P,K:P,T:P,L:P
