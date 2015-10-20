'''iSIGHT Partners makes no representations about the suitability of this software for any purpose.  
The software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement.  
In no event shall the author(s) be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use of the software.'''


import hashlib
import hmac
import httplib
import email

public_key = ‘YOUR_PUBLIC_KEY’
private_key = ‘YOUR_PRIVATE_KEY’

search_query = '/view/iocs'

accept_version = '2.0'
accept_header = 'application/json'
time_stamp = email.Utils.formatdate(localtime=True)

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
