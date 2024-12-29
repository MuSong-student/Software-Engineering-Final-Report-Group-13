import mysql.connector #mariadb

try:
	#連線DB 若沒錯誤建立一個cursor，如有錯誤則執行底下"except"區塊，目的是不讓使用者知道有出錯
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="foodpangolin"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e) #把錯誤訊息印出來
	print("Error connecting to DB")
	exit(1) #錯誤代碼
	

def login(uid, upwd):
    # SQL 查詢
    query = "SELECT * FROM user WHERE uid = %s AND pwd = %s"
    cursor.execute(query, (uid, upwd))
    user = cursor.fetchone()
	#獲取查詢結果的第一行資料，並將其存儲在 user 變數中。如果查詢沒有匹配的用戶，user 將是 None。這個操作實際上是將資料庫返回的用戶資料讀取到 Python 中。
    return user

def get_rid_by_account(A_account):
    sql = "SELECT R_id FROM restaurant WHERE A_account = %s;"
    cursor.execute(sql, (A_account,))
    result = cursor.fetchone()
    if result:
        return result['R_id']
    return None



def add_menu_item(R_id, name, content, price):
    try:
        sql = """
            INSERT INTO menu (M_name, M_description, M_price, R_id) 
            VALUES (%s, %s, %s, %s);
        """
        params = (name, content, price, R_id)
        cursor.execute(sql, params)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"新增商品失敗: {e}")
        conn.rollback()


def delete(id):
	sql="delete from menu where M_id=%s; "
	param=(id,) #注意後面"，" 當只有一的時候後面，才會被當list 。如果多個就不用
	cursor.execute(sql,param)
	#cursor.execute(sql,(id,))
	conn.commit() #要commit出去才會寫到DB
	return

def my_Menu(A_account):
	sql="""
        SELECT m.M_id, m.M_name, m.M_price, m.M_description FROM menu m
        JOIN restaurant r ON m.R_id = r.R_id
        JOIN account a ON r.A_account = a.A_account
        WHERE a.A_account = %s;
        """#sql 指令
	cursor.execute(sql,(A_account,))
	return cursor.fetchall()#結果用"fetchall"把牠撈出來


def get_menu_by_id(M_id):
    sql = "SELECT M_id, M_name, M_description, M_price FROM menu WHERE M_id = %s;"
    cursor.execute(sql, (M_id,))
    return cursor.fetchone()

def updategood(name, content, price, M_id):
    try:
        sql = "UPDATE menu SET M_name = %s, M_description = %s, M_price = %s WHERE M_id = %s;"
        params = (name, content, price, M_id)  # 注意參數順序
        cursor.execute(sql, params)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error updating record: {e}")
        conn.rollback()

def get_good_details(good): #印出價紀錄及詳情
    sql = """
    SELECT goodid, goodname, content, startprice, highestprice
    FROM goods WHERE goodid = %s;
    """
    cursor.execute(sql, (good,))
    good_details = cursor.fetchone() 
    #設變數才可以一次回傳兩個東西
    
    sql_bid = "SELECT userid, bidprice FROM bid WHERE goodid = %s ORDER BY bidprice DESC;"
    #印出出價紀錄
    cursor.execute(sql_bid, (good,))
    bid_records = cursor.fetchall()
    return good_details, bid_records
    
def get_orders_by_restaurant(A_account):
    sql = """
        SELECT o.O_id, o.total_price, o.status, o.time FROM `orders` o
        JOIN restaurant r ON o.R_id = r.R_id
        JOIN account a ON r.A_account = a.A_account
        WHERE a.A_account = %s
        ORDER BY time DESC;
        """
    cursor.execute(sql, (A_account,))
    return cursor.fetchall()

def update_accepted_status(O_id, status):
    try:
        sql = "UPDATE `orders` SET status = %s WHERE O_id = %s;"
        cursor.execute(sql, (status, O_id))

        # 更新 item 表的 status 為 '已拒單'
        sql_items = "UPDATE `item` SET status = %s, time = NOW() WHERE O_id = %s;"
        cursor.execute(sql_items, ('待接單', O_id))

        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error updating order status: {e}")
        conn.rollback()

def update_rejected_status(O_id, status):
    try:
        # 更新 orders 表的 status
        sql_orders = "UPDATE `orders` SET status = %s WHERE O_id = %s;"
        cursor.execute(sql_orders, (status, O_id))

        # 更新 item 表的 status 為 '已拒單'
        sql_items = "UPDATE `item` SET status = %s, time = NOW() WHERE O_id = %s;"
        cursor.execute(sql_items, ('商家已拒單', O_id))

        # 提交更改
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error updating order status: {e}")
        conn.rollback()

def update_order_status(O_id, status):
    try:
        sql = "UPDATE orders SET status = %s WHERE O_id = %s;"
        cursor.execute(sql, (status, O_id))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error updating order status: {e}")
        conn.rollback()

def get_merchant_daily_stats(A_account):
    sql = """
        SELECT 
            COUNT(CASE WHEN o.status = 'ready' THEN 1 END) AS accepted_count,
            COUNT(CASE WHEN o.status = 'rejected' THEN 1 END) AS rejected_count,
            SUM(CASE WHEN o.status = 'ready' THEN o.total_price ELSE 0 END) AS total_income
        FROM orders o
        JOIN restaurant r ON o.R_id = r.R_id
        WHERE r.A_account = %s 
          AND DATE(o.time) = CURDATE();
    """
    cursor.execute(sql, (A_account,))
    return cursor.fetchone()

def get_order_details(O_id):
    try:
        # 查詢訂單的基本資訊
        order_sql = """
        SELECT 
            o.O_id AS order_id,
            o.total_price,
            o.status AS order_status,
            o.time AS order_time,
            c.C_name AS customer_name,
            c.C_address AS customer_address,
            c.C_phone AS customer_phone
        FROM `orders` o
        JOIN `customer` c ON c.C_id = (
            SELECT i.C_id FROM `item` i WHERE i.O_id = o.O_id LIMIT 1
        )
        WHERE o.O_id = %s;
        """
        cursor.execute(order_sql, (O_id,))
        orders = cursor.fetchone()

        if not orders:
            return None, None

        # 查詢商品列表
        items_sql = """
        SELECT 
            m.M_name AS item_name,
            i.I_quantity AS item_quantity,
            i.price AS item_price
        FROM `item` i
        JOIN `menu` m ON i.M_id = m.M_id
        WHERE i.O_id = %s;
        """
        cursor.execute(items_sql, (O_id,))
        items = cursor.fetchall()

        return orders, items

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None, None




