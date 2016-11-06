#coding:utf-8 

from selenium import webdriver  
# from selenium.common.exceptions import NoSuchElementException  
# from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait
import time
# import time,os,sys


# chromedriver = "c:/Python27/Scripts/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# browser = webdriver.Chrome(chromedriver)


# file=open('d:/elong_crawler.txt','a+')
# file.write('hotel'+'\t'+'name'+'\t'+'mark'+'\t'+'price'+'\t'+'promotion'+'\t'+'roomid'+'\t'+'breakfastid\n')
def get_elong(e_id):
	urlelong='http://hotel.elong.com/beijing/%s/'%e_id
	print urlelong
	c.get(urlelong)
	c.get(urlelong)
	time.sleep(1) 
	# WebDriverWait(c,10).until(lambda the_driver: the_driver.find_element_by_xpath('//div[@handle="ratePlan"]').is_displayed())#接受一个dr对象和设置最长等待时间为10s




	rooms=c.find_elements_by_xpath('//div[@handle="ratePlan"]')
	# [class="infoBox borst clx"]
	print len(rooms)
	i=0

	
	for room in rooms:	

		
		# name= c3.find_element_by_xpath("//div[contains(@class,'clrfix order-detail')]")
		
		price = room.find_element_by_xpath('	.//span[@method="AvgPrice"]')
		
		# promo=room.find_element_by_xpath('	.//span[@method="coupon"]')
		try:
			promo=room.find_element_by_xpath('	.//span[@method="coupon"]')
			promotion=promo.text
		except:
			promotion='0'
			
			
		name=room.find_element_by_xpath('../.././/a[@class="rpname"]')
		breakfast=room.find_element_by_xpath('.//p[@class="rpw1"]')
		roomid=room.get_attribute("sroomid")
		breakfastid=room.get_attribute("rpid")
		
		
		# if 1:
		gift_string="no gift"
		
		try:
			# time.sleep(0.1) 
			gift=room.find_element_by_xpath('.//span[@method="gift"]')
			print 'yes '+name.text +breakfast.text
			gift.click()
			gift_string="has gift"
			time.sleep(1) 
			try:
				gift_content=room.find_element_by_xpath('//div[@class="el-poptip-content"]')
				print gift_content.text
				gift_string=gift_content.text
			except:	
				print 'no content'
		except:
			pass
		
		
			
		# print ( promotion+'\t').encode('mbcs')
		
		each = name.text + '\t' + breakfast.text.replace('\n','') +'\t' + price.text+'\t'+promotion + '\t' + roomid + '\t' + breakfastid + '\t' + gift_string.replace('\n','\t')
		each=each.encode('mbcs')
		
		# print each
		file.write(e_id +'\t'+ each +'\n')


	# c.quit()
	
def get_elong_t7(e_id,ruzhu):
	c.get('http://hotel.elong.com/beijing/%s/'%e_id)

	# 反后价
	aftercoupon=c.find_element_by_xpath('//*[@id="detailTab"]/li/label[@method="aftercouponprice"]')
	aftercoupon.click()
	# time.sleep(5) 
	WebDriverWait(c,10).until(lambda the_driver: the_driver.find_element_by_xpath('//div[@handle="ratePlan"]').is_displayed())#接受一个dr对象和设置最长等待时间为10s
	time.sleep(1) 
	# t+7

	# 选择入住日期
	if ruzhu==0:
	# if ruzhu==111:
		apply=c.find_element_by_id('checkInDateApply')
		apply.click()
		month=c.find_element_by_xpath('//table[@date="2015-1-"]')
		date=month.find_element_by_xpath('.//tr/td[text()=30]')
		date.click()
		
		time.sleep(1)
		
		# 选择退房日期
		apply=c.find_element_by_id('checkOutDateApply')
		apply.click()
		month=c.find_element_by_xpath('//table[@date="2015-2-"]')
		date=month.find_element_by_xpath('.//tr/td[text()=6]')
		time.sleep(1)
		date.click()

		change=apply.find_element_by_xpath('.././/input[@id="Revise"]')
		
		change.click()
	
	# t+7
	
	# time.sleep(1) 
	
	# 处理unbookable
	# if c.find_element_by_xpath('//*[@id="noRoom"]') :
		# noroom=c.find_element_by_xpath('//*[@id="noRoom"]/text()')
		# print 'no room'
	# else:
		# WebDriverWait(c,5).until(lambda the_driver: the_driver.find_element_by_xpath('//div[@handle="ratePlan"]').is_displayed())
		# pass
	

	rooms=c.find_elements_by_xpath('//div[@handle="ratePlan"]')
	# [class="infoBox borst clx"]
	print len(rooms)
	i=0

	
	for room in rooms:	
		
		jxj=0
		try :
			room.find_element_by_xpath('.//span[@class="lijiane"]')
			print 'jxj'
			jxj=1
		except:
			pass

		if jxj==1 :
			continue
				
		# name= c3.find_element_by_xpath("//div[contains(@class,'clrfix order-detail')]")
		
		price = room.find_element_by_xpath('.//span[@method="AvgPrice"]')
		
		# promo=room.find_element_by_xpath('	.//span[@method="coupon"]')
		try:
			promo=room.find_element_by_xpath('	.//span[@method="coupon"]')
			promotion=promo.text
		except:
			promotion='0'
			
			
		name=room.find_element_by_xpath('../.././/a[@class="rpname"]')
		breakfast=room.find_element_by_xpath('.//p[@class="rpw1"]')
		roomid=room.get_attribute("sroomid")
		breakfastid=room.get_attribute("rpid")
		bookable=room.find_element_by_xpath('.//p[@class="rpw7"]').text.replace('\n','')
		
		# print ( promotion+'\t').encode('mbcs')
		
		each = name.text + '\t' + breakfast.text.replace('\n','') +'\t' + price.text+'\t'+promotion + '\t' + roomid + '\t' + breakfastid + '\t' +bookable
		each=each.encode('mbcs')
		
		print each
		file.write(e_id +'\t'+ each +'\n')
list=''
for line in open('d:\list.txt','r').readlines():
	list=list+line.strip()+'\n'



file=open('d:/elong_crawler.txt','r')


# already done lists
already=[]
# kekka=open('d:\elong_crawler.txt','r')
count=0
for lines in file:
	row=lines.split('\t')
	if not row[0] in already:
		if len(row[0] ) < 8:
			this= "0"* (8-len(row[0] )) + row[0]  
		else:
			this= row[0]
		already.append(this)
		count+=1
print already
file.close()

file=open('d:/elong_crawler.txt','a+')
file.write('hotel'+'\t'+'name'+'\t'+'mark'+'\t'+'price'+'\t'+'promotion'+'\t'+'roomid'+'\t'+'breakfastid\n')

c = webdriver.Chrome()
# c.set_window_size(1024, 768)

count=1
for i in list.strip().split('\n'):
	if len(i) < 8:
		i= "0"* (8-len(i)) + i
	if not i in already:
		print str(count) + ' times' + i
		count+=1
		if count==2:
			get_elong_t7(i,0)
		elif count >2:
			get_elong_t7(i,1)
	else:
		print 'already' 
		
