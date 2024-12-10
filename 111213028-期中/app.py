from flask import Flask, request,render_template, session, redirect
from functools import wraps
from databass import mygood,allgood,login,add,delete,get_good_by_id,updategood,get_good_details,update_bid # type: ignore
#Test
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):#"wrapper"包裝原始函數f
        # *args 和 **kwargs 是為了讓 wrapper 能夠接受任意數量的位置參數和關鍵字參數
		loginID = session.get('loginID') #將ID存到session
		if not loginID:
			return redirect('/loginui.html')        
		return f(*args, **kwargs)
        #如果 loginID 存在（即用戶已登入），則繼續執行原始函數 f
	return wrapper

#another way to check login session
def isLogin():
	return session.get('loginID')
'''
@app.route("/")
#check login with decorator function
@login_required
def hello(): 
	message = "Hello, World 1"
	return message
'''

@app.route('/', methods=['GET', 'POST']) #login
def login_user():
    if request.method == 'POST':
        form = request.form
        uid = form.get('ID')
        upwd = form.get('PWD')
        # 使用 databass.py 中的 login 函數
        user = login(uid, upwd)
        # 驗證帳號密碼是否正確
        if user:
            session['loginID'] = user['uid']  # 保存用戶ID到 session
            return redirect("/myselfgood")
        else:
            session['loginID'] = False
            return redirect("/loginui.html")
    return redirect("/loginui.html")

@app.route('/logout')
def logout():
    # 清除Session中的登入資訊，"None"避免讓loginID不存在時出現錯誤，也就是可接受logid或none這兩個值
    session.pop('loginID', None)
    return redirect('/loginui.html')

@app.route("/myselfgood") #@app....為定義網址
@login_required
#使用server side render: template 樣板
def gl():
    user_id = session.get('loginID')  # 獲取登入用戶的ID
    dat=mygood(user_id) #連到DB，印出特定UserID商品
    return render_template('/myselfgoodUI.html',data=dat)

@app.route("/allgood") 
@login_required
def all():
	dat=allgood() #db顯示 #印出所有商品
	return render_template('/allgoodUI.html', data=dat) 

@app.route('/addgoods',methods=['post'])
@login_required
def addgood():
	if request.method == 'POST':
		form =request.form
	else:
		form= request.args
	uid=session.get('loginID') #獲取ID
	name = form['name']
	content=form['description']
	startprice=form['startprice']
	highestprice=form['startprice']
	add(uid,name,content,startprice,highestprice)#DB執行updat
	return redirect("/myselfgood")

@app.route('/delete', methods=['GET']) 
@login_required
def delete_job():
	if request.method == 'POST':
		form =request.form
	else:
		form= request.args
	id = form.get('goodid') 
	delete(id)
	return redirect("/myselfgood")


@app.route('/edit/<int:good_id>', methods=['GET'])#botton用GET傳送參數
@login_required
def edit_good(good_id):
    good = get_good_by_id(good_id)
    if good:
        return render_template('editUI.html', good=good)
    else:
        return "商品不存在", 404
	
@app.route('/update_good', methods=['POST'])
def update_good():
    if request.method == 'POST':
        form = request.form
        good_id = form.get('goodid')
        name = form.get('goodname')
        content = form.get('content')
        startprice = form.get('startprice')
        highestprice = form.get('startprice')
        # 更新商品資料
        updategood(good_id, name, content, startprice,highestprice)
    return redirect('/myselfgood')

@app.route('/bid/<int:good_id>', methods=['Get','POST'])
@login_required
def bid(good_id):
    if request.method == 'POST':
        form = request.form
    else:
        form= request.args    
    bid_price = int(form.get('bidprice'))#因為底下要比較，所以要轉成int
    bidder = session.get('loginID')
    good, _ = get_good_details(good_id)#要先獲得詳細訊息，底下才能比較
    # 檢查新價格是否高於現有最高價和底價
    if good and bid_price > max(good['highestprice'], good['startprice']):
        #good 必须存在（即物品存在）。
        #bid_price 必须高于当前最高价和起始价中的较大值。
        update_bid(good_id, bidder, bid_price) #更新
        return redirect(f'/auction/{good_id}') 
         # f表示“格式化字符串”，因為反回特定路由一定要字串
    else:
        return "出價必須高於目前最高價和底價", 400
        
@app.route('/auction/<int:good_id>', methods=['GET']) #詳情及競標
@login_required
def auction_details(good_id):
    good, bid = get_good_details(good_id)
    if good:
        return render_template('bidrecordeUI.html', good=good, bid=bid)
    else:
        return "拍賣品不存在", 404
