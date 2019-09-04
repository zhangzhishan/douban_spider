#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
import argparse
import urllib2
import re

class douban_hot:
	"""一个用来爬取豆瓣热门内容的简单爬虫"""
	def __init__(self):
		self.base_url = "https://www.douban.com/explore/"
		self.classifications = ["影视", "读书", "音乐", "人文", "艺术", "旅行", "美食", "爱美丽", "生活家", "画画儿", "摄影", "自然", "Selenium", "建筑", "讲故事", "找乐", "二次元", "技术宅", "涨知识", "萌宠", "情感", "成长", "娱乐八卦", "运动健身", "美女", "理财", "大家正在聊"]
		self.classifications_column = [5, 10, 17, 13, 7, 2, 12, 18, 11, 8, 4, 14, 24, 19, 6, 3, 1029, 20, 26, 16, 23, 25, 9, 15, 22, 21, 27]
		self.headers=[{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'},\
					{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'},\
					{'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30)'},\
					{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'},\
					{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}]




	#写入图片
	def saveImg(self, imageUrl, fileName):
	    u=urllib2.urlopen(imageUrl)
	    data=u.read()
	    f=open(fileName + '.jpg','wb')
	    f.write(data)
	    f.close()

	def get_argument(self):
		parser = argparse.ArgumentParser(description='一个爬取豆瓣热门内容的简单爬虫')
		parser.add_argument('-p', action='store', dest='page_value', default='1',
		                    help='读取内容的页数')
		parser.add_argument('-c', action='store', dest='class_value', default='全部',
		                    help='热门内容的种类：影视 读书 音乐 人文 艺术 旅行 美食 爱美丽 生活家 画画儿 摄影 自然 手作 建筑 讲故事 找乐 二次元 技术宅 涨知识 萌宠 情感 成长 娱乐八卦 运动健身 美女 理财 大家正在聊')
		parser.add_argument('--version', action='version', version='%(prog)s 1.0')

		results = parser.parse_args()
		return results

	def get_douban(self, nb_page, nb_column):
		if (nb_column == '全部'):
			url = self.base_url
		elif (nb_column in self.classifications):
			nb_column = self.classifications.index(nb_column)
			url = self.base_url + 'column/' + str(nb_column)
		else:
			print('[+] 所选分类不包含在基本分类中，采用默认所有热门内容')
			url = base_url
		for i in range(int(nb_page)):
			#创建请求的request
			try:
				req = urllib2.Request(url, headers=self.headers[i%len(self.headers)])
				result = urllib2.urlopen(req).read()
			except (urllib2.HTTPError, urllib2.URLError), e:
				print e
				continue
			soup = BeautifulSoup(result, "lxml")

			for hot_content in soup.find_all('div', {'class':'item'}):
				user_name = hot_content.find('div', {'class': 'hd'}).find('div',{'class':'usr-pic'}).find_all('a')[1].string.strip()
				# 有些条目只有图片没有内容，所以在这里需要一个判断
				content = hot_content.find('div', {'class': 'bd'}).find('div',{'class':'content'})
				if content.find('p'):
					title = hot_content.find('div', {'class': 'bd'}).find('div',{'class':'content'}).find('div',{'class':'title'}).find('a').string.strip()
					content = content.find('p').find('a').string.strip()
				else:
					title = hot_content.find('div', {'class': 'bd'}).find('div',{'class':'title'}).find('a').string.strip()
					content = content.find('div', {'class': 'photoslider'}).find('div', {'class': 'first-pic'}).find('a').find('img').get('src').strip()
					self.saveImg(content, title)

				print title

if __name__ == '__main__':
	crawl = douban_hot()
	results = crawl.get_argument()
	nb_page = results.page_value
	nb_column = results.class_value
	crawl.get_douban(nb_page, nb_column)
