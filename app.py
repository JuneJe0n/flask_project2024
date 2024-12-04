from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import DBhandler
import hashlib
import os
import json
import math
from datetime import datetime

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

# Initialize an empty list to store item data
items = []

@application.route("/")
def Hello():
    return render_template("index.html")

@application.route('/mypage')
def mypage():
    user_id = session.get('id')
    like_items = []
    recent_items = []

    if user_id:
        hearts = DB.db.child("heart").child(user_id).get()

        if hearts.val():
            for heart in hearts.each():
                item_name = heart.key()  # 아이템 이름
                item_data = heart.val()  # 찜 데이터
                
                # 관심 데이터만 추가
                if item_data.get('interested') == 'Y':
                    like_items.append({
                        "name": item_name,
                        "image": item_data.get("image"),  # 이미지 추가
                        "data": item_data
                    })

        # 최신 아이템 4개 선택
        recent_items = like_items[-4:] if len(like_items) > 4 else like_items
    
    return render_template('mypage.html', recent_items=recent_items)

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
    category = request.args.get("category", "all")
    per_page = 8  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    if category == "all":
        data = DB.get_items()  # 모든 아이템 데이터 가져오기
    else:
        data = DB.get_items_bycategory(category)

    # 리뷰 개수를 계산하여 데이터에 추가
    for key, value in data.items():
        if "reviews" in value and isinstance(value["reviews"], dict):
            value["reviews"] = len(value["reviews"])  # 리뷰 개수로 변환
        else:
            value["reviews"] = 0  # 리뷰가 없으면 0으로 설정

    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=False))  # 상품명 기준 정렬
    item_counts = len(data)

    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)

    for i in range(row_count):  # 마지막 행 처리
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

    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts / per_page)),
        total=item_counts,
        finalprices=finalprices,  # 템플릿으로 finalprices 전달
        category=category
    )



@application.route("/myitems")
def view_myitems():
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    per_page = 8  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    current_user = session.get('nickname')  # 현재 사용자 확인

    if category == "all":
        data = DB.get_items()  # 모든 아이템 가져오기
    else:
        data = DB.get_items_bycategory(category)  # 카테고리별 아이템 가져오기

    # seller가 session['nickname']과 일치하는 데이터만 필터링
    if current_user:
        data = {key: value for key, value in data.items() if value.get('seller') == current_user}

    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=False))  # 상품명으로 정렬
    item_counts = len(data)

    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)

    for i in range(row_count):  # 마지막 행 처리
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

    return render_template(
        "myitems.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts / per_page)),
        total=item_counts,
        finalprices=finalprices,  # 템플릿으로 finalprices 전달
        category=category
    )



@application.route('/dynamicrul/<varible_name>/')
def DynamicUrl(varible_name):
    return str(varible_name)

@application.route("/detail")
def view_itemdetail():
    return render_template("detail.html")


@application.route("/review_page/<name>", methods=['GET'])
def view_review_page(name):
    # 특정 아이템의 리뷰 가져오기
    data = DB.get_item_byname(name) or {}  # 데이터가 없을 경우 빈 딕셔너리 반환
    reviews = data.get('reviews', {}).values()  # 'reviews' 키가 없는 경우 빈 리스트로 처리

    # 정렬 기준 파라미터 받기 (최신순 또는 별점순)
    sort_order = request.args.get("sort", "latest")

    # 날짜 또는 별점 기준 정렬
    try:
        if sort_order == "best":
            reviews = sorted(reviews, key=lambda r: int(r.get('star', 0)), reverse=True)
        else:
            reviews = sorted(reviews, key=lambda r: datetime.strptime(r.get('date', '1900-01-01'), '%Y-%m-%d'), reverse=True)
    except Exception as e:
        print(f"Error in sorting reviews: {e}")
        reviews = list(reviews)

    # 페이지네이션
    page = request.args.get("page", 1, type=int)
    per_page = 5
    total_reviews = len(reviews)
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_reviews)  # 범위 체크 추가
    paginated_reviews = reviews[start_idx:end_idx]

    total_pages = (total_reviews + per_page - 1) // per_page

    return render_template(
        "review_page.html",
        reviews=paginated_reviews,
        current_page=page,
        total_pages=total_pages,
        name=name,
        sort_order=sort_order  # 현재 정렬 기준 전달
    )





