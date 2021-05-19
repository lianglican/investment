import requests
import json

url = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___'

response = requests.get(url)
js=response.json()

cb_dict = {"宝莱转债":102, "乐歌转债":120, "银河转债":123, "溢利转债":185, "正元转债":120, "金农转债":120, "联得转债":110,
		   "模塑转债":160, "凯发转债":118, "新天转债":115, "尚荣转债":120, "万顺转债":113, "久吾转债":110, "英联转债":120,
		   "通光转债":170, "东时转债":120, "智能转债":103, "飞鹿转债":118, "雷迪转债":105, "今飞转债":102, "哈尔转债":101}

low_scale_list = [] # 低规模

for i in js['rows']:
	# 剩余规模小于3亿
	# 转股价值小于130
	# 未强赎
	# 低于指定价格
	if i['cell']['price_tips'] != '待上市'\
		and i['cell']['btype'] == 'C'\
		and i['cell']['bond_nm'] in cb_dict\
		and i['cell']['redeem_dt'] == None\
		and float(i['cell']['convert_value']) < 130 \
		and float(i['cell']['price']) < cb_dict[i['cell']['bond_nm']]:
		tmp=[i['cell']['bond_nm'], '债券代码:'+i['id'], '现价:'+i['cell']['price'], '建仓价:', cb_dict[i['cell']['bond_nm']]]
		low_scale_list.append(tmp)

print('--------------------------------')
print('妖债潜伏')
Num = 0
low_scale_list.sort()
for i in low_scale_list:
	Num += 1
	print('No.%02d %s'% (Num, i))
