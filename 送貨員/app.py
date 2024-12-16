from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/delivery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 送貨員模型
class DeliveryPerson(db.Model):
    __tablename__ = 'delivery_person'
    D_id = db.Column(db.Integer, primary_key=True)
    D_name = db.Column(db.String(100), nullable=False)
    D_phone = db.Column(db.String(15), nullable=False)
    D_available = db.Column(db.Boolean, default=True)

# 配送訂單模型
class DeliveryOrder(db.Model):
    __tablename__ = 'delivery_orders'
    D_I_id = db.Column(db.Integer, primary_key=True)
    I_id = db.Column(db.Integer, nullable=False)
    D_id = db.Column(db.Integer, db.ForeignKey('delivery_person.D_id'), nullable=True)
    D_pickup_time = db.Column(db.DateTime)
    D_delivery_time = db.Column(db.DateTime)
    D_status = db.Column(db.String(20), nullable=False, default='待接單')

    delivery_person = db.relationship('DeliveryPerson', backref='orders')

# 訂單模型
class Order(db.Model):
    __tablename__ = 'orders'
    I_id = db.Column(db.Integer, primary_key=True)
    R_id = db.Column(db.Integer, nullable=False)
    C_id = db.Column(db.Integer, nullable=False)
    I_time = db.Column(db.DateTime, nullable=False)
    I_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='已下單')

# 根路徑跳轉
@app.route('/')
def index():
    return redirect(url_for('view_delivery_orders'))

# 查看所有配送訂單
@app.route('/delivery_orders')
def view_delivery_orders():
    # 查詢配送訂單並連結送貨員名稱
    orders = db.session.query(
        DeliveryOrder.D_I_id,
        DeliveryOrder.I_id,
        DeliveryOrder.D_pickup_time,
        DeliveryOrder.D_delivery_time,
        DeliveryOrder.D_status,
        DeliveryPerson.D_name
    ).outerjoin(DeliveryPerson, DeliveryOrder.D_id == DeliveryPerson.D_id).all()

    # 將結果打包成字典傳遞給模板
    orders_list = []
    for order in orders:
        orders_list.append({
            'D_I_id': order.D_I_id,
            'D_id': order.I_id,
            'D_name': order.D_name if order.D_name else "未指派",
            'D_pickup_time': order.D_pickup_time,
            'D_delivery_time': order.D_delivery_time,
            'D_status': order.D_status
        })

    return render_template('delivery_orders.html', orders=orders_list)

# 接受配送訂單
@app.route('/accept_order/<int:delivery_order_id>', methods=['POST'])
def accept_order(delivery_order_id):
    delivery_order = DeliveryOrder.query.get(delivery_order_id)
    if delivery_order and delivery_order.D_status == '待接單':
        delivery_order.D_status = '配送中'
        delivery_order.D_pickup_time = db.func.current_timestamp()
        db.session.commit()
        flash('訂單已接單！')
    else:
        flash('無法接單，可能已被接走。')
    return redirect(url_for('view_delivery_orders'))

# 完成配送訂單
@app.route('/complete_order/<int:delivery_order_id>', methods=['POST'])
def complete_order(delivery_order_id):
    delivery_order = DeliveryOrder.query.get(delivery_order_id)
    if delivery_order and delivery_order.D_status == '配送中':
        delivery_order.D_status = '已完成'
        delivery_order.D_delivery_time = db.func.current_timestamp()
        db.session.commit()
        flash('配送完成！')
    else:
        flash('無法完成，可能尚未接單或已完成。')
    return redirect(url_for('view_delivery_orders'))

if __name__ == '__main__':
    db.create_all()  # 初始化資料表
    app.run(debug=True)
