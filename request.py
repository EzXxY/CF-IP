import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(ip: str, port: int) -> str:
    """
    向给定IP和端口发送GET请求，返回特定响应或超时指示。

    参数:
    ip: 表示IP地址的字符串。
    port: 表示端口号的整数。

    返回:
    表示结果的字符串（'https_error' 或 'timeout'）。
    """
    url = f"http://{ip}:{port}"
    try:
        # 禁用重定向，并设置超时为 1.5 秒
        response = requests.get(url, timeout=1.5, allow_redirects=False)
        if "<center>The plain HTTP request was sent to HTTPS port</center>" in response.text:
            return 'https_error'
        return None
    except requests.exceptions.Timeout:
        return 'timeout'
    except requests.exceptions.RequestException:
        return None

def scan_ports(file_path: str) -> None:
    """
    从CSV文件中逐批读取IP和端口进行扫描，并将特定结果记录到文件中。

    参数:
    file_path: CSV文件的路径。
    """
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    with open('06-提取反代了CF的ip及端口.txt', 'w') as file:
        for start in range(0, len(df), 100):
            batch = df[start:start + 100]
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(check_port, row[0], row[1]): (row[0], row[1])
                    for row in batch.itertuples(index=False)
                }
                for future in as_completed(futures):
                    ip_port = futures[future]
                    result = future.result()
                    if result == 'https_error':
                        file.write(f"{ip_port[0]}:{ip_port[1]}\n")
            time.sleep(0.01)  # 间隔 10 毫秒，防止 CPU 被干爆

# 使用示例
file_path = './05-可视化扫描结果.csv'  # 替换为CSV文件的实际路径
scan_ports(file_path)
