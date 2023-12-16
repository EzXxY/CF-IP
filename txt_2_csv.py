import csv
import sys
import os
import ipaddress

def sort_and_save_to_csv(txt_file, csv_file):
    data = set()
    try:
        # 读取并解析 txt 文件
        with open(txt_file, 'r') as file:
            for line in file:
                ip, port = line.strip().split(':')
                data.add((ip, port))

        # 根据IP地址和端口号进行排序
        sorted_data = sorted(data, key=lambda x: (ipaddress.ip_address(x[0]), int(x[1])))

        # 将排序后的数据写入 CSV 文件
        with open(csv_file, mode='w', newline='', encoding='GBK') as file:
            writer = csv.writer(file)
            writer.writerow(['IP 地址', '反代 CF 的端口'])
            for ip, port in sorted_data:
                writer.writerow([ip, port])
        print(f"Data successfully written to {csv_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_txt_file> <output_csv_file>")
    else:
        txt_file_path = sys.argv[1]
        csv_file_path = sys.argv[2]
        sort_and_save_to_csv(txt_file_path, csv_file_path)
