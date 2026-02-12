#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for retrieving Catalyst Center interface status data, and 
printing it out in a Splunk friendly JSON format. This script could then be
added to Splunk as a scripted input.

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
    devices:list = [
        {
            "hostname": "c9000v-helsinki.dcloud.cisco.com",
            "id": "d63be853-b630-4b49-bfa8-8630683f7b51"
        },
        {
            "hostname": "c9000v-paris.dcloud.cisco.com",
            "id": "dba6fc50-c64b-4459-8c1e-00014eb2ef27"
        }
    ]

    user:str = None
    pw:str = None
    host:str = None
    token:str = None
    interfaces:list = None

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

    def get_interfaces(self)->None:
        if self.token and self.host:
            url = f"https://{self.host}/dna/intent/api/v1/interface"
            headers = {"x-auth-token":self.token}
            response = requests.get(url, headers=headers, verify=False)
            
            if response.ok:
                self.interfaces = response.json()["response"]
            else:
                raise Exception(f"Issue while retrieving interfaces: {response.text}")
        else:
            raise Exception("Token or host missing")
        

    def print_for_splunk(self)->None:
        if not self.interfaces:
            raise Exception("You need to first retrieve interface data")

        for device in self.devices:
            hostname = device["hostname"]
            device_id = device["id"]

            device_interfaces = [
                {
                    "portName":interface["portName"],
                    "portMode": interface["portMode"],
                    "description": interface["description"],
                    "status":interface["status"],
                    "adminStatus":interface["adminStatus"],
                    "addresses":interface["addresses"]
                }
                for interface in self.interfaces
                if interface["deviceId"] == device_id
            ]
            data = {"device_id": device_id,
                    "hostname": hostname,
                    "interfaces": device_interfaces}

            print(json.dumps(data))


if __name__ == "__main__":
    cc = CatalystCenter("admin", "C1sco12345", "198.18.129.100")
    cc.get_token()
    cc.get_interfaces()
    cc.print_for_splunk()
