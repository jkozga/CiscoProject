#!/usr/bin/env python

import requests
import json
import sys

requests.packages.urllib3.disable_warnings()

username = 'cisco'
password = 'cisco'
host = '10.10.10.240'
port = '55443'
headers = {'Content-Type': 'application/vnd.yang.data+json',
           'Accept': 'application/json'}
content_type="application/json"

class Devices:
    type = 'none'
    host = 'none'
    port = 0
    def __init__(self, type, host, port):
        self.port = port
        self.host = host
        self.type = type
        return super().__init__()

def checkCodeCorrect(code):
    if code == 200:
        return True
    elif code == 201:
        return True
    elif code == 404:
        return False

def getToken():
    uri = 'https://{}:{}/api/v1/auth/token-services'.format(host, port)

    response = requests.post(uri,auth = (username, password), headers = headers, verify = False, timeout=1)
    if checkCodeCorrect(response.status_code):
        return (response.json())['token-id'] 
    return False

def getTokenDevice(host2, port2):
    uri = 'https://{}:{}/api/v1/auth/token-services'.format(host2, port2)

    response = requests.post(uri,auth = (username, password), headers = headers, verify = False, timeout=1)
    if checkCodeCorrect(response.status_code):
        return (response.json())['token-id'] 
    return False

def getBgpNeighbors(token, asn, vrf):
    headers = {"content-type": "application/json", "X-Auth-Token":token}
    uri = 'https://{}:{}/api/v1/vrf/{}/routing-svc/bgp/{}/neighbors'.format(host, port, vrf, asn)
    
    response = requests.get(uri, headers=headers, verify=False, timeout=10)
    if checkCodeCorrect(response.status_code):
        return (response.json())['items']
    return False

def getConfiguredInterfaces(token):
    headers = {"content-type": "application/json", "X-Auth-Token":token}
    url = 'https://{}:{}/api/v1/interfaces'.format(host, port)

    response = requests.get(url, headers=headers, verify=False, timeout=10)
    if checkCodeCorrect(response.status_code):
        return (response.json())['items']
    return False

def getConfiguredInterfacesDevice(token, host2, port2):
    headers = {"content-type": "application/json", "X-Auth-Token":token}
    url = 'https://{}:{}/api/v1/interfaces'.format(host2, port2)

    response = requests.get(url, headers=headers, verify=False, timeout=10)
    if checkCodeCorrect(response.status_code):
        return (response.json())['items']
    return False

def setBGP(token, asn, vrf):
    headers = {"content-type": "application/json", "X-Auth-Token":token}
    uri = 'https://{}:{}/api/v1/vrf/{}/routing-svc/bgp'.format(host, port, vrf)
    body = {"routing-protocol-id": asn}
    response = requests.post(uri, data=json.dumps(body), headers=headers, verify=False, timeout=1)
    #content = b'{"error-code": -1, "error-message": "BGP router 222 already exists in VRF a", "detail": " "}'
    if response.ok == True:
     print('BGP {} created in VRF {} !'.format(asn, vrf))
     return True
    else:
        rresponse = response.json()
        if rresponse["error-code"] == -1:
            print(rresponse["error-message"])
        return False

def main():

    #token = getToken()
    #if token == False:
    #    print('Issue with token')
    #    return

    
    #setBGP(token,'222','b')
    #print('abc')
    #print(getBgpNeighbors(token, '222', 'a'))
    #interfaces = (getConfiguredInterfaces(token))

    #for interface in interfaces:
    #    print(interface['if-name'] + '/' + interface['ip-address'])

    devices = {'10.10.10.240', '10.10.10.241'}
    for dev in devices:
        d = Devices('asr', dev, 55443)
        token = getTokenDevice(d.host, d.port)
        interfaces = (getConfiguredInterfacesDevice(token, d.host, d.port))
        for interface in interfaces:
            print(interface['if-name'] + '/' + interface['ip-address'])

if __name__ == '__main__':
    sys.exit(main())