import os
from dotenv import load_dotenv
import redis

load_dotenv()

class Redis:
    def __init__(self):
        self.redis = None
        self.connect()

    def connect(self):
        try:
            self.redis = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                db=os.getenv("REDIS_DB")
            )
            return True
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            return False

    def set(self, key, value):
        try:
            self.redis.set(key, value)
            return True
        except Exception as e:
            print(f"Error setting key: {e}")
            return False

    def get(self, key):
        try:
            return self.redis.get(key)
        except Exception as e:
            print(f"Error getting key: {e}")
            return None

    def trim(self, key, start, end):
        try:
            self.redis.ltrim(key, start, end)
            return True
        except Exception as e:
            print(f"Error trimming key: {e}")
            return False

    def push(self, key, value):
        try:
            self.redis.lpush(key, value)
            return True
        except Exception as e:
            print(f"Error pushing key: {e}")
            return False

    def get_list(self, key):
        try:
            return self.redis.lrange(key, 0, -1)
        except Exception as e:
            print(f"Error getting list: {e}")
            return None


if __name__ == "__main__":
    redis = Redis()
    # redis.set("test", "test")
    # print(redis.get("test").decode('UTF-8'))
    redis.push("user", "test1")
    redis.push("user", "test2")
    redis.push("user", "test3")
    redis.push("user", "test4")
    redis.push("user", "test5")
    redis.push("user", "test6")
    redis.trim("user", 0, 2)
    print(redis.get_list("user"))
    