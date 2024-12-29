from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/foodpangolin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    status = db.Column(db.String(20), nullable=False, default='待接單')  # 訂單狀態
    time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    delivery_person = db.relationship('DeliveryPerson', backref='items')

# 根路徑跳轉
@app.route('/')
def index():
    return redirect(url_for('view_delivery_orders'))

# 查看所有配送訂單
@app.route('/delivery_orders')
def view_delivery_orders():
    # 查詢 item 表並連結送貨員名稱
    orders = db.session.query(
        Item.I_id,
        Item.D_id,
        Item.time,
        Item.status,
        DeliveryPerson.D_name
    ).outerjoin(DeliveryPerson, Item.D_id == DeliveryPerson.D_id).all()

    # 將結果打包成字典傳遞給模板
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
    return redirect(url_for('view_delivery_orders'))

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
    return redirect(url_for('view_delivery_orders'))

if __name__ == '__main__':
    db.create_all()  # 初始化資料表
    app.run(debug=True)
