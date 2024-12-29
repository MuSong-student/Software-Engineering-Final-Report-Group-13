from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from db import fetch_one, fetch_restaurant_earnings, fetch_delivery_order_count, fetch_customer_payments
from databass import my_Menu,get_rid_by_account,add_menu_item,delete,get_menu_by_id,updategood,get_orders_by_restaurant, update_order_status, get_merchant_daily_stats, get_order_details,update_rejected_status, update_accepted_status
from auth import login_user_by_credentials, register_user
from datetime import datetime
from db import db, fetch_restaurants, fetch_menu_items, add_to_cart, fetch_cart_items
from db import fetch_cart_items, place_order_in_db,group_cart_by_restaurant
from db import create_order,update_cart_items_order_id,finalize_order_in_db,get_customer_id
from db import fetch_user_orders, submit_review_to_db, fetch_review

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


# 訂單模型 (替代 DeliveryOrder)
class Item(db.Model):
    __tablename__ = 'item'
    I_id = db.Column(db.Integer, primary_key=True)
    R_id = db.Column(db.Integer, nullable=False)  # FK-餐廳ID
    D_id = db.Column(db.Integer, db.ForeignKey('delivery.D_id'), nullable=True)  # FK-送貨員ID
    C_id = db.Column(db.Integer, nullable=False)  # FK-顧客ID
    M_id = db.Column(db.Integer, nullable=False)  # FK-菜品ID
    I_quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)  # 新增訂單價格
    status = db.Column(db.String(20), nullable=False, default='待接單')
    time = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    D_pickup_time = db.Column(db.DateTime, nullable=True)
    D_delivery_time = db.Column(db.DateTime, nullable=True)


    

# 送貨員模型
class DeliveryPerson(db.Model):
    __tablename__ = 'delivery'
    D_id = db.Column(db.Integer, primary_key=True)
    D_name = db.Column(db.String(100), nullable=False)  # 外送員名稱
    D_phone = db.Column(db.String(15), nullable=False)  # 外送員電話
    A_account = db.Column(db.String(20), nullable=False)  # 外送員帳號

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    R_id = db.Column(db.Integer, primary_key=True)
    R_name = db.Column(db.String(100), nullable=False)
    R_address = db.Column(db.String(255), nullable=False)  # 餐廳地址
    R_phone = db.Column(db.String(15), nullable=False)  # 餐廳電話
    A_account = db.Column(db.String(20), nullable=False)  # 顧客帳號

# 顧客模型
class Customer(db.Model):
    __tablename__ = 'customer'
    C_id = db.Column(db.Integer, primary_key=True)
    C_name = db.Column(db.String(100), nullable=False)
    C_address = db.Column(db.String(255), nullable=False)  # 顧客地址
    C_phone = db.Column(db.String(15), nullable=False)  # 顧客電話
    A_account = db.Column(db.String(20), nullable=False)  # 顧客帳號


class Menu(db.Model):
    __tablename__ = 'menu'
    M_id = db.Column(db.Integer, primary_key=True)
    R_id = db.Column(db.Integer, db.ForeignKey('restaurant.R_id'), nullable=False)
    M_price = db.Column(db.Float, nullable=False)  # 菜品價格
    M_name = db.Column(db.String(100), nullable=False)


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
                return redirect(url_for('merchantHome'))
            elif user.role == 1:
                return redirect(url_for('customer_home'))
            elif user.role == 4:
                return redirect(url_for('view_delivery_orders'))

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




@app.route('/platform')
def platform():
    # 檢查使用者是否已登入
    if 'user_id' not in session:
        flash('請先登入。')  # 如果未登入，顯示提示訊息
        return redirect(url_for('login'))  # 重導至登入頁面

    # 獲取數據：餐廳收益、配送訂單數量、顧客付款
    restaurant_earnings = fetch_restaurant_earnings()
    delivery_order_count = fetch_delivery_order_count()
    customer_payments = fetch_customer_payments()

    # 將數據傳遞給模板，供前端顯示
    return render_template(
        'platform.html',
        restaurant_earnings=restaurant_earnings,
        delivery_order_count=delivery_order_count,
        customer_payments=customer_payments
    )

