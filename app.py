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
    return redirect(url_for('view_list'))

@application.route('/mypage')
def mypage():
    user_id = session.get('id')
    like_items = []

    if user_id:
        hearts = DB.db.child("heart").child(user_id).get()

        if hearts.val():
            for heart in hearts.each():
                item_name = heart.key()
                item_data = heart.val()

                if item_data.get('interested') == 'Y':
                    like_items.append({
                        "name": item_name,
                        "image": item_data.get("image"),  # 이미지 추가
                        "data": item_data
                    })


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
        data = DB.get_items() #read the table
    else:
        data = DB.get_items_bycategory(category)

    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=False)) #key는 상품명, 상품명을 사용해서 정렬
    item_counts = len(data)

    if item_counts<=per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data =dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)

    for i in range(row_count):  # last row
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:(i + 1) * per_row])

    finalprices = {}
    review_count = {}
    average_stars = {} 

    if data:
        for key, item in data.items():
            price = float(item.get('price', 0))
            discount = float(item.get('discount', 0))
            finalprice = int(price * (100 - discount) * 0.01)
            finalprices[key] = finalprice
            reviews = DB.get_reviews(key)
            review_count[key] = len(reviews)

            if review_count[key] > 0:
                try:
                    total_stars = sum([int(review.get('star', 0)) for review in reviews if 'star' in review and str(review['star']).isdigit()])
                    average_stars[key] = round(total_stars / review_count[key], 1)
                except Exception as e:
                    print(f"Error in calculating average stars: {e}")
                    average_stars[key] = "데이터 없음"
            else:
                average_stars[key] = " "


    # 이후 finalprices를 템플릿에 넘길 수 있음.
    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts/per_page)),
        total=item_counts,
        finalprices=finalprices, # 템플릿으로 finalprices 전달
        category=category,
        review_count=review_count,
        average_stars=average_stars
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
    review_count = {}
    average_stars = {} 

    if data:
        for key, item in data.items():
            price = float(item.get('price', 0))
            discount = float(item.get('discount', 0))
            finalprice = int(price * (100 - discount) * 0.01)
            finalprices[key] = finalprice
            reviews = DB.get_reviews(key)
            review_count[key] = len(reviews)

            if review_count[key] > 0:
                try:
                    total_stars = sum([int(review.get('star', 0)) for review in reviews if 'star' in review and str(review['star']).isdigit()])
                    average_stars[key] = round(total_stars / review_count[key], 1)
                except Exception as e:
                    print(f"Error in calculating average stars: {e}")
                    average_stars[key] = "데이터 없음"
            else:
                average_stars[key] = " "


    # 이후 finalprices를 템플릿에 넘길 수 있음.
    return render_template(
        "myitems.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts/per_page)),
        total=item_counts,
        finalprices=finalprices, # 템플릿으로 finalprices 전달
        category=category,
        review_count=review_count,
        average_stars=average_stars
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
    sellernickname = data['seller']
    seller = DB.find_user_bynickname(sellernickname)

    price = float(data['price'] or 0)
    discount = float(data['discount'] or 0)

    finalprice = int(price * (100 - discount) * 0.01)

    return render_template("detail.html", name=name, data=data, finalprice=finalprice, seller=seller)


@application.route('/detail_info/<name>/',methods=['GET'])
def view_detail_info(name):
    print("##detailinfo#name:",name)
    data = DB.get_item_byname(str(name))
    print("####detailinfodata:",data)

    return render_template("detail_info.html", name=name, data=data)


@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    data = DB.get_item_byname(str(name))
    return render_template("reg_reviews.html", name=name, data=data)

@application.route("/apply_custom_init/<name>/")
def apply_custom_init(name):
    data = DB.get_item_byname(str(name))
    return render_template("apply_custom.html", name=name, data=data)

@application.route("/reg_review", methods=['POST'])
def reg_review():
    data = request.form
    
    img_list = []

    for i in range(1, 3):

        image_file = request.files.get(f'file{i}')
        if image_file:
            image_path = f"static/images/{image_file.filename}"
            image_file.save(image_path)
            image_url = f"/static/images/{image_file.filename}"
            img_list.append(image_url)

    # username과 현재 날짜를 추가
    data = dict(data)
    data['username'] = session.get('nickname', 'unknown_user')  # 현재 로그인된 사용자 이름
    data['date'] = datetime.now().strftime("%Y-%m-%d")  # 현재 날짜를 'YYYY-MM-DD' 형식으로 추가
    data['image_url'] = img_list[0] if img_list else None  # 첫 번째 이미지를 image_url로 추가

    DB.insert_review(data, img_list)
    return redirect(url_for('view_item_detail', name=data['itemname']))


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
            image_url = f"/static/images/{image_file.filename}"
            img_list.append(image_url)
    
    DB.insert_item(data['name'], data, img_list, opt_list)


    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    per_page = 8  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page / per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    if category == "all":
        data = DB.get_items() #read the table
    else:
        data = DB.get_items_bycategory(category)

    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=False)) #key는 상품명, 상품명을 사용해서 정렬
    item_counts = len(data)

    if item_counts<=per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data =dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)

    for i in range(row_count):  # last row
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:(i + 1) * per_row])

    finalprices = {}
    review_count = {}
    average_stars = {} 

    if data:
        for key, item in data.items():
            price = float(item.get('price', 0))
            discount = float(item.get('discount', 0))
            finalprice = int(price * (100 - discount) * 0.01)
            finalprices[key] = finalprice
            reviews = DB.get_reviews(key)
            review_count[key] = len(reviews)

            if review_count[key] > 0:
                try:
                    total_stars = sum([int(review.get('star', 0)) for review in reviews if 'star' in review and str(review['star']).isdigit()])
                    average_stars[key] = round(total_stars / review_count[key], 1)
                except Exception as e:
                    print(f"Error in calculating average stars: {e}")
                    average_stars[key] = "데이터 없음"
            else:
                average_stars[key] = " "


    # 이후 finalprices를 템플릿에 넘길 수 있음.
    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts/per_page)),
        total=item_counts,
        finalprices=finalprices, # 템플릿으로 finalprices 전달
        category=category,
        review_count=review_count,
        average_stars=average_stars
    )

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
            image_url = f"/static/images/{image_file.filename}"
            img_list.append(image_url)
    
    DB.apply_custom(data['name'], data, img_list)

    user_id = session.get('id')
    like_items = []

    if user_id:
        hearts = DB.db.child("heart").child(user_id).get()

        if hearts.val():
            for heart in hearts.each():
                item_name = heart.key()
                item_data = heart.val()

                if item_data.get('interested') == 'Y':
                    like_items.append({
                        "name": item_name,
                        "image": item_data.get("image"),  # 이미지 추가
                        "data": item_data
                    })


    recent_items = like_items[-4:] if len(like_items) > 4 else like_items

    return render_template("mypage.html",recent_items=recent_items)

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
    keyword = request.args.get('search_kw', type=str, default='').strip()
    page = request.args.get('page', 0, type=int)

    if not keyword:
        flash("Please enter a search term.")
        return redirect(url_for('view_list'))

    try:
        # Firebase에서 아이템 가져오기
        items = DB.get_items()

        if not items:  # 아이템이 없을 경우 빈 리스트로 처리
            flash("No items found.")
            return render_template('search_results.html', items=[], keyword=keyword, page=page, page_count=1)

        filtered_items = []

        # 아이템들 중에서 검색어와 일치하는 아이템 필터링
        keyword_lower = keyword.lower()  # 검색어를 소문자로 변환
        for item_name, item_data in items.items():
            name = item_name.lower()  # 아이템 이름 (소문자로 처리하여 비교)
            info = item_data.get("info", "").lower()  # 아이템 설명 (소문자로 처리하여 비교)

            # 검색어가 이름이나 설명에 포함되면 필터링
            if keyword_lower in name or keyword_lower in info:
                # 할인율 적용된 가격 계산
                price = float(item_data.get('price', 0))
                discount = float(item_data.get('discount', 0))
                final_price = int(price * (100 - discount) * 0.01)
                
                # 최종 가격을 추가한 아이템 데이터 생성
                filtered_items.append({"name": item_name, **item_data, "final_price": final_price})

        # 검색 결과가 있을 때
        if filtered_items:
            total_items = len(filtered_items)
            items_per_page = 8
            start_idx = page * items_per_page
            end_idx = start_idx + items_per_page
            paginated_items = filtered_items[start_idx:end_idx]

            return render_template(
                'search_results.html',
                items=paginated_items,
                keyword=keyword,
                page=page,
                page_count=(total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0)
            )
        else:
            flash("No items found.")
            return render_template('search_results.html', items=[], keyword=keyword, page=page, page_count=1)
    except Exception as e:
        # 오류 처리
        flash(f"Error occurred while fetching items: {str(e)}")
        return render_template('search_results.html', items=[], keyword=keyword, page=page, page_count=1)





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
    


