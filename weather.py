# 设置编码集
# coding  = uft-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class web_driver_base:
    def __init__(self, option, path, factory):
        # 初始化web_driver
        self.web_driver = webdriver.Chrome(options=option)
        # 爬取路径
        self.path = path
        self.page_source = None
        self.thread_factory = factory

    def close_driver(self):
        self.web_driver.close()
        self.web_driver.quit()
        print("====关闭爬虫 success ====")

    def read_source(self):
        pass


class weather_spider(web_driver_base):

    def read_source(self):
        pass


class excel_handler:
    def __init__(self):

        pass
    # def handler(self):


if __name__ == '__main__':
    # 声明爬虫构造器
    # 初始化浏览器参数
    ChromeOptions: Options = webdriver.ChromeOptions()

    # 设置浏览器无头选项
    ChromeOptions.add_argument('--headless')
    # 设置关闭gpu
    ChromeOptions.add_argument('--disable-gpu')
    # 关闭sandbox
    ChromeOptions.add_argument('--no-sandbox')


    pass
