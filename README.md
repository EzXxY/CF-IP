# 1. 期望目标：


>  ① 使用开源的 masscan 工具寻找好线路 IP 下开放的端口；


>  ② 使用 Python 调用 CloudFlare 的公开 API【/cdn-cgi/trace】，寻找反代了 CF 的 IP 及套了 TLS 的端口；


>  ③ 针对找到的【IP:port】并行测速，寻找自己网络下的优选 IP 及端口。


# 2. 使用开源的 masscan 工具寻找好线路 IP 下向大众都公开开放的端口

&emsp;&emsp;据  **masscan**  自己官方介绍，他们家这个开源的工具可以在 5 分钟之内扫描全网所有的服务器端口开放情况，[GitHub 链接](https://github.com/robertdavidgraham/masscan)。我们作为小用户，只需要找适合自己网站服务器的优质线路全段 IP 下的端口即可，之后的用途很广泛，本篇以 **使用 SaaS 回源，让海内外华人同胞高速访问你的网站服务** 为例，介绍全部操作流程。

&emsp;&emsp;建议使用 Linux 服务器完成这一步的操作，最好是 Debian 或者 Ubuntu 系统。

```bash
# 安装 masscan
apt install masscan
```

&emsp;&emsp;高效使用这个工具，寻找好线路的多个IP段下全部公开开放的端口号。以 **搬瓦工 HK85** 这条线路为例，如果要用机器上的其他网络接口（比如 warp）来扫描，在命令后面加上 **【--interface warp】** 即可。

```bash
# 快速寻找反代了 CF 的 IP 及端口，并保存成 .xml 文件
masscan 149.62.46.0/24 149.62.47.0/24 157.119.100.0/24 157.119.101.0/24 -p0-65535 -oX scan_HK85_2023-12-16.xml --rate 1000000
```

&emsp;&emsp;稍等几分钟就找完并保存到当前路径下了，可以看到，masscan 支持多个 CIDR 形式的 IP 段扫描，上面的命令扫描的是 4 个 24 位网络前缀的 IP 全段，如果不知道 CIDR 的表示方法，请查看[这里的 CIDR 网络地址计算器](https://www.sioe.cn/xinqing/CIDR.php)。命令中 **-p** 紧跟着的是要扫描的端口范围，可以是这样的大范围，也可以是 **-p80,443,2052** 这样的小范围。 **-oX** 代表输出的是一个xml文件，方便折叠等在浏览器查看。 **--rate** 表示的是扫描速率，填了这个 **100万** 比不填快很多，但也没有给机器造成多大的负载。

---

> # 如何自己找优质线路 CIDR 格式的 IP 地址呢？

&emsp;&emsp;用 ipinfo.io 查厂商的 ASN 编号即可，比如这个搬瓦工 HK85 的 ASN 是 AS9312，那么查询他家所有 IP 段的网址为：[https://ipinfo.io/AS9312]
(https://ipinfo.io/AS9312)，只知道某家的一个测试 IP，可以来我搭建的批量查 IP 的网站查询他家的 ASN 值：[https://ip.ezxxy.work](https://ip.ezxxy.work)。因为我的网页是用 VUE 写的，所以第一次加载会稍微慢一点，以后的加载就很快，哈哈。如果想要看他家 IPv4 的上游关系图表，链接在这里：[https://bgp.he.net/AS9312#_graph4]
(https://bgp.he.net/AS9312#_graph4)。

&emsp;&emsp;这就是 **搬瓦工HK85 ASN9312** 现阶段的 IPv4 地址范围和其他托管域。

![厂家 ASN 下的 IP 地址范围](https://ezxxy.github.io/img/03-反代IP/IP地址.png) 
![厂家 ASN 下的其他托管域](https://ezxxy.github.io/img/03-反代IP/其他托管域.png) 

---

# 3. 使用 Python 调用 CloudFlare 的 API，快速找套了 tls 的 IP:port

&emsp;&emsp;点击链接下载我的 Python 代码和适用于 Windows 的一步一步的 .bat 批处理文件压缩包，[下载链接](https://urls.ezxxy.work/CF)。刚刚开源到了 [GitHub](https://github.com/EzXxY/CF-IP)，你也可以来给我按一个 Star⭐  呦！

&emsp;&emsp;将上一步提取出的 **scan_HK85_2023-12-16.xml** 文件放到下载并解压好的 **CF-IP-1.0.zip** 文件目录下。除了 Python 安装好自带的标准库之外，只需要安装 **requests和pandas** 这两个库即可执行以下内容的全部 Python 程序。可以在当前路径下的命令行窗口中执行以下语句进行安装。

```bash
pip install -r requirements.txt
```

&emsp;&emsp;如果是 Windows 用户，请直接按顺序双击 **00-可视化扫描结果.bat** 、 **01-提取反代了CF的ip及端口.bat** 和  **02-可视化排序成csv.bat** ，等待执行完成即可看到 **05-可视化扫描结果.csv** 、 **06-提取反代了CF的ip及端口.txt** 和  **07-提取反代了CF的ip及端口.csv**  这三个文件。

&emsp;&emsp;如果是 Linux 用户，请打开 **000-执行顺序，Windows系统直接按顺序双击bat文件即可.txt** 这个文件一步一步执行即可。此处只需要执行：

```bash
# 将第一步提取的，放到当前路径下的任意名字的.xml 文件转化为 05-可视化扫描结果.csv 文件
python xml_to_csv_parser_updated_no_duplicates.py ./ ./05-可视化扫描结果.csv

# 测试扫描到的端口是否为反代了 CloudFlare 的 CDN 时，可以开全局代理测试，这一步时间比较久，会输出 06-提取反代了CF的ip及端口.txt 这么一个每行都是 IP:port 的反代了 CF 的 IP 的形式
python request.py

# 将 txt 转化为 csv
python txt_2_csv.py ./06-提取反代了CF的ip及端口.txt ./07-提取反代了CF的ip及端口.csv
```

&emsp;&emsp;这一步到这里，不同系统都会得到想要的套了 tls 的 IP:port 形式的 txt 和更加便于人类观察和分析的可视化的 csv 文件了。以下是对  **request.py**  这一文件的简单解释，不需要修改参数的小伙伴，可以直接看 4.XXX 了。

---

&emsp;&emsp;这个 Python 文件是在给扫描得到的 .xml 经过转化、排序为 **05-可视化扫描结果.csv** 这一文件的每一个  **IP**  和  **端口号**  并行发送 http 请求（每 1.51 秒并行发送 100 个请求并处理），请求的链接为 **“http://IP:port/cdn-cgi/trace”** ，如果得到了这个端口反代了 CloudFlare 的 CDN，则记录在 **06-提取反代了CF的ip及端口.txt** 文件中，如果请求超过了 1.5 秒没有响应或者不是反代了 CF 的 IP及端口，则丢弃。实测处理 160000 行 IP 和 端口 的 csv 文件，需要一个小时左右，6000 行的只需要不到 3 分钟。以下是详细的 Python 文件，懂的可以简单看看，并按照自己的意愿修改这些参数。

 **【request.py】** 

```python
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

```

---


# 4. 对找到的 IP:port 并行测速，寻找适合自己网站线路的反代 IP

&emsp;&emsp;并行测速时使用的是开源的[CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)程序，如果是其他系统，请前往下载 v2.2.4 版本的程序文件并放置在我的这个文件夹内，如果是 Windows 系统，则可以直接使用。

&emsp;&emsp;如果是 Windows 用户，请直接按顺序双击 **03-开始针对性测速.bat** 和 **04-查看测试结果.bat** 稍等片刻即可看到 **08-针对性测速结果完整文件.txt** 和 **09-最终可视化测试结果.csv** 这两个文件了。

&emsp;&emsp;如果是 Linux 用户，请打开 **000-执行顺序，Windows系统直接按顺序双击bat文件即可.txt** 这个文件一步一步执行即可。此处只需要执行：

```bash
# 测速时不能开代理，要测试本机连接的真实速度
python SpeedTest.py

# 冗余的 txt 转为对人类可视化及其友好的筛选干净的 csv
python filter.py
```

&emsp;&emsp;到这里，找自己喜欢的优质线路的反代IP的过程就已经完成了，所有程序已经由 ChatGPT 写好了，只要一步一步执行即可，是不是很简单呀？

&emsp;&emsp; **SpeedTest.py** 中有一些可以调节的参数，希望大家都注意一下：测速需要使用本地网络。如果哪一天代码中的测速链接失效了，请更换为自己的测速链接。针对性批量测速是对 50 个确定反代了 CloudFlare CDN 的 IP 和 端口 进行并行测速，对着50个端口测速，只会占用一个给你的宽带拉满的带宽，速度仅供参考，如果需要精确测速，请手动一个一个测。并且给定的测速超时时间是 20 秒，所有测速临时文件所在目录已经打印到了命令行窗口中，可以前往那个路径自行查看测速进度。或者打开“任务管理器”这种面板看本地网络的使用情况。这些提到的参数可以尽情修改使用。

 **【SpeedTest.py】** 

```python
import subprocess
import threading
from queue import Queue
import os
import tempfile

def run_command(ip_port: str, output_file: str) -> None:
    ip, port = ip_port.split(':')
    
    # 【！！！如果哪天下面这个测速链接不能用了，请换成自己的测速链接！！！】
    command = f"CloudflareST.exe -url https://cloudflare.cdn.openbsd.org/pub/OpenBSD/7.3/src.tar.gz -o "" -tl 5000 -dn 20 -p 20 -ip {ip} -tp {port}"
    
    with open(output_file, "w") as file:
        process = subprocess.Popen(command, shell=True, stdout=file, stderr=subprocess.STDOUT,
                                   creationflags=subprocess.CREATE_NO_WINDOW)

        try:
            process.wait(timeout=20)  # 并行测速 50 个确定反代了 CloudFlare 的【ip:port】时，总的超时时间，单位（秒）
        except subprocess.TimeoutExpired:
            pass

        process.send_signal(subprocess.signal.CTRL_C_EVENT)

def worker(queue: Queue, output_dir: str) -> None:
    while not queue.empty():
        ip_port = queue.get()
        temp_file = os.path.join(output_dir, f"output_{ip_port.replace(':', '_')}.txt")
        run_command(ip_port, temp_file)
        queue.task_done()

def main() -> None:
    input_file = '06-提取反代了CF的ip及端口.txt'
    output_file = '08-针对性测速结果完整文件.txt'
    max_threads = 50  # 并行测速的数量

    queue = Queue()
    threads = []
    output_dir = tempfile.mkdtemp()
    print(f"临时测速结果文件夹路径: {output_dir}")

    with open(input_file, 'r') as file:
        for line in file:
            queue.put(line.strip())

    for _ in range(min(max_threads, queue.qsize())):
        thread = threading.Thread(target=worker, args=(queue, output_dir))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # 顺序合并临时文件
    temp_files = sorted(os.listdir(output_dir))
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in temp_files:
            with open(os.path.join(output_dir, filename), 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n')

if __name__ == "__main__":
    main()

```

&emsp;&emsp;最后的文件夹情况如下图：

![最后的文件情况](https://ezxxy.github.io/img/03-反代IP/最后的文件情况.jpg) 

&emsp;&emsp;经过上述的操作，相信你在测了几个 IP 段之后，已经找到了自己想要的线路的优选 IP 及其套了 TLS 的 端口号。当前给出的 HK85 是有可用的 IP 及端口的。接下来就可以干很多事情啦，以 **SaaS 回源** 为例，可以参考下面链接的大佬的文章，这样的教程已有很多，我就不自己写了。

【[使用 SaaS 回源，让海内外华人同胞高速访问你的网站服务！](https://dooo.ng/archives/1701171631107)】

&emsp;&emsp;上面的 Python 文件全部出自 **gpt4**，已经完成了想要的功能，而且找得很快。

&emsp;&emsp;找我当前给的 4 个 24 位网络前缀的 IP 全段所有端口的 搬瓦工 HK85 线路的反代 IP 只需要不到 40 分钟，具体时间请大家自行在本地测试。