@application.route("/review_detail/<item_name>/<review_key>")
def review_detail(item_name, review_key):
    try:
        # 데이터베이스에서 리뷰 가져오기
        review = DB.get_review_by_keys(item_name, review_key)
        if review:
            return render_template("detailed_review.html", review=review)
        else:
            return "Review not found", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



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
    per_page = 8  # items per page
    start_idx = page * per_page
    end_idx = start_idx + per_page

    user_id = session.get('id')
    like_items = []

    if user_id:
        hearts = DB.get_heart_by_user(user_id)

        if hearts:
            for item_name, item_data in hearts.items():
                if item_data.get('interested') == 'Y':
                    # 아이템의 상세 정보를 가져와서 필요한 데이터 추가
                    item_info = DB.get_item_byname(item_name)
                    if item_info:
                        like_items.append({
                            "name": item_name,
                            "image": item_data.get("image"),
                            "seller": item_info.get("seller"),
                            "price": item_info.get("price"),
                            "discount": item_info.get("discount"),
                            "rating": item_info.get("rating", 5.0),
                            "reviews": len(DB.get_reviews(item_name)),
                            "final_price": int(float(item_info.get("price")) * (100 - float(item_info.get("discount"))) * 0.01)
                        })

    # Paginate liked items
    total_items = len(like_items)
    paginated_items = like_items[start_idx:end_idx]
    page_count = (total_items + per_page - 1) // per_page

    return render_template(
        'like.html',
        like_items=paginated_items,
        total=total_items,
        page=page,
        page_count=page_count
    )

