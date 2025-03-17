from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

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

# 创建唯一索引
movies_collection.create_index("url", unique=True)

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