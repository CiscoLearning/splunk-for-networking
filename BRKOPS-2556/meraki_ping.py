#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for initiating a Meraki Ping job, and subscribing to
receive the response through Meraki's callback functionality.

This script collects input through arguments submitted when running the script.

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

import sys
import requests

requests.urllib3.disable_warnings()

class Meraki():
    device_serials:list = None
    base_url:str = "https://api.meraki.com/api/v1"

    header:dict = {"Authorization": None}
    payload: dict = {"target": None}

    def __init__(self, token:str, device_serials:list, target_ip:str, callback:str)->None:
        self.header["Authorization"] = f"Bearer {token}"
        self.device_serials = device_serials
        self.payload["target"] = target_ip
        self.payload["callback"] = {
            "url": callback,
            "sharedSecret": "secret"
        }

    def initiate_ping(self):
        for serial in self.device_serials:
            url = f"{self.base_url}/devices/{serial}/liveTools/ping"
            response = requests.post(url, headers=self.header, json=self.payload)
        
            if not response.ok:
                raise Exception(f"Issue while initiating ping: {response.text}")

if __name__ == "__main__":

    try:
        target_ip = sys.argv[1]
        callback = sys.argv[2]
        token = sys.argv[3]
        device_serials = sys.argv[4:]

    except:
        raise Exception(f"Missing one or more arguments!")

    my_meraki = Meraki(token=token,
                        device_serials=device_serials,
                        target_ip=target_ip,
                        callback=callback)

    my_meraki.initiate_ping()
