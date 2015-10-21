import hashlib 
import hmac 
import httplib 
 
public_key = ‘YOUR_PUBLIC_KEY’
private_key = ‘YOUR_PRIVATE_KEY’

search_query = '/view/iocs?format=json'

hashed = hmac.new(private_key, '', hashlib.sha256)
 
headers = { 
    'X-Auth' : public_key, 
    'X-Auth-Hash' : hashed.hexdigest()
}

conn = httplib.HTTPSConnection('api.isightpartners.com')
conn.request('GET', search_query, '', headers)
 
response = conn.getresponse()
print response.status
print response.read()
