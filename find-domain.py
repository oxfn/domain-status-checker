#!/usr/bin/env python

import os
import re
import sys
import subprocess

class NSResponse:
    def __init__(self, domain: str, registered: bool=False, ip:str=None):
        self.domain = domain
        self.registered = registered
        self.ip = ip

    def __str__(self):
        return f"<{self.domain}:{self.ip}>"

class NSRequest:
    def __init__(self, domain:str):
        self.domain = domain

    def run(self):
        args = ['nslookup', self.domain]
        kwargs = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with subprocess.Popen(args, **kwargs) as proc:
            proc.wait()
            registered = proc.returncode == 0
            ip = None
            if registered:
                for line in proc.stdout.readlines():
                    line = line.decode('utf-8')
                    if line.startswith('Address:'):
                        m = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                        if m:
                            ip = m.groups(1)
            return NSResponse(self.domain, registered, ip)

def get_domains():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for a in letters:
        for b in letters:
            yield f"{a}{b}.su"


if __name__ == "__main__":
    for domain in get_domains():
        print(NSRequest(domain).run())

