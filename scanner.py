import _thread
import argparse
import time
from typing import Optional, Tuple
import requests
from termcolor import cprint
import urllib3
import os
import random
import json
import sys
import threading
import ssl

from bs4 import BeautifulSoup
from enum import Enum


class Survive_Scanner:
    __ua = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]

    class EServival(Enum):
        REJECT = -1
        SURVIVE = 1
        DIED = 0

    __thread_limit = 1000
    __delay = 10
    __url = []
    __scanned_url = []
    __filepath = ""
    __proxy_pool = []
    __proxy = ""
    __test_url = "https://www.baidu.com"

    __out_path = "output.txt"
    __err_path = "outerr.txt"

    def __init__(self):
        self.__scanned_url = []
        self.__out_path = "output.txt"
        self.__err_path = "outerr.txt"

    def set_thread_limit(self, thread_num):

        thread_num = int(thread_num)

        if thread_num < 0 or thread_num > 50000:
            cprint(f" invalid thread number limit", "red")
            cprint("use the default thread num", "red")

            return
        self.__thread_limit = thread_num

    def show_thread_limit(self):
        cprint(f"the thread limit is {self.__thread_limit}", "cyan")

    def set_delay(self, delay):

        delay = int(delay)

        if delay < 0 or delay > 100:
            cprint(f" invalid delay", "red")
            cprint("use the default delay", "red")

            return

        self.__delay = delay

    def show_delay(self):
        cprint(f"the delay {self.__delay}", "cyan")

    def set_filepath(self, filepath: str):
        self.__filepath = str(filepath)

    def show_filepath(self):
        cprint(f"当前的文件路径为 {self.__filepath}", 'cyan')

    def read_urls(self, filename: str):
        try:
            with open(file=filename, mode='r') as file:
                for line in file:
                    self.__url.append(line.strip())

            cprint(f"读取url文件成功，读取的数量为{len(self.__url)}", "cyan")

        except FileNotFoundError as e:
            cprint(e.strerror, "red")

    def show_url(self):
        for url in self.__url:
            print(f"{url}")

    # todo 创建输出文件 output.txt 和  outerr.txt , 此处，逻辑有问题， 输入yes应该覆盖文件，无论如何都要创建文件

    def file_init(self, out_fname="output.txt", err_fname="outerr.txt"):

        if os.path.exists(out_fname):
            cprint(f"当前文件{out_fname}已存在，输入yes覆盖文件", "green")

            if input(">>> ") == "yes":
                f1 = open(file=out_fname, mode='wb+')
                f1.close()

        if os.path.exists(err_fname):
            cprint(f"当前文件{err_fname}已存在，输入yes覆盖文件", "green")

            if input(">>> ") == "yes":
                f2 = open(file=err_fname, mode='wb+')
                f2.close()

    # todo 添加代理池功能

    def set_proxy(self, proxy):
        self.__proxy = proxy
        # todo 验证代理池地址格式

    def set_proxy_pool(self, proxy_path: str):
        try:
            with open(file=proxy_path, mode='r') as f:
                for line in f:
                    self.__proxy_pool.append(line)
        except FileNotFoundError as e:
            cprint(e.strerror, 'red')

    def show_proxy_pool(self):

        if self.__proxy_pool:
            for proxy in self.__proxy_pool:
                cprint(f"{proxy}", 'cyan')

        cprint("当前代理池为空", 'cyan')

    def is_proxy_pool(self):
        if self.__proxy_pool:
            return True

        return False

    def test_proxy_pool(self):

        for proxy in self.__proxy_pool:
            r = requests.get(url=self.__test_url, proxies=proxy, timeout=self.__delay)

            if r.status_code == 200:
                continue
            else:
                cprint(f"代理地址: {proxy} 不可用", "red")
                return False

        return True

    def test_proxy(self):

        r = requests.get(url=self.__test_url, proxies=self.__proxy, timeout=self.__delay)

        if r.status_code == 200:
            return True

        return False

    def is_proxypool(self):

        if self.__proxy_pool:
            return self.test_proxy_pool()

        return False

    def is_proxy(self):

        if self.__proxy:
            return self.test_proxy()

        return False

    # todo !!!!!!!这里https访问有问题
    def survive(self, url):
        # if self.__url == "":
        #     cprint("当前urls为空，请检查是否成功读取文件","red")
        #     sys.exit()

        if url in self.__scanned_url:
            return

        header = {"User-Agent": random.choice(self.__ua)}
        urllib3.disable_warnings()

        try:
            if self.is_proxy():
                r = requests.get(url=url, headers=header, timeout=self.__delay, verify=False, proxies=self.__proxy, )
                soup = BeautifulSoup(r.content, 'html.parser')
                title = str(soup.title.string)

            elif self.is_proxypool():
                r = requests.get(url=url, headers=header, timeout=self.__delay, verify=False,
                                 proxies=random.choice(self.__proxy_pool))
                soup = BeautifulSoup(r.content, 'html.parser')
                title = str(soup.title.string)

            else:
                r = requests.get(url=url, headers=header, timeout=self.__delay, verify=False)

                soup = BeautifulSoup(r.content, 'html.parser')
                title = str(soup.title.string)

        except Exception:
            r = None
            title = str("error")
            # cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过", "magenta")
            self.report((self.EServival.REJECT, 0, url, 0, title))
            # return self.EServival.REJECT, 0, url, 0, title

        if r is not None:

            if r.status_code == 200 or r.status_code == 403:
                self.report((self.EServival.SURVIVE, r.status_code, url, len(r.content), title))
                # return self.EServival.SURVIVE, r.status_code, url, len(r.content), title
            else:
                title = str("error")
                self.report((self.EServival.DIED, r.status_code, url, 0, title))
                # return self.EServival.DIED, r.status_code, url, 0, title
        # * 下面的语句会导致重复的错误信息输出， 判断逻辑和前面except中添加的 r = None重复了
        # else:
        #     self.report((self.EServival.REJECT, 0, url, 0, title))

        self.__scanned_url.append(url)

    def report(self, result: Tuple[EServival, Optional[int], str, int, str]):

        (status, code, url, length, title) = result

        if status == self.EServival.SURVIVE:
            cprint(f"[+] 状态码为: {code} 存活URL为: {url} 页面长度为: {length} 网页标题为: {title}", "red")

        if status == self.EServival.DIED:
            cprint(f"[-] 状态码为: {code} 无法访问URL为: {url} ", "yellow")

        if status == self.EServival.REJECT:
            cprint(f"[-] URL为 {url} 的目标积极拒绝请求，予以跳过", "magenta")

        if status == self.EServival.SURVIVE:
            fileName = "output.txt"
        elif status == self.EServival.DIED:
            fileName = "outerr.txt"

        if status == self.EServival.SURVIVE or status == self.EServival.DIED:
            with open(file=fileName, mode='w+') as file:
                file.write(f"[{code}]  {url}\n")

            file.close()

    def scan(self):

        index = 0
        length = len(self.__url)
        threads = []

        while index < length:

            while threading.active_count() < self.__thread_limit and index < length:
                thread = threading.Thread(target=self.survive, args=(self.__url[index],))
                thread.start()
                time.sleep(0.5)
                threads.append(thread)
                index += 1

            for thread in threads:
                thread.join()


if __name__ == "__main__":

    banner = r"""
      _____            _____                 
     / ____|          / ____|                
    | (___  _   _ _ _| (___   ___ __ _ _ __  
     \___ \| | | | '__\___ \ / __/ _` | '_ \ 
     ____) | |_| | |  ____) | (_| (_| | | | |
    |_____/ \__,_|_| |_____/ \___\__,_|_| |_|

    """
    cprint(banner, "red")
    # 必选参数

    # file_path = input(">>> 输入文件名 :  ")
    # # 可选参数
    # thread_limit = 500
    # delay = 10

    parser = argparse.ArgumentParser(description="A Web Url Survival Scanner")

    parser.add_argument("-f", "--file-path", dest="file_path", help="输入url文件路径", required=True)
    parser.add_argument("-d", "--delay", dest="delay", help="输入判断时延", type=int)
    parser.add_argument("-t", "--thread_limit", dest="thread_limit", help="输入线程数量", type=int)
    parser.add_argument("-p", "--proxy", dest="proxy", help="输入代理", type=str)
    parser.add_argument("-pool", "--proxy_pool", dest="proxy_pool", help="输入代理池文件地址", type=str)

    args = parser.parse_args()
    """
    创建输出文件
    读取url
    
    存活探测
        探测函数
        线程管理
        结果输出
    
    end
    """

    if args.file_path:
        try:
            scanner = Survive_Scanner()
            scanner.file_init()  # 输出文件名和错误输出文件名可选

            if args.delay:
                # 从args中获取 delay, thread_limit
                scanner.set_delay(delay=args.delay)
                scanner.show_delay()
            if args.thread_limit:
                scanner.set_thread_limit(thread_num=args.thread_limit)
                scanner.show_thread_limit()

            # 从args中获取文件路径
            scanner.read_urls(filename=args.file_path)
            # scanner.show_url()

            scanner.show_filepath()

            if args.proxy:
                scanner.set_proxy(proxy=args.proxy)

            if args.proxy_pool:
                scanner.set_proxy_pool(proxy_path=args.proxy_pool)
                cprint("再设置单独代理情况下，代理池不起作用", 'cyan')

            # print(scanner.is_proxy())
            # print(scanner.is_proxypool())
            scanner.scan()

        except KeyboardInterrupt:
            cprint("^c interrupt", 'red')

    # end

    print("探测结束，结果已保存到output.txt和outerr.txt")
