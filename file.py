import json

from BuessExpection import BuessExpection


def Log(func):
    def wrapper(*args, **kwargs):
        print("[DEBUG]: {} start execute, args: {}, kwargs: {}".format(func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        print("[DEBUG]: {} end execute".format(func.__name__))
        return result

    return wrapper


'''序列化字符串到文件'''


@Log
def save_dict_to_json(dict_param: dict, file_path: str, save_type: type):
    if dict_param is None or str is None:
        raise BuessExpection('参数不存在')
    if not isinstance(save_type, type):
        raise TypeError('save_type参数应为类型')
    with open(file_path, 'w+') as f:
        try:
            json.dump(dict_param, f)
        except Exception as e:
            print(e)
        else:
            print('=' * 8, '写入成功')
        finally:
            print('执行结束end')


'''从指定文件中反序列化'''


@Log
def read_str_from_file(read_type: type, file_path: str):
    if file_path is None:
        raise BuessExpection('参数不存在')
    if not isinstance(read_type, type):
        raise TypeError('save_type参数应为类型')
    with open(file_path, 'r+') as f:
        '直接将所有文件load'
        try:
            result = json.load(f)
            print(result)
            return result
        except Exception as e:
            print(e)
        finally:
            print("加载结束")


if __name__ == '__main__':
    # my_dict = {'name': 'Alice', 'age': 20, 'gender': 'female'}
    # save_dict_to_json(my_dict, 'output.json', dict)
    result = read_str_from_file(dict, 'output.json')
    print(result, type(result))
