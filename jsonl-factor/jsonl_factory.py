import json


def delete_by_str(path, filter_str):
    """
    删除包含 filter_str 的行，并将更改写回文件
    :param path: 文件路径
    :param filter_str: 需要过滤的字符串
    :return: None
    """
    with open(path, "r+", encoding="utf-8-sig") as f:
        data = []
        affected_lines = 0  # 新增一个计数器
        for line in f:
            try:
                json_obj = json.loads(line)
                # 检查 prompt 和 response 中是否包含 filter_str
                if filter_str not in json.dumps(json_obj, ensure_ascii=False):
                    data.append(json_obj)
                else:
                    affected_lines += 1  # 如果过滤了这一行,计数器加1
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {line}")
                print(e)

        # 将文件指针移动到文件开头
        f.seek(0)
        # 将过滤后的数据写回文件
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
        # 截断多余的部分
        f.truncate()

    print("done")
    print(f"总共过滤了 {affected_lines} 行")


def count_str(path):
    """
    计算文件中所有 prompt 和 response 的字符数
    以推断token数量
    :param path: 文件路径
    :return: None
    """
    with open(path, "r+", encoding="utf-8-sig") as f:
        sum = 0  # 新增一个计数器
        for line in f:
            try:
                json_obj = json.loads(line)
                # 计算 prompt 和 response 中的字符数

                prompt_len = len(json_obj[0].get("prompt"))
                # 如果 response 不为为空，才计算 response 的字符数
                if json_obj[0].get("response") is not None:
                    response_len = len(json_obj[0].get("response")[0][0])
                sum += prompt_len + response_len
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {line}")
                print(e)

    print("done")
    print(f"该文件总共有字符 {sum} 个")


def select_by_str(path, filter_str, version):
    """
    选择包含 filter_str 的行，并将其写入新文件
    :param path: 文件路径
    :param filter_str: 需要过滤的字符串
    :return:
    """
    with open(path, "r+", encoding="utf-8-sig") as f:
        data = []
        affected_lines = 0  # 新增一个计数器
        for line in f:
            try:
                json_obj = json.loads(line)
                # 检查 prompt 和 response 中是否包含 filter_str
                if filter_str in json.dumps(json_obj, ensure_ascii=False):
                    data.append(json_obj)
                    affected_lines += 1  # 如果选择到了这一行,计数器加1
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {line}")
                print(e)
        # 将文件指针移动到文件开头
        f.seek(0)
        # 将过滤后的数据写到指定文件
        with open(
            f"res/broken/{version}-{clean_filename(filter_str)}.jsonl",
            "w",
            encoding="utf-8-sig",
        ) as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
            # 截断多余的部分
            f.truncate()

    print("done")
    print(f"总共选择了 {affected_lines} 行")


def add_prompt_role(path, jo, version):
    """
    添加自建的 prompt 语句
    :param path: 输入文件路径
    :param jo: 需要添加的 prompt 语句
    :param version: 输出的文件版本
    :return:
    """
    # 将 jo 字符串转换为 Python 对象
    jo = json.loads(jo)

    with open(path, "r+", encoding="utf-8-sig") as f:
        data = []
        for line in f:
            try:
                json_obj = json.loads(line)
                # 将 jo 添加到 json_obj 的开始位置
                json_obj = jo + json_obj
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error adding line: {line}")
                print(e)
        # 将文件指针移动到文件开头
        f.seek(0)
        # 将添加的数据写到指定文件
        with open(
            f"res/release/{version}.jsonl",
            "w",
            encoding="utf-8-sig",
        ) as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
            # 截断多余的部分
            f.truncate()

    print("done")


def count_empty_resp(path):
    """
    计算文件中 response 为空的行数
    :return: None
    """
    with open(path, "r+", encoding="utf-8-sig") as f:
        sum = 0  # 新增一个计数器
        for line in f:
            try:
                json_obj = json.loads(line)
                # 如果 response 为空，计数器加1
                if json_obj[0].get("response") is None:
                    sum += 1
            except json.JSONDecodeError as e:
                print(f"Error decoding line: {line}")
                print(e)

    print("done")
    print(f"该文件中 response 为空的行数为 {sum} 行")


def clean_filename(filename):
    """
    清理文件名中的非法字符
    :param filename:
    :return:
    """
    invalid_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*", "\n"]
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


if __name__ == "__main__":
    version = "v8_5"
    path = f"./res/{version}.jsonl"
    # 需要过滤的字符串
    # filter_str = "陨悦哉"
    # filter_str = "阅灾栽"
    # filter_str = "研究中"
    # filter_str = "\\n"

    # select_by_str(path, filter_str, version)
    # delete_by_str(path, filter_str)
    # count_str(path)
    # count_empty_resp()
    jo = [
        {
            "prompt": "你是一个“健康懂王”，你被专门设计用来提供静脉血栓栓塞症(VTE)及其他慢性相关健康问题的知识提供者，请在我"
            "提出问题时，尝试引导我发现自己的企图，并结合我提出的感受或其他相关信息提供对应建议，使你的建议更有说服力。"
            "如果你知晓，请回复“好的。”",
            "response": [["好的"]],
        },
        {
            "prompt": "请不要在对话中提及你的职责与能力，而是简短直接的回答我的问题，如果是复杂并且解释起来会较为冗长的问题，就使用一"
            "段话的形式回复我，而不是使用列表列出所有的可能。如果你知晓，请回复“了解。”。",
            "response": [["了解"]],
        },
    ]

    jo = json.dumps(jo, ensure_ascii=False)
    add_prompt_role(path, jo, "9.0")
