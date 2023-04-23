# coding:utf-8


"""外联方法"""


def check_str(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == '1':
            return True
        else:
            return False

    return inner


@check_str
def test(data):
    return data


# print(test('0'))


class Test:
    name = None

    def __init__(self, name):
        self.name = name

    def run_test(self):
        print('run file')
        return

    @classmethod
    def test_class_method(cls, val):
        print(val)

    @staticmethod
    def test_static_method():
        print()

    @property
    def name_property(self):
        return self.name

    @name_property.setter
    def name_property(self, val):
        self.name = val


result = Test('11')
result.test_class_method('2222')
