# 注意事项
1. 程序默认使用translate.google.cn获取翻译内容 
 
2. 如果.cn域名不可用或者获取超时将自动使用代理，到translate.google.com获取翻译内容 
 
3. 代理使用的是socks5, 监听在本地的1080端口 可通过修改tranen.py里 proxyport=1080 语句重定义 
   

# 功能
* **中英互译(单词、句子)**
* **支持代理**
* **提取图片字符并翻译(英译中)**
* **程序内翻译语言切换**

# 部分运行效果截图 
![image](./imgs/effect.png)
![image](./imgs/effect1.png)

# 安装
## 需要在setup.py目录下进行

      sudo pip3 install -r requirements.txt
      sudo ./setup.py install

# 基本用法
* Ctrl-c退出 <br> 
   
* tranen 调用程序, 自动识别输入，进行翻译

* tranen "string" 进行单次翻译， 译完自动退出




# 截图翻译
1. 先按安装步骤完成程序部署
 
3. 终端键入tranpic直接运行
4. 利用截图软件截图保存到指定位置，默认是~/Pictures/pic，可修改
5. 可以设置截图软件默认保存位置为tranpic检测的文件位置，截图自动保存，并设置快捷键截图，3方式配合食用更佳
6. 后期将增加双击或鼠标提取翻译到可视化窗口

# 安装方式

            pip3 install -r requirements.txt  #前提：安装pip3

            sudo ./setup.py install