# 查看所有配送訂單
@app.route('/delivery_orders')
def view_delivery_orders():
    # 檢查使用者是否已登入
    if 'user_id' not in session:
        flash('請先登入。')  # 如果未登入，顯示提示訊息
        return redirect(url_for('login'))  # 重導至登入頁面

    # 從資料庫查詢配送訂單，結合送貨員、餐廳和顧客的相關數據
    orders = db.session.query(
        Item.I_id,  # 訂單ID
        Item.D_id,  # 外送員ID
        Item.D_pickup_time,  # 取餐時間
        Item.D_delivery_time,  # 配送完成時間
        Item.status,  # 訂單狀態
        DeliveryPerson.D_name,  # 外送員名稱
        Restaurant.R_address.label('restaurant_address'),  # 餐廳地址
        Customer.C_address.label('customer_address'),  # 顧客地址
        Item.price  # 訂單總價
    ).outerjoin(DeliveryPerson, Item.D_id == DeliveryPerson.D_id) \
     .outerjoin(Restaurant, Item.R_id == Restaurant.R_id) \
     .outerjoin(Customer, Item.C_id == Customer.C_id) \
     .all()

    # 轉換查詢結果為字典列表，以便傳遞到模板
    orders_list = []
    for order in orders:
        orders_list.append({
            'I_id': order.I_id,
            'D_id': order.D_id if order.D_id else "未指派",
            'D_name': order.D_name if order.D_name else "未指派",
            'restaurant_address': order.restaurant_address if order.restaurant_address else "未提供",
            'customer_address': order.customer_address if order.customer_address else "未提供",
            'D_pickup_time': order.D_pickup_time if order.D_pickup_time else "未取貨",
            'D_delivery_time': order.D_delivery_time if order.D_delivery_time else "未完成",
            'status': order.status,
            'price': order.price  # 加入靜態價格
        })
    
    # 傳遞訂單列表給模板
    return render_template('delivery_orders.html', orders=orders_list)

# 接受配送訂單
@app.route('/accept_order/<int:item_id>', methods=['POST'])
def accept_order(item_id):
    # 檢查使用者是否已登入
    if 'user_id' not in session:
        flash('請先登入。')  # 如果未登入，顯示提示訊息
        return redirect(url_for('login'))  # 重導至登入頁面

    # 獲取當前登入的外送員帳戶
    delivery_account = session.get('username')
    delivery_person = DeliveryPerson.query.filter_by(A_account=delivery_account).first()

    if not delivery_person:
        # 若找不到外送員資料，提示用戶編輯個人資料
        flash('無法找到外送員資料，請先編輯個人資料。')
        return redirect(url_for('edit_delivery_info'))

    # 查詢指定的訂單
    item = db.session.query(Item).filter_by(I_id=item_id).first()

    if item and item.status == '待接單':  # 確認訂單狀態是否可接單
        # 查詢菜品價格，計算總價
        menu_item = Menu.query.filter_by(M_id=item.M_id).first()
        if menu_item:
            item.price = menu_item.M_price * item.I_quantity

        # 更新訂單狀態和外送員資訊
        item.status = '配送中'
        item.D_id = delivery_person.D_id
        item.D_pickup_time = datetime.now()  # 設定取餐時間
        db.session.commit()  # 提交更改
        flash('訂單已由您接單！')  # 提示用戶接單成功
    else:
        flash('無法接單，可能已被接走或不符合條件。')

    # 重導至配送訂單列表頁面
    return redirect(url_for('view_delivery_orders'))

