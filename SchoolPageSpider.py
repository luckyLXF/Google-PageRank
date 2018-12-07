import requests
import re
import threading
from queue import Queue


web_page_num = 500  #爬取的网站链接数量
websites = []   #存放已爬取的链接
tmp_websites = Queue()  #存放待爬取的队列

pattern_url = re.compile(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')')  #提取网址的正则表达式
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

def find_urls_in_content(content):
    '''
    找到该页面内的所有网址链接，加入到待爬取队列中
    '''
    result = pattern_url.findall(content)
    for website in result:
        tmp_websites.put(website)


def find_urls(url):
    '''
    从待爬取队列中取出一个网址用于爬取其中的链接，并跳过已经爬取的链接
    '''
    if url in websites:
        return
    try:
        s = requests.session()
        s.keep_alive = False
        response = s.get(url,headers=headers,timeout=5,stream=True)
        # response = requests.get(url,headers=headers,timeout=5,stream=True)
    except:
        return
    if response.status_code == 200:
        print(url)
        content = response.text
        find_urls_in_content(content)
        websites.append(url)


def start_scaning():
    '''
    判断是否达到爬取最大长度或者待爬取队列为空
    '''
    while len(websites)<=web_page_num-1 and tmp_websites.empty():
        lock.acquire() #获得互斥锁，防止多线程间出错
        current_url = tmp_websites.get()
        lock.release()
        find_urls(current_url)


def main():
    init_url = input('Please input the init WEB_URL(default:https://www.jnu.edu.cn/):')
    if init_url == '':
        init_url = 'https://www.jnu.edu.cn/'

    tmp_websites.put(init_url)
    print('[+] SET INIT URL: ' + init_url)
    print("[+] NOW STARTING SCAN……")

    global lock
    lock = threading.Lock()

    threads = []
    for i in range(5): #多线程爬取
        t = threading.Thread(target=start_scaning)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("[+] Scan finished. ")
    print("[+] Now saving the result.")
    with open("spider_result.txt", "w") as fp: #将爬取结果存储到txt中
        for each_weburl in websites:
            fp.write(each_weburl + "\n")
    print("[+] The Scan result has already save to spider_result.txt.")

if __name__=="__main__":
    main()
