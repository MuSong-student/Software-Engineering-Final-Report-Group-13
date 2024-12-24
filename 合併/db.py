import mysql.connector

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
def fetch_one(query, params=()):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        db.close()

# 獲取多行結果的函數
def fetch_all(query, params=()):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        db.close()

# 驗證用戶的函數
def validate_user(username, password, role=None):
    query = "SELECT * FROM account WHERE A_account = %s AND A_password = %s"
    params = [username, password]

    if role:
        query += " AND A_role = %s"
        params.append(role)

    print(f"Executing query: {query}")
    print(f"Parameters: {params}")

    return fetch_one(query, tuple(params))

def fetch_restaurant_earnings():
    query = """
        SELECT r.R_name AS restaurant_name, SUM(m.M_pirce * i.I_quantity) AS total_earnings
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
        SELECT c.C_name AS customer_name, SUM(m.M_pirce * i.I_quantity) AS total_payment
        FROM item i
        JOIN menu m ON i.M_id = m.M_id
        JOIN customer c ON i.C_id = c.C_id
        WHERE DATE(i.time) = CURDATE()
        GROUP BY c.C_id, c.C_name
    """
    return fetch_all(query)
