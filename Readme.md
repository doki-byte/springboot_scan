## SpringBoot 漏洞扫描利用工具
![alt text](img/image.png)

### 使用教程：
    默认优先使用收集路径进行扫描（springboot_urls.txt）
    当扫描不存在接口时，使用api前缀拼接扫描，可以自行添加
    
### 扫描URL：
    本工具不想使用参数方式（记性不好，时不时就忘了参数是啥~~~）
    需要扫描的url直接放在urls.txt里面即可
    
### 结果保存：
    扫描结果以及下载的heapdump文件最终保存在result路径

### 命令：
    python3 main.py

### 更新记录
#### 2024.09.26 
    + 修复heapdump下载失败情况
    + 修复扫描结束即使存在heapdump也报不存在的情况
    + 增加扫描进度条，便于观察扫描情况
    + 美化输出结果
    + 修改扫描逻辑，加快扫描速率
    + 程序默认设定为10线程，需要修改请查看代码main.py，第5行：# 需要开启的线程数量 thread_number = 10

## 运行结果
![alt text](img/image1.png)

![alt text](img/image2.png)

![alt text](img/image3.png)
