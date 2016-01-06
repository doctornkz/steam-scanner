# steam-scanner

Disclaimer: Just for python learning, not serious.

####Steam marketplace parser. 

Scan page with offers without cookies, with delay. 
Check anomaly in prices and push notifications in STDOUT and Telegram (as option)
Update local database with Rifels, Knifes, etc and price on market.

Dependences
---------------
### Python 2.7 with modules: requests, MySQLdb
### Telegram-cli https://github.com/vysheng/tg
### Mysql server

Using
----------------

1. git clone
2. Update local mysql with dump file.
3. Update properties and paths in py file and tg.sh(optional)
4. If you want loop scanning - feel free to use
while true; do (python ./steam_spider.py; sleep 500); done

What's next?
----------------

 * Nothing. Just training.
