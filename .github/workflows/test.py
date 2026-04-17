import os

password = "admin123"  # hardcoded password

def get_user(id):
    query = "SELECT * FROM users WHERE id=" + id  # SQL injection
    return query

def divide(a, b):
    return a / b  # no zero division check
