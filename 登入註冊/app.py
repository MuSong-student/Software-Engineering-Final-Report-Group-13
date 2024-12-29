from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin
from db import fetch_one,fetch_restaurant_earnings,fetch_delivery_order_count,fetch_customer_payments
from auth import login_user_by_credentials,register_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 定義 User 類別，繼承自 Flask-Login 的 UserMixin
class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id  # 使用者的 ID
        self.username = username  # 使用者名稱
        self.role = role  # 登入角色
@app.route('/')
def index():
    return redirect(url_for('login'))

# 登入路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if not username or not password or not role:
            flash("請填寫所有欄位")
            return redirect(url_for('login'))

        user = login_user_by_credentials(username, password, role)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            print("User logged in:", session)

            if user.role == 2:
                return redirect(url_for('merchant'))
            elif user.role == 1:
                return redirect(url_for('customer'))
            elif user.role == 4:
                return redirect(url_for('delivery'))
            elif user.role == 3:
                return redirect(url_for('platform'))
            else:
                flash("無效的角色類型")
                return redirect(url_for('login'))
        else:
            flash("帳號或密碼錯誤，或角色不符")
            return redirect(url_for('login'))

    return render_template('login.html')

# 註冊路由
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if not username or not password or not role:
            flash("請填寫所有欄位")
            return redirect(url_for('signup'))

        existing_user = fetch_one("SELECT * FROM account WHERE A_account = %s", (username,))
        if existing_user:
            flash("用戶名已存在，請選擇其他用戶名。")
            return redirect(url_for('signup'))

        register_user(username, password, role)
        flash("註冊成功！請登入。")
        return redirect(url_for('login'))

    return render_template('signup.html')

# 登出路由
@app.route('/logout')
def logout():
    session.clear()
    flash("您已成功登出。")
    return redirect(url_for('login'))

@app.route('/merchant')
def merchant():
    if 'user_id' not in session:  # 檢查用戶是否已登入
        flash('請先登入。')
        return redirect(url_for('login'))
    return "歡迎商家用戶！"

@app.route('/customer')
def customer():
    if 'user_id' not in session:  # 檢查用戶是否已登入
        flash('請先登入。')
        return redirect(url_for('login'))
    return "歡迎客戶用戶！"

@app.route('/delivery')
def delivery():
    if 'user_id' not in session:  # 檢查用戶是否已登入
        flash('請先登入。')
        return redirect(url_for('login'))
    return "歡迎外送員！"


@app.route('/platform')
def platform():
    if 'user_id' not in session:
        flash('請先登入。')
        return redirect(url_for('login'))

    # 獲取所需數據
    restaurant_earnings = fetch_restaurant_earnings()
    delivery_order_count = fetch_delivery_order_count()
    customer_payments = fetch_customer_payments()

    return render_template(
        'platform.html',
        restaurant_earnings=restaurant_earnings,
        delivery_order_count=delivery_order_count,
        customer_payments=customer_payments
    )

