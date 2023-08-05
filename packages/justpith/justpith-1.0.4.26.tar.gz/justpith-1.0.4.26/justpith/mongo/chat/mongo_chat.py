# encoding: utf-8
from ..mongo import Mongo
from datetime import datetime
import time

class MongoChat(Mongo):
    def __init__(self,host, port, db):
        super(MongoChat,self).__init__(host, port, db)
        self.collection_chat = "Chat"
        self.collection_user_social_sid = "Users_Social_Sid"
        self.collection_user_social = "Users_Social"
        self.collection_user_social_chat_room_id = "Users_Social_Chat_Room_{}"

    def set_status(self, user, status):
        selected_collection = self.connection[self.collection_chat]
        tmp = {
            "user": user,
            "status": status
        }
        selected_collection.insert_one(tmp)

    def update_user_sid(self, user_id, sid):
        selected_collection = self.connection[self.collection_user_social_sid]
        selected_collection.update({"_id": user_id}, {"$set": {"sid": sid}}, upsert=True)

    def get_user_sid(self, user_id):
        selected_collection = self.connection[self.collection_user_social_sid]
        sid = selected_collection.find_one({"_id": user_id}, {"sid": 1})
        if sid:
            return sid["sid"]
        return sid

    def update_status(self, user_id, status):
        selected_collection = self.connection[self.collection_user_social]
        selected_collection.update({"_id": user_id}, {"$set": {"status": status}})

    def register_user(self, user_id):
        selected_collection = self.connection[self.collection_user_social]
        selected_collection.insert_one({"_id": user_id, "friends": [], "status": 0})

    def add_friend(self, user_id, friend_user_id):
        selected_collection = self.connection[self.collection_user_social]
        selected_collection.update({"_id": user_id}, {"$addToSet": {"friends": friend_user_id}})

    def remove_friend(self, user_id, friend_user_id):
        selected_collection = self.connection[self.collection_user_social]
        selected_collection.update({"_id": user_id}, {"$pull": {"friends": friend_user_id}})

    def get_social_user(self, user_id):
        selected_collection = self.connection[self.collection_user_social]
        user = selected_collection.find_one({"_id": user_id})
        return user

    def get_friends_list(self, user_id):
        selected_collection = self.connection[self.collection_user_social]
        friends = selected_collection.find_one({"_id": user_id}, {"friends": 1})
        if friends:
            return friends["friends"]
        return []

    def get_user_id_from_sid(self, sid):
        selected_collection = self.connection[self.collection_user_social_sid]
        user_id = selected_collection.find_one({"sid": sid})
        if user_id:
            return user_id["_id"]
        return user_id

    def store_chat_msg(self, room_id, writer, msg, timestamp):
        collection = self.collection_user_social_chat_room_id.format(room_id)
        selected_collection = self.connection[collection]
        ts = int(timestamp)
        dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        selected_collection.insert_one({"_id": ts, "writer": writer, "msg": msg, "date": dt})

    def get_chat_msg(self, room_id, num_msg, last_msg_id):
        collection = self.collection_user_social_chat_room_id.format(room_id)
        selected_collection = self.connection[collection]
        if last_msg_id == 0:
            messages = selected_collection.find().limit(num_msg).sort("_id", -1)
        else:
            messages = selected_collection.find({"_id":{"$lt": last_msg_id}}).limit(num_msg).sort("_id", -1)
        return messages