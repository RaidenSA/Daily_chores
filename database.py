"""
database.py -- db interface
=================================
Used in server.py
"""

import sql


def init(conn):
    """"Initializes DB state"""

    cursor = conn.cursor()
    cursor.execute(sql.CREATE_USERS)
    cursor.execute(sql.CREATE_NOTES)
    conn.commit()
    conn.close()


def get_user(conn, username):
    """get user by username"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_USER, (username,))
    return cursor.fetchone()


def add_user(conn, user):
    """add new user"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_USER, (user['username'], user['password']))


def get_note(conn, uuid):
    """get note by uuid"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_NOTE, (uuid,))
    note = cursor.fetchone()
    if note is None:
        return None

    return note

def get_notes(conn, username):
    """get notes by username"""

    cursor = conn.cursor()
    cursor.execute(sql.SELECT_NOTES, (username,))
    notes = cursor.fetchall()
    if notes is None:
        return None

    return notes

def add_note(conn, note):
    """add new note"""

    cursor = conn.cursor()
    cursor.execute(sql.INSERT_NOTE, (
        note['uuid'],
        note['user'],
        note['ctime'],
        note['atime'],
        note['date'],
        note['text']
    ))


def update_note(conn, note):
    """update existing note"""

    cursor = conn.cursor()
    cursor.execute(sql.UPDATE_NOTE, (
        note['user'],
        note['ctime'],
        note['atime'],
        note['date'],
        note['text'],
        note['uuid']
    ))
