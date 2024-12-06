import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
        
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def apply_custom(self, name, data, img_list):
        custom = {
            "amount": data['amount'],
            "size": data['size'],
            "color": data['color'],
            "material": data['material'],
            "상세 요청사항": data['info'],
            "images": img_list,
            "progress": "요청됨"
        }
        self.db.child("application").child(data['seller']).child(name).child(data['applier']).set(custom)
        return True
    
    def change_custom_progress(self, seller, name, applier):
        self.db.child("application").child(seller).child(name).child(applier).update({"progress": "완료됨"})
        return True

    def get_customs(self):
        try:
            # Firebase에서 데이터를 가져오기
            customs = self.db.child("application").get()
            if customs.val() is None:
                return {}  # 데이터가 없으면 빈 딕셔너리 반환
            
            # 데이터 구조를 출력하여 확인
            print("Fetched customs data:", customs.val())

            return customs.val()  # 딕셔너리 형태로 반환
        except Exception as e:
            print(f"Error fetching customs: {str(e)}")
            return {}  

    def get_customs_byinfo(self, seller, item, writer):
        try:
            data = self.db.child("application").child(seller).child(item).child(writer).get()
            if data.val() is None:
                return {}
            return data.val()
        except Exception as e:
            print(f"Error fetching customs: {str(e)}")
            return {}  

    def insert_item(self, name, data, img_list, opt_list):
        item_info = {
            "seller": data['seller'],
            "amount": data['amount'],
            "category": data['category'],
            "price": data['price'],
            "discount": data['discount'],
            "info": data['info'],
            "custom": data['customizing'],
            "images": img_list,
            "options": opt_list
        }
        self.db.child("item").child(name).set(item_info)
        return True

    def insert_review(self, data, img_list):

        img_list = [f"/{img}" for img in img_list]  

        reivew_info = {
            "preview": data['info'][:10],
            "info": data['info'],
            "option": data['options'], #name으로 받음
            "star": data['clovers'],
            "img_path": img_list,
            "username": data.get('username', 'unknown_user'),
            "date": data.get('date', 'unknown_date'),
            "likes": 0
        }
        self.db.child("review").child(data['itemname']).child(data['info'][:10]).set(reivew_info)
        return True


    def insert_user(self, data, pw):
        if not data.get('id') or not data.get('nickname'):
            print("Error: Missing 'id' or 'nickname' in input data")
            return False

        user_info = {
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname'],
            "email":data['email'],
            "phone":data['phone']
        }
        
        try:
            if self.user_duplicate_check(data['id']):  # 중복 확인
                self.db.child("user").child(data['id']).set(user_info)  # 데이터 저장
                print("User registered successfully:", user_info)
                return True
            else:
                print("Duplicate user ID found!")
                return False
        except Exception as e:
            print(f"Error in insert_user: {e}")
            return False

    def user_duplicate_check(self, id_string):
        try:
            users = self.db.child("user").get()  # Firebase에서 전체 user 데이터 가져오기
            if not users.each():  # 데이터가 없을 경우 (빈 데이터 처리)
                return True  # 중복 없음
            
            for user in users.each():  # 각 user 데이터를 순회
                value = user.val()  # Firebase 데이터를 딕셔너리로 변환
                if value.get('id') == id_string:  # ID 비교
                    return False  # 중복된 ID 발견
            return True  # 중복 없음
        except Exception as e:
            print(f"Error in user_duplicate_check: {e}")
            return False


    def get_items(self):
        try:
            # Firebase에서 아이템들을 가져오기 (child().get()을 대체)
            items = self.db.child("item").get()
            if items.val() is None:
                return {}  # 데이터가 없을 때 빈 딕셔너리 반환
            return items.val()  # 아이템들을 딕셔너리 형태로 반환
        except Exception as e:
            print(f"Error fetching items: {str(e)}")
            return {}

  

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########",name)
        for res in items.each():
            key_value = res.key()
            
            if key_value == name:
                target_value=res.val()
        return target_value


    def find_user(self, id_, pw_hash):
        try:
            users = self.db.child("user").get()
            if not users.each():  # 사용자 데이터가 없으면 None 반환
                return None

            for user in users.each():
                value = user.val()  # 사용자 데이터 딕셔너리로 변환
                if value['id'] == id_ and value['pw'] == pw_hash:  # ID와 비밀번호 확인
                    return value  # 사용자 데이터 반환
            return None  # 일치하는 사용자 없음
        except Exception as e:
            print(f"Error in find_user: {e}")
            return None
        
    def find_user_bynickname(self, nickname):
        try:
            users = self.db.child("user").get()
            if users.each():
                for user in users.each():
                    user_data = user.val()
                    if user_data.get("nickname") == nickname:
                        return {
                            "user_id": user.key(),
                            "email": user_data.get("email")
                        }
            return None
        except Exception as e:
            print(f"Error fetching user info by nickname: {e}")
            return None


    def search_items(self, keyword):
        try:
            # Firebase에서 모든 아이템 가져오기
            items = self.db.child("item").get()
            if not items.each():  # 데이터가 없을 경우 빈 리스트 반환
                return []

            # 검색어에 해당하는 아이템 필터링
            result = []
            for item in items.each():
                item_data = item.val()  # 아이템 데이터 딕셔너리 가져오기
                name = item.key()  # 아이템 이름 가져오기
                info = item_data.get('info', '')  # 아이템 설명 가져오기

                # name 또는 info에 검색어가 포함되면 결과에 추가
                if keyword.lower() in name.lower() or keyword.lower() in info.lower():
                    result.append({"name": name, **item_data})  # 아이템 데이터 추가

            return result  # 조건에 맞는 아이템 리스트 반환

        except Exception as e:
            print(f"Error in search_items: {e}")
            return []
    
    def get_reviews(self, name):
        try:
            # Firebase에서 리뷰 데이터 가져오기
            reviews = self.db.child("review").child(name).get()
            if not reviews.each():  # 리뷰 데이터가 없으면 빈 리스트 반환
                return []

            # 리뷰 데이터를 리스트로 변환
            result = []
            for review in reviews.each():
                review_data = review.val() 
                review_data["star"] = int(review_data.get("star", 0)) 
                review_data["name"] = name  # 리뷰 이름(key)을 추가 (필요에 따라)
                review_data["username"] = review_data.get("username", "unknown_user") 
                review_data["date"] = review_data.get("date", "unknown_date")
                review_data["image_url"] = review_data["img_path"][0] if review_data.get("img_path") else None
                result.append(review_data)

            return result  # 리뷰 리스트 반환
        except Exception as e:
            print(f"Error fetching reviews: {str(e)}")
            return [] 
        
    def get_review_by_id(self, review_id):
        try:
            # Firebase에서 리뷰 ID에 맞는 리뷰 가져오기
            review = self.db.child("review").child(str(review_id)).get()
            if review.val():
                review_data = review.val()
                # star 값 변환
                try:
                    review_data["star"] = int(review_data.get("star", 0))
                except ValueError:
                    review_data["star"] = 0
                return review_data
            else:
                return None
        except Exception as e:
            print(f"Error fetching review by id: {str(e)}")
            return None
    
    #찜 기능
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value
        
        for res in hearts.each():
            key_value = res.key()

            if key_value == name:
                target_value=res.val()
        print("###target_value##",target_value)
        return target_value
    
    # 사용자 찜한 상품 가져오기
    def get_heart_by_user(self, user_id):
        try:
            hearts = self.db.child("heart").child(user_id).get()
            if not hearts.val():
                return {}  # 데이터가 없으면 빈 딕셔너리 반환
            
            return hearts.val()  # 찜한 상품 데이터를 딕셔너리 형태로 반환
        except Exception as e:
            print(f"Error fetching hearts: {str(e)}")
            return {}
    
    def update_heart(self, user_id, isHeart, item, image):
        heart_info ={
            "image" : image,
            "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
    
    def get_heart(self):
        likes = self.db.child("heart").get().val()
        return likes


    #카테고리별 상품리스트 보여주기
    def get_items_bycategory(self, cate):
        items = self.db.child("item").get()
        target_value = []
        target_key = []
        
        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['category'] == cate:
                target_value.append(value)
                target_key.append(key_value)
        
        print("######target_value", target_value)

        new_dict = {}
        for k, v in zip(target_key, target_value):
            new_dict[k] = v
        
        return new_dict
    
    def get_review_by_keys(self, item_name, review_key):
        try:
            review = self.db.child("review").child(item_name).child(review_key).get()
            if review.val():
                review_data = review.val()
                review_data["star"] = int(review_data.get("star", 0))  # 숫자로 변환
                return review_data
            return None
        except Exception as e:
            print(f"Error fetching review: {str(e)}")
            return None