@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

@application.route("/reg_review", methods=['POST'])
def reg_review():
    data = request.form
    img_list = []

    for i in range(1, 3):  # 최대 2개의 이미지를 처리
        image_file = request.files.get(f'file{i}')
        if image_file:
            image_path = f"static/images/{image_file.filename}"
            image_file.save(image_path)
            img_list.append(image_path)

    # 리뷰 데이터 준비
    data = dict(data)
    data['username'] = session.get('nickname', 'unknown_user')  # 현재 로그인된 사용자 이름
    data['date'] = datetime.now().strftime("%Y-%m-%d")  # 현재 날짜 추가
    item_name = data.get('itemname')  # 리뷰가 속한 아이템 이름

    # Firebase에 리뷰 저장
    DB.insert_review(item_name, data, img_list)

    return redirect(url_for('view_item_detail', name=item_name))  # 아이템 상세 페이지로 리다이렉트


@application.route("/apply_custom_init/<name>/")
def apply_custom_init(name):
    data = DB.get_item_byname(str(name))
    return render_template("apply_custom.html", name=name, data=data)



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

@application.route("/submit_custom_post", methods=['POST'])
def submit_custom_post():
    data = request.form
    img_list = []

    # 이미지 파일 저장 및 경로 리스트에 추가
    for i in range(1, 10):  # 최대 9개의 이미지를 처리
        image_file = request.files.get(f'file{i}')
        if image_file:
            image_path = f"static/images/{image_file.filename}"
            image_file.save(image_path)
            img_list.append(image_path)
    
    DB.apply_custom(data['name'], data, img_list)

    return render_template("mypage.html")

@application.route('/applier_custom')
def view_applier_customs():
    data = DB.get_customs()

    if not isinstance(data, dict):
        print("Error: Data is not a dictionary. Data:", data)
        data = {}

    # session['nickname']과 일치하는 applier만 필터링
    applier_data = []
    
    for seller, customs in data.items():
        for name, appliers in customs.items():
            for applier, applier_details in appliers.items():
                if applier == session.get('nickname'):  # applier가 session['nickname']과 일치하면
                    item_data = DB.get_item_byname(name)
                    progress_data = DB.get_customs_byinfo(seller, name, applier)
                    if item_data:
                        applier_data.append({
                            "seller": seller,
                            "custom_name": name,
                            "custom_data": applier_details,
                            "item_data": item_data,
                            "images": item_data.get("images", []),
                            "applier": applier,
                            "progress": progress_data.get("progress")
                        })

    return render_template("applier_custom.html", combined_data=applier_data)

def get_custom_data():
    data = DB.get_customs()

    if not isinstance(data, dict):
        print("Error: Data is not a dictionary. Data:", data)
        return []

    combined_data = []
    current_user = session.get('nickname')

    if not current_user:
        print("Error: User is not logged in or 'nickname' not in session.")
        return combined_data  # 빈 리스트 반환

    for seller, customs in data.items():
        if seller != current_user:
            continue  # 현재 사용자와 seller가 일치하지 않으면 무시

        for name, appliers in customs.items():
            for applier, applier_details in appliers.items():
                item_data = DB.get_item_byname(name)
                progress_data = DB.get_customs_byinfo(seller, name, applier)
                if item_data:
                    combined_data.append({
                        "seller": seller,
                        "custom_name": name,
                        "custom_data": applier_details,
                        "item_data": item_data,
                        "images": item_data.get("images", []),
                        "applier": applier,
                        "progress": progress_data.get("progress")
                    })

    return combined_data

@application.route('/custom')
def view_customs():
    combined_data = get_custom_data()
    return render_template("custom.html", combined_data=combined_data)

@application.route('/end/<user>/<category>/<detail_key>', methods=['GET'])
def change_details(user, category, detail_key):
    DB.change_custom_progress(user, category, detail_key)
    combined_data = get_custom_data()
    return render_template("custom.html", combined_data=combined_data)

@application.route('/application/<user>/<category>/<detail_key>', methods=['GET'])
def get_data_details(user, category, detail_key):
    data = DB.get_customs_byinfo(user, category, detail_key)
    return render_template('application.html', data=data, seller=user, itemname=category, applier=detail_key)

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

@application.route("/like_review", methods=['POST'])
def like_review():
    try:
        review_id = request.json.get('review_id')
        if not review_id:
            return jsonify({"success": False, "message": "Missing review ID"}), 400

        # 좋아요 수 업데이트
        updated_likes = DB.update_likes(review_id)

        if updated_likes is not None:
            return jsonify({"success": True, "new_likes": updated_likes})
        else:
            return jsonify({"success": False, "message": "Review not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@application.route("/view_detail/<name>/")
def view_item_detail(name):
    data = DB.get_item_byname(name)  # 특정 아이템 데이터 가져오기
    reviews = data.get('reviews', {})  # 'reviews' 키가 없으면 빈 딕셔너리를 반환

    # 리뷰 데이터를 리스트로 변환하고 정렬
    review_list = list(reviews.values()) if reviews else []
    review_list = sorted(review_list, key=lambda r: r.get('date', ''), reverse=True)  # 최신순 정렬

    # 가격 계산
    price = float(data.get('price', 0))
    discount = float(data.get('discount', 0))
    finalprice = int(price * (100 - discount) * 0.01)

    return render_template(
        "detail.html",
        name=name,
        data=data,
        reviews=review_list,  # 템플릿으로 리뷰 전달
        finalprice=finalprice
    )

#찜 기능
@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    print("###show_heart#####",session['id'],name)
    my_heart = DB.get_heart_byname(session['id'],name)
    print("####show_heart####",my_heart)
    return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    image = request.form.get('image')
    my_heart = DB.update_heart(session['id'],'Y',name, image)
    return jsonify({})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    image = request.form.get('image')
    my_heart = DB.update_heart(session['id'],'N',name, image)
    return jsonify({})

@application.route('/like')
def view_like():
    page = request.args.get("page", 0, type=int)
    
    user_id = session.get('id')
    like_items = []
    recent_items = []

    if user_id:
        hearts = DB.db.child("heart").child(user_id).get()

        if hearts.val():
            for heart in hearts.each():
                item_name = heart.key()  # 아이템 이름
                item_data = heart.val()  # 찜 데이터
                    
                # 관심 데이터만 추가
                if item_data.get('interested') == 'Y':
                        items = DB.get_item_byname(item_name)

                        price = float(items.get("price") or 0)
                        discount = float(items.get("discount") or 0)

                        finalprice = int(price * (100 - discount) * 0.01)
            
                        like_items.append({
                            "name": item_name,
                            "image": item_data.get("image"),  # 이미지 추가
                            "data": items,
                            "seller": items.get("seller"),
                            "discount": items.get("discount"),
                            "price": items.get("price"),
                            "finalprice": finalprice
                        })

                print("########like_items",like_items)

                item_counts=len(like_items)
        
        # 최근 아이템 4개 선택
        recent_items = like_items[-4:] if len(like_items) > 4 else like_items

    return render_template('like.html', like_items=like_items, total=item_counts, recent_items=recent_items, finalprice=finalprice)



#구매하기
@application.route('/buy')
def buy():
    name = request.args.get('name')
    image = request.args.get('image')
    total_price = request.args.get('totalPrice')
    discount = request.args.get('discount')
    seller = request.args.get('seller')

    options_json = request.args.get('selectedOption')  # JSON 형식으로 전달받음
    options = json.loads(options_json)

    return render_template('buy.html', name=name, image=image, total_price=total_price, options=options, discount=discount, seller=seller)

@application.route('/review/<item_name>/<review_id>')
def review_detail(item_name, review_id):
    # DBhandler 인스턴스인 DB를 사용하여 리뷰 데이터를 가져옵니다.
    review_data = DB.get_review_by_id(item_name, review_id)
    
    # 리뷰 데이터가 없을 경우를 처리합니다.
    if review_data is None:
        return "리뷰를 찾을 수 없습니다.", 404

    # 리뷰 데이터를 템플릿에 전달하여 렌더링합니다.
    return render_template('detailed_review.html', review=review_data)






if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
