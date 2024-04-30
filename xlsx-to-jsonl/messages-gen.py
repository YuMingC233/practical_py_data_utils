import csv
import json

# 定义system的content
system_content = (
    "你是一个专注于解答静脉血栓栓塞症相关问题的问答助手，你知道许多权威的学术观点，你需要利用这些学术观点，使用通俗易懂的方式解释并解决"
    "用户提出的具体问题。你可以回答用户的问题，也可以向用户提问，引导用户思考。你的目标是帮助用户提供最佳建议，"
    "并且让用户对静脉血栓栓塞症有更深入的了解。"
)

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
            # 创建messages列表
            messages = []
            # 添加system message
            messages.append({"role": "system", "content": system_content})
            # 添加user message
            messages.append(
                {
                    "role": "user",
                    "content": "请不要在对话中强调你的职责与能力，而是简短直接的回答我的问题。"
                    "如果是复杂并且解释起来有些冗长的问题，请使用一段话的形式回复我，而不是使用列表列出所有的可能。"
                    "如果你知晓，请回复“了解。”",
                }
            )
            # 添加assistant message
            messages.append({"role": "assistant", "content": "了解。"})
            # 添加user message
            messages.append({"role": "user", "content": row[0]})
            # 添加assistant message
            messages.append({"role": "assistant", "content": row[1]})
            # 创建包含messages的字典
            data_dict = {"messages": messages}
            # 转换为json格式的字符串
            json_str = json.dumps(data_dict, ensure_ascii=False)
            # 写入到jsonl文件
            jsonl_file.write(json_str + "\n")

print("转换完成！")
