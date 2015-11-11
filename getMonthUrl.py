#!/usr/bin/env python
#coding:utf-8
import urllib2
import re
from HTMLParser import HTMLParser
from itertools import count
from fileinput import filename




#得到每个page页中每篇文档的URL
def getpageurl(url,page_count):   
    p = '(<a href=")((https://gendertrender.wordpress.com/)((\d){4}/(\d){2}/(\d){2}/(.)*/))(" rel="bookmark")'
    pageurl = url+str(page_count)
    response = urllib2.urlopen(pageurl)
    content  = response.read()
    page_list = re.findall(p,content,re.M)
    url_list = []    
        
    for i in page_list:
        url_list.append(i[1])
    return url_list    

def strip_tags(html):  
    """  
    Python中过滤HTML标签的函数  
    >>> str_text=strip_tags("<font color=red>hello</font>")  
    >>> print str_text  
    hello  
    """  
    html = html.strip()  
    html = html.strip("\n")  
    result = []  
    parser = HTMLParser()  
    parser.handle_data = result.append  
    parser.feed(html)  
    parser.close()  
    return ''.join(result)  

#保存到本地，路径为程序的当前文件夹
def savetotext(count,title,text):
    filename = str(count)+'.txt'
    print filename
    f = open(filename,'w')
    f.write(text)
    f.close()
#抓取每篇文章的title、正文、以及评论
def getblogs(url, page_count):
    #正则表达式
    pattern_title = '(<title>)((.)*)(</title>)'
    pattern_time = '(<h3>)((\w)* (\d){1,2}, (\d){1,4})(</h3>)'
    pattern_blog_text = '<p>((.)*)</p>'
    count = 1
    for i in getpageurl(url, page_count):
        response = urllib2.urlopen(i)
        content  = response.read()
        #得到title元素
        page_list = re.findall(pattern_title,content,re.M)
        parser = HTMLParser()
        title =  parser.unescape(page_list[0][1])
        #得到发表时间
        time = re.findall(pattern_time, content,re.M)
        time = time[0][1]
        #得到正文
        m = re.findall(pattern_blog_text, content,re.M)
        blog_text = ''
        for i in m:
            blog_text = blog_text +'\n'+'\n'+ i[0]
        blog_text =  strip_tags(blog_text)
        if isinstance(title, unicode):
            title = title.encode('utf-8')
        if isinstance(time, unicode):
            time = time.encode('utf-8')
        if isinstance(blog_text, unicode):
            blog_text = blog_text.encode('utf-8')       
        text = 'title:'+title+'\n'+'\n'+'created time:'+time+'\n'+'\n'+blog_text
        #文件命名规则为“page页-文档编号”
        filename = str(page_count)+'-'+str(count)
        savetotext(filename,title,text)
        count = count+1



if __name__=='__main__':
    url = 'https://gendertrender.wordpress.com/page/'
    for i in range(1,108):
        getblogs(url, i)
