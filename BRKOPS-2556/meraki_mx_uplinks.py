#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for retrieving Meraki MX uplink status data, and 
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

import requests

requests.urllib3.disable_warnings()

class Meraki():
    base_url:str = "https://api.meraki.com/api/v1"
    header:dict = {"Authorization": None}
    org_id:str = None

    def __init__(self, token:str, org_id:str)->None:
        self.header["Authorization"] = f"Bearer {token}"
        self.org = org_id

    def org_appliance_uplink_status(self)->None:
            url = f"{self.base_url}/organizations/{self.org}/appliance/uplink/statuses"
            response = requests.get(url, headers=self.header)
        
            if not response.ok:
                raise Exception(f"Issue while getting uplinks: {response.text}")
            
            print(response.text)

if __name__ == "__main__":

    token = "<YOUR TOKEN>"
    org = "<YOUR MERAKI ORG>"

    my_meraki = Meraki(token=token, org_id=org)
    my_meraki.org_appliance_uplink_status()