# 完成配送訂單
@app.route('/complete_order/<int:item_id>', methods=['POST'])
def complete_order(item_id):
    # 查詢指定的訂單
    item = Item.query.get(item_id)
    if item and item.status == '配送中':  # 確認訂單是否在配送中
        # 更新訂單狀態和完成時間
        item.status = '已完成'
        item.D_delivery_time = datetime.now()  # 設定配送完成時間
        db.session.commit()  # 提交更改
        flash('配送完成！')  # 提示用戶配送完成
    else:
        flash('無法完成，可能尚未接單或已完成。')

    # 重導至配送訂單列表頁面
    return redirect(url_for('view_delivery_orders'))

# 外送員新增/更新資料
@app.route('/edit_delivery_info', methods=['GET', 'POST'])
def edit_delivery_info():
    # 檢查使用者是否已登入
    if 'user_id' not in session:
        flash('請先登入。')  # 如果未登入，顯示提示訊息
        return redirect(url_for('login'))  # 重導至登入頁面

    # 獲取當前登入的外送員帳戶
    delivery_account = session.get('username')
    delivery_person = DeliveryPerson.query.filter_by(A_account=delivery_account).first()

    if request.method == 'POST':  # 如果提交表單
        # 獲取表單中的姓名和電話號碼
        name = request.form.get('D_name')
        phone = request.form.get('D_phone')

        if not name or not phone:  # 驗證是否填寫所有欄位
            flash("請填寫所有欄位")
            return redirect(url_for('edit_delivery_info'))

        if delivery_person:  # 如果外送員資料已存在，則更新
            delivery_person.D_name = name
            delivery_person.D_phone = phone
        else:  # 如果外送員資料不存在，則新增
            delivery_person = DeliveryPerson(
                D_name=name,
                D_phone=phone,
                A_account=delivery_account
            )
            db.session.add(delivery_person)

        db.session.commit()  # 提交更改
        flash("個人資料已成功儲存！")  # 提示用戶資料儲存成功
        return redirect(url_for('view_delivery_orders'))  # 重導至訂單列表頁面

    # 顯示外送員資料編輯頁面
    return render_template('edit_delivery_info.html', delivery_person=delivery_person)


#商家
@app.route("/myMenu") 
def myMenus():
    A_account = session.get('username')  # 可以用user_id接到R_id ??? 還是要用db語法連??
    dat=my_Menu(A_account) #連到DB，印出特定R_ID商品
    return render_template('/mymanuUI.html',data=dat)

@app.route('/addgood.html')
def addgood():
    return render_template('addgood.html')


@app.route('/addgoods', methods=['POST'])
def add_goods():
    if request.method == 'POST':
        # 從表單獲取商品資料
        form = request.form
        name = form.get('name')
        content = form.get('description')
        price = form.get('price')
        
        # 從 session 獲取 A_account
        A_account = session.get('username')
        if not A_account:
            return "未登入，無法新增商品", 403

        # 根據 A_account 獲取 R_id
        R_id = get_rid_by_account(A_account)
        if not R_id:
            return "無法找到對應餐廳，請檢查資料", 404

        # 呼叫資料庫函數新增商品
        add_menu_item(R_id, name, content, price)
        return redirect('/myMenu')


@app.route('/delete', methods=['GET']) 
def delete_job():
	if request.method == 'POST':
		form =request.form
	else:
		form= request.args
	id = form.get('M_id') 
	delete(id)
	return redirect("/myMenu")


@app.route('/edit/<int:M_id>', methods=['GET'])#botton用GET傳送參數
def edit_good(M_id):
    menu = get_menu_by_id(M_id)
    if menu:
        return render_template('editUI.html', menu=menu)
    else:
        return "商品不存在", 404
	
@app.route('/update_good', methods=['POST'])
def update_goods():
    if request.method == 'POST':
        form = request.form
        M_id = form.get('Mid')
        name = form.get('Mname')
        content = form.get('Mdescription')
        price = form.get('Mprice')
        # 更新商品資料
        updategood(name, content, price, M_id)
    return redirect('/myMenu')

