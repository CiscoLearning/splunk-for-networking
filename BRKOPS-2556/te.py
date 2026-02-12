#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for creating a simple ThousandEyes instant test,
retrieving the results, and printing them out in a Splunk friendly JSON
format. This script could then be added to Splunk as a scripted input.

Before making this into a Splunk scripted input, remove the extra print statements.
Now they are left in for transparency purposes when running the script locally.

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
import time
import json
import requests

class ThousandEyes():

    base_url = "https://api.thousandeyes.com/v7"
    headers = {"Content-Type": "application/json"}

    test_id_list = []
    test_results = []

    def __init__(self, token:str)->None:
        self.headers["Authorization"] = f"Bearer {token}"

    def create_instant_test(self, agents:list, urls_to_test:list)->None:
        api_endpoint = f"{self.base_url}/tests/http-server/instant"

        for url in urls_to_test:
            print(f"Creating ThousandEyes instant test for: {url}")

            payload = {
                "agents": [{"agentId": agent} for agent in agents],
                "url": url
            }

            response = requests.post(api_endpoint, headers=self.headers, json=payload, timeout=30)
            if response.ok:
                test_id = response.json()["testId"]
                self.test_id_list.append((test_id, agents))
            else:
                print(f"Issue while creating test for {url}: {response.text}")

    def retrieve_test_metrics(self)->None:
        for test_id, agents in self.test_id_list:
            for i in range(9):
                url = f"{self.base_url}/test-results/{test_id}/network"
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.ok:
                    data = response.json()
                    if data["results"]:
                        if len(data["results"]) == len(agents):
                            self.test_results.append({
                                    "url":data['test']['url'],
                                    "results":data['results']
                                })
                            break
                        else:
                            print(f"{i}. Results partially available, waiting for the rest.")
                            time.sleep(10)
                    else:
                        print(f"{i}. Results are not yet available.")
                        time.sleep(10)
                else:
                   raise Exception(f"Issue while retrieving test results: {response.text}")
            else:
                self.test_results.append({"error": f"Couldn't retrieve metrics for {test_id} after 10 attempts"})
        
    def print_for_splunk(self)->None:
        print(json.dumps(self.test_results))


if __name__ == "__main__":

    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        urls = ["google.com","https://cisco.com", "123"]

    token = "<YOUR TOKEN>"
    agents = [
        "10", #Paris
        "4739", #Helsinki
    ]

    my_te = ThousandEyes(token=token)
    my_te.create_instant_test(agents=agents, urls_to_test=urls)
    my_te.retrieve_test_metrics()
    my_te.print_for_splunk()
