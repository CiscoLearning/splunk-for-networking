#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for initiating a Meraki Ping job, and subscribing to
receive the response through Meraki's callback functionality.

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

import requests

requests.urllib3.disable_warnings()

BASE_URL = "https://api.meraki.com/api/v1"
TOKEN = "<YOUR TOKEN>"

def initiate_ping(token, serial, target_ip):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "target": target_ip,
        "callback": {
            "url": "<YOUR URL>",
            "sharedSecret": "secret"
        }
    }
    
    url = f"{BASE_URL}/devices/{serial}/liveTools/ping"
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":

    device_serials = ["Q2EW-NGY4-9YZP", "Q2EW-NHQT-2DM6"]

    for serial in device_serials:
        initiate_ping(TOKEN, serial, "8.8.8.8")
