import requests 
import time
import re
import MySQLdb
from random import randint
import subprocess

def looper():
	for tag in ['strange','tournament']:
		max_rows = int((int(status(1,1,tag)[0][1]) // 100) * 100)
		#max_rows = 200
		for part in range(1, (max_rows),100):
			time.sleep(randint(5,20))
			print("Mining section " + str(part) +  " from " + str(max_rows) + " in " + tag + " category")
			database_mining(part, tag)
	print("Mining " + tag + " complete....")
	return 0
def telegram(message):
	try:
		subprocess.Popen(["/home/doctor/telegram/tg.sh", message]) 
	except:
		print("Smth wrong")

def status(pages,pool,tag):
	array = []
	#tag = strange tournament
	if int(pages) > 0:
		url = 'http://steamcommunity.com/market/search/render/?query=&'\
		'start='+ str(pages) + '&'\
		'count=' + str(pool) + '&'\
		'search_descriptions=0&'\
		'sort_column=price&'\
		'sort_dir=asc&'\
		'appid=730&'\
		'category_730_ProPlayer[]=any&'\
		'category_730_StickerCapsule[]=any&'\
		'category_730_TournamentTeam[]=any&'\
		'category_730_Weapon[]=any&'\
		'category_730_Quality[]=tag_' + tag
		try:
			r = requests.get(url)
		except:
			print("Network or DNS problem, exit...")
			return 0
		list_page = r.text.split(" class")
		for i in list_page:
			if "{" in i:
				array.append(["info_line",i.split(",")[3].split(":")[1].decode('unicode_escape').encode('ascii','ignore')])
				continue
			if "normal_price" in i and "table" not in i:
				new_price = float(i.replace('USD','$').split('$')[1].encode('ascii','ignore'))
			if "href" in i:
				url = i.replace('\/','/').split('\\')[3].encode('ascii','ignore').replace('"','')
			if "market_listing_item_name" in i and "block" not in i:
				name = i.split('>')[1].split('<')[0].encode('ascii','replace').replace('\\u2122','').replace('\\u2605','')
				array.append([new_price, name, url])
	return array

def database_mining(part, tag):	
	message = ''
	name = ''
	price = ''
	new_price = ''
	db = MySQLdb.connect(host = "localhost",
					user = "****",
					passwd = "****",
					db = "steam_database")
	cur = db.cursor()
	dump = status(part,100,tag)
	if len(dump) > 5:
		for items in dump:
			if items[0] != "info_line" and items[1] != "":
				new_price = float(items[0])
				name = str(items[1])
				url = str(items[2])
				"""
				Main Logic. Finding Max Price, Min Price, Comparing, Updating.
				"""
				sql = """SELECT * FROM 	items WHERE id_items LIKE %s""" 
				cur.execute(sql, (name))
				results = cur.fetchall()
				if len(results) > 0:
					for row in results:
						#moving price
						#current to old
						sql_update_old = """UPDATE items SET old_price = %s WHERE id_items LIKE %s """ 
						try:
							cur.execute(sql_update_old, (row[1], name))
							db.commit()
						except:
							db.rollback()
						#new to current
						sql_update_new = """UPDATE items SET new_price = %s WHERE id_items LIKE %s """

						try:
							cur.execute(sql_update_new, (new_price,name))
							db.commit()
						except:
							db.rollback()

						# updating min and max

						if row[3] > new_price:
							# 0.3 better 0.2
							if (1 - (new_price / row[3])) > 0.25:
								string = ("EXTREAM MINIMUM! ", str(row[3]), " now:", str(new_price)," max:" , str(row[4]), name, url)
								# Notify
								telegram(" ".join(string))
								
								print(" ".join(string))
							else:
								string = ("minimum ", str(row[3]), " now:", str(new_price)," max:" , str(row[4]), name, url)
								
								#print(" ".join(string))
							sql_update_min = """UPDATE items SET min_price = %s WHERE id_items LIKE %s """
							try:
								cur.execute(sql_update_min, (new_price,name))
								db.commit()
							except:
								db.rollback()
						if row[4] < new_price:
							if (1 - (row[4] / new_price)) > 0.3:
								string = ("EXTREAM MAXIMUM! ", str(row[4]), " now:", str(new_price), " min:",str(row[3]),name, url)
								#print(" ".join(string))
							else:
								string = ("maximum ", str(row[4]), " now:", str(new_price), " min:",str(row[3]),name, url)
								#print(" ".join(string))
						
							sql_update_max = """UPDATE items SET max_price = %s WHERE id_items LIKE %s """
							try:
								cur.execute(sql_update_max, (new_price,name))
								db.commit()
							except:
								db.rollback()

				# If item not found - update database
				else:
					try: 
						cur.execute("""INSERT INTO items VALUES (%s,%s,%s,%s,%s)""", (name,new_price,0.0,1000,0))
						db.commit()
					except:
						db.rollback()
	else:
		print("Wrong data. Check ban status.")
	db.close()
	return 0
looper()

