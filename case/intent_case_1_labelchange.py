# =======================================================================
# 情境1.  開發新的ERP模組，開發測試環境通過驗證，今天開始遷移上部屬正式提供服務
# =======================================================================

import requests
import json

url = "http://sdn.yuntech.poc.com/datacenter/submit_labels"

RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'


# 策略改變
# 1. 將 101 的Testing 改成 Production
data = {
    "hostInfo" : {
        "ipv4" : ["192.168.173.101",]
    },
    "labels" : {
        "function" : "Null",
        "priority" : "Null",
        "type": "Order",
        "application": "Null",
        "environment" : "Testing"
    }    
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {YELLOW}CHANGE{RESET} h1 environment:Testing => Production ✅")
else :
    print(f" {YELLOW}CHANGE{RESET} h1 environment:Testing => Production ❌")


    