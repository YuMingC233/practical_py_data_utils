import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


"""
主要分析方法，根据“说明”列中的具体关键字查找出现次数
"""


def get_stu_count_by_keyword(df, keyword):
    # 移除姓名列前后的空格
    df['姓名'] = df['姓名'].str.strip()

    # 过滤出包含 "班会" 的行
    df = df[df['说明'].str.contains(keyword)]

    # 根据姓名进行分组并计数
    result = df['姓名'].value_counts()

    # 输出各学生的出现结果
    print(result)

    # 返回结果供绘图方法使用
    return result


"""
找到出现次数的极值（最大值和最小值）
"""


def find_extremum(df, x, isSmaller):
    # 移除姓名列前后的空格
    df['姓名'] = df['姓名'].str.strip()

    # 根据姓名进行分组并计数
    result = df['姓名'].value_counts()

    if isSmaller:
        # 获取出现次数最少的学生
        return result.nsmallest(x)
    else:
        # 获取出现次数最多的学生
        return result.nlargest(x)


"""
求各学生的总分
"""


def get_total_scores(df):
    # 移除姓名列前后的空格
    df['姓名'] = df['姓名'].str.strip()

    # 将分数列中的 NaN 值替换为0
    df['分数'] = df['分数'].fillna(0)

    # 根据姓名进行分组，然后对每组的分数求和
    total_scores = df.groupby('姓名')['分数'].sum()

    return total_scores


"""
根据总分结果集由高到低排序
并根据及格线判断是否及格
"""


def is_total_score_passing(df, p_line):
    total_scores = get_total_scores(df)
    # 对结果进行排序
    sorted_scores = total_scores.sort_values(ascending=False)
    # 找出大于等于70分的学生
    students_above_70 = sorted_scores[sorted_scores >= p_line]
    # 找出小于70分的学生
    students_below_70 = sorted_scores[sorted_scores < p_line]
    print('Scores above or equal to 70:')
    print(students_above_70)
    print('\nScores below 70:')
    print(students_below_70)


"""
画出分布图
"""


def draw_dist_map(result, isRuledata):
    # 设置字体为SimHei，用来显示中文
    font = FontProperties(fname="res/艺黑简.ttf")

    # 对结果进行再次计数
    grouped_result = result.value_counts()

    # 根据索引（参会次数）进行排序
    sorted_result = grouped_result.sort_index(
        ascending=False)  # 如果你想要升序排序（从小到大），你可以将 ascending=False 改为 ascending=True。

    # 数据是否是规则的？如果是，则创建柱状图，反之亦然
    if isRuledata:
        # 创建柱状图
        plt.bar(sorted_result.index, sorted_result.values)

        # 添加标题和轴标签
        plt.title('参与次数分布', fontproperties=font)
        plt.xlabel('参与次数', fontproperties=font)
        plt.ylabel('学生数量', fontproperties=font)

    else:
        # 创建直方图
        plt.hist(result, bins=20, edgecolor='black')

        # 添加标题和轴标签
        plt.title('学生总分分布', fontproperties=font)
        plt.xlabel('总分', fontproperties=font)
        plt.ylabel('学生数量', fontproperties=font)

    # 显示图形
    plt.show()


if __name__ == '__main__':
    # 从Excel文件中读取数据
    df = pd.read_excel('res/file_2.xlsx')

    # 删除所有列都是NaN的行
    df = df.dropna(how='all')

    # 70分及格
    is_total_score_passing(df, 70)

    # 找出参加活动最少与最多的前3名学生
    # print(find_extremum(df, 3, False))  # 真为最少，假为最多

    # 求学生班会参与次数的分布情况
    # draw_dist_map(get_stu_count_by_keyword(df, "班会"), False)

    # 求学生方阵参与次数的分布情况
    # draw_dist_map(get_stu_count_by_keyword(df, "问卷"), False)
