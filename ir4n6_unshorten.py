from __future__ import print_function
import requests
import sys
from pprint import pprint

if len(sys.argv) < 2:
    print("Need a URL to unshorten...")
    sys.exit()

s_url = sys.argv[1]
s_url = s_url.replace('http://', '').replace('https://', '')
#print(s_url)

#s_url = 'http://bit.ly/2GmLHzg'
url = 'https://unshorten.me/json/'
r = requests.get(url + s_url)
pprint(r.json())
