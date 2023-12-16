import xml.etree.ElementTree as ET
import csv
import sys
import os
import ipaddress

def parse_xml_and_save_to_csv(xml_file, csv_file):
    data = set()
    try:
        # 解析 XML 文件
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 提取数据
        for host in root.findall('host'):
            ip_address = host.find('address').get('addr')
            ports = host.find('ports')
            if ports:
                for port in ports.findall('port'):
                    port_number = port.get('portid')
                    data.add((ip_address, port_number))

        # 按 IP 地址和端口号排序数据
        sorted_data = sorted(data, key=lambda x: (ipaddress.ip_address(x[0]), int(x[1])))

        # 将排序后的数据写入 CSV
        with open(csv_file, mode='w', newline='', encoding='GBK') as file:
            writer = csv.writer(file)
            writer.writerow(['IP 地址', '端口号'])
            for ip, port in sorted_data:
                writer.writerow([ip, port])
        print(f"数据已成功写入 {csv_file}")
    except Exception as e:
        print(f"发生错误：{e}")

def process_directory(directory, output_csv):
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(directory, filename)
            parse_xml_and_save_to_csv(xml_file_path, output_csv)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python3 script.py <输入目录或xml文件> <输出csv文件>")
    else:
        input_path = sys.argv[1]
        csv_file_path = sys.argv[2]
        if os.path.isdir(input_path):
            process_directory(input_path, csv_file_path)
        else:
            parse_xml_and_save_to_csv(input_path, csv_file_path)
