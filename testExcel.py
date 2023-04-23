import json

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

env = {'host': '127.0.0.1', 'port': '3307', 'username': 'root', 'password': 'lk-local', 'dbname': 'test_database'}
DB_URI = f"mysql+pymysql://{env['username']}:{env['password']}@{env['host']}:{env['port']}/{env['dbname']}"
print(DB_URI)
engine = create_engine(DB_URI, echo=True)
Base = declarative_base()  # SQLORM基类
Session = sessionmaker(bind=engine)  # 构建session对象
session = Session()


def main0():
    # series = pd.Series({'a': 0., 'b': 1., 'c': 2.})
    # print(series.map(lambda x: x * 2).to_numpy())
    # print(series.get('a', 3))
    # d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
    #      'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
    # df = pandas.DataFrame(d)
    # print(df.columns)
    # csv = pd.read_csv('test.csv')
    # print(csv)
    # csv.to_csv()
    pass


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    username = Column(String(10))
    age = Column(Integer, default=0)
    address = Column(String(100))

    def __int__(self, age=0, username='', address='', id=None):
        self.age = age
        self.address = address
        self.username = username
        self.id = id

    # @property
    # def age(self):
    #     return self
    #
    # @age.setter
    # def age(self, age):
    #     self.age = age
    #
    # @age.getter
    # def age(self):
    #     return self

    @staticmethod
    def user_to_json(user):
        return {'username': user.username, 'age': user.age, 'id': user.id, 'address': user.address}

    @staticmethod
    def print_user(**kwargs):
        for key, value in kwargs.items():
            print(f'{key}: {value}')


def saveOne(entity):
    # 创建一个新用户
    session.add(entity)
    session.commit()


def selectOne(entity):
    nodes = session.query(UserInfo).filter_by(id=entity.id)
    if nodes.count() > 1 or nodes.count() == 0:
        raise Exception(f'too many result or null result is  {nodes.count()}')
    else:
        first_node = nodes.first()
        print(json.dumps(first_node, default=UserInfo.user_to_json))
        return first_node


def queryAll():
    return session.query(UserInfo)


def updateEntity(entity):
    session.commit()


def delEntity(**kwargs):
    new_dict = {k: v for k, v in kwargs.items() if k != '_sa_instance_state'}
    session.query(UserInfo).filter_by(**new_dict).delete()
    session.commit()


def delAll():
    print(session.query(UserInfo).delete())
    session.commit()


if __name__ == '__main__':
    '''
    Base.metadata.create_all(engine)
    saveOne(UserInfo(username='Alice', age=25))
    user_info = selectOne()
    user_info.age = 20
    updateEntity(user_info)
    selectOne()
    session.close()
    '''
    # delAll()
    # saveOne(UserInfo(username='Alice', age=25))
    user_info = UserInfo(username='Alice', age=25, id=6)
    delEntity(**vars(user_info))
    # selectOne(user_info)
    session.close()
