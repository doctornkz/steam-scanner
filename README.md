# steam-scanner

Steam marketplace parser. 
(Just for python learning, not serious.)
==================

Scan page with offers without cookies, with delay. 
Check anomaly in prices and push notifications in STDOUT and Telegram (as option)
Update local database with rifels, knives, etc and price on market.

Dependences
---------------
Python 3 with modules: requests
Telegram-cli (optional)

Using
----------------

1. git clone
2. Update properties and paths in py file and tg.sh(optional)
3. If you want loop scanning - feel free to use
%%while true; do (python ./steam_spider.py; sleep 500); done%%

What's next?
----------------

 * Nothing. Just training.
