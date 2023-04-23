from redis import *
import pickle

args = dict(host='localhost', port='6379', db='1', password='blog-local-redis')

redisConnect = Redis(**args,decode_responses=True)


def setStr(key, value):
    redisConnect.set(name=key, value=value)


def setHash(key, mapping):
    print(mapping)
    redisConnect.hset(name=key, mapping=mapping)


def getHash(key):
    print(dict(redisConnect.hgetall(name=key)))


def getStr(key):
    print(redisConnect.get(name=key))


# 定义一个简单的类
class TestClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    # hashParams = {"name": "lk", "age": 20}
    # setHash("pr", dict(hashParams))
    # getHash("pr")
    # setStr("name", "likui")
    # getStr("name")

    # 创建一个类的实例
    '''
    my_object = TestClass("1", 2)

    # 使用 pickle 序列化对象
    pickled_object = pickle.dumps(my_object)

    # 将序列化后的对象存储到 Redis 中
    redisConnect.set('my_key', pickled_object)

    # 从 Redis 中获取对象并反序列化
    unpickled_object = pickle.loads(redisConnect.get('my_key'))
    # 打印对象的属性
    print(type(unpickled_object.x))
    print(type(unpickled_object.y))
    '''
    my_object = TestClass("1", 2)

    # 使用 pickle 序列化对象
    pickled_object = pickle.dumps(my_object)
    redisConnect.set('my_key', pickled_object)
    print(redisConnect.get('my_key'))

    redisConnect.close()
