# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import MySQLdb
import MySQLdb.cursors
class TaobaoPipeline(object):

	def process_item(self, item, spider):

		price = item['price_attr'];
		phone = ['机身颜色','网络类型','套餐类型','机身内存'];
		for (ptattr,pattr) in price.items():
			if not ptattr in phone:
				return item;
		# 类型ID
		type_id = 1; 

		db = MySQLdb.connect(host="localhost",user="root",passwd="xiehui",db="mall258",charset='utf8')
		cur = db.cursor();
		g_price = 0;
		for (prs,vals) in item['price_value'].items():
			g_price = vals['price'];
			break
		# 插入商品内容
		cur.execute("insert into goods(g_number,g_name,g_keywords,g_description,gt_id,g_img,g_price) values(%s,%s,%s,%s,%s,%s,%s)",[item['temp'],item['name'],item['keywords'],item['description'],type_id,item['img'],g_price]);
		g_id = cur.lastrowid;
		print '---------------g_id='+str(g_id);
		# 获取商品类型属性
		cur.execute('select gta_name,gta_id from gt_attr where gt_id=%s',[type_id]);
		gtat = cur.fetchall();
		gta = {}
		for ga in gtat:
			gta[ga[0]] = ga[1];
		
		# 插入商品属性 如果类型没有就加
		attrs = item['attr'];
		for type_attr in attrs:
			for (tattr,vattr) in attrs[type_attr].items():
				gta_id =0;
				if gta.has_key(tattr):
					gta_id = gta.get(tattr);
				else:
					cur.execute("insert into gt_attr(gt_id,gta_name,gta_type) values(%s,%s,%s)",[type_id,tattr,type_attr]);
					gta_id = cur.lastrowid;

				cur.execute("insert into g_attr(g_id,ga_value,gta_id) values(%s,%s,%s)",[g_id,vattr,gta_id]);
					


		# 获取商品类型价格
		cur.execute('select gtp_name,gtp_id from gt_price where gt_id=%s',[type_id]);
		gtpt = cur.fetchall();
		gtp = {}
		for gp in gtpt:
			gtp[gp[0]] = gp[1];


		# 插入价格属性
		prices = {};
		for (ptattr,pattr) in price.items():
			gtp_id =0;
			if gtp.has_key(ptattr):
				gtp_id = gtp.get(ptattr);
			else:
				cur.execute("insert into gt_price(gt_id,gtp_name) values(%s,%s)",[type_id,ptattr]);
				gtp_id = cur.lastrowid;

			for ps in pattr:
				cur.execute("insert into g_price(g_id,gtp_id,gp_name) values(%s,%s,%s)",[g_id,gtp_id,ps['price_value']]);
				prices[ps['price_id']] = cur.lastrowid;


		# 插入价格值
		price_value = item['price_value'];
		for (prs,vals) in price_value.items():

			cur.execute("insert into g_price_info(g_id,gpi_img,gpi_sum,gpi_price) values(%s,%s,%s,%s)",[g_id,item['img'],100,vals['price']]);
			gpi_id = cur.lastrowid;
			psr = prs.split(';');
			for ip in psr:
				if prices.has_key(ip):
					cur.execute("insert into g_price_list(gp_id,gpi_id) values(%s,%s)",[prices[ip],gpi_id])



		db.commit();

		cur.close();
		db.close();
		return item
