import re
import csv

# 定义输入和输出文件名
input_file = "08-针对性测速结果完整文件.txt"
output_file = "09-最终可视化测试结果.csv"

# 定义CSV文件的表头
header = ["IP地址", "已发送", "已接收", "丢包率", "平均延迟", "下载速度 (MB/s)", "端口号"]

# 用于匹配IP地址和端口号的正则表达式
ip_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
port_regex = r"端口：(\d+)，"

# 用于存储提取的数据
data = []

# 读取results.txt文件
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 清理行末尾的空格
lines = [line.strip() for line in lines]

# 查找包含IP地址且最后三个数字不是0.00的行
for i, line in enumerate(lines):
    ip_match = re.search(ip_regex, line)
    if ip_match:
        ip = ip_match.group()
        values = line.split()
        if not values[-1].endswith("0.00"):
            # 向上查找端口号
            port = None
            for j in range(i - 1, -1, -1):  # 从当前行向上搜索
                port_match = re.search(port_regex, lines[j])
                if port_match:
                    port = port_match.group(1)
                    break

            # 如果找到端口号，提取需要的数据
            if port:
                data.append([ip] + values[1:] + [port])
            else:
                print(f"警告：未找到IP地址 {ip} 的端口号。")

# 写入CSV文件
with open(output_file, "w", encoding="GBK", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data)

print("提取完成！")
