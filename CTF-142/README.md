# Integrate Catalyst Center Data into Splunk with Scripted Inputs!

This repository includes the supplemental material for the Cisco Live Amsterdam 2025 minitheater session: CTF-142. Here you can find the code for the demo that was delivered during the session.

## Preparing to run the code

1. Install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

1. Update your Catalyst Center credentials into the `minitheater_demo.py`

    ```python lines="36-39"
    # UPDATE YOUR CATALYST CENTER DETAILS
    CC_ADDRESS = "198.18.129.100"
    CC_USERNAME = "admin"
    CC_PASSWORD = "C1sco12345"
    ```

1. Update your device's information into the `minitheater_demo.py`. Device ID can be retrieved with a simple GET `/network-device` API call.

    ```python
    # UPDATE YOUR DEVICE'S INFORMATION
    # You can retrieve your device's ID with the Catalyst Center
    # api call for GET Device list: /network-device

    DEVICE = {
        "hostname": "c9000v-helsinki.dcloud.cisco.com",
        "id": "d63be853-b630-4b49-bfa8-8630683f7b51",
    }

    ```

## Run the code

Run the code to print out the status of different interfaces on your device.

```bash
$ python minitheater_demo.py 
{"portName": "GigabitEthernet0/0", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/1", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/2", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/3", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/4", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/5", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/6", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/7", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "GigabitEthernet1/0/8", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "SR0", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
{"portName": "Vlan1", "status": "up", "adminStatus": "UP", "device": "c9000v-helsinki.dcloud.cisco.com"}
```

## Author
Juulia Santala (jusantal@cisco.com)