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
