import time
import random
import os
import requests as req
from bs4 import BeautifulSoup as bs

path = os.path.join(os.path.dirname(__file__), 'log', 'doubanj.log')


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open(path, 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)


def get_url_content(url, proxys=None, head={}):
    log('开始抓取url...')
    max_retry = 5
    session = req.Session()
    c = req.cookies.RequestsCookieJar()

    headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
    }
    headers.update(head)

    while max_retry > 0:
        if proxys is not None:
            data = req.get(url, headers=headers, proxies=random.choice(proxys))
        else:
            data = req.get(url, headers=headers)
        # print data.text.
        if len(data.text) > 0:
            break
        max_retry = max_retry - 1
        time.sleep(10)
        log('failed ..... will try another time')

    soup = bs(data.text, 'html5lib')

    return soup


#num获取num页 国内高匿ip的网页中代理数据
def fetch_proxy(num):
    #修改当前工作文件夹
    api = 'http://www.xicidaili.com/nn/{}'
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    fp = open('host.txt', 'a+', encoding=('utf-8'))
    for i in range(num+1):
        api = api.format(1)
        respones = req.get(url=api, headers=header)
        soup = bs(respones.text, 'lxml')
        container = soup.find_all(name='tr',attrs={'class':'odd'})
        for tag in container:
            try:
                con_soup = bs(str(tag),'lxml')
                td_list = con_soup.find_all('td')
                ip = str(td_list[1])[4:-5]
                port = str(td_list[2])[4:-5]
                IPport = ip + '\t' + port + '\n'
                fp.write(IPport)
            except Exception as e:
                print('No IP！')
        time.sleep(1)
    fp.close()

#生成代理池子，num为代理池容量
def proxypool(num):
    n = 1
    path = os.path.join(os.path.dirname(__file__), 'host.txt')
    fp = open(path, 'r')
    proxys = list()
    ips = fp.readlines()
    while n < num:
        for p in ips:
            ip = p.strip('\n').split('\t')
            proxy = 'https:\\' + ip[0] + ':' + ip[1]
            proxies = {'proxy': proxy}
            proxys.append(proxies)
            n+=1
    return proxys


def url_for(url, query):
    return url+'?'+query

if __name__ == '__main__':
    log('hello world')