@app.route('/orders', methods=['GET'])
def view_orders():
    # 獲取商家 ID
    A_account = session.get('username')  # 假設商家 ID 存在 session
    if not A_account:
        return "未登入，請先登入", 403
    # 查詢訂單
    orders = get_orders_by_restaurant(A_account)
    return render_template('showOrder.html', orders=orders)

@app.route('/order/<int:O_id>') #orderDetail
def order_detail(O_id):
    orders, items = get_order_details(O_id)
    print(orders)
    if not orders:
        print(orders)

        return "訂單不存在", 404
    return render_template('OrderDetail.html', orders=orders, items=items)

@app.route('/accepting_order/<int:O_id>', methods=['POST'])
def accept_orders(O_id):
    update_accepted_status(O_id, 'accepted')
    return redirect('/orders')

@app.route('/reject_order/<int:O_id>', methods=['POST'])
def reject_orders(O_id):
    update_rejected_status(O_id, 'rejected')
    return redirect('/orders')

@app.route('/notify_ready/<int:O_id>', methods=['POST'])
def notifyready(O_id):
    update_order_status(O_id, 'ready')
    return redirect('/orders')

@app.route('/merchant_home')
def merchantHome():
    # 從 session 獲取 A_account
    A_account = session.get('username')
    if not A_account:
        return redirect('/login')  # 若未登入，跳轉至登入頁面

    # 調用資料庫函數獲取數據
    stats = get_merchant_daily_stats(A_account)

    # 渲染數據到前端模板
    return render_template(
        'merchant_home.html',
        accepted_count=stats['accepted_count'],
        rejected_count=stats['rejected_count'],
        total_income=stats['total_income'] or 0  # 避免 None 值
    )

@app.route('/edit_merchant_info', methods=['GET', 'POST'])
def edit_merchant_info():
    if 'user_id' not in session:
        flash('請先登入。')
        return redirect(url_for('login'))
    
    merchant_account = session.get('username')
    merchant_persoon = Restaurant.query.filter_by(A_account=merchant_account).first()

    if request.method == 'POST':
        name = request.form.get('R_name')
        address = request.form.get('R_address')
        phone = request.form.get('R_phone')

        if not name or not phone:
            flash("請填寫所有欄位")
            return redirect(url_for('edit_merchant_info'))

        if merchant_persoon:
            merchant_persoon.R_name = name
            merchant_persoon.R_address = address
            merchant_persoon.R_phone = phone
        else:
            merchant_persoon = Restaurant(
                R_name=name,
                R_address = address,
                R_phone=phone,
                A_account=merchant_account
            )
            db.session.add(merchant_persoon)

        db.session.commit()
        flash("個人資料已成功儲存！")
        return redirect(url_for('merchantHome'))

    return render_template('edit_merchant_info.html', merchant_persoon=merchant_persoon)


# 顧客新增/更新資料
@app.route('/edit_customer_info', methods=['GET', 'POST'])
def edit_customer_info():
    if 'user_id' not in session:
        flash('請先登入。')
        return redirect(url_for('login'))
    
    customer_account = session.get('username')
    customer_person = Customer.query.filter_by(A_account=customer_account).first()

    if request.method == 'POST':
        name = request.form.get('C_name')
        address = request.form.get('C_address')
        phone = request.form.get('C_phone')

        if not name or not phone:
            flash("請填寫所有欄位")
            return redirect(url_for('edit_customer_info'))

        if customer_person:
            customer_person.C_name = name
            customer_person.C_address = address
            customer_person.C_phone = phone
        else:
            customer_person = Customer(
                C_name=name,
                C_address = address,
                C_phone=phone,
                A_account=customer_account
            )
            db.session.add(customer_person)

        db.session.commit()
        flash("個人資料已成功儲存！")
        session.clear()
        return redirect(url_for('login'))

    return render_template('edit_customer_info.html', customer_person=customer_person)





