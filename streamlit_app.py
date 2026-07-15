import streamlit as st
import json
import os
from hashlib import sha256  # optional but recommended

USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user(username, password):
    users = load_users()
    # Hash the password (simple version)
    hashed = sha256(password.encode()).hexdigest()
    users[username] = hashed
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Signup
if st.button("Sign Up"):
    if username and password:
        save_user(username, password)
        st.success("Account created! Now try logging in.")

# Login
users = load_users()
if username in users and users[username] == sha256(password.encode()).hexdigest():
    st.success("Login successful!")
    # proceed to app
else:
    st.error("Invalid username or password")
if username == "hardcoded" and password == "hardcoded":
    # login success
