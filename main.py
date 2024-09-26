from utils.tools import *
from utils.logo import logo

if __name__ == "__main__":
    logo()

    print(Fore.GREEN + "扫描程序正在初始化~~~" + Fore.RESET)
    urls = init_scan()
    print(Fore.GREEN + "初始化运行完毕，即将开始扫描~~~" + Fore.RESET)
    print()

    print(Fore.GREEN + "即将开始基础扫描模式~~~" + Fore.RESET)
    for url in urls:
        url = url.strip()
        if url.endswith("/"):
            url = url[:-1]
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
    
        scan_base(url)
    print(Fore.GREEN + "基础扫描模式运行结束，正在处理结果~~~" + Fore.RESET)
    print()

    with open("./result/success.txt", "a+", encoding="utf-8") as f:
        success_urls = f.readlines()
    if success_urls == []:
        print(Fore.GREEN + "即将开始前缀API扫描模式~~~" + Fore.RESET)
        for url in urls:
            if url.endswith("/"):
                url = url[:-1]
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
        
            scan_api_url(url)
        print(Fore.GREEN + "前缀API扫描模式运行结束，正在处理结果~~~" + Fore.RESET)
        print()
        
        with open("./result/success.txt", "r", encoding="utf-8") as f:
            success_urls = f.readlines()
        if success_urls == []:
            print(Fore.GREEN + "扫描结束，未找到接口泄露~~~" + Fore.RESET)
        else:
            for success_url in success_urls:
                success_url = success_url.strip()
                if success_url.endswith("heapdump"):
                    print(Fore.GREEN + "扫描到存在heapdump文件，即将进行下载~~~" + Fore.RESET)
                    download_heapdump(success_url)
                else:
                    print(Fore.GREEN + "扫描结束，请前往result路径查看~~~" + Fore.RESET)
    else:
        for success_url in success_urls:
            success_url = success_url.strip()
            if success_url.endswith("heapdump"):
                print(Fore.GREEN + "扫描到存在heapdump文件，即将进行下载~~~" + Fore.RESET)
                download_heapdump(success_url)
            else:
                print(Fore.GREEN + "扫描结束，请前往result路径查看~~~" + Fore.RESET)

