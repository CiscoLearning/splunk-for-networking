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

# UPDATE YOUR CATALYST CENTER DETAILS
CC_ADDRESS = "198.18.129.100"
CC_USERNAME = "admin"
CC_PASSWORD = "C1sco12345"

# UPDATE YOUR DEVICE'S INFORMATION
# You can retrieve your device's ID with the Catalyst Center
# api call for GET Device list: /network-device

DEVICE = {
    "hostname": "c9000v-helsinki.dcloud.cisco.com",
    "id": "d63be853-b630-4b49-bfa8-8630683f7b51",
}

def get_token(address, username, password):
    """
    Function to retrieve Catalyst Center token, that can then
    be used to authorize any subsequent API calls.
    """

    auth = (username, password)
    url = f"https://{address}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=auth, verify=False)
            
    if response.ok:
        token = response.json()["Token"]
        return token
    else:
        raise Exception(f"Issue while getting token: {response.text}")

def get_interfaces(address, token, device_id):
    """
    Function to retrieve the interfaces of a specified device managed by
    Catalyst Center. The device is identified by the ID.
    """
    url = f"https://{address}/dna/intent/api/v1/interface/network-device/{device_id}"
    headers = {"x-auth-token":token}
    response = requests.get(url, headers=headers, verify=False)

    if response.ok:
        interfaces = response.json()["response"]
        return interfaces
    else:
        raise Exception(f"Issue while retrieving interfaces: {response.text}")

def print_for_splunk(hostname, interfaces):
    """
    To get the best use of Splunk, print the data in a format that is
    most useful to your use case. In this example, the port status
    is printed out in JSON format, which is easy for us to search 
    in Splunk.
    """
    for interface in interfaces:
        data = {
            "portName":interface["portName"],
            "status":interface["status"],
            "adminStatus":interface["adminStatus"],
            "device": hostname
        }

        print(json.dumps(data))

# This is the entry point to the script - all the three
# functions are called one by one.
if __name__ == "__main__":
    token = get_token(CC_ADDRESS, CC_USERNAME, CC_PASSWORD)
    interfaces = get_interfaces(CC_ADDRESS, token, DEVICE["id"])
    print_for_splunk(DEVICE["hostname"], interfaces)
