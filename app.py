from flask import Flask, render_template, request, redirect, url_for
import os

application = Flask(__name__)

# Initialize an empty list to store item data
items = []

@application.route("/")
def Hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    # Pass the stored items list to the template
    return render_template("list.html", items=items)

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
def reg_item_submit_post():
    # Save the uploaded image file
    image_file = request.files["file"]
    image_path = f"static/images/{image_file.filename}"
    image_file.save(image_path)

    # Collect form data and add it to the items list
    data = {
        'seller': request.form.get('seller'),
        'name': request.form.get('name'),
        'category': request.form.get('category'),
        'status': request.form.get('status'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'addr': request.form.get('addr'),
        'card': request.form.get('card'),
        'price': request.form.get('price'),
        'rating': request.form.get('rating'),
        'img_path': image_path
    }
    items.append(data)  # Append the new item to the items list

    # Redirect to the list view after submission
    return render_template("submit_item_result.html", data=data, img_path=image_path)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
