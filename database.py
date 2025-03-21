from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import time

# 带用户名和密码的 MongoDB URI
MONGO_USERNAME = "admin"  # 改成你的用户名
MONGO_PASSWORD = "admin"  # 改成你的密码
MONGO_HOST = "localhost"          # 如果是本地就 localhost，云上就填 IP 或域名
MONGO_PORT = 27017                # 默认端口
MONGO_DB = "douban_movies"        # 数据库名

# URI 格式：mongodb://username:password@host:port/
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
movies_collection = db["movies"]
users_collection = db["users"]
history_collection = db["history"]

# 创建唯一索引
movies_collection.create_index("url", unique=True)
users_collection.create_index("username", unique=True)

def save_movie(data):
    """保存电影数据，URL 重复就更新"""
    try:
        movies_collection.update_one(
            {"url": data["url"]},
            {"$set": data},
            upsert=True
        )
        return True
    except DuplicateKeyError:
        return False

def get_movie_by_name(name):
    """按电影名模糊查询"""
    return movies_collection.find_one({"title": {"$regex": name, "$options": "i"}})

def get_all_movies():
    """返回所有电影"""
    return list(movies_collection.find({}, {"_id": 0}))

def save_user(username, password_hash):
    try:
        users_collection.insert_one({"username": username, "password": password_hash})
        return True
    except DuplicateKeyError:
        return False

def get_user(username):
    return users_collection.find_one({"username": username})

def save_search_history(username, movie_data):
    history_collection.update_one(
        {"username": username, "url": movie_data["url"]},
        {"$set": {"username": username, "movie": movie_data, "searched_at": time.ctime()}},
        upsert=True
    )

def get_user_history(username):
    return list(history_collection.find({"username": username}, {"_id": 0, "movie": 1, "searched_at": 1}))