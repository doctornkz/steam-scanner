# steam-scanner

Disclaimer: Just for python learning, not serious.

####Steam marketplace parser. 

Scan page with offers without cookies, with delay. 
Check anomaly in prices and push notifications in STDOUT and Telegram (as option)
Update local database with rifels, knives, etc and price on market.

Dependences
---------------
<<<<<<< HEAD
Python 3 with modules: requests
Telegram-cli (optional)
=======
### Python 2.7 with modules: requests, MySQLdb
### Telegram-cli https://github.com/vysheng/tg
### Mysql server
>>>>>>> 9cc06c0b0477b4c5f225c948bd8602dd86efeaf5

Using
----------------

1. git clone
<<<<<<< HEAD
2. Update properties and paths in py file and tg.sh(optional)
3. If you want loop scanning - feel free to use
%%while true; do (python ./steam_spider.py; sleep 500); done%%
=======
2. Update local mysql with dump file.
3. Update properties and paths in py file and tg.sh(optional)
4. If you want loop scanning - feel free to use
while true; do (python ./steam_spider.py; sleep 500); done
>>>>>>> 9cc06c0b0477b4c5f225c948bd8602dd86efeaf5

What's next?
----------------

 * Nothing. Just training.
