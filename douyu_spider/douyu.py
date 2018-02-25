import time
import re
import requests
import lxml.etree
from selenium import webdriver

# 使用selenium模拟浏览器访问
driver = webdriver.Chrome()
driver.delete_all_cookies()
driver.set_window_size(1280, 2400)
driver.get("https://www.douyu.com/directory/all")

# 模拟浏览器头信息
header_base = {
    'Host': 'www.douyu.com',
    'connection': "keep-alive",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
    'upgrade-insecure-requests': "1",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.8",
    'cache-control': "no-cache",
}

# 获得响应
response = requests.get("https://www.douyu.com/directory/all", headers=header_base)

# 通过正则解析获取页面数
page_str = re.compile(r'count: "(\d+)"').search(response.text).group()
print(page_str)
# 获取最大页数
max_page = int(page_str.split('"')[1])
print("max_page:", max_page)

# 循环遍历每一页
for i in range(max_page):

    # 获取当前页面响应信息
    html = driver.page_source

    # 模拟浏览器点击下一页
    driver.find_element_by_xpath('//*[@id="J-pager"]/a[11]').click()
    time.sleep(3)

    dom = lxml.etree.HTML(html)
    # print(dom)

    # 获取斗鱼主播名称、主播类型、主播人气
    name = dom.xpath("//*[@id='live-list-contentbox']/li/a/div/p/span[1]/text()")
    type = dom.xpath("//*[@id='live-list-contentbox']/li/a/div/div/span/text()")
    population = dom.xpath("//*[@id='live-list-contentbox']/li/a/div/p/span[2]/text()")

    # 将爬取到的信息一一对应起来
    info = zip(name, type, population)

    time.sleep(1)
    # 将爬取到的信息保存到csv文件中
    with open('/home/rock/CrawDouYu/douyu1.csv', 'a') as rf:
        # 遍历爬取到的信息并处理主播人气，使其变成整形
        for n, t, p in info:
            try:
                p = int(p)
            except:
                p = int(float(p[:-1]) * 10000)
            index += 1
            # print(n, t, p)
            rf.write(n + ',')
            rf.write(t + ',')
            rf.write(str(p))
            rf.write('\n')
            rf.flush()

# 关闭并退出浏览器
driver.close()
driver.quit()
