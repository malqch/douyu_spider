import time
import re
import requests
import lxml.etree
from selenium import webdriver

driver = webdriver.Chrome()
driver.delete_all_cookies()
driver.set_window_size(1280, 2400)
driver.get("https://www.douyu.com/directory/all")

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

response = requests.get("https://www.douyu.com/directory/all", headers=header_base)

page_str = re.compile(r'count: "(\d+)"').search(response.text).group()
print(page_str)
max_page = int(page_str.split('"')[1])
print("max_page:", max_page)

index = 0
for i in range(max_page):

    html = driver.page_source

    driver.find_element_by_xpath('//*[@id="J-pager"]/a[11]').click()
    time.sleep(3)
    # r.encoding = 'utf-8'
    # print(r)

    dom = lxml.etree.HTML(html)
    # print(dom)

    name = dom.xpath("//*[@id='live-list-contentbox']/li/a/div/p/span[1]/text()")
    type = dom.xpath("//*[@id='live-list-contentbox']/li/a/div/div/span/text()")
    population = dom.xpath("//*[@id='live-list-contentbox']/li/a/div/p/span[2]/text()")

    info = zip(name, type, population)

    time.sleep(1)
    with open('/home/rock/CrawDouYu/douyu1.csv', 'a') as rf:
        for n, t, p in info:
            try:
                p = int(p)
            except:
                p = int(float(p[:-1]) * 10000)
            index += 1
            # print(n, t, p)
            # rf.write(str(index))
            rf.write(n + ',')
            rf.write(t + ',')
            rf.write(str(p))
            rf.write('\n')
            rf.flush()


driver.close()
driver.quit()
