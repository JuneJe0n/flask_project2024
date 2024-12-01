from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import DBhandler
import hashlib
import os

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

# Initialize an empty list to store item data
items = []

@application.route("/")
def Hello():
    return render_template("index.html")

@application.route("/mypage")
def mypage():
    return render_template("mypage.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('Hello'))

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_ = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    user = DB.find_user(id_, pw_hash)  # 사용자 데이터 가져오기

    if user:  # 사용자가 존재하면 로그인 성공
        session['id'] = user['id']
        session['nickname'] = user['nickname']
        session['email'] = user['email']
        flash(f"Welcome, {user['nickname']}!")
        return redirect(url_for('view_list'))
    else:  # 사용자 없으면 로그인 실패
        flash("Wrong ID or Password!")
        return redirect(url_for('login'))



@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        flash("Registration successful! Please log in.")
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")

@application.route("/check_id")
def check_id():
    id_to_check = request.args.get("id")
    if DB.user_duplicate_check(id_to_check):
        return jsonify({"available": True})
    else:
        return jsonify({"available": False})

@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page = 8  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    data = DB.get_items()  # read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):  # last row
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:(i + 1) * per_row])

    finalprices = {}
    if data:
        for key, item in data.items():
            price = float(item.get('price', 0))
            discount = float(item.get('discount', 0))
            finalprice = int(price * (100 - discount) * 0.01)
            finalprices[key] = finalprice


    # 이후 finalprices를 템플릿에 넘길 수 있습니다.
    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts / per_page) + 1),
        total=item_counts,
        finalprices=finalprices  # 템플릿으로 finalprices 전달
    )



@application.route('/dynamicrul/<varible_name>/')
def DynamicUrl(varible_name):
    return str(varible_name)

@application.route("/detail")
def view_itemdetail():
    return render_template("detail.html")

@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)

    price = float(data['price'] or 0)
    discount = float(data['discount'] or 0)

    finalprice = int(price * (100 - discount) * 0.01)

    return render_template("detail.html", name=name, data=data, finalprice=finalprice)


@application.route("/review_page")
def view_review_page():
    return render_template("review_page.html")

@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    data = DB.get_item_byname(str(name))
    return render_template("reg_reviews.html", name=name, data=data)

@application.route("/reg_review", methods=['POST'])
def reg_review():
    data = request.form
    img_list = []

    for i in range(1, 3):
        image_file = request.files.get(f'file{i}')
        if image_file:
            image_path = f"static/images/{image_file.filename}"
            image_file.save(image_path)
            img_list.append(image_path)
    
    DB.insert_review(data, img_list)
    return render_template("review_page.html")

@application.route("/submit_item_post", methods=['POST'])
def submit_item_post():
    data = request.form
    img_list = []
    opt_list = [opt for opt in request.form.getlist('option[]') if opt.strip()]

    # 이미지 파일 저장 및 경로 리스트에 추가
    for i in range(1, 10):  # 최대 9개의 이미지를 처리
        image_file = request.files.get(f'file{i}')
        if image_file:
            image_path = f"static/images/{image_file.filename}"
            image_file.save(image_path)
            img_list.append(image_path)
    
    DB.insert_item(data['name'], data, img_list, opt_list)


    page = request.args.get("page", 0, type=int)
    per_page=8 # item count to display per page
    per_row=4 # item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_items() #read the table
    item_counts=len(data)
    data=dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else: 
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])

    finalprices = {}
    if data:
        for key, item in data.items():
            price = float(item.get('price', 0))
            discount = float(item.get('discount', 0))
            finalprice = int(price * (100 - discount) * 0.01)
            finalprices[key] = finalprice

    return render_template( 
        "list.html",
        datas=data.items(), 
        row1=locals()['data_0'].items(), 
        row2=locals()['data_1'].items(), 
        limit=per_page,
        page=page, page_count=int((item_counts/per_page)+1),
        total=item_counts,
        finalprices=finalprices)

@application.route("/search", methods=['GET'])
def search():
    # 검색어 가져오기
    keyword = request.args.get('search_kw', type=str, default='').strip()  # 'search_kw'는 검색창 input의 name
    if not keyword:  # 검색어가 비어 있으면 검색 결과 페이지로 이동
        flash("Please enter a search term.")
        return redirect(url_for('view_list'))  # 'home' 페이지로 리디렉션 (view_list 대신)

    try:
        # Firebase에서 아이템 가져오기 (DB.child("item").get() 대신 직접 가져오기)
        items = DB.get_items()  # DB에서 아이템을 가져오는 메서드 수정 필요 (DBhandler 객체에 맞게)
        filtered_items = []

        # 아이템들 중에서 검색어와 일치하는 아이템 필터링
        for item_name, item_data in items.items():  # items는 딕셔너리 형태로 반환됨
            name = item_data.get("name", "").lower()  # 아이템 이름 (소문자로 처리하여 비교)
            info = item_data.get("info", "").lower()  # 아이템 설명 (소문자로 처리하여 비교)

            # 검색어가 이름이나 설명에 포함되면 필터링
            if keyword.lower() in name or keyword.lower() in info:
                filtered_items.append(item_data)

        # 검색 결과가 있을 때
        if filtered_items:
            return render_template('search_results.html', items=filtered_items, keyword=keyword)
        else:
            flash("No items found.")
            return render_template('search_results.html', items=[], keyword=keyword)  # 검색 결과가 없으면 빈 리스트 전달
    except Exception as e:
        # 오류 처리: Firebase에서 데이터를 가져오는 중 예외가 발생한 경우
        flash(f"Error occurred while fetching items: {str(e)}")
        return render_template('search_results.html', items=[], keyword=keyword)  # 오류 발생 시 빈 리스트 전달




if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
