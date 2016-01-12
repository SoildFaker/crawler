#coding:utf-8
from __future__ import print_function
from time import ctime,sleep
import sys
import re
import urllib2
import threading

keys=[]
IDs=[]
runing = []
userMainUrl = 'http://tieba.baidu.com/'
threads = []

class gKey:

    name = ''
    respHtml = ''


    i=1
    def __init__(self,n):
        self.name=n
        for j in range(10):
            threads.append("td"+str(j))
            threads[j] = threading.Thread(target=td_getKey,args=())
            #threads[j].setDaemon()
            threads[j].start()

    def searchInPage(self,p):
        req = urllib2.Request(userMainUrl + 'f?kw=' + self.name + '&&pn=' + str(50 * p))
        resp = urllib2.urlopen(req)
        respHtml = resp.read()
        match = re.findall(r'<a href="/p/\d+',respHtml)
        for m in match:
            if not m in IDs:
                runing.append(m[10:])


def td_getKey():
    while(1):
        if(len(runing)>0):
            pid=runing[0]
            runing.remove(runing[0])
            if(len(pid)>0):
                req = urllib2.Request(userMainUrl +pid)
                resp = urllib2.urlopen(req)
                respHtml = resp.read()
                inPage = re.search(r'class="red">\d+',respHtml)
                if(inPage!=None):
                    pageNum = int(inPage.group()[12:])
                    if(pageNum>1):
                        IDs.append(pid)
                    keyMatch = re.findall(r'(?<!-)[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}(?!\-)',respHtml)
                    keyMatch2 = re.findall(r'(?<!-)[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}(?!\-)',respHtml)
                    keyMatch.extend(keyMatch2)
                    for km in keyMatch:
                        if not km in keys:
                            keys.append(km)
                            author_left=respHtml.find('username="',respHtml.find(km,0))
                            giver = respHtml[author_left+10:respHtml.find('"',author_left+10)]
                            hosted_left=respHtml.find('id="post_content_',respHtml.find(km,0))
                            hosted = respHtml[hosted_left+17:respHtml.find('"',hosted_left+18)]
                            print("%s\r\n"%(ctime()))
                            print ("Get:%s \r\nFrom:%s At:%s"%(km,giver,userMainUrl+pid+"?pid="+hosted+"#"+hosted))

getKey=gKey('steam')
n=1
while(1):
    print ("Number %d Searching..."%n,end="\r")
    sys.stdout.flush()
    n=n+1
    getKey.searchInPage(0)
