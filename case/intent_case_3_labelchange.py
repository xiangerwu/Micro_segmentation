# =======================================================================
# 情境3.  脫離業務意圖（Intent-based Violation）偵測
# =======================================================================

import requests
import json

url = "http://sdn.yuntech.poc.com/datacenter/submit_labels"

RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'


# 策略改變
# 1. 將 101 的 normal  改成 quarantined
data = {
    "hostInfo" : {
        "ipv4" : ["192.168.173.101",]
    },
    "labels" : {
        "function" : "Null",
        "priority" : "Null",
        "type": "Order",
        "application": "Null",
        "environment" : "Null",
        "security" : "quarantined"
    }    
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {YELLOW}CHANGE{RESET} h1 security:normal => quarantined ✅")
else :
    print(f" {YELLOW}CHANGE{RESET} h1 security:normal => quarantined ❌")


    