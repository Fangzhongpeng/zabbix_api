#!/usr/bin/env python2.7

#coding=utf-8

import json

import urllib2

from urllib2 import URLError

# based url and required header

url = "http://zabbix.qkvoice.com/api_jsonrpc.php"

header = {"Content-Type":"application/json"}

# request json

data = json.dumps(

{

   "jsonrpc":"2.0",

   "method":"history.get",

   "params":{

       "output":"extend",

       "history":3,

       "itemids":"34727",

       "limit":1000

   },

   "auth":"fc446e795bf30cb42faf7522f6a30d79", # theauth id is what auth script returns, remeber it is string

   "id":1,

})

# create request object

request = urllib2.Request(url,data)

for key in header:

   request.add_header(key,header[key])

# get host list

try:

   result = urllib2.urlopen(request)

except URLError as e:

    if hasattr(e, 'reason'):

       print 'We failed to reach a server.'

       print 'Reason: ', e.reason

    elif hasattr(e, 'code'):

       print 'The server could not fulfill the request.'

       print 'Error code: ', e.code

else:

    response = json.loads(result.read())

    result.close()

    print "Item History: ", response['result']

    #print ("aaa")
    #print "Number Of Hosts: ", len(response['result'])


    #for host in response['result']:

            #print host

        #print "Host ID:",host['hostid'],"HostName:",host['name']
