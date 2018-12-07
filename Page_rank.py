from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import operator

relation_matrix = np.loadtxt("result_matrix.txt")

page_num = 500  #处理的页面数
default_a = 0.85 #默认阻尼系数 0.85


def show_picture():
    '''
    展示页面链接稀疏图
    :return:
    '''
    print('[+] NOW CREATING PICTURE.')
    x=[]
    y=[]
    for i in range(0,page_num):
        for j in range(0,page_num):
            if relation_matrix[i][j] == 1:
                x.append(i)
                y.append(j)
    plt.scatter(x,y,s=1)
    plt.savefig("result.png") #要先保存再show，不然会保存到空白图片
    # plt.show()
    print('[+] PICTURE CRWATED FINISHED.')


def deal_with_origin_matrix():
    print('[+] Now dealing the origin matrix')
    for i in range(0,page_num):
        flag = False
        for j in range(0,page_num):  #判断矩阵某一列是否全为0
            if relation_matrix[j][i] == 1:
                flag = True
        if flag == False:  #若某一列全为0，赋给这一列一个相同的值，加起来为1
            new_val = 1/page_num
            for j in range(0,page_num):
                relation_matrix[j][i] = new_val
        else: #对不全为0的列归一化，使其加起来全为0
            tmp_sum = 0
            for j in range(0,page_num):
                tmp_sum = tmp_sum + relation_matrix[j][i]
            for j in range(0,page_num):
                if relation_matrix[j][i] != 0:
                    relation_matrix[j][i] = relation_matrix[j][i]/tmp_sum
        for j in range(0,page_num): #G = αB + (1/n)*(1 − α)*ee'   G is positive and column stochastic
            relation_matrix[j][i] = relation_matrix[j][i]*default_a + (1-default_a)/page_num
        np.savetxt('tmp_result.txt',relation_matrix)
    print('[+] The Origin Matrix Has Been Dealed')

def Cal_The_Score():
    '''
    用Power Method计算链接分数
    :return: 链接分数的向量
    '''
    print('[+] Now calculating the score of each url link.')
    x0 = np.zeros(page_num)
    x0[0] = 1
    x0 = x0.reshape(-1, 1)
    deal_with_origin_matrix()
    for i in range(5):
        x0 = np.dot(relation_matrix, x0)
    print('[+] The score of each url link has been calculated.')
    return x0


def Sort_And_Save():
    '''
    根据页面链接的分数对链接进行排序，输出前二十个分数最高的链接，并将爬取到的链接按降序保存
    '''
    print('[+] Now saving the final result.')
    urls = []
    with open("spider_result.txt","r") as fp: #获得爬取到的全部链接
        url = fp.readline().rstrip("\n")
        while url:
            urls.append(url)
            url = fp.readline().rstrip("\n")

    result = Cal_The_Score() #计算分数
    sorted_data = {}
    for i in range(0,page_num):
        sorted_data[urls[i]] = result[i] #构造字典用于之后排序
    sorted_result = sorted(sorted_data.items(),key=operator.itemgetter(1),reverse=True) #按第二列的值进行降序排列
    for i in range(0,20): #输出前二十个分数最高的链接
        print('NO{} : {}'.format(i+1,sorted_result[i][0]))
    with open("url_rank_sorted.txt","w") as fp:  #保存全部的链接，按分数进行排列
        for i in range(0,page_num):
            fp.write(sorted_result[i][0])
    print('[+] ALL FINFIAHED.')

def main():
    show_picture()
    Sort_And_Save()


if __name__ == '__main__':
    main()
