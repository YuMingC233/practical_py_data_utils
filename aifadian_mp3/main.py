import os
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import threading
from concurrent.futures import ThreadPoolExecutor

# 从.env文件中导入账号(ACCOUNT)和密码(PASSWORD)
dotenv_path = '../.env'
load_dotenv(dotenv_path)
ACCOUNT = os.getenv('AFD_ACCOUNT')
PASSWORD = os.getenv('AFD_PASSWORD')


# 使用selenium登录网页后获取网页源代码
def get_html(url):
    driver = webdriver.Chrome()
    # 获取网页源代码
    driver.get(url)
    driver.maximize_window()
    # 登录网页
    login(driver)
    while True:
        # 获取滚动相关的参数
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_top = driver.execute_script("return window.scrollY")
        inner_height = driver.execute_script("return window.innerHeight")

        # 判断是否到达底部
        if scroll_top + inner_height < scroll_height:
            # 线性滚动网页到底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 等待页面加载
            time.sleep(3)
        else:
            # 跳出循环
            break
    # 获取网页源代码
    html = driver.page_source
    # 保持浏览器
    # driver.quit() # 退出浏览器
    return html


def login(driver):
    # 查找name为account的input标签，并输入账号
    driver.find_element(By.NAME, 'account').send_keys(ACCOUNT)
    # 查找name为password的input标签，并输入密码
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
    # 查找class为.btn-group > .vm-btn的div标签，并点击
    driver.find_element(By.CSS_SELECTOR, '.btn-group > .vm-btn').click()
    # 等待3秒
    time.sleep(3)


# 使用bs4解析网页源代码
def get_mp3(html):
    # 使用lxml解析网页源代码
    soup = BeautifulSoup(html, 'lxml')
    # 获取网页中的所有class名称为feed-content的div标签列表
    feed_content_list = soup.find_all('div', class_='feed-content')
    # 创建mp3字典
    mp3_list = []
    # 遍历feed_content_list
    for feed_content in feed_content_list:
        # 获取feed_content中的所有class名称为audio的audio标签列表
        audio = feed_content.find('audio')
        # 获取feed_content中的所有class路径为 .title-box > a标签下的string
        title_element = feed_content.select('.title-box > a')

        # 检查是否找到了title元素，并获取其内容
        title = title_element[0].contents if title_element else None

        # 检查是否找到了audio标签，并获取其src属性
        href = audio.get('src') if audio else None

        # 将mp3字典添加到mp3列表中
        mp3 = {
            'title': title,
            'href': href
        }
        mp3_list.append(mp3)
    # 返回mp3列表
    return mp3_list


def download_mp3_data(mp3):
    title = mp3['title'][0] if mp3['title'] else None
    mp3_name = clean_filename(title)
    href = mp3['href']
    mp3_data = requests.get(href).content
    return mp3_data, mp3_name


def save_mp3(mp3_data, mp3_name):
    with open('mp3/' + mp3_name + '.mp3', 'wb') as f:
        f.write(mp3_data)
        print('正在下载%s' % mp3_name)


def download_mp3s(mp3_list, max_threads=5):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # 提交下载任务到线程池
        future_to_mp3 = {executor.submit(download_mp3_data, mp3): mp3 for mp3 in mp3_list}
        for future in future_to_mp3:
            mp3_data, mp3_name = future.result()
            save_mp3(mp3_data, mp3_name)


# 替换或移除文件名中的特殊字符
def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|"]+', '', filename)


# 主函数
if __name__ == '__main__':
    # 获取网页源代码
    html = get_html('https://afdian.net/album/d2357224a78511ec914952540025c377')
    # 获取mp3列表
    mp3_list = get_mp3(html)
    # 如果list中的任何项为None，则删除该项
    mp3_list = [mp3 for mp3 in mp3_list if mp3['title'] and mp3['href']]
    # 下载mp3
    download_mp3s(mp3_list)
