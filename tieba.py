# coding: utf8
import urllib2  
import re  
import pymongo

db=pymongo.Connection('localhost',27017).test
url = 'http://tieba.baidu.com/f/good?kw=%BE%F8%CA%C0%CC%C6%C3%C5&cid=0&tp=0&pn=0'  
find_re = re.compile(r'notStarList "><a href="(.+?)".+?class="j_th_tit">(.+?)</a><span >', re.DOTALL)  
html = urllib2.urlopen(url).read()  
for x in find_re.findall(html):  
	str1 = x[0].decode('gb2312').encode('utf-8')
	str2 = x[1].decode('gb2312').encode('utf-8')
	values = dict(  
		category = str1,  
		name = str2
    )
	if str1.count('#') < 1:	
		if str2.count('章') > 0:
			if str2.count('第') >0:
				print str1
				print str2
				db.priate.save(values)
print 'Done!'  
