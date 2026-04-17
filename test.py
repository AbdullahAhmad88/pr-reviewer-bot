import os
import subprocess

# Hardcoded credentials
DB_PASSWORD = "supersecret123"
API_KEY = "sk-abc123xyz789"

def get_user(user_id):
    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE id=" + user_id
    return query

def divide(a, b):
    # No zero division check
    return a / b

def read_file(filename):
    # File never closed
    f = open(filename)
    return f.read()

def run_command(user_input):
    # Command injection vulnerability
    os.system("ls " + user_input)

def login(username, password):
    # Comparing passwords in plain text
    if password == DB_PASSWORD:
        return True

def get_all_data(data):
    results = []
    for i in range(len(data)):  # should use enumerate
        results.append(data[i])
    return results

x = 0
while True:  # infinite loop
    x += 1
