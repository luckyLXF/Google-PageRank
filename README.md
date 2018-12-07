# Google-PageRank


Implement Google PageRank algorithm  with Python

使用的Python版本：Python3


所用到的库：
queue
numpy
re
requests
threading
matplotlib
operator
__future__

一共有四个主要的代码文件：

SchoolPageSpider.py 用于从一个入口开始爬取所需要数量的网页链接，采用多线程的方式进行爬取，每次从队列中取出一个进行爬取，并将爬取到的新链接放入队列。将爬取到的链接存储在spider_result.txt中。

create_matric.py 用于根据爬取到的链接生成Google matric
采用多线程运行时会报错，因此采用单线程的方式生成矩阵。生成的矩阵放在result_matrix.txt中

Page_rank.py 用于根据生成的Google matric生成网页链接的稀疏图，保存为result.png；并且根据Power Method计算出主特征向量，主特征向量的值就是网页的分数，最后根据分数对网页链接进行排序，将前二十个分数最高的网站链接保存在Top_URL.txt中，并且将所有爬取到的网页链接按分数的降序排列，保存在url_rank_sorted.txt中。

main.py 用于将上述三个代码文件整合起来，在main.py中修改crawl_num即可修改要爬取的页面链接数量。

使用方法：运行main.py
