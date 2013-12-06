#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import sys
import time
import urllib2  
import re  
import pymongo
import time
import sched,os,threading
sys.path.append("..")
from Channel import *
from pymongo import MongoClient

apiKey = '4GytEKEx2svP4WnlZG3CjWsd'
secretKey = 'fS3uZqw6f8KDkoGNk4arEGgfClMD71Kr'
user_id = '590753203017939367'
channel_id = '3537340264275310445'

message = ""
message_key = "key1"
tagname = "tangmen"

client = MongoClient('localhost',27017)
db = client.tangmen
url = 'http://tieba.baidu.com/f/good?kw=%BE%F8%CA%C0%CC%C6%C3%C5&cid=0&tp=0&pn=0'

s = sched.scheduler(time.time,time.sleep)

def test_pushMessage_to_tag():
	c = Channel(apiKey, secretKey)
	push_type = 2
	optional = dict()
	optional[Channel.TAG_NAME] = tagname
	optional[Channel.MESSAGE_TYPE] = 1
#	print 'hi:::::', push_type, message, message_key, optional
	ret = c.pushMessage(push_type, message, message_key, optional)
#	print 'Push Message.Detail:'
#	print ret

def perform():
	find_re = re.compile(r'notStarList "><a href="(.+?)".+?class="j_th_tit">(.+?)</a><span >', re.DOTALL)  
	html = urllib2.urlopen(url).read()  
	for x in find_re.findall(html):  
		str1 = 'http://tieba.baidu.com' + x[0].decode('gb2312', 'ignore').encode('utf-8')
		str2 = x[1].decode('gb2312', 'ignore').encode('utf-8')
		values = dict(  
			category = str1,  
			name = str2
		)
		num = db.chapter.find({"category":str1}).count()
		if num == 0:
			if str1.count('#') < 1:	
				if str2.count('章') > 0:
					if str2.count('第') >0:
#						print str1
#						print str2
						db.chapter.save(values)
						global message
						message = "{'title':'绝世唐门更新啦','description':'" + str2 +"','open_type': 1,'url': '"+str1 +"','user_confirm': 0}"
#						print message
						test_pushMessage_to_tag()
	print 'Done!',"Current Time:", time.strftime("%Y-%m-%d %A %X %Z", time.localtime())

def perthread(inc):
	print 'count',threading.activeCount()
	s.enter(inc,0,perthread,(inc,))
	t1 = threading.Thread(target=perform)
	t1.setDaemon(True)
	t1.start()
	t1.join(15)

def mymain(inc=20):
   s.enter(0,0,perthread,(inc,))
   s.run()

if __name__ == "__main__":
    mymain() 
