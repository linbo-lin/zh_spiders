# coding=utf-8

import time
import os
import json

import requests
from selenium import webdriver


def ZhiHuSpider():

    # 创建可见的Chrome浏览器， 方便调试
    driver = webdriver.Chrome()

    # 创建Chrome的无头浏览器
    # opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # driver = webdriver.Chrome(options=opt)

    driver.implicitly_wait(10)
    count = 1

    driver.get("https://www.zhihu.com/question/304706190")

    question_title = driver.title[:-6]
    if not os.path.exists(question_title):
        os.makedirs(question_title)

    list_items = driver.find_elements_by_class_name("List-item")
    time.sleep(5)
    for item in list_items:
        author = json.loads(item.find_element_by_tag_name("div").get_attribute("data-zop"))["authorName"]
        print(author)
        if not os.path.exists(os.path.join(question_title, author)):
            os.makedirs(os.path.join(question_title, author))
        figures = item.find_elements_by_tag_name("figure")
        for figure in figures:
            img = figure.find_element_by_tag_name("img").get_attribute("data-original")
            print(img)
            if img:
                res = requests.get(img)
                ima_name = os.path.join(question_title, author, img.split("/")[-1])
                with open(ima_name, "wb") as f:
                    f.write(res.content)
        print("5秒后抓取下一个用户回答")
        time.sleep(5)

    driver.quit()


if __name__ == '__main__':
    ZhiHuSpider()
