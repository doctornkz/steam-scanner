#!/bin/bash
# Notify via telegram. Console client using.
# Telegram CLI : https://github.com/vysheng/tg
# Can be bypassed

telegram-cli --disable-output -W -e  "msg <username> $1" > /dev/null 2>&1
