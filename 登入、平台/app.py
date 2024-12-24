from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from db import fetch_one, fetch_restaurant_earnings, fetch_delivery_order_count, fetch_customer_payments
from auth import login_user_by_credentials, register_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLAlchemy 設置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/foodpangolin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定義 User 類別，繼承自 Flask-Login 的 UserMixin
class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

# 送貨員模型
class DeliveryPerson(db.Model):
    __tablename__ = 'delivery'
    D_id = db.Column(db.Integer, primary_key=True)
    D_name = db.Column(db.String(100), nullable=False)
    D_phone = db.Column(db.String(15), nullable=False)

# 訂單模型 (替代 DeliveryOrder)
class Item(db.Model):
    __tablename__ = 'item'
    I_id = db.Column(db.Integer, primary_key=True)
    R_id = db.Column(db.Integer, nullable=False)  # FK-餐廳ID
    D_id = db.Column(db.Integer, db.ForeignKey('delivery.D_id'), nullable=True)  # FK-送貨員ID
    C_id = db.Column(db.Integer, nullable=False)  # FK-顧客ID
    M_id = db.Column(db.Integer, nullable=False)  # FK-菜品ID
    I_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='待接單')
    time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    delivery_person = db.relationship('DeliveryPerson', backref='items')

# 根路徑跳轉
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
                return redirect(url_for('delivery_orders'))
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
    if 'user_id' not in session:
        flash('請先登入。')
        return redirect(url_for('login'))
    return "歡迎商家用戶！"

@app.route('/customer')
def customer():
    if 'user_id' not in session:
        flash('請先登入。')
        return redirect(url_for('login'))
    return "歡迎客戶用戶！"

@app.route('/delivery_orders')
def delivery_orders():
    if 'user_id' not in session:
        flash('請先登入。')
        return redirect(url_for('login'))

    # 查詢所有訂單
    orders = db.session.query(
        Item.I_id,
        Item.D_id,
        Item.time,
        Item.status,
        DeliveryPerson.D_name
    ).outerjoin(DeliveryPerson, Item.D_id == DeliveryPerson.D_id).all()

    orders_list = []
    for order in orders:
        orders_list.append({
            'I_id': order.I_id,
            'D_id': order.D_id if order.D_id else "未指派",
            'D_name': order.D_name if order.D_name else "未指派",
            'time': order.time,
            'status': order.status
        })

    return render_template('delivery_orders.html', orders=orders_list)

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

# 接受配送訂單
@app.route('/accept_order/<int:item_id>', methods=['POST'])
def accept_order(item_id):
    item = Item.query.get(item_id)
    if item and item.status == '待接單':
        item.status = '配送中'
        db.session.commit()
        flash('訂單已接單！')
    else:
        flash('無法接單，可能已被接走。')
    return redirect(url_for('delivery_orders'))

# 完成配送訂單
@app.route('/complete_order/<int:item_id>', methods=['POST'])
def complete_order(item_id):
    item = Item.query.get(item_id)
    if item and item.status == '配送中':
        item.status = '已完成'
        db.session.commit()
        flash('配送完成！')
    else:
        flash('無法完成，可能尚未接單或已完成。')
    return redirect(url_for('delivery_orders'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
