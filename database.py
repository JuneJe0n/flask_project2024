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
    
    def insert_user(self, data, pw):
        user_info ={
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname']
            }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        if users.val() is None:  # First registration
            return True
        else: 
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
                return True

    def get_items(self):
        items = self.db.child("item").get().val()
        return items    

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value