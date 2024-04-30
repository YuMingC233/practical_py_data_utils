import csv
import json

# 打开csv文件
with open("input.csv", "r", encoding="utf-8-sig") as csv_file:
    # 创建csv reader
    reader = csv.reader(csv_file)
    # 获取表头
    headers = next(reader)

    # 创建jsonl文件
    with open("output/aizc-messages.jsonl", "w", encoding="utf-8") as jsonl_file:
        # 遍历csv reader
        for row in reader:
            # 创建字典
            data_dict = {headers[i]: row[i] for i in range(len(headers))}
            # 转换为json格式的字符串
            json_str = json.dumps(data_dict, ensure_ascii=False)
            # 写入到jsonl文件
            jsonl_file.write(json_str + "\n")

print("转换完成！")
