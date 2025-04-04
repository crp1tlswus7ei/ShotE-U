import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
shot = MongoClient(MONGO_URI)
db = shot["kiko"]
w_coll = db["warns"]

def get_warns(self, user_id):
   user_data = w_coll.find_one({"_id": user_id})
   return user_data["warnings"] if user_data else []

def add_warns(self, user_id, reason):
   warns = self.get_warns(user_id)
   warns.append(reason)
   w_coll.update_one({"_id": user_id}, {"$set": {"warnings": warns}}, upsert=True)
   return len(warns)

def clear_warns(self, user_id):
   w_coll.update_one({"_id": user_id}, {"$set": {"warnings": []}})

def remove_warn(self, user_id, amount):
   warns = self.get_warns(user_id)
   if 0 <= amount < len(warns):
      del warns[amount]
      w_coll.update_one({"_id": user_id}, {"$set": {"warnings": warns}})
      return True
   return False