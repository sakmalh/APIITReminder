from dotenv import load_dotenv
import os
import logging

load_dotenv(override=False)
IPS = os.getenv('IPS')
PRIVATE = os.getenv('PRIVATE')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
PRESHARED = os.getenv('PRESHARED')
ENDPOINT = os.getenv('ENDPOINT')

mappings = {
    'ADDRESS': IPS,
    'PRIVATEKEY': PRIVATE,
     'PUBLICKEY': PUBLIC_KEY,
     'PRESHAREDKEY': PRESHARED,
     'ENDPOINT': ENDPOINT,
}

with open('wireguard.conf', 'r') as file:
    filedata = file.read()

for x, y in mappings.items():
    filedata = filedata.replace(x, y)

with open('wireguard.conf', 'w') as file:
    file.write(filedata)