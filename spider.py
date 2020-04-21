# coding=utf-8

import time
import os
import re

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def get_ans_cnt(nums):
    ans = 0
    for i in range(len(nums)):
        ans = ans * 10 + int(nums[i])
    return ans


def ZhiHuSpider():

    # 创建可见的Chrome浏览器， 方便调试
    driver = webdriver.Chrome()
    action = ActionChains(driver)

    # 创建Chrome的无头浏览器
    # opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # driver = webdriver.Chrome(options=opt)

    driver.implicitly_wait(10)
    crawled = 0

    driver.get("https://www.zhihu.com/question/304706190")

    answer_count = re.findall(r"\d", driver.find_element_by_class_name("List-headerText").text)
    answer_count = get_ans_cnt(answer_count)
    print(answer_count)

    question_title = driver.title[:-6]

    pop_flag = False
    with open(question_title + ".txt", "a") as f:
        while crawled < answer_count:
            list_items = driver.find_elements_by_class_name("List-item")
            for i in range(crawled, len(list_items)):
                item = list_items[i]
                # author = json.loads(item.find_element_by_tag_name("div").get_attribute("data-zop"))["authorName"]
                figures = item.find_elements_by_tag_name("figure")
                for figure in figures:
                    img = figure.find_element_by_tag_name("img").get_attribute("data-original")
                    print(img)
                    if img:
                        f.write(img+"\n")
                crawled += 1
                print(crawled)
                print("1秒后抓取下一个用户回答")
                time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if not pop_flag:
                action.move_by_offset(200, 100).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标
                action.reset_actions()
                action.move_by_offset(200, 100).click().perform()
                pop_flag = True
            time.sleep(3)
    driver.quit()


def download(url, path):
    res = requests.get(url.strip())
    ima_name = os.path.join(path, url.split("/")[-1].strip())
    with open(ima_name, "wb") as new_img:
        new_img.write(res.content)


if __name__ == '__main__':
    # ZhiHuSpider()
    if not os.path.exists("images"):
        os.makedirs("images")
    count = 0
    with open("images.txt", "r") as f:
        line = f.readline()
        while line:
            if count > 1106:
                download(line, "images")
            count += 1
            print("已下载" + str(count) + "张图片")
            # if count % 100 == 0:
            #     time.sleep(5)
            line = f.readline()
