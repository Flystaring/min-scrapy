# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
 
if __name__ == '__main__':
    target = 'http://guba.eastmoney.com/list,waihui_1.html'
    req = requests.get(url=target)
    html = req.text
    #print(html)
    bf = BeautifulSoup(html,"lxml")
    #获取页面所有帖子html结构
    titles = bf.find_all("div", class_="articleh")

    #解析每个节点, 切分每个帖子的标题和URL以及作者
    for item in titles:        
        spanTitle = item.find("span", class_="l3")
        if spanTitle:
            #当讨论,新闻,悬赏帖子时,跳过爬取
            em = spanTitle.find("em")
            if em and "settop" in em["class"]:
                continue
            if em and "hinfo" in em["class"]:
                continue

            #获取每个帖子的跳转链接
            title = spanTitle.find("a")
            aUrl = 'http://guba.eastmoney.com' + title["href"]
            
            #获取每个帖子的作者
            spanAuthor = spanTitle.next_sibling
            aAuthor = spanAuthor.find("a").string
            a = {"url":aUrl,"Author":aAuthor}
            #print(a["url"])
            req = requests.get(url=a["url"])
            html = req.text
            #print(html)
            bf = BeautifulSoup(html,"lxml")
            contents = bf.find("div", class_="stockcodec")
           
            print(contents.get_text())

            