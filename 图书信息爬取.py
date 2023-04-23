# coding = utf-8
import concurrent
from concurrent.futures import ThreadPoolExecutor

import requests

# 定义线程池
pool = ThreadPoolExecutor(max_workers=10)
# 定义线程池的的线程数
features = []
request_url = 'http://yushu.talelin.com/book/search?q=python&page='
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


# 构造请求路径
def build_request_url(page_number):
    if type(page_number) is not int:
        raise Exception
    for number in range(1, page_number):
        do_request_url = request_url + str(number)
        print('解析到路径为{}'.format(do_request_url))
        features.append(pool.submit(sendRequest, do_request_url, number))


# 构造多线程工具
def run_with_thread():
    build_request_url(4)
    concurrent.futures.wait(features, return_when=concurrent.futures.ALL_COMPLETED)
    print("===执行完毕===")


# 发送请求
def sendRequest(requestUrl, i):
    try:
        response = requests.get(url=requestUrl, headers=header, timeout=5000)
        with open(f'/page{i}.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
    except Exception as e:
        print(e)
    else:
        print(f'{requestUrl} 请求成功')


def main():
    run_with_thread()


if __name__ == '__main__':
    main()