# 顧客主頁
@app.route('/customer_home' ,methods=['GET', 'POST'])
def customer_home():
    # 假設顧客已經登入，並從 session 取得顧客ID
    user_id = session.get('user_id')
    print("userid是",user_id)
    if not user_id:
        return redirect(url_for('login'))

    if 'C_id' not in session:
        session['C_id'] = get_customer_id(user_id)
        if not session['C_id']:
            print("找不到C_id")
            flash('無法取得顧客資訊')
            return redirect(url_for('login'))

     # 從 session 中取得 C_id
    C_id = session.get('C_id')

    # Print 檢查 C_id 的值
    print(f"Debug: C_id = {C_id}")

    # 取得所有餐廳
    restaurants = fetch_restaurants()
    return render_template('customer_home.html', restaurants=restaurants)

@app.route('/restaurant/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurant_menu(restaurant_id):
    # 查詢該餐廳的資訊
    restaurant = fetch_one("SELECT * FROM restaurant WHERE R_id = %s", (restaurant_id,))
    
    if not restaurant:
        # 若查無此餐廳，返回 404
        return "Restaurant not found", 404

    # 查詢該餐廳的菜單項目
    menu_items = fetch_menu_items(restaurant_id)
    
    # 傳遞餐廳資訊與菜單項目到模板
    return render_template('menu.html', menu_items=menu_items, restaurant=restaurant)
    

@app.route('/restaurant/<int:restaurant_id>/add_to_cart', methods=['POST'])
def add_to_cart_route(restaurant_id):
    customer_id = session.get('C_id')
    if not customer_id:
        flash("請先登入！")
        return redirect(url_for('login'))

    quantity = request.form.get('quantity')
    menu_id = request.form.get('menu_id')

    print(f"Received form data: quantity={quantity}, menu_id={menu_id}, customer_id={customer_id}")

    if not quantity or not menu_id:
        flash("請提供有效的菜品數量和菜品 ID。")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))

    try:
        quantity = int(quantity)  # 確保 quantity 是整數
        menu_id = int(menu_id)  # 確保 menu_id 是整數
        add_to_cart(customer_id, restaurant_id, menu_id, quantity)
        flash("菜品已成功加入購物車！")
    except ValueError as ve:
        flash(f"數量或菜品 ID 無效: {ve}")
        print(f"Invalid quantity or menu_id: {ve}")
    except Exception as e:
        flash(f"加入購物車時發生錯誤：{e}")
        print(f"Error adding to cart: {e}")

    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))

@app.route('/view_cart', methods=['GET'])
def view_cart():
    user_id = session.get('user_id')
    C_id = session.get('C_id')
    print(f"Session user_id: {user_id}")  # Debug print

    if not user_id:
        return redirect(url_for('login'))

    # 取得顧客的購物車項目
    cart_items = fetch_cart_items(C_id)

    print(f"Cart items: {cart_items}")  # Debug print


    # 如果購物車為空，回傳提示並導回主頁
    if not cart_items:
        flash("購物車為空！請先選擇商品。")
        return redirect(url_for('customer_home'))
    
    # 初始化 session['cart']
    session['cart'] = [
        {
            "item_id": item["I_id"],
            "name": item["M_name"],
            "price": item["M_price"],
            "quantity": item["I_quantity"],
            "restaurant_id": item["R_id"]
        }
        for item in cart_items
    ]

    # 計算總金額
    total_price = sum(item['M_price'] * item['I_quantity'] for item in cart_items)
    
    # 印出 total_price 來確認計算結果
    print(f"Total price (calculated): {total_price}")

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)



