import re
import os
import pyperclip


while True:
    # 获取markdown写法的图片链接
    src = input("请输入图片链接：")
    if src == "exit":  # 如果用户输入"exit"，则退出循环
        break
    match = re.search(r"\!\[.*?\]\((.*?)\)", src)
    if match:
        img_src = match.group(1)
        pyperclip.copy(img_src)  # 复制到剪贴板
        print("已复制到剪切板……")
    else:
        print("未找到图片地址，请确保输入的格式正确。")
