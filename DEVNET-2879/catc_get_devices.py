#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for retrieving Catalyst Center devices, and 
printing it out in a Splunk friendly JSON format. This script could then be
added to Splunk as a scripted input.

This script can also be used as a source for device IDs, which could be utilized
in the "catc_get_interfaces.py" script.

------------

Copyright (c) 2025 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import json
import requests

requests.urllib3.disable_warnings()

class CatalystCenter():
    user:str = None
    pw:str = None
    host:str = None
    token:str = None
    devices:list = None

    def __init__(self, user:str, pw:str, host:str)->None:
        self.user = user
        self.pw = pw
        self.host = host

    def get_token(self):
        if self.user and self.pw and self.host:
            auth = (self.user, self.pw)
            url = f"https://{self.host}/dna/system/api/v1/auth/token"
            response = requests.post(url, auth=auth, verify=False)
            
            if response.ok:
                self.token = response.json()["Token"]
            else:
                raise Exception(f"Issue while getting token: {response.text}")
        else:
            raise Exception("Username, password, and/or host missing")

    def get_device_list(self)->None:
        if self.token and self.host:
            url = f"https://{self.host}/dna/intent/api/v1/network-device"
            headers = {"x-auth-token":self.token}
            response = requests.get(url, headers=headers, verify=False)
            
            if response.ok:
                self.devices = response.json()["response"]
            else:
                raise Exception(f"Issue while retrieving devices: {response.text}")
        else:
            raise Exception("Token or host missing")
        

    def print_for_splunk(self):
        for device in self.devices:
            print(json.dumps(device))


if __name__ == "__main__":
    cc = CatalystCenter("admin", "C1sco12345", "198.18.129.100")
    cc.get_token()
    cc.get_device_list()
    cc.print_for_splunk()