@app.route('/update_order_id', methods=['POST'])
def update_order_id_route():
    user_id = session.get('user_id')
    C_id = session.get ('C_id')
    if not user_id:
        return redirect(url_for('login'))

    cart_items = session.get('cart', [])
    if not cart_items:
        flash("購物車為空，無法提交訂單！")
        return redirect(url_for('view_cart'))

    try:
        restaurant_id = request.form.get('restaurant_id')
        total_price = request.form.get('total_price')
        #quantities = {item['item_id']: item['quantity'] for item in cart_items}

        # 新建訂單並取得 O_id
        order_id = create_order(C_id, restaurant_id, total_price)

        # 更新購物車項目的 O_id
        update_cart_items_order_id(C_id, restaurant_id, order_id)

        # 將訂單資訊存入 session 以便在確認頁面顯示
        session['order'] = {
            'order_id': order_id,
            'restaurant_id': restaurant_id,
            'total_price': total_price,
            'items': cart_items
        }

        return redirect(url_for('order_confirmation'))
    except Exception as e:
        print(f"Error: {e}")
        flash(f"更新訂單時發生錯誤：{e}")
        return redirect(url_for('view_cart'))


@app.route('/order_confirmation', methods=['GET'])
def order_confirmation():
    order = session.get('order')
    if not order:
        flash("無法找到訂單資訊！")
        return redirect(url_for('view_cart'))

    return render_template('order_confirmation.html', cart_items=order['items'], total_price=order['total_price'])

@app.route('/finalize_order', methods=['POST'])
def finalize_order_route():
    order = session.get('order')
    if not order:
        flash("無法找到訂單資訊！")
        return redirect(url_for('view_cart'))
    try:
        finalize_order_in_db(order)
        flash("訂單已成功提交！")
        session.pop('cart', None)  # 清空購物車
        session.pop('order', None)  # 清空訂單資訊
        return redirect(url_for('customer_home'))
    except Exception as e:
        print(f"Error: {e}")
        flash(f"提交訂單時發生錯誤：{e}")
        return redirect(url_for('view_cart'))



@app.route('/place_order', methods=['POST'])
def place_order_route():
    user_id = session.get('user_id')
    C_id = session.get('C_id')
    if not user_id:
        return redirect(url_for('login'))

    cart_items = session.get('cart', [])
    if not cart_items:
        flash("購物車為空，無法提交訂單！")
        print(f"購物車很空查看一下:{cart_items}")
        return redirect(url_for('view_cart'))

    grouped_items = group_cart_by_restaurant(cart_items)
    try:
        for restaurant_id, items in grouped_items.items():
            print(f"Processing restaurant_id: {restaurant_id}")
            print(f"Items for this restaurant: {items}")  # 顯示 items 是什麼
            for item in items:
                print(f"Item details: {item}")  # 顯示單個 item 的內容
    
            total_price = sum(item['price'] * item['quantity'] for item in items)
            quantities = {item['item_id']: item['quantity'] for item in items}
            print(f"Calculated quantities: {quantities}")  # 顯示 quantities

            place_order_in_db(C_id, restaurant_id, total_price, quantities)
        flash("所有訂單已成功提交！")
        session['cart'] = []  # 清空購物車
        return redirect(url_for('customer_home'))
    except Exception as e:
        print(f"Error: {e}")
        flash(f"提交訂單時發生錯誤：{e}")
        return redirect(url_for('view_cart'))



@app.route('/history')
def view_history():
    C_id = session.get('C_id')
    if not C_id:
        return redirect(url_for('login'))
    orders = fetch_user_orders(C_id)
    return render_template('history.html', orders=orders)

@app.route('/write_review/<int:O_id>')
def write_review(O_id):
    return render_template('write_review.html', O_id=O_id)

@app.route('/submit_review/<int:O_id>', methods=['POST'])
def submit_review(O_id):
    C_id = session.get('C_id')
    stars = request.form['stars']
    comment = request.form['comment']
    submit_review_to_db(O_id, C_id, stars, comment)
    flash('評論提交成功！')
    return redirect(url_for('view_history'))

@app.route('/view_review/<int:O_id>')
def view_review(O_id):
    review = fetch_review(O_id)
    return render_template('view_review.html', review=review)