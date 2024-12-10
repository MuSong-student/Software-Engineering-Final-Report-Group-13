import mysql.connector #mariadb

try:
	#連線DB 若沒錯誤建立一個cursor，如有錯誤則執行底下"except"區塊，目的是不讓使用者知道有出錯
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="test"
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

def add(uid,name,content,startprice,highprice):#用參數連接
	sql="insert into goods (userid,goodname,content,startprice,highestprice) values(%s,%s,%s,%s,%s);"#sql 指令
	param=(uid,name,content,startprice,highprice)
	cursor.execute(sql,param) #執行指令
	conn.commit()
	return

def delete(id):
	sql="delete from goods where goodid=%s; "
	param=(id,) #注意後面"，" 當只有一的時候後面，才會被當list 。如果多個就不用
	cursor.execute(sql,param)
	#cursor.execute(sql,(id,))
	conn.commit() #要commit出去才會寫到DB
	return

def mygood(user_id):
	sql="select goodid,content,goodname,startprice from goods WHERE userid = %s ;"#sql 指令
	cursor.execute(sql,(user_id,))
	return cursor.fetchall()#結果用"fetchall"把牠撈出來

def allgood():
	sql="select goodid,goodname,highestprice from goods ;"
	cursor.execute(sql) #查詢結果回傳回去CALL我的這個人
	return cursor.fetchall() #把結果全部印出來

def get_good_by_id(good_id):
    sql = "SELECT goodid, goodname, content, startprice FROM goods WHERE goodid = %s;"
    cursor.execute(sql, (good_id,))
    return cursor.fetchone()

def updategood(good_id, name, content, startprice,highestprice):
    try:
        sql = "UPDATE goods SET goodname = %s, content = %s, startprice = %s,highestprice=%s WHERE goodid = %s;"
        params = (name, content, startprice,highestprice, good_id)  # 注意參數順序
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
    

def update_bid(good_id, bidder, bid_price):#更新最高價，及匯入新的競標紀錄
    try:
        sql_update_good = "UPDATE goods SET highestprice = %s WHERE goodid = %s;"
        sql_insert_bid = "INSERT INTO bid (goodid, userid, bidprice) VALUES (%s, %s, %s);"
        
        cursor.execute(sql_update_good, (bid_price, good_id))
        cursor.execute(sql_insert_bid, (good_id, bidder, bid_price))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error updating bid: {e}")
        conn.rollback()
    except Exception as e:
        print(f"General Error: {e}")

