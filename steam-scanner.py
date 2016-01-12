#return 0
import requests 
import time
import re
import sqlite3
import subprocess
from random import randint

PATH_SQLITE_DB = "sqlite/steam_database.sqlite"  # sqlite items storage. 
PATH_TELEGRAM_SHELL = "telegram/tg.sh" # telegram-cli must be installed from https://github.com/vysheng/tg

def looper():

	for tag in ['strange','tournament']:
		max_rows = int((int(status(1,1,tag)[0][1]) // 100) * 100)
		for part in range(1, (max_rows),100):
			time.sleep(randint(5,20))
			print("Mining section " + str(part) +  " from " + str(max_rows) + " in " + tag + " category")
			database_mining(part, tag)
	print("Mining " + tag + " complete....")
	return 0

def telegram(message):

	try:
		subprocess.Popen([PATH_TELEGRAM_SHELL, message]) 
	except:
		print("Something wrong with Telegram client...")

def make_nice(s):
	# Unicoding /uXXXX symbols
    return re.subn('(#u[0-9a-f]{4})', lambda cp: chr(int(cp.groups()[0][2:],16)), s) [0]

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
				array.append(["info_line",i.split(",")[3].split(":")[1]])
			
			if "normal_price" in i and "table" not in i:
				new_price = float(i.replace('USD','$').split('$')[1])
			
			if "href" in i:
				url = i.replace('\/','/').split('"')[3].replace('\\','')
			
			if "market_listing_item_name" in i and "block" not in i:
				name = (i.split('>')[1].split('<')[0]).replace("\\","#")			

				array.append([new_price, name, url])

	return array

def database_mining(part, tag):	

	message = ''
	name = ''
	price = ''
	new_price = ''

	db = sqlite3.connect(PATH_SQLITE_DB)
	cur = db.cursor()
	dump = status(part,100,tag)
	if len(dump) > 5:
		for items in dump:
			if items[0] != "info_line" and items[1] != "":
				new_price = float(items[0])
				name = make_nice(str(items[1]))
				url = str(items[2])
				"""
				Main Logic. Finding Max Price, Min Price, Comparing, Updating.
				"""
				try:
					cur.execute ("SELECT * FROM  items WHERE id_items LIKE ?", (name,)) 
				except:
					print("Database Problem. Can't SELECT")
					return 0
				results = cur.fetchall()
				if len(results) > 0:
					for row in results:
						#moving price
						#current to old

						try:
							cur.execute("UPDATE items SET old_price = ? WHERE id_items LIKE ? ", [(row[1]), (name)])
							cur.execute("UPDATE items SET new_price = ? WHERE id_items LIKE ? ", [(new_price),(name)])
							db.commit()
						except:
							print("update in moving has problem")
							db.rollback()
						# updating min and max

						if row[3] > new_price:
							# 0.3 better 0.2
							if (1 - (new_price / row[3])) > 0.3:
								string = ("EXTREAM MINIMUM! ", str(row[3]), " now:", str(new_price)," max:" , str(row[4]), name, url)
								# Notify
								if row[3] != 1000: #default cost. Not notify after actual cost updating.
									telegram(" ".join(string))
									print(" ".join(string))

							else:
								#string = ("minimum ", str(row[3]), " now:", str(new_price)," max:" , str(row[4]), name, url)
								#print(" ".join(string))
								pass

							try:
								cur.execute("UPDATE items SET min_price = ? WHERE id_items LIKE ? ", [(new_price),(name)])
								db.commit()
							except:
								print("update in minimum has problem")
								db.rollback()
						if row[4] < new_price:
							if (1 - (row[4] / new_price)) > 0.3:
								string = ("EXTREAM MAXIMUM! ", str(row[4]), " now:", str(new_price), " min:",str(row[3]),name, url)
								#print(" ".join(string))
							else:
								string = ("maximum ", str(row[4]), " now:", str(new_price), " min:",str(row[3]),name, url)
								#print(" ".join(string))
						
							try:
								cur.execute("UPDATE items SET max_price = ? WHERE id_items LIKE ? ", [(new_price),(name)])
								db.commit()
							except:
								print("update in maximium has problem")
								db.rollback()

				# If item not found - update database
				else:
					record = [(name), (new_price), (0.0), (1000), (0)]
					try: 
						cur.execute('INSERT INTO items VALUES (?,?,?,?,?)', record)
						db.commit()
					except:
						print("insert new item has problem")
						db.rollback()
	else:
		print("Wrong data. Check ban status.")
	db.close()
	return 0

looper()