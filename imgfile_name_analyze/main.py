import pandas as pd
import os

# 读取班级名称
df = pd.read_csv("./static/namelist.csv",encoding="gbk")

# 读取图片文件夹中所有图片的名称
path = "./static/img/"
files = os.listdir(path)
for i in files:
    foo = os.path.splitext(i.__str__())
    # 比较files中的数据相对于df中是否有缺失，如有，输出files中相对于df中缺失的数据。
    if foo[0] not in df["name"].values:
        print(foo[0])

print("全部通过！")