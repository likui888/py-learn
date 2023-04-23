# 登录部分，直接打开页面，点击登录就可以了
# 打开订单列表页面 http://sleeve.talelin.com/#/statics/order/list
# 抓取页面的数据,需要点击下一页,把数据存储到mongodb

# 注意事项
# 1、正确获取chrome浏览器的版本
# 2、正确的获取chrome driver的版本,下载driver
# 3、正确的设置环境变量
# 4、虚拟机是开启状态的
# 5、mongodb服务是启动的,服务的设置是正确的,虚拟机的网卡转发状态设置正常的
# 6、linux的防火墙是关闭的

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo
from selenium.webdriver.common.by import By
# 等待用包
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree


class crawl_project(object):
    def __init__(self, chrome_options):
        self.driver = webdriver.Chrome(options=chrome_options)
        # 设置浏览器的最大化
        self.driver.maximize_window()
        # 初始化mongo连接信息
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:1112")
        # 存储的数据库
        mydb = myclient["db_order"]
        # 集合
        self.mycollection = mydb["order_info"]

    def login(self, url):
        """
        登录的方法
        :param url: 登录的URL
        :return: 登录成功或失败
        """
        # 登录URLhttp://sleeve.talelin.com/#/login
        print("登录系统: {}".format(url))
        # 打开登录页面
        self.driver.get(url=url)
        if WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "login-form"))):
            # 点击登录
            self.driver.find_element_by_xpath("//button[@class='submit-btn']").click()
            if WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "welcome"))):
                print("登录成功")
                return True
            else:
                print("登录失败")
                return False

    def crawl_website(self, url):
        """
        抓取订单数据
        :param url: 订单页面的URL
        :return:
        """
        print("开始抓取订单数据")
        self.driver.get(url=url)
        while True:
            # 判断是否进入到订单页面
            if WebDriverWait(self.driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination"))):
                # page_source就是网页源代码
                self.parse_html(content=self.driver.page_source)
                # 点击翻页
                self.driver.find_element_by_xpath("//button[@class='btn-next']").click()
                if self.driver.find_element_by_xpath("//button[@class='btn-next']").get_attribute("disabled"):
                    break
        # 拿到数据之后，执行浏览器退出
        self.driver.quit()

    def parse_html(self, content):
        """
        解析网页数据
        :param content: 网页源代码
        :return:
        """
        html = etree.HTML(content)
        items = html.xpath("//tbody/tr")
        for i in items:
            # 每一个I就是每一条订单数据
            datas = i.xpath("./td/div/text()")
            status = "".join(i.xpath("./td//div[@class='tags']/span/text()"))
            data = {
                "order_id": datas[0],
                "order_num": datas[1],
                "order_value": datas[2],
                "price": datas[3],
                "status": status
            }
            # 插入到mongo
            self.mycollection.insert_one(data)


def main():
    # 可以定义一个空字典, 设置浏览器参数
    options = {
        "headless": "--headless",
        "no_sandbox": "--no-sandbox",
        "gpu": "--disable-gpu"
    }
    chrome_options = Options()
    for k, v in options.items():
        print("设置浏览器参数: {}".format(v))
        # 设置浏览器参数
        chrome_options.add_argument(v)
    s = crawl_project(chrome_options=chrome_options)
    url = "http://sleeve.talelin.com/#/login"
    # 登录操作
    login_status = s.login(url=url)
    if login_status:
        # 抓取订单数据
        s.crawl_website(url="http://sleeve.talelin.com/#/statics/order/list")


if __name__ == '__main__':
    main()
