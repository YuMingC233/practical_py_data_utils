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


def select_by_str(path, filter_str):
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
        with open(f"res/v7-{filter_str}.jsonl", "w", encoding="utf-8-sig") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
            # 截断多余的部分
            f.truncate()

    print("done")
    print(f"总共选择了 {affected_lines} 行")


def count_empty_resp():
    """
    计算文件中 response 为空的行数
    :return: None
    """
    with open("res/v7.jsonl", "r+", encoding="utf-8-sig") as f:
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


if __name__ == "__main__":
    path = "./res/v7.jsonl"
    # 需要过滤的字符串
    # filter_str = "陨悦哉"
    # filter_str = "阅灾栽"
    filter_str = "背景"

    select_by_str(path, filter_str)
    delete_by_str(path, filter_str)
    # count_str(path)
    # count_empty_resp()
