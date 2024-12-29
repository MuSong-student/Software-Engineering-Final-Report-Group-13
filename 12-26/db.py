import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import session
from mysql.connector import connect
from collections import defaultdict



# 初始化資料庫
db = SQLAlchemy()

# 連接到資料庫的函數
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # 依照實際設定填入你的資料庫密碼
        port=3306,  # 連接的資料庫端口號，預設為 3306
        database="foodpangolin"  # 要連接的資料庫名稱
    )

# 執行更新、插入或刪除操作的函數
def execute_query(query, params=()):
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, params)
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

# 獲取單行結果的函數
def fetch_one(query, params=None):
    """執行 SELECT 查詢，返回單個結果"""
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)  # 確保返回字典
    
    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result is None:
            print("查詢未返回任何結果")
        else:
            print(f"查詢結果: {result}")
        return result
    except Exception as e:
        print(f"發生錯誤: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()


def fetch_all(query, params=None):
    """執行 SELECT 查詢，返回所有結果"""
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Exception as e:
        raise e
    finally:
        cursor.close()
        connection.close()

# 驗證用戶的函數
def validate_user(username, password, role=None):
    """
    驗證用戶是否存在並返回匹配的用戶記錄
    :param username: 用戶名 (帳戶)
    :param password: 密碼
    :param role: 用戶角色 (可選)
    :return: 用戶記錄 (字典形式) 或 None
    """
    query = "SELECT * FROM account WHERE A_account = %s AND A_password = %s"
    params = [username, password]

    if role:
        query += " AND A_role = %s"
        params.append(role)

    print(f"Executing query: {query}")  # 調試用，記得在生產環境中移除或替換為日誌
    print(f"Parameters: {params}")      # 同上

    # 執行查詢並返回結果
    user = fetch_one(query, tuple(params))
    if user:
        print(f"用戶驗證成功: {user}")
    else:
        print("用戶驗證失敗，無匹配記錄。")
    
    return user

def fetch_restaurant_earnings():
    query = """
        SELECT r.R_name AS restaurant_name, SUM(m.M_price * i.I_quantity) AS total_earnings
        FROM item i
        JOIN menu m ON i.M_id = m.M_id
        JOIN restaurant r ON m.R_id = r.R_id
        WHERE DATE(i.time) = CURDATE()
        GROUP BY r.R_id, r.R_name
    """
    return fetch_all(query)

def fetch_delivery_order_count():
    query = """
        SELECT d.D_name AS delivery_name, COUNT(i.I_id) AS order_count
        FROM item i
        JOIN delivery d ON i.D_id = d.D_id
        WHERE DATE(i.time) = CURDATE()
        GROUP BY d.D_id, d.D_name
    """
    return fetch_all(query)

def fetch_customer_payments():
    query = """
        SELECT c.C_name AS customer_name, SUM(m.M_price * i.I_quantity) AS total_payment
        FROM item i
        JOIN menu m ON i.M_id = m.M_id
        JOIN customer c ON i.C_id = c.C_id
        WHERE DATE(i.time) = CURDATE()
        GROUP BY c.C_id, c.C_name
    """
    return fetch_all(query)



def fetch_restaurants():
    query = "SELECT * FROM restaurant"
    return fetch_all(query)

def fetch_menu_items(restaurant_id):
    query = "SELECT * FROM menu WHERE R_id = %s"
    return fetch_all(query, (restaurant_id,))

def add_to_cart(customer_id, restaurant_id, menu_id, quantity):
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)  # 確保返回字典

    try:
        query = "SELECT M_price FROM menu WHERE M_id = %s"
        cursor.execute(query, (menu_id,))
        result = cursor.fetchone()
        print(f"Query result: {result}")  # 打印查詢結果

        if result:
            price = result['M_price']
            print(f"Price fetched for menu_id={menu_id}: {price}")
        else:
            raise ValueError("無法獲取菜品價格")


        print(customer_id)

        total_price = price * int(quantity)
        print(f"Calculated total price: {total_price}")

        query = """
            INSERT INTO item (R_id, C_id, D_id, M_id, I_quantity, status, time, D_pickup_time, D_delivery_time, price)
            VALUES (%s, %s, NULL, %s, %s, %s, NOW(), NULL, NULL, %s)
        """
        cursor.execute(query, (
            restaurant_id,
            customer_id,
            menu_id,
            quantity,
            '待接單',
            total_price
        ))
        connection.commit()
        print("Item successfully inserted into the database.")

        
        cart = session.get('cart', [])
        cart.append({
            'item_id': cursor.lastrowid,  
            'restaurant_id': restaurant_id,
            'menu_id': menu_id,
            'quantity': quantity,
            'price': price,
        })
        session['cart'] = cart

    except Exception as e:
        connection.rollback()
        print(f"Error in add_to_cart: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

# 查詢購物車中的項目
def fetch_cart_items(C_id):
    query = """
        SELECT i.I_id, m.M_name, m.M_price, i.I_quantity ,i.R_id
        FROM item i
        JOIN menu m ON i.M_id = m.M_id
        WHERE i.C_id = %s AND i.status = '待接單'
    """
    print("現在再找",C_id)
    return fetch_all(query, (C_id,))

def group_cart_by_restaurant(cart_items):
    grouped = defaultdict(list)
    for item in cart_items:
        grouped[item['restaurant_id']].append(item)
        print(f"Grouped cart items: {grouped}")

    return grouped



def get_customer_id(user_id):
    query = "SELECT A_account FROM account WHERE A_id = %s"
    account_result = fetch_one(query, (user_id,))
    if not account_result:
        return None
    print("這是result",account_result)

    A_account = account_result['A_account']

    query = "SELECT C_id FROM customer WHERE A_account = %s"
    customer_result = fetch_one(query, (A_account,))
    print("這是c_RESULT",customer_result)
    return customer_result['C_id'] if customer_result else None


def remove_item_from_cart(item_id):
    """從購物車中移除特定項目"""
    connection = connect_db()
    cursor = connection.cursor()
    query = "DELETE FROM item WHERE I_id = %s"
    cursor.execute(query, (item_id,))
    connection.commit()
    cursor.close()
    connection.close()



def create_order(C_id, restaurant_id, total_price):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        orders_query = """
            INSERT INTO orders (R_id, C_id, total_price, status, time)
            VALUES (%s, %s, %s, 'pending', NOW())
        """
        cursor.execute(orders_query, (restaurant_id, C_id, total_price))
        order_id = cursor.lastrowid
        connection.commit()
        return order_id
    except Exception as e:
        connection.rollback()
        print(f"Error creating order: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def update_cart_items_order_id(C_id, restaurant_id, order_id):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        update_cart_query = """
            UPDATE item
            SET O_id = %s
            WHERE C_id = %s AND R_id = %s AND status = '待接單'
        """
        cursor.execute(update_cart_query, (order_id, C_id, restaurant_id))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating cart items: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def finalize_order_in_db(order):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        order_id = order['order_id']
        restaurant_id = order['restaurant_id']
        user_id = session.get('user_id')
        items = order['items']

        for item in items:
            item_id = item['item_id']
            menu_id = item['menu_id']
            quantity = item['quantity']
            price = item['price']

            detail_query = """
                INSERT INTO order_details (O_id, M_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(detail_query, (order_id, item_id, quantity, price * quantity))

        # 更新訂單狀態
        update_order_query = """
            UPDATE orders
            SET status = 'confirmed'
            WHERE O_id = %s
        """
        cursor.execute(update_order_query, (order_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error finalizing order: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()


# 提交訂單並將其保存到 orders 資料表
def place_order_in_db(C_id,user_id, restaurant_id, total_price, quantities):
    connection = connect_db()
    cursor = connection.cursor()
    print(C_id,user_id, restaurant_id, total_price, quantities)
    

    try:
        # 插入訂單總表
        orders_query = """
            INSERT INTO orders (R_id, C_id, total_price, status, time)
            VALUES (%s, %s, %s,'pending', NOW())
        """
        cursor.execute(orders_query, (restaurant_id, C_id, total_price))
        order_id = cursor.lastrowid
        print(f"New order created with O_id: {order_id}")

        # 在這裡更新購物車項目的 O_id 為新創建的訂單 ID
        update_cart_query = """
            UPDATE item
            SET O_id = %s
            WHERE C_id = %s AND R_id = %s AND status = '待接單'
        """
        cursor.execute(update_cart_query, (order_id, user_id, restaurant_id))

        # 插入訂單詳細表
        for item_id, quantity in quantities.items():
            # 獲取菜品詳細信息
            query_price = "SELECT M_price FROM menu WHERE M_id = %s"
            cursor.execute(query_price, (item_id,))
            item_price = cursor.fetchone()['M_price']

            detail_query = """
                INSERT INTO order_details (O_id, M_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(detail_query, (order_id, item_id, quantity, item_price * quantity))

        # 清空購物車
        clear_cart_query = "DELETE FROM item WHERE C_id = %s AND R_id = %s"
        cursor.execute(clear_cart_query, (C_id, restaurant_id))

        connection.commit()
        print("Order and cart cleared successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error processing order: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def fetch_user_orders(C_id):
    query = '''
        SELECT Orders.O_id, Orders.time, 
               EXISTS (SELECT 1 FROM stars WHERE stars.O_id = Orders.O_id) AS reviewed
        FROM Orders
        WHERE Orders.C_id = %s
    '''
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='foodpangolin')
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (C_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

def submit_review_to_db(O_id, C_id, stars, comment):
    query = '''
        INSERT INTO stars (O_id, C_id, S_stars, S_comment)
        VALUES (%s, %s, %s, %s)
    '''
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='foodpangolin')
    cursor = conn.cursor()
    cursor.execute(query, (O_id, C_id, stars, comment))
    conn.commit()
    conn.close()

def fetch_review(O_id):
    query = '''
        SELECT S_stars, S_comment 
        FROM stars 
        WHERE O_id = %s
    '''
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='foodpangolin')
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (O_id,))
    review = cursor.fetchone()
    conn.close()
    return review