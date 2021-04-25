import requests
import properties

def log_in(username, password):
    return requests.get(
        properties.server_url + '/api/v1/auth',
        auth = (username, password)
    )

def register(username, password):
    return requests.put(
        properties.server_url + '/api/v1/auth',
        json = {
            "username": username,
            "password": password,
        }
    )

def pass_change(username, password, new_password):
    return requests.post(
        properties.server_url + '/api/v1/auth',
        auth = (username, password),
        json = {"password": new_password}
    )

def new_note(username, password, text):
    return requests.put(
        properties.server_url + '/api/v1/note',
        auth = (username, password),
        json = {"text": text}
    )

def get_notes(username, password):
    return requests.get(
        properties.server_url + '/api/v1/note',
        auth = (username, password)
    )

def update_note(username, password, id, text):
    return requests.post(
        properties.server_url + '/api/v1/note/' + str(id),
        auth = (username, password),
        json = {"text": text}
    )

def get_note(username, password, id):
    return requests.get(
        properties.server_url + '/api/v1/note/' + str(id),
        auth = (username, password)
    )

def delete_note(username, password, id):
    return requests.delete(
        properties.server_url + '/api/v1/note/' + str(id),
        auth = (username, password)
    )
