import os
import subprocess

# 仓库路径列表
repositories = [
    "E://Projects/WebstormProject/law-quiz-admin",
    "E://Projects/WXProjects/sip_spring_life_wx"
]

author = "Connor White"
since = "last.week"

# 初始化统计数据
total_commits = 0
total_added_lines = 0
total_removed_lines = 0

def run_git_command(command):
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = result.communicate()
    if result.returncode != 0:
        print(f"Error executing command: {stderr}")
        return ""
    return stdout

# 遍历所有仓库
for repo in repositories:
    # 切换到仓库目录
    os.chdir(repo)

    # 统计提交次数
    commit_count_command = f'git log --author="{author}" --since={since} --pretty=oneline'
    commit_count_output = run_git_command(commit_count_command)
    commit_count = len(commit_count_output.splitlines())
    total_commits += commit_count

    # 统计更改的代码行数
    lines_changed_command = f'git log --author="{author}" --since={since} --pretty=tformat: --numstat'
    lines_changed_output = run_git_command(lines_changed_command)

    added_lines = 0
    removed_lines = 0

    for line in lines_changed_output.splitlines():
        if line.strip():  # 确保行不为空
            parts = line.split()
            if len(parts) >= 2:
                added = parts[0].replace('-', '0')
                removed = parts[1].replace('-', '0')
                added_lines += int(added)
                removed_lines += int(removed)

    total_added_lines += added_lines
    total_removed_lines += removed_lines

# 输出总计结果
print(f"Total commits: {total_commits}")
print(f"Total added lines: {total_added_lines}")
print(f"Total removed lines: {total_removed_lines}")
print(f"Total lines changed: {total_added_lines + total_removed_lines}")
