import _thread
import requests
from termcolor import cprint
import urllib3
import os


"""
返回信息: 
status:[200] , url: https://www.baidu.com , 网页长度: 2021 , 网页标题: xxxx
status:[]


"""
cprint("hello word","green")
# todo 导出文件函数

def output_file_init():

    f1 = open("output.txt","wb+")
    f1.close()

    f2 = open("error.txt",'wb+')
    f2.close()

    if not os.path.exists(".data"):
        os.mkdir(".data")
    
    report = open(".data/report.json",'wb+')
    report.close()

def check_proxy(proxy):
    cprint("检测代理是否可用")

    porxies = {
        "http":f"http://{proxy}",
        "https":f"https://{proxy}"

    }

    cprint("测试地址为 www.baidu.com",'green')
    testurl = "https://www.baidu.com"


def main():
    # 输出logo
    banner = r"""
  _____            _____                 
 / ____|          / ____|                
| (___  _   _ _ _| (___   ___ __ _ _ __  
 \___ \| | | | '__\___ \ / __/ _` | '_ \ 
 ____) | |_| | |  ____) | (_| (_| | | | |
|_____/ \__,_|_| |_____/ \___\__,_|_| |_|
                                                                                 
""" 
    cprint(banner,"red")
    # 创建导出文件
    output_file_init()

    # todo 获取相关信息
    """
    扫描的url文件名称 txt_name
    文件所在路径 dir_name
    代理和端口 proxy
    """

    txt_name = str(input("输入扫描的文件名称:\n FileName >>> "))
    dir_name = str(input("输入扫描文件的路径:\n DirName >>>"))
    proxy = str(input("输入使用的代理地址:\n Proxy >>>"))

    if proxy :
        check_proxy(proxy=proxy)



if __name__ == "__main__":
    main()
