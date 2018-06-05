import filecmp
import difflib
import re 
import os
import subprocess
import requests

def get_id():
    
    w = open('test.txt', 'w+')
    l = open('log.txt', 'w+')


    headers = {'X-OTX-API-KEY': 'd9d2976d89b7288d4499f6d54630a6985e324be75fa286b338c2d31b5d0d6334',}
    response = requests.get('https://otx.alienvault.com/api/v1/pulses/user/AlienVault', headers=headers)
    
    l.write(response.text)
    l.close()


def what():
    q = open('log.txt', 'r') 
    l2 = open('log2.txt', 'w+')    
    for line in q:
        s = re.search(r'(?<="id": ")(.*?)(?=")', line)
        l2.write(s)
    q.close()
    l2.close()



get_id()
what()
