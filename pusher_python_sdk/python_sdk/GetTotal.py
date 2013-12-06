#!/usr/bin/python
# _*_ coding: UTF-8 _*_

import sys
import time
import urllib2  
import re  
import pymongo
import time
sys.path.append("..")
from Channel import *
from pymongo import MongoClient

url0 = 'http://tieba.baidu.com/p/1980204171' 

find_re0 = re.compile(r'<span class="red">(.+?)</span>', re.DOTALL)
html0 = urllib2.urlopen(url0).read()
#client = MongoClient('ds039507.mongolab.com',39507)
#db = client.tangmen
#db.authenticate('jiangzhouq', 'biu1biu2biu3')
 
for x in find_re0.findall(html0):
	count = int(x) + 1

for i in range(1,count):
	find_re = re.compile(r'<span class="edit_font_normal">(.+?)</span><br><a href=.+?target="_blank">http://tieba.baidu.com(.+?)</a>', re.DOTALL)  
	url = url0 +'?pn='+ str(i)
	html = urllib2.urlopen(url).read()  
	for x in find_re.findall(html):  
		str1 = 'http://tieba.baidu.com' + x[1].decode('gb2312', 'ignore').encode('utf-8')
		str2 = x[0].decode('gb2312', 'ignore').encode('utf-8')
		values = dict(  
			category = str1,  
			name = str2
		)
#		num = db.chapter1.find({"category":str1}).count()
#		if num == 0:
		if str1.count('#') < 1:	
			if str2.count('章') > 0:
				if str2.count('第') >0:
					print str1," ", str2
#						db.chapter1.save(values)
	print 'Done!'
