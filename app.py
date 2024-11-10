from flask import Flask, render_template, request, redirect, url_for
from database import DBhandler
import os

application = Flask(__name__)

DB = DBhandler()

# Initialize an empty list to store item data
items = []

@application.route("/")
def Hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    # Pass the stored items list to the template
    return render_template("list.html", items=items)
    
@application.route("/itemdetail")
def view_itemdetail():
    return render_template("itemdetail.html")

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/reg_items")
def reg_items():
    return render_template("reg_items.html")

@application.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")

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

    return render_template("list.html", items=items)

@application.route("/submit_review_post", methods=['POST'])
def submit_review_post():
    data = request.form
    img_list = []

    for i in range(1, 3):
        image_file = request.files.get(f'file{i}')
        if image_file:
            image_path = f"static/images/{image_file.filename}"
            image_file.save(image_path)
            img_list.append(image_path)
    
    DB.insert_review(data, img_list)
    
    return render_template("list.html", items=items)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
