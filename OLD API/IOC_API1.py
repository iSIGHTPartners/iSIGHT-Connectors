'''iSIGHT Partners makes no representations about the suitability of this software for any purpose.  
The software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement.  
In no event shall the author(s) be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use of the software.'''


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
