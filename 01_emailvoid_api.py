#!/usr/bin/python

from __future__ import print_function

from logging import basicConfig, DEBUG

from emailvoid import EmailVoidClient

basicConfig(level=DEBUG)

# Prepare variable and client
user = 'support'
c = EmailVoidClient(apikey="b8818f4c8594021a9ca1489d135a2540d726f855767496788c6f1d76f2f5917d")


# Step 1. Fetc message count
print( c.msg_count(user) )

# Step 2. Fetch index
items = c.msg_search(user)
for item in items:
    print( item )

# Step 3. Fetch message
for item in items:
    msgid = item.get_msgid()
    #
    msg = c.msg_content(msgid=msgid)
    print(msg)

# Step 4. Dispose clisent
c.dispose()
c = None
