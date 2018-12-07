import SchoolPageSpider
import create_matric
import Page_rank

crawl_num = 100 #爬取的网站链接数量
def main():
    SchoolPageSpider.web_page_num=crawl_num
    SchoolPageSpider.main()  #爬取相应数量的网址
    create_matric.url_len=crawl_num
    create_matric.main()  #生成矩阵
    Page_rank.page_num=crawl_num
    Page_rank.main()

if __name__=='__main__':
    main()