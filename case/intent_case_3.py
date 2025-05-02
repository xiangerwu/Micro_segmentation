# =======================================================================
# 情境3.  脫離業務意圖（Intent-based Violation）偵測
# =======================================================================

import requests
import json



RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
url = "http://sdn.yuntech.poc.com/datacenter/submit_labels"
# 初始化 RPG ==>  初始化
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
        "security" : "normal"
    }    
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {YELLOW}初始化{RESET} h1 初始化 (type:Order,security:normal) ✅")
else :
    print(f" {YELLOW}初始化{RESET} h1 初始化 (type:Order,security:normal)❌")

data = {
    "hostInfo" : {
        "ipv4" : ["192.168.173.102",]
    },
    "labels" : {
        "function" : "Null",
        "priority" : "Null",
        "type": "Order",
        "application": "Null",
        "environment" : "Null",
        "security" : "normal"
    }    
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {YELLOW}初始化{RESET} h2 初始化 (type:Order,security:normal) ✅")
else :
    print(f" {YELLOW}初始化{RESET} h2 初始化 (type:Order,security:normal) ❌")


url = "http://sdn.yuntech.poc.com/datacenter/intent"

# Allow 的設置
data = {
    "method" : "allow",
    "egresstype" : "security",
    "egress" : "normal",
    "protocol": "TCP",
    "port" : "22",
    "ingresstype" : "type",
    "ingress" : "Order"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} security: normal  ===TCP 22 ===> type : Order ✅")
else :
    print(f" {GREEN}Allow{RESET} security: normal ===TCP 22===> type : Order ❌")
    
    # Allow 的設置
data = {
    "method" : "allow",
    "egresstype" : "security",
    "egress" : "normal",
    "protocol": "ICMP",
    "ingresstype" : "type",
    "ingress" : "Order"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} security: normal  === ICMP ===> type : Order ✅")
else :
    print(f" {GREEN}Allow{RESET} security: normal === ICMP ===> type : Order ❌")
    
