# -*- coding: utf-8 -*-
# python 3.5.2
# 测试系统，Win10
# Author:Van
# 实现自动下载高清最新pdf的实现
# V1.0 当前只针对效果还可以的国外zippyshare网盘
# 其他的网盘还没添加进判断语句，先共享如何迅雷下载等
# 如果您有经验优化，改进此脚本，请不吝指教
# QQ群： 206241755
# 简介：因下载最新高清pdf，正好发现www.foxebook.net提供
# 但是很多的广告，特烦人，所以尝试脚本，最后因下载需求，
# 加载了迅雷，这功能的实现小牛，不过也是网络别人共享的。

from selenium import webdriver
import requests
from lxml import etree
import re
import os
from win32com.client import Dispatch

# def down_book(i):
#     href = selector.xpath('/html/body/div/div/main/div[i+1]/div[2]/h3/a/@href')
#     print(href)

#test name of book : SciPy and NumPy
# book_name = input('Please input the book name in English:\n')
book_name = 'Introduction to Machine Learning with Python'
print ('begin to search book(s)...')
print ('---------------------------------')
# search link is :http://www.foxebook.nethttp://www.foxebook.net/search/SciPy%20and%20NumPySciPy%20and%20NumPy
PostUrl = "http://www.foxebook.net/search/" + book_name
# print(PostUrl)
# get the content of html
html = requests.get(PostUrl).content

# use etree selector
selector = etree.HTML(html)

# /html/body/div/div/main/div[2]/div[2]/h3/a
# /html/body/div/div/main/div[3]/div[2]/h3/a
# above is two books' xpath, so the right xpath for all book is :
# /html/body/div/div/main//div[2]/h3/a
# it can be confirmed by 'xpath checker'
total_books = selector.xpath("/html/body/div/div/main//div[2]/h3/a/text()")
# print('total books from searching are:', total_books)

num1 = 0
link_address = []
real_address = []
def find_link():
    global num1
    # find the right book, put all links in a list of : link_address

    for i in total_books:
        num1 += 1
        if re.search(book_name,i):

            print('Congrdulations, we find the book(s):\n')
            print ('**********************************')
            print(i)
            print ('**********************************\n')
            href = 'http://www.foxebook.net' + selector.xpath('//*[@id="content"]/div/main/div[%d]/div[2]/h3/a/@href'%num1)[0]
            # print('the book link is :', href)
            # print('will downloading...')
            html_new = requests.get(href).content
            selector_new = etree.HTML(html_new)
            link_new = selector_new.xpath('//*[@id="download"]/div[2]/table/tbody/tr[1]/td[2]/a/@href')[0]
            # split the next link
            link_new = 'http:'+link_new.split(':')[-1]
            link_address.append(link_new)
    print('download link is :', link_address)
    print('\n\n')

def real_book_link():
    # print('link_address is :', link_address)
    # dynamic on zippyshare
    for j in link_address:
        # 用浏览器实现访问

        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(j)


        try:

            # find the download button
            title_list = driver.find_element_by_xpath('//*[@id="dlbutton"]')
            film_link = title_list.get_attribute('href')
            real_address.append(film_link)

        except:
            print('can not download the book')

    print('real_book_link:', real_address)
    return real_address

def addTasktoXunlei(down_url,course_infos):
    flag = False
    o = Dispatch("ThunderAgent.Agent.1")
    if down_url:
        course_path = os.getcwd()
        try:
            #AddTask("下载地址", "另存文件名", "保存目录","任务注释","引用地址","开始模式", "只从原始地址下载","从原始地址下载线程数")
            o.AddTask(down_url, '', course_path, "", "", -1, 0, 5)
            o.CommitTasks()
            flag = True
        except Exception:

            print(Exception.message)
            print(" AddTask is fail!")
    return flag

if __name__ == '__main__':
    find_link()
    real_link = real_book_link()
    for i in real_link:
        addTasktoXunlei(i, course_infos=None)

