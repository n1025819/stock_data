#-*-coding:utf-8-*-
#默认设置：程序可见，只打开不新建工作薄，屏幕更新关闭
import xlwings as xw
from stock_data import stock
import datetime

app=xw.App(visible=True,add_book=False)
app.display_alerts=False
app.screen_updating=False
filepath=r'F:\工作\三只牛股推荐记录 (自动保存的).xlsx'
wb=app.books.open(filepath)

#a推荐时间	b代码	c简称	d更新时间	e最新价	f今日涨跌幅	g建仓价	h最大盈利

def input_data(sheet_name):
	i=4
	while type(wb.sheets[sheet_name].range('a'+str(i)).value)==datetime.datetime:
		#获取表格数据部分
		stock_name=wb.sheets[sheet_name].range('b'+str(i)).value#从表的b列获取股票代码
		start_date=wb.sheets[sheet_name].range('a'+str(i)).value#从表的a列获取推荐时间
		start_date=start_date.strftime('%Y%m%d')#解析推荐时间为合适格式
		stock_class=stock(stock_name,start_date)#创建一个stock类的实例：stock_class
		#填表部分
		wb.sheets[sheet_name].range('c'+str(i)).value=stock_class.get_name()
		wb.sheets[sheet_name].range('d'+str(i)).value=stock_class.get_new_date()
		wb.sheets[sheet_name].range('e'+str(i)).value=stock_class.get_new_price()
		wb.sheets[sheet_name].range('f'+str(i)).value=stock_class.get_CHG()
		wb.sheets[sheet_name].range('g'+str(i)).value=stock_class.get_buy_price(start_date)
		wb.sheets[sheet_name].range('h'+str(i)).value=stock_class.get_highest_profit(start=start_date)
		wb.sheets[sheet_name].range('i'+str(i)).value=stock_class.get_new_profit(start_date)
		i+=1

if __name__=='__main__':
	a=input("请输入表名:")
	input_data(a)