@application.route('/buy_item', methods=['POST'])
def buy_item():
    username = session['nickname']
    
    # request.form에서 selectedOption을 가져옵니다.
    options = request.form.get('selectedOption')
    data = request.form
    name = request.form.get('name')

    optionsDict = json.loads(options) if options else {}

    # DB에 데이터 저장
    DB.buy_item(username, data, name, optionsDict)

    # 데이터를 buy.html로 넘기기 위해 리다이렉트
    return redirect(url_for('view_buyitems', username=username))

@application.route('/buy')
def view_buyitems():
    username = session.get('nickname')
    data = DB.get_buyitems(username)

    return render_template('buy.html', data=data, username=username)




@application.route('/reviews/sort', methods=['GET'])
def sort_reviews():
    name = request.args.get('name')  # 아이템 이름
    sort_order = request.args.get('sort', 'latest')  # 정렬 기준

    # 리뷰 데이터 가져오기
    reviews = DB.get_reviews(name)
    if not reviews:
        return jsonify({"error": "No reviews found"}), 404

    # 정렬 로직
    if sort_order == 'latest':
        reviews = sorted(reviews, key=lambda x: x['date'], reverse=True)
    elif sort_order == 'best':
        reviews = sorted(reviews, key=lambda x: int(x['star']), reverse=True)

    # JSON 응답으로 반환
    return jsonify(reviews=reviews)

@application.route("/review_page/<name>/", methods=['GET'])
def view_review_page(name):
    reviews = DB.get_reviews(name)  # 리뷰 데이터 가져오기
    
    # 총 리뷰 수 계산
    total_reviews = len(reviews)

    # 평균 별점 계산
    if total_reviews > 0:
        try:
            # 별점 데이터를 숫자로 변환해 합산
            total_stars = sum([int(review.get('star', 0)) for review in reviews if 'star' in review and str(review['star']).isdigit()])
            average_stars = round(total_stars / total_reviews, 1)
        except Exception as e:
            print(f"Error in calculating average stars: {e}")
            average_stars = "데이터 없음"
    else:
        average_stars = " "  # 리뷰가 없을 경우 처리

    print(f"Total reviews: {total_reviews}, Average stars: {average_stars}")  # 디버깅 출력

    # 페이징 처리
    page = request.args.get("page", 1, type=int)  # 현재 페이지 번호
    per_page = 5  # 페이지당 표시할 리뷰 수
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_reviews = reviews[start_idx:end_idx]
    
    # 총 페이지 수 계산
    total_pages = (total_reviews + per_page - 1) // per_page

    return render_template(
        "review_page.html",
        name=name,
        reviews=paginated_reviews,
        current_page=page,
        total_pages=total_pages,
        total_reviews=total_reviews,
        has_prev=page > 1,
        has_next=page < total_pages,
        average_stars=average_stars
    )



if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
