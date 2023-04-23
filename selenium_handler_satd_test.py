# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import concurrent.futures
from lxml import etree
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# sqlalchemy 连接数据库
Base = declarative_base()


# 1.定义 selenium driver构造 web_driver 对象
class web_driver:
    def __init__(self, options, path, factory):
        # 初始化web_driver
        self.web_driver = webdriver.Chrome(options=options)
        # 爬取路径
        self.path = path
        self.page_source = None
        self.thread_factory = factory

    # 关闭web_driver
    def close_driver(self):
        self.web_driver.close()
        self.web_driver.quit()

    def read_page_source(self):
        print("====开始爬取====")
        # 获取路径打开页面
        self.web_driver.get(self.path)
        # 判断页面是否已经加载完成 显示等待
        try:
            if WebDriverWait(self.web_driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='submit-btn']"))):
                print("====已找到表单====")
                # 填充用户名
                username_ele = self.web_driver.find_element(By.XPATH, "//div[contains(@class,'nickname')]/input")
                username_ele.clear()
                username_ele.send_keys('guest')
                # 填充密码
                password_ele = self.web_driver.find_element(By.XPATH, "//div[contains(@class,'password')]/input")
                password_ele.clear()
                password_ele.send_keys('123456')
                # 点击登陆
                self.web_driver.find_element(By.XPATH, "//button[@class='submit-btn']").submit()
                # 判断是否已经登陆成功
                if WebDriverWait(self.web_driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='welcome']"))):
                    # 跳转到订单页面
                    self.web_driver.get("http://sleeve.talelin.com/#/statics/order/list")
                    # 判断是否已经跳转到订单页面
                    if WebDriverWait(self.web_driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='pagination']"))):
                        # 判断是否已经跳转到订单页面 是否还有下一页
                        while (self.web_driver.find_element(By.XPATH, "//button[@class='btn-next']").get_attribute(
                                "disabled") is None):
                            current_page = self.web_driver.find_element(By.XPATH, '//li[@class=\'number active\']').text
                            print(f"开始解析页面{current_page}")
                            # 解析页面数据 将数据扔进线程池
                            self.thread_factory.add_task_and_start(handler_page_resource(self.web_driver.page_source))
                            # 点击下一页
                            self.web_driver.find_element(By.XPATH, "//button[@class='btn-next']").click()
                            # 爬取前十页
                            if current_page == "10":
                                break
                        self.thread_factory.await_done()
        except Exception as e:
            print(e)
        finally:
            self.thread_factory.close_thread_pool()
            self.close_driver()


# 自定义线程工厂
class thread_factory:
    def __init__(self, num):
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=num)
        self.tasks = []

    def add_task_and_start(self, task):
        self.tasks.append(self.thread_pool.submit(task))

    def await_done(self):
        if len(self.tasks) > 0:
            # 等待所有任务执行完毕
            concurrent.futures.wait(self.tasks)
            print("====所有任务执行完毕====")

    # 处理结果
    def handler_result(self, func):
        for task in self.tasks:
            func(task.result())
        # 关闭线程池

    def close_thread_pool(self):
        self.thread_pool.shutdown(wait=True)


# 数据库信息操作
class db_handler:
    def __init__(self):
        self.db = None
        self.engine = create_engine('mysql+pymysql://root:lk-local@localhost:3307/spider?charset=utf8mb4', echo=True)
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(bind=self.engine)
        print("====数据库连接成功====")

    def insert_data(self, datas):
        self.session.add_all(datas)
        self.session.commit()

    # 关闭连接
    def close_db(self):
        self.session.close()
        self.engine.dispose()
        print("====数据库连接关闭====")


class trade(Base):
    # 表名
    __tablename__ = 'trade'
    # 表结构
    id = Column(Integer, primary_key=True)
    order_id = Column(String(20))
    order_num = Column(String(20))
    order_value = Column(String(20))
    price = Column(String(20))
    status = Column(String(20))


# 处理页面资源
def handler_page_resource(page_source):
    html = etree.HTML(page_source)
    print(html)
    items = html.xpath("//div[@class='el-table__fixed-body-wrapper']//tbody/tr")
    save_datas = []
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
        save_datas.append(trade(**data))
    # 插入数据库
    insert_to_db(save_datas)


# 插入数据库
def insert_to_db(spider_data):
    db_handler.insert_data(spider_data)
    pass


if __name__ == '__main__':
    # 初始化数据库
    db_handler = db_handler()
    # 初始化浏览器参数
    ChromeOptions: Options = webdriver.ChromeOptions()
    # 设置浏览器无头选项
    ChromeOptions.add_argument('--headless')
    # 设置关闭gpu
    ChromeOptions.add_argument('--disable-gpu')
    # 关闭sandbox
    ChromeOptions.add_argument('--no-sandbox')
    driver = web_driver(ChromeOptions, "http://sleeve.talelin.com/#/login", thread_factory(10))
    # 记录开始时间
    start_time = time.time()
    driver.read_page_source()
    # 记录结束时间
    end_time = time.time()
    # 计算耗时
    print(f"总耗时{end_time - start_time}")
    # 关闭数据库连接
    db_handler.close_db()
