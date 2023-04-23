import requests
# import pymongo
from queue import Queue
from lxml import etree
import threading


def handle_request(url):
    """
    处理request函数
    :param url:
    :return: response.text
    """
    # 自定义请求头
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    }
    # 发送请求,有代理信息，就将代理添加进来
    response = requests.get(url=url, headers=headers, timeout=(5, 5), proxies=None)
    if response.status_code == 200 and response:
        return response.text


class PageSpider(threading.Thread):
    """
    页码URL请求多线程爬虫类
    """

    def __init__(self, thread_name, page_queue, detail_queue):
        super(PageSpider, self).__init__()
        self.thread_name = thread_name
        self.detail_queue = detail_queue
        self.page_queue = page_queue

    def parse_detail_url(self, content):
        """
        处理page_url页面的返回数据，解析详情页的URL
        :param content:page_response.text
        :return: detail_url, self.detail_queue
        """
        # 页码返回数据HTML实例化
        item_html = etree.HTML(content)
        # 解析出所有的详情页URL
        detail_urls = item_html.xpath("//a[@class='thumbnail']/@href")
        for detail_url in detail_urls:
            # 将详情页的URL放入detail_queue
            self.detail_queue.put(detail_url)

    def run(self):
        # 实际发送请求，请求页码URL
        print("{}启动".format(self.thread_name))
        # 需要不断的从页码QUEUE里面获取URL，并且发送请求，要看self.page_queue是否为空
        try:
            while not self.page_queue.empty():
                # 从QUEUE中获取数据，并设置为非阻塞状态
                page_url = self.page_queue.get(block=False)
                # 请求页码链接
                page_response = handle_request(url=page_url)
                if page_response:
                    # 解析30条详情页的URL
                    self.parse_detail_url(content=page_response)
        except Exception as e:
            print("{} run error:{}".format(self.thread_name, e))
        print("{}结束".format(self.thread_name))


class DetailSpider(threading.Thread):
    """
    详情页URL请求多线程爬虫类
    """

    def __init__(self, thread_name, detail_queue, data_queue):
        super(DetailSpider, self).__init__()
        self.thread_name = thread_name
        self.detail_queue = detail_queue
        self.data_queue = data_queue

    def run(self):
        # 实际发送请求，请求页码URL
        print("{}启动".format(self.thread_name))
        try:
            # 从detail queue里不断的获取这90个详情页的URL
            while not self.detail_queue.empty():
                # 从QUEUE中获取数据，并设置为非阻塞状态
                detail_url = self.detail_queue.get(block=False)
                # 请求页码链接
                detail_response = handle_request(url=detail_url)
                if detail_response:
                    # 请求回来的详情页的数据放入到dataqueue里面去
                    self.data_queue.put(detail_response)
        except Exception as e:
            print("{} run error:{}".format(self.thread_name, e))
        print("{}结束".format(self.thread_name))


class DataParse(threading.Thread):
    """
    详情页数据处理类
    """

    def __init__(self, thread_name, data_queue, mongo, lock):
        super(DataParse, self).__init__()
        self.thread_name = thread_name
        self.data_queue = data_queue
        # self.mongo = mongo
        self.lock = lock

    def _join_list(self, item):
        """
        处理列表的
        :param item:
        :return:
        """
        return "".join(item)

    def parse(self, data):
        """
        解析data_queue里面的数据
        :param data: data_queue.get()
        :return: pymongo
        """
        # 实例化程HTML数据
        html = etree.HTML(data)
        info = {
            # xpath解析出来之后是一个列表
            "title": self._join_list(html.xpath("//div[@class='page-header']/h1/text()")),
            "update_time": self._join_list(html.xpath("//div[@class='panel-body']/p[1]/text()")),
            "type": self._join_list(html.xpath("//div[@class='panel-body']/p[2]/text()")),
            "starring": self._join_list(html.xpath("//div[@class='panel-body']/p[3]/text()")),
            "desc": self._join_list(html.xpath("//div[@class='panel-body']/p[4]/text()")),
            "download_url": self._join_list(html.xpath("//div[@class='panel-body']/p[5]/text()")),
            "source_url": self._join_list(html.xpath("//div[@class='panel-body']/p[6]/a/text()"))
        }
        print(info)
        # 由于是多线程并发插入数据，因此使用lock来进行控制
        # with self.lock:
        #     self.mongo.insert_one(info)

    def run(self):
        print("{}启动".format(self.thread_name))
        try:
            # 从dataqueue里不断的获取这90个详情页的数据
            while not self.data_queue.empty():
                # 取数据
                detail_info = self.data_queue.get(block=False)
                # xpath解析网页数据
                self.parse(detail_info)
        except Exception as e:
            print("{} run error:{}".format(self.thread_name, e))
        print("{}结束".format(self.thread_name))


def main():
    # 页码队列
    page_queue = Queue()
    # 仅发送3页数据，用于测试
    for i in range(1, 172):
        page_url = "http://movie.54php.cn/movie/?&p={}".format(i)
        page_queue.put(page_url)
    # 电影详情页URL队列
    detail_queue = Queue()
    # 详情页数据队列
    data_queue = Queue()


    # 第一个爬虫
    page_spider_threadname_list = ["列表页采集线程1号", "列表页采集线程2号", "列表页采集线程3号"]
    page_spider_list = []
    for thread_name in page_spider_threadname_list:
        thread = PageSpider(thread_name, page_queue, detail_queue)
        # 启动线程
        thread.start()
        page_spider_list.append(thread)

    # 查看当前page_queue里面数据状态
    while not page_queue.empty():
        # 有数据的时候什么都不干
        pass
    # 释放资源
    for thread in page_spider_list:
        if thread.is_alive():
            thread.join()

    # 第二个爬虫
    detail_spider_threadname_list = ["详情页采集线程1号", "详情页采集线程2号", "详情页采集线程3号", "详情页采集线程4号", "详情页采集线程5号"]
    detail_spider_list = []
    # 启动了5个线程去抓取详情页的信息
    for thread_name in detail_spider_threadname_list:
        thread = DetailSpider(thread_name, detail_queue, data_queue)
        # 启动线程
        thread.start()
        detail_spider_list.append(thread)

    # 查看当前detail_queue里面数据状态
    while not detail_queue.empty():
        # 有数据的时候什么都不干
        pass
    # 释放资源
    for thread in detail_spider_list:
        if thread.is_alive():
            thread.join()
    # # 在这里能看到90能看到90条数据
    # print(data_queue.qsize())

    # 第三个，没有发送请求，解析数据
    # 使用Lock，要向mongo插入数据
    lock = threading.Lock()

    # 数据存入mongo,1\看虚拟机端口转发是否配置,2\mongo服务是否启动3\防火墙是否关闭,4\查看mongo的配置文件
    # myclient = pymongo.MongoClient("mongodb://127.0.0.1:1112")
    # mydb = myclient["db_movie"]
    # mycollection = mydb["movie_info"]

    # 启动多线程，处理数据
    data_parse_threadname_list = ["数据处理线程1号", "数据处理线程2号", "数据处理线程3号", "数据处理线程4号", "数据处理线程5号"]
    data_parse_list = []
    # 启动了5个线程处理详情页的信息
    for thread_name in data_parse_threadname_list:
        thread = DataParse(thread_name, data_queue, None, lock)
        # 启动线程
        thread.start()
        data_parse_list.append(thread)

    # 查看当前data_queue里面数据状态
    while not data_queue.empty():
        # 有数据的时候什么都不干
        pass
    # 释放资源
    for thread in data_parse_list:
        if thread.is_alive():
            thread.join()


if __name__ == '__main__':
    main()
