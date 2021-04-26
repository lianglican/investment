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

dl_cblist  = [] # 双低
lpp_cblist = [] # 低溢价
lp_cblist  = [] # 低价
banks_list = [] # 银行

for i in js['rows']:
	# 银行转债达到下修条件时,一定会下修到底
	# 转股价值低于85
	# PB>0.7
	# 价格低于到期赎回价
	if i['cell']['price_tips'] != '待上市'\
		and i['cell']['btype'] == 'C'\
		and i['cell']['stock_nm'] in bank_stock\
		and float(i['cell']['convert_value']) < 85 \
		and float(i['cell']['pb']) > 0.7\
		and float(i['cell']['price']) < float(i['cell']['redeem_price']):
		tmp=['现价:',round(float(i['cell']['price']),1), i['cell']['bond_nm'], '债券代码:'+i['id'], '溢价率:'+i['cell']['premium_rt'], '转股价值:'+i['cell']['convert_value']]
		banks_list.append(tmp)

	#攻守兼备:双低筛选规则
	# 1.PB > 1 
	# 2.价格低于到期赎回价 
	# 3.剩余规模小于25亿
	# 4.溢价率小于20%
	# 5.有回售
	# 6.未强赎
	# 7.剩余年限大于2年
	# 8.位于转股期
	# 9.税前收益率大于2% 
	if i['cell']['price_tips'] != '待上市'\
		and i['cell']['btype'] == 'C'\
		and float(i['cell']['pb']) > 1 \
		and float(i['cell']['price']) < float(i['cell']['redeem_price'])\
		and float(i['cell']['curr_iss_amt']) < 25 \
		and float(i['cell']['premium_rt'].strip('%')) < 20\
		and i['cell']['put_price'] != None\
		and i['cell']['redeem_dt'] == None\
		and float(i['cell']['year_left']) > 2\
		and i['cell']['convert_cd'] != '未到转股期'\
		and float(i['cell']['ytm_rt'].strip('%')) > 2:
		tmp=['双低:',float(i['cell']['dblow']), '债券代码:'+i['id'], i['cell']['bond_nm'], '现价:'+i['cell']['price'], '溢价率:'+ i['cell']['premium_rt']]
		dl_cblist.append(tmp)

	#进攻型：低溢价筛选规则
	# 1.未强赎
	if i['cell']['price_tips'] != '待上市'\
		and i['cell']['btype'] == 'C'\
		and i['cell']['redeem_dt'] == None :
		tmp=['溢价率:', float(i['cell']['premium_rt'].strip('%')), '债券代码:'+i['id'], i['cell']['bond_nm'], '现价:'+i['cell']['price']]
		lpp_cblist.append(tmp)

	#防守型：低价筛选规则
	# 1. 未强赎
	# 2. 有回售
	# 3. PB > 1, 100 <= 价格 < 105 且溢价率小于15%
	# 4. PB > 0.8, 90 <= 价格 < 100 且溢价率小于23%
	# 5. 85 <= 价格 < 90  且溢价率小于25%
	# 6. 80 <= 价格 < 85  且溢价率小于30%
	# 7. 价格 < 80        且溢价率小于50%
	# 8. 评级AA以上，税后年化收益7%以上
		if i['cell']['put_price'] != None\
			and ( (100 <= float(i['cell']['price']) < 105 and float(i['cell']['premium_rt'].strip('%')) < 15 ) \
				or (90 <= float(i['cell']['price']) < 100 and float(i['cell']['premium_rt'].strip('%')) < 23) \
				or (85 <= float(i['cell']['price']) < 90 and float(i['cell']['premium_rt'].strip('%')) < 25) \
				or (80 <= float(i['cell']['price']) < 85 and float(i['cell']['premium_rt'].strip('%')) < 30) \
				or (float(i['cell']['price']) < 80 and float(i['cell']['premium_rt'].strip('%')) < 50) \
				or i['cell']['rating_cd'].find("AA") != -1 and i['cell']['ytm_rt'].find("-") == -1 and float(i['cell']['ytm_rt'].strip('%')) > 7):
			tmp=['现价:',round(float(i['cell']['price']),1), i['cell']['bond_nm'], '债券代码:'+i['id'], '溢价率:'+i['cell']['premium_rt'], '税后收益率:'+i['cell']['ytm_rt']]
			lp_cblist.append(tmp)

print('--------------------------------')
print('银行低风险套利(下修套利)')
Num = 0
banks_list.sort()
for i in banks_list:
	Num += 1
	print('No.%02d %s'% (Num, i))
	
print('--------------------------------')
print('防守型：低价格(需自行剔除无法下修转股价格的标)')
Num = 0
lp_cblist.sort()
for i in lp_cblist[0:10]:
	Num += 1
	print('No.%02d %s'% (Num, i))

print('--------------------------------')
print('攻守兼备:双低')
Num = 0
dl_cblist.sort()
for i in dl_cblist[0:10]:
	Num += 1
	print('No.%02d %s'% (Num, i))
	# print('No.%02d %s'% (Num, json.dumps(i).decode("unicode-escape")))

print('--------------------------------')
print('进攻型：低溢价')
Num = 0
lpp_cblist.sort()
for i in lpp_cblist[0:5]:
	Num += 1
	print('No.%02d %s'% (Num, i))