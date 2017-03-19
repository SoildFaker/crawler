# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from time import ctime, sleep
import sys
import re
import urllib.request as urlreq
import threading

keys = []
tasks = []
threads = []
historys = {}

userMainUrl = 'http://tieba.baidu.com/'
exp5key = r'(?<!-)[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}(?!\-)'
exp3key = r'(?<!-)[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}(?!\-)'
expReply = r'(\d+)</span>回复贴'
expPID = r'<a href="/p/\d+'

class tieba:

    name = ''
    respHtml = ''

    def __init__(self, n):
        self.name = n
        for j in range(5):
            threads.append("td"+str(j))
            threads[j] = threading.Thread(target=td_match, args=())
            #threads[j].setDaemon()
            threads[j].start()

    def crawlPage(self, p):
        if len(tasks) < 1:
            req = urlreq.Request(userMainUrl + 'f?kw=' + self.name + '&&pn=' + str(50 * p))
            resp = urlreq.urlopen(req)
            respHtml = resp.read().decode('utf-8')
            match = re.findall(expPID, respHtml)
            for m in match:
                pid = m[10:]
                if not pid in historys:
                    tasks.append(pid)
            return 0
        return 1


def td_match():
    while 1:
        while len(tasks) == 0:
            pass
        try:
            pid = tasks[0]
            tasks.remove(pid)
        except ValueError:
            print("pid:%r remove from tasks list fail."%(pid))
        else:
            if len(pid) > 0:
                req = urlreq.Request(userMainUrl + pid)
                resp = urlreq.urlopen(req)
                respHtml = resp.read().decode('utf-8')
                matchKeys(respHtml, pid)

def matchKeys(respHtml,pid):
    replyMatch = re.search(expReply,respHtml)
    if replyMatch != None:
        replyNum = int(replyMatch.group(1))
        if pid not in historys or replyNum > historys[pid]:
            historys[pid]=replyNum
            key5Match = re.findall(exp5key, respHtml)
            key3Match = re.findall(exp3key, respHtml)
            keyMatch = key5Match + key3Match
            for km in keyMatch:
                if not km in keys:
                    keys.append(km)
                    author_left = respHtml.find('username="', respHtml.find(km, 0))
                    giver = respHtml[author_left+10:respHtml.find('"', author_left+10)]
                    hosted_left = respHtml.find('id="post_content_', respHtml.find(km, 0))
                    hosted = respHtml[hosted_left+17:respHtml.find('"', hosted_left+18)]
                    print("%s\r\n"%(ctime()))
                    print("Get:%s \r\nFrom:%s At:%s"%(km, giver, userMainUrl+pid+"?pid="+hosted+"#"+hosted))
    return

def main():
    getKey = tieba('steam')
    n = 1
    while 1:
        while getKey.crawlPage(0):
            pass
        print("time:%d\t\tKeys:%r"%(n, keys), end="\r")
        n = n+1
        sys.stdout.flush()
    return
if __name__=="__main__":
    main()
