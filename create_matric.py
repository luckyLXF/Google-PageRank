import numpy as np
import re
import requests
import threading
from  queue import Queue

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
pattern_url = re.compile(r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')')

# tmp_urls = Queue() #待处理的链接队列
url_len = 500 #生成的矩阵维度
 #当前正在处理第几个链接

def deal_each_website(url,i):
    '''
    处理单个页面，找到其中所有的页面链接，如果在爬取结果中出现，则相应的位置置1
    :param url:网址链接
    :param i:当前网址链接在矩阵的第几行
    '''
    finded = 0
    print("Dealing The "+str(i)+"th URL :"+url)
    try:
        s = requests.session()
        s.keep_alive = False
        response = s.get(url, headers=headers, timeout=5, stream=True)
    except Exception as e:
        print("Wrong url:"+url)
        return
    content = response.text
    result = pattern_url.findall(content)
    for j in range(0,url_len):
        if urls[j] in result:
            finded += 1
            relation_matrix[j][i] = 1
    print("Found {} URL Link".format(finded))

# def begin():
#     global page_num
#     lock.acquire() #获得互斥锁
#     try:
#         url = tmp_urls.get()
#     except:
#         lock.release()
#         return
#     deal_each_website(url,page_num)
#     page_num = page_num + 1 #当前处理页面编号 递增
#     lock.release()

def main():
    print('[+] NOW CREATING THE RELATION_MATRIX.')
    global urls
    urls = []
    global tmp_urls
    tmp_urls = Queue()
    global page_num
    page_num = 0
    with open("spider_result.txt","r") as fp:
        url = fp.readline().rstrip('\n')
        while url:
            # print(url)
            urls.append(url)
            tmp_urls.put(url)
            url = fp.readline().rstrip('\n')

    global relation_matrix
    relation_matrix = np.zeros((url_len, url_len))

    # global lock
    # lock = threading.Lock()
    # threads = []
    # for i in range(1):
    #     t = threading.Thread(target=begin)
    #     threads.append(t)
    #     t.start()
    #     t.join()
    page_num = 0
    while tmp_urls.empty() != True:
        url = tmp_urls.get()
        deal_each_website(url, page_num)
        page_num = page_num + 1 #当前处理页面编号 递增

    np.savetxt('result_matrix.txt',relation_matrix)

    print('[+] FINISHED.')
    print('[+] The result has save to result_matrix.txt')

if __name__=='__main__':
    main()
