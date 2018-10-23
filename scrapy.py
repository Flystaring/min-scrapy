# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import datetime
 
def selectComments(commentTitle, keywords, delFlag=True):
    for item in keywords:
        if item in commentTitle:
            if delFlag: 
                flag = True
            else:
                flag = False
            break
        else:
            if delFlag: 
                flag = False
            else:
                flag = True
    return flag


if __name__ == '__main__':

    #评论的起止时间段
    startTime = datetime.datetime(2015, 10, 1)
    endTime = datetime.datetime(2018, 9, 30)

    pageNum = 1
    target = 'http://guba.eastmoney.com/list,waihui,f_'+ pageNum +'.html'
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
            aTag = spanTitle.find("a")
            commentTitle = aTag['title'] 

            #当讨论,新闻,悬赏帖子,或者title含有图片时,跳过该帖子
            em = spanTitle.find("em") 
            if em:
                continue
                    
            #剔除标题中含有指定关键字的帖子
            delKeyWords = ['贬基','攻略','维权']         
            skipFlag = selectComments(commentTitle,delKeyWords,True)
            if skipFlag:
                continue
            
            
            #保留带有外汇,欧,美,中国,日,镑,情绪,人民币,汇率的帖子
            cotKeyWords = ['外汇','欧','美','中国','日','镑','情绪','人民币','汇率']
            skipFlag = selectComments(commentTitle,cotKeyWords,False)
            if skipFlag:
                continue
        
            #print(commentTitle)   
            #获取每个帖子的跳转链接
            title = spanTitle.find("a")
            aUrl = 'http://guba.eastmoney.com' + title["href"]
            
            #获取每个帖子的作者
            spanAuthor = spanTitle.next_sibling
            print(spanAuthor)
            try:
                aAuthor = spanAuthor.find("a").string
            except Exception:
                print("作者未知")
            a = {"url":aUrl,"Author":aAuthor}
            #print(a["url"])
            req = requests.get(url=a["url"])
            html = req.text
            #print(html)
            bf = BeautifulSoup(html,"lxml")

            #评论在选择的时间段内, 则获取该帖子内容 
            commentTimeTag = bf.find("div", class_="zwfbtime")
            commentTime = commentTimeTag.get_text().split(" ")[1].split("-")
            commentTime = datetime.datetime(int(commentTime[0]), int(commentTime[1]), int(commentTime[2]))
            if ((commentTime - startTime).days >= 0 and (commentTime - endTime).days <= 0):
                print(commentTime)
                contents = bf.find("div", class_="stockcodec")
                #print(contents.get_text())
            #当时间小于开始时间时, 后面的帖子不获取
            elif((commentTime - startTime).days < 0):
                break
            
            

            