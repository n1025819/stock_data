#coding:utf-8
import requests
import json
import time
import datetime

class stock(object):
	"""股票相关数据的类"""
	url_root='http://quotes.money.163.com/service/chddata.html'
	fields='TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG'
	time_now=time.strftime('%Y%m%d',time.localtime())
	yesterday=(datetime.date.today()-datetime.timedelta(days = 1)).strftime("%Y%m%d")

	def __init__(self,stock_code,start='20180101',end=time_now):
		if stock_code[-2:]=='sz':
			self.code = '1{0}'.format(stock_code[0:-3])
		elif stock_code[-2:]=='sh':
			self.code = '0{0}'.format(stock_code[0:-3])
		self.start=start
		self.end=end

	def get_data(self,start='20180101',end=time_now): #获取个股区间内高低开收价格数据
		url='{0}?code={1}&start={2}&end={3}&fields={4};'.format(stock.url_root,self.code,start,end,stock.fields)
		req=requests.get(url)
		data_str=req.text
		data_list=data_str.split('\r\n')[1:]
		data_list=data_list[0:len(data_list)-1]
		return data_list

	def highest_price(self,start='20180101',end=time_now): #通过价格列表计算区间内最高价data_list[i][4]
		data_list=self.get_data(start,end)
		highest=float(data_list[0].split(',')[4])
		for i in data_list:
			temp_high=float(i.split(',')[4])
			if temp_high>highest:
				highest=temp_high
		return highest

	def get_close(self,date_open=yesterday,date_close=time_now): #获取当日收盘价
		data_list=self.get_data(date_open,date_close)
		return data_list[-1].split(',')[3]

	def get_buy_price(self,date_open=yesterday,date_close=time_now): #获取建仓日开盘价
		data_list=self.get_data(date_open,date_close)
		return data_list[-1].split(',')[6]
	
	def get_CHG(self,date_open=yesterday,date_close=time_now): #获取今日涨跌幅
		data_list=self.get_data(date_open,date_close)
		return data_list[-1].split(',')[8]
	
	def get_new_date(self,date_open=yesterday,date_close=time_now): #获取最新更新时间
		data_list=self.get_data(date_open,date_close)
		return data_list[-1].split(',')[0]
	
	def get_name(self,date_open=yesterday,date_close=time_now): #获取名称
		data_list=self.get_data(date_open,date_close)
		return data_list[-1].split(',')[2]

	def get_highest_profit(self,start='20180101',end=time_now):
		data_list=self.get_data(start,end)
		highest=self.highest_price(start,end)
		tclose=self.get_close()
		buy_price=self.get_buy_price(date_open=start)
		highest_profit=(float(highest)-float(buy_price))/float(buy_price)
		return highest_profit
		

if __name__=='__main__':
	pass
