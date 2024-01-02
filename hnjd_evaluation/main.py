import os
import random
import time
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# 从.env文件中导入账号(ACCOUNT)和密码(PASSWORD)
dotenv_path = "../.env"
load_dotenv(dotenv_path)
ACCOUNT = os.getenv("HNJD_ACCOUNT")
PASSWORD = os.getenv("HNJD_PASSWORD")

back_url = (
    "http://172.16.101.107/jwglxt/xtgl/index_initMenu.html?jsdm=&_t=1704182472811"
)
busness_url = "http://172.16.101.107/jwglxt/xspjgl/xspj_cxXspjIndex.html?doType=details&gnmkdm=N401605&layout=default&su=202220220474"
msg = [
    {
        "role": "system",
        "content": "你是一位擅长根据已有的信息去为老师编写不多于50字评价的评价专家。"
        "请不要在评价中透露任何成绩，并且忽略好的地方，只给有缺陷的部分给出建设性建议。"
        "如“您需要在作业的部分着重优化，您可以尝试与学生直接沟通去改善该质量。”",
    },
]


form_data = dict()

client = OpenAI()


def select_teacher(driver):
    """
    选择老师
    :param driver:
    :return:
    """

    need_handle = input("请输入您需要手动评价的老师，使用英文逗号分隔。" "选择完毕后按回车键继续，为空则全部随机：")
    print("正在选择老师...")
    # 获取css path为#tempGrid .jqgrow的所有老师的行
    rows = driver.find_elements(By.CLASS_NAME, "jqgrow")
    for i in range(len(rows)):
        # 重新获取行元素，以确保它们是最新的并且与DOM关联
        try:
            row = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "jqgrow"))
            )[i]

            # 检查行内是否存在title为“提交”的td
            if len(row.find_elements(By.CSS_SELECTOR, "td[title='提交']")) != 0:
                continue
            # 检查行内是否存在title为“已评完”的td
            elif len(row.find_elements(By.CSS_SELECTOR, "td[title='已评完']")) != 0:
                continue
            # 点击该row
            row.click()
            # 等待2秒
            time.sleep(2)
            if i + 1 in need_handle.split(","):
                fill_form(driver, True)
            else:
                fill_form(driver, False)
        except StaleElementReferenceException:
            break


# 自动填写表单方法
def fill_form(driver, Handle):
    global all_select

    all_select = False

    # 查找class为form-group的form-group列表
    rows = driver.find_elements(By.CSS_SELECTOR, ".tr-xspj")

    # 收集所有的form_groups
    all_form_groups = []
    for row in rows:
        form_groups = row.find_elements(By.CSS_SELECTOR, ".form-group")
        all_form_groups.extend(form_groups)  # 将这个row的form_groups添加到总列表中

    # 检查是否所有的form_groups中都有被选中的radio元素
    if all(
        form_group.find_element(By.CSS_SELECTOR, 'input[type="radio"]').is_selected()
        for form_group in all_form_groups
    ):
        all_select = True

    if not all_select:
        # 遍历form_groups，并点击其中的第一个radio标签
        for form_group in all_form_groups:
            form_group.find_element(By.CSS_SELECTOR, 'input[type="radio"]').click()
            # 等待0.5秒
            time.sleep(0.5)
        if not Handle:
            # 随机选择一个radio
            random_choice(driver)

    if Handle:
        comment = get_comment(generate_prompt()).content
        # 查找name为py的textarea标签，并输入评语
        driver.find_element(By.NAME, "py").send_keys(comment)
        # 点击提交按钮
        submit()
    else:
        if input("请检查评分是否正确，正确则按回车键继续，否则请手动评价后再按回车：") == "":
            print("正在生成评语...")
        comment = get_comment(generate_prompt()).content
        # comment = hitokoto_comment()
        # 查找name为py的textarea标签，并输入评语
        driver.find_element(By.NAME, "py").send_keys(comment)
        # 点击保存按钮
        save()


def submit():
    """
    点击提交按钮
    :return:
    """
    driver.find_element(By.ID, "btn_xspj_tj").click()
    driver.find_element(By.ID, "btn_ok").click()
    time.sleep(2)


def save():
    """
    点击保存按钮
    :return:
    """
    driver.find_element(By.ID, "btn_xspj_bc").click()
    driver.find_element(By.ID, "btn_ok").click()
    time.sleep(2)


def hitokoto_comment():
    """
    获取一言评语
    :return:
    """
    # 请求获得一个来自诗词的句子，并以纯文本格式输出
    response = requests.get("https://v1.hitokoto.cn/?k=f&encode=text")
    return response.text


def generate_prompt():
    """
    根据目前的表单结果生成prompt
    :return:
    """
    # 查找class为form-group的form-group列表
    rows = driver.find_elements(By.CSS_SELECTOR, ".tr-xspj")

    # 枚举映射
    enum_map = {0: "A", 1: "B", 2: "C", 3: "D"}
    # 获取所有的教学质量评价信息与对应的评价，作为大模型的prompt
    for row in rows:
        # 在每个row元素中查找第一个td下的文字
        info = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        radios = row.find_elements(By.CSS_SELECTOR, ".radio-pjf")

        # 获取第几个radio被选中
        radio_index = None
        for index, radio in enumerate(radios):
            if radio.is_selected():
                radio_index = index
                break

        # 将radio_index转换为enum类型的A:0,B:1
        if radio_index is not None:
            form_data.update({info[1:]: enum_map[radio_index]})

    prompt = "目前的评价结果如下：\n"

    for key, value in form_data.items():
        prompt += f"{key}，评价为：{value}。\n"

    return prompt


def random_choice(driver):
    # 获取所有的form-group
    form_groups = driver.find_elements(By.CSS_SELECTOR, ".form-group")
    # 随机选择从第五个5开始的form_group，除了最后一个
    random_index = random.randint(5, len(form_groups) - 2)
    selected_form_group = form_groups[random_index]
    # 在选定的form_group中选择第二个radio
    second_radio = selected_form_group.find_elements(
        By.CSS_SELECTOR, 'input[type="radio"]'
    )[1]
    second_radio.click()


# 自动根据评价等级生成评语的方法
def get_comment(prompt):
    msg.append(
        {"role": "user", "content": "请你根据下面的质量评价等级，为老师编写不多于50字评价的评论：\n" + prompt}
    )

    response = client.chat.completions.create(model="gpt-4-1106-preview", messages=msg)

    # 生成评语
    return response.choices[0].message


def init_driver():
    # 访问网页
    driver.get(back_url)
    driver.add_cookie(
        {"name": "JSESSIONID", "value": "4263217443BF89F0B6B92414BB977045"}
    )
    driver.add_cookie({"name": "route", "value": "f12953d92e58f8a8129d6825fc19007f"})
    driver.maximize_window()
    # 等待2秒
    time.sleep(2)
    # 刷新网页
    driver.refresh()
    # 重新访问指定网页
    driver.get(busness_url)
    # 查找name为currentPage的select
    select = driver.find_element(By.NAME, "currentPage")
    # 选择value为100的option
    select.find_element(By.CSS_SELECTOR, "option[value='100']").click()
    # 等待3秒
    time.sleep(3)
    return driver


if __name__ == "__main__":
    driver = webdriver.Chrome()
    select_teacher(init_driver())
