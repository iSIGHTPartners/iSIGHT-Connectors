import hashlib
import hmac
import httplib
import email
import time
import datetime

public_key = ‘YOUR_PUBLIC_KEY’
private_key = ‘YOUR_PRIVATE_KEY’

time_stamp = email.Utils.formatdate(localtime=True)

search_time = datetime.datetime.now() - datetime.timedelta(days = 14)

search_time_in_epoch = int(time.mktime(search_time.timetuple()))

search_query = '/view/targets?since=' + str(search_time_in_epoch) + '&threatType=malwareFamily&value=dridex'

accept_version = '2.1'
accept_header = 'application/json'

hash_data = search_query + accept_version + accept_header + time_stamp
hashed = hmac.new(private_key, hash_data, hashlib.sha256)

headers = {
	'Accept' : accept_header,
	'Accept-Version' : accept_version,
	'X-Auth' : public_key,
	'X-Auth-Hash' : hashed.hexdigest(),
	'Date'  :  time_stamp,
}

conn = httplib.HTTPSConnection('api.isightpartners.com')
conn.request('GET', search_query, '', headers)
 
response = conn.getresponse()
print response.status
print response.read()
