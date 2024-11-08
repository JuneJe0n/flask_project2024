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
    print('##############################')
    image_file = request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)
    
    return render_template("submit_item_result.html", data=data, img_path="static/images/{}".format(image_file.filename))

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
