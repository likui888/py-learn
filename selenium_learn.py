import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#chrome driver 下载地址
# https://npm.taobao.org/mirrors/chromedriver/
# 定义selenium
# driver = webdriver.Chrome()
#设置浏览器无头选项
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#关闭sandbox
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
# 获取路径
driver.get("https://www.baidu.com")

# 获取xpath 路径
inputSearch = driver.find_element('xpath', '//input[@id="kw"]')
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id="kw"]')))

#隐式等待
driver.implicitly_wait(10)

inputSearch.find_elements('name', 'wd')
assert inputSearch
# 清空输入框
inputSearch.clear()
inputSearch.send_keys("Python")
inputSearch.submit()
time.sleep(1)
# 设置浏览器串口
driver.close()
driver.quit()


