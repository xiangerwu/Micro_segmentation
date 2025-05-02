# =======================================================================
# 情境2.  偵測到該服務模組有 CVE 資安漏洞，暫時下線封鎖
# =======================================================================

import requests
import json

url = "http://sdn.yuntech.poc.com/datacenter/submit_labels"

RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'


# 策略改變
# 1. 將 101 Security:normal 改成 Security:vulnerable
data = {
    "hostInfo" : {
        "ipv4" : ["192.168.173.101",]
    },
    "labels" : {
        "function" : "Web",
        "priority" : "Null",
        "type": "Null",
        "application": "Null",
        "environment" : "Null",
        "security" : "vulnerable"
    }    
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {YELLOW}CHANGE{RESET} h1 security:normal => vulnerable ✅")
else :
    print(f" {YELLOW}CHANGE{RESET} h1 security:normal => vulnerable ❌")
    
user_input = input(f"{YELLOW} 進行下一步隔離嗎? (Y)：{RESET}")
if user_input.strip().upper() == "Y":

    # 2. 將 101 Security:vulnerable 改成 Security:quarantined
    data = {
        "hostInfo" : {
            "ipv4" : ["192.168.173.101",]
        },
        "labels" : {
            "function" : "Web",
            "priority" : "Null",
            "type": "Null",
            "application": "Null",
            "environment" : "Null",
            "security" : "quarantined"
        }    
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f" {YELLOW}CHANGE{RESET} h1 security:vulnerable => quarantined ✅")
    else :
        print(f" {YELLOW}CHANGE{RESET} h1 security:vulnerable => quarantined ❌")

    