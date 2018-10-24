# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import datetime
 
def selectComments(commentTitle, keywords):
    for item in keywords:
        if item in commentTitle: 
            flag = True
            break
        else:
            flag = False
    return flag

def getComments(pageNum):
    pageStart = 410
    comCount = 0
    while pageStart <= pageNum:
        target = 'http://guba.eastmoney.com/list,waihui,f_'+ str(pageStart) +'.html'
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
                skipFlag = selectComments(commentTitle,delKeyWords)
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
                
                try:
                    commentTimeTag = bf.find("div", class_="zwfbtime")
                    commentTime = commentTimeTag.get_text().split(" ")[1].split("-")
                    #除去帖子中间夹杂了2011年份的帖子
                    if int(commentTime[0]) == 2011:
                        continue
                    commentTime = datetime.datetime(int(commentTime[0]), int(commentTime[1]), int(commentTime[2]))
                except Exception:
                    print("发表时间未知")
                if ((commentTime - startTime).days >= 0 and (commentTime - endTime).days <= 0):
                    print(commentTime)
                    contents = bf.find("div", class_="stockcodec")
                    comCount = comCount + 1
                    #print(contents.get_text())
                    #当时间小于开始时间时, 后面的帖子不获取
                elif((commentTime - startTime).days < 0):
                    print("获取帖子总数为 = " + str(comCount))
                    return               
        pageStart = pageStart + 1
                      


if __name__ == '__main__':

    #评论的起止时间段
    startTime = datetime.datetime(2015, 10, 1)
    endTime = datetime.datetime(2018, 9, 30)

   

    getComments(2307)

    
    
            

            