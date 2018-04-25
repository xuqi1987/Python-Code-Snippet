#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from urllib2 import *
import random

class ProxyPool():

    def __init__(self):
        self.valid_proxyes = []
        self.proxyes = []
        pass

    def get_html(self,url):
        request = Request(url)
        request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36")
        html = urlopen(request)
        return html.read()

    def get_soup(self,url):
        data = self.get_html(url)
        soup = BeautifulSoup(data, "lxml")
        return soup

    def fetch_xici(self,https):
        """
        http://www.xicidaili.com/nn/
        """
        proxyes = []
        try:
            url = "http://www.xicidaili.com/nn/"
            soup = self.get_soup(url)
            table = soup.find("table", attrs={"id": "ip_list"})
            trs = table.find_all("tr")
            for i in range(1, len(trs)):
                tr = trs[i]
                tds = tr.find_all("td")
                ip = tds[1].text
                port = tds[2].text
                if https and tds[5].text.strip()!="HTTPS":
                    continue
                speed = tds[6].div["title"][:-1]
                latency = tds[7].div["title"][:-1]
                if float(speed) < 3 and float(latency) < 1:
                    if https:
                        proxyes.append("https://%s:%s" % (ip, port))
                    else:
                        proxyes.append("http://%s:%s" % (ip, port))
        except:
            print "fail to fetch from xici"
        return proxyes

    def fetch_66ip(self,https):
        """
        http://www.66ip.cn/
        每次打开此链接都能得到一批代理, 速度不保证
        """
        proxyes = []
        try:
            # 修改getnum大小可以一次获取不同数量的代理
            if https:
                url = "http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=1&api=66ip"
            else:
                url = "http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip"
            content = self.get_html(url)
            content = str(content)
            urls = content.split("</script>")[1].split("</div>")[0].split("<br />")
            for u in urls:
                u = u.split("\\t")[-1]
                if u.strip():
                    if https:
                        proxyes.append("https://" + u.strip())
                    else:
                        proxyes.append("http://" + u.strip())

        except Exception as e:
            print "fail to fetch from 66ip: %s" % e
        return proxyes

    def check(self,proxy):
        if proxy.startswith("https"):
            url = "https://www.baidu.com/js/bdsug.js?v=1.0.3.0"
            proxy_handler = ProxyHandler({'https': proxy})
        else:
            url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
            proxy_handler = ProxyHandler({'http': proxy})
        opener = build_opener(proxy_handler,HTTPHandler)
        try:
            response = opener.open(url, timeout=3)
            return response.code == 200 and response.url == url
        except Exception:
            return False

    def fetch_all(self,endpage=2, https=False):
        self.proxyes = []
        self.valid_proxyes = []

        print "fetch proxyes"
        self.proxyes += self.fetch_xici(https)
        self.proxyes += self.fetch_66ip(https)

        print "checking proxyes validation"
        for p in self.proxyes:
            if self.check(p):
                self.valid_proxyes.append(p)
        return self.valid_proxyes

    def get_random_proxy(self):
        if len(self.valid_proxyes) == 0:
            self.fetch_all()
        while len(self.valid_proxyes) > 0:
            proxy = random.choice(self.valid_proxyes)
            if self.check(proxy):
                return proxy
            else:
                self.valid_proxyes.remove(proxy)

                if len(self.valid_proxyes) == 0:
                    self.fetch_all()

proxy = ProxyPool()
print proxy.get_random_proxy()