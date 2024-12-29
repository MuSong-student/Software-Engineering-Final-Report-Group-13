from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin
from db import fetch_one, execute_query

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 定義 User 類別，繼承自 Flask-Login 的 UserMixin
class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id  # 使用者的 ID
        self.username = username  # 使用者名稱
        self.role = role  # 登入角色

# 通過用戶憑證（用戶名稱和密碼）登入用戶
def login_user_by_credentials(username, password, role=None):
    query = "SELECT * FROM account WHERE A_account = %s"
    user = fetch_one(query, (username,))

    if user is None:
        print("User not found in database.")
        return None

    stored_password = user['A_password']
    if password == stored_password and (role is None or str(user['A_role']) == str(role)):
        return User(user_id=user['A_id'], username=user['A_account'], role=user['A_role'])
    return None

# 註冊新用戶
def register_user(username, password, role):
    query = "INSERT INTO account (A_account, A_password, A_role) VALUES (%s, %s, %s)"
    execute_query(query, (username, password, role))


