import random
import time
import warnings
import requests
import threading
from colorama import Fore, Style, init
import urllib3
from tqdm import tqdm

# 初始化Colorama，使其在 Windows 终端中正常工作
init(autoreset=True)

# 关闭警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")
lock = threading.Lock()

# 路径请求
"""
路径扫描
"""
def ask(url):
    with lock:
        try:
            response = requests.get(url,timeout=1)
            if response.status_code == 200 and "This application has no configured error view, so you are seeing this as a fallback." not in response.text and "40" not in response.text and "50" not in response.text:
                print(Fore.GREEN + f"Success: 存在接口：{url}" + Style.RESET_ALL)
                with open("./result/success.txt", "a+", encoding="utf-8") as f:
                    f.write(url + "\n")
            else:
                print(Fore.WHITE + f"Filded 不存在接口：{url}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Error: 访问失败{url}" + Style.RESET_ALL)

def scan(urls):
    for url in urls:
        ask(url)


# 基础路径扫描
"""
基础路径扫描 
springboot_urls.txt
"""
def scan_base(baseurl):
    with open("./config/springboot_urls.txt", "r", encoding="utf-8") as f:
        springboot_url_paths = f.readlines()

    url_paths = []
 
    for url_path in springboot_url_paths:
        url_path = url_path.strip()
        url_paths.append(baseurl + url_path)

    # 分成10个线程
    threads = []
    path_thread = len(url_paths) // 10
    for i in range(10):
        start_index = i * path_thread
        end_index = (i + 1) * path_thread if i != 9 else len(url_paths)
        thread_lines = url_paths[start_index:end_index]

        thread = threading.Thread(target=scan, args=(thread_lines,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


# 前缀接口式路径扫描
"""
前缀接口式路径扫描 
api.txt + base_urls.txt
"""
def scan_api_url(baseurl):
    with open("./config/api.txt", "r", encoding="utf-8") as f:
        api_paths = f.readlines()
    
    with open("./config/base_urls.txt", "r", encoding="utf-8") as f:
        base_paths = f.readlines()

    url_paths = []
 
    for api_path in api_paths:
        for base_path in base_paths:
            api_path = api_path.strip()
            base_path = base_path.strip()
            url_paths.append(baseurl + api_path + base_path)

    # 分成10个线程
    threads = []
    path_thread = len(url_paths) // 10
    for i in range(10):
        start_index = i * path_thread
        end_index = (i + 1) * path_thread if i != 9 else len(url_paths)
        thread_lines = url_paths[start_index:end_index]

        thread = threading.Thread(target=scan, args=(thread_lines,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


# 下载heapdump
"""
访问heapdump路径
下载文件至本地
"""
def download_heapdump(url):
    try:
        with requests.get(url, stream=True) as r:
            total_size = int(r.headers.get('content-length', 0))
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="下载：heapdump") as bar:
                with open(("./result/heapdump" + str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)
                        bar.update(len(chunk))
        print(Fore.GREEN + "完美下载，请前往result路径查看~~~" + Fore.RESET)
    except:
        print(Fore.RED + "下载失败，请手动尝试下载~~~" + Fore.RESET)
        

"""
程序初始化操作
"""
def init_scan():
    try:
        with open("urls.txt", "r", encoding="utf-8") as f:
            urls = f.readlines()
            return urls
    except Exception as e:
        print(Fore.RED + "初始化运行失败~~~" + Fore.RESET)
        print(Fore.RED + "urls.txt扫描Url不存在，请退出程序，添加需要扫描的Url目标~~~" + Fore.RESET)
        with open("urls.txt", "a+", encoding="utf-8") as f:
            f.close()
        exit()