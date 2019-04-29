'''
author:Kilter.wang
time:2019/4/29
function:爬取笔趣阁的部分小说
'''
import requests
from lxml import etree

class Novel_Spider(object):
    def __init__(self,novel_name):
        self.__url="http://www.xbiquge.la"
        self.__novel_name=novel_name

    #获取小说的链接
    def get_request(self):
        #请求网站获取到HTML源码
        response=requests.get(self.__url)
        xml=etree.HTML(response.text)
        #使用xpath进行特定部分的提取
        result_name_1=xml.xpath('//div[@class="item"]//dt/a/text()')
        result_url_1=xml.xpath('//div[@class="item"]//dt/a/@href')
        result_name_2=xml.xpath('//div[@class="novelslist"]//ul/li/a/text()')
        result_url_2=xml.xpath('//div[@class="novelslist"]//ul/li/a/@href')
        result_name=result_name_1+result_name_2
        result_url=result_url_1+result_url_2
        #将小说名和小说链接组合成字典，形成1v1的关系
        ndict=dict(zip(result_name,result_url))
        #判断小说是否在可爬取的范围内
        if not self.__novel_name in result_name:
            print("该小说不在范围内，请重新输入。。。")
            print("可爬取的小说有：",)
            for n in result_name:
                #end="" 可使输出不换行
                print(n+"  ",end="")
        else:
            self.get_chapter(ndict.get(self.__novel_name))

    #获取每一章节的链接，并调用获取章节内容的方法，将文本写入文件
    def get_chapter(self,str_url):
        response=requests.get(str_url)
        #response为返回的html源代码，可能存在中文乱码的情况。 采用下行代码，获取源码中的编码规则，可解决乱码问题
        response.encoding=response.apparent_encoding
        xml=etree.HTML(response.text)
        chapter_name=xml.xpath('//div[@class="box_con"]//dd/a/text()')
        chapter_url=xml.xpath('//div[@class="box_con"]//dd/a/@href')
        i=0
        while i<len(chapter_url):
           chapter_url[i]=self.__url+chapter_url[i]
           i+=1
        f = open(self.__novel_name+".txt", "w", encoding="utf-8")
        generator=(self.download_file(n,u) for n,u in zip(chapter_name,chapter_url))
        print("下载中。。。。请稍后")
        rate=0
        for gi in generator:
            #用于记载爬取进度
            rate+=1
            print("进度：",round((rate/len(chapter_name)*100),2),"%")
            for xi in gi:
                f.write(xi)
        f.close()

    #获取章节内容
    def download_file(self,str_name,str_url):
        response=requests.get(str_url)
        response.encoding=response.apparent_encoding
        xml=etree.HTML(response.text)
        txt=xml.xpath('//div[@class="box_con"]/div[@id="content"]/text()')
        #插入章节标题到每一章节的开头，并修改输出格式，以符合原文章格式
        txt.insert(0,"    "+str_name+"\n\n")
        txt.append("\n\n")
        return txt



if __name__=="__main__":
    #简单交互
    print("----小说爬取----")
    print("---------------")
    a=input("请输入小说名：")
    novel_spider=Novel_Spider(a)
    novel_spider.get_request()
    input()
