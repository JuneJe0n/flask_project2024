import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
        
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def insert_item(self, name, data, img_list, opt_list):
        item_info = {
            #seller에 대한 정보는 reg_items에서 사용하가 작성하지 않으므로 백엔드 서버에서 더 작업 필요
            "amount": data['amount'],
            "category": data['category'],
            "price": data['price'],
            "discount": data['discount'],
            "info": data['info'],
            "images": img_list,
            "options": opt_list
        }
        self.db.child("item").child(name).set(item_info)
        return True

    def insert_review(self, data, img_list):
        reivew_info = {
            #seller에 대한 정보는 reg_items에서 사용하가 작성하지 않으므로 백엔드 서버에서 더 작업 필요
            #별점은 js에 기록되는데 이거 가져와서 저장하는 방법도 필요
            "info": data['info'],
            "img_path": img_list
        }
        self.db.child("review").child(data['info']).set(reivew_info)
        return True