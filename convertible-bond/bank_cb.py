import requests
import json

url = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___'

response = requests.get(url)
js=response.json()

bank_stock = ['无锡银行', '紫金银行', '张家港行', '中信银行', '郑州银行', '浦发银行', '贵阳银行', '西安银行',
			  '常熟银行', '江阴银行', '苏州银行', '渝农商行', '苏农银行', '江苏银行', '交通银行', '中国银行', 
			  '招商银行', '青岛银行', '重庆银行', '浙商银行', '光大银行', '华夏银行', '青农银行', '厦门银行', 
			  '长沙银行', '民生银行', '南京银行', '北京银行', '兴业银行', '上海银行', '建设银行', '农业银行', 
			  '成都银行', '邮政银行', '工商银行', '平安银行', '宁波银行', '杭州银行']
banks_list = []

# 银行转债达到下修条件时,一定会下修到底
# 转股价值低于85
# PB>0.7
# 价格低于到期赎回价
for i in js['rows']:
	if i['cell']['price_tips'] != '待上市'\
		and i['cell']['btype'] == 'C'\
		and i['cell']['stock_nm'] in bank_stock\
		and float(i['cell']['convert_value']) < 85 \
		and float(i['cell']['pb']) > 0.7\
		and float(i['cell']['price']) < float(i['cell']['redeem_price']):
		tmp=['现价:',round(float(i['cell']['price']),1), i['cell']['bond_nm'], '债券代码:'+i['id'], '溢价率:'+i['cell']['premium_rt'], '转股价值:'+i['cell']['convert_value']]
		banks_list.append(tmp)


print('--------------------------------')
print('银行低风险套利(下修套利)')
Num = 0
banks_list.sort()
for i in banks_list:
	Num += 1
	print('No.%02d %s'% (Num, i))
