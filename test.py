import os

password = "admin123"  # hardcoded password

def get_user(id):
    query = "SELECT * FROM users WHERE id=" + id  # SQL injection
    return query

def divide(a, b):
    return a / b  # no zero division check

def read_file(filename):
    f = open(filename)  # never closed
    return f.read()
