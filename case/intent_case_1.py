# =======================================================================
# 情境1.  開發新的ERP模組，開發測試環境通過驗證，今天開始遷移上部屬正式提供服務
# =======================================================================

import requests
import json

url = "http://sdn.yuntech.poc.com/datacenter/intent"

RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'


# Deny 策略
# 1. Environment: Testing ===TCP 3306 ===> Environment : Production
data = {
    "method" : "deny",
    "egresstype" : "environment",
    "egress" : "Testing",
    "protocol": "TCP",
    "port": 3306,
    "ingresstype" : "environment",
    "ingress" : "Production"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {RED}Deny{RESET} Environment: Testing ===TCP 3306===> Environment : Production ✅")
else :
    print(f" {RED}Deny{RESET} Environment: Testing ===TCP 3306===> Environment : Production ❌")

# Testing 環境設置
# 1. Environment: Testing ===ICMP===> Type : Order
data = {
    "method" : "allow",
    "egresstype" : "environment",
    "egress" : "Testing",
    "protocol": "ICMP",
    "ingresstype" : "type",
    "ingress" : "Order"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} Environment: Testing ===ICMP===> Type : Order ✅")
else :
    print(f" {GREEN}Allow{RESET} Environment: Testing ===ICMP===> Type : Order ❌")
    
# 2. Environment: Testing ===ICMP===> Type : Payment
data = {
    "method" : "allow",
    "egresstype" : "environment",
    "egress" : "Testing",
    "protocol": "ICMP",
    "ingresstype" : "type",
    "ingress" : "Payment"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} Environment: Testing ===ICMP===> Type : Payment ✅")
else :
    print(f" {GREEN}Allow{RESET} Environment: Testing ===ICMP===> Type : Payment ❌")
    
# 3. Type: Order ===TCP 3306===> Function : Database 
data = {
    "method" : "allow",
    "egresstype" : "type",
    "egress" : "Order",
    "protocol": "TCP",
    "port": 3306,
    "ingresstype" : "function",
    "ingress" : "Database"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} Type: Order ===TCP 3306===> Function : Database ✅")
else :
    print(f" {GREEN}Allow{RESET} Type: Order ===TCP 3306===> Function : Database ❌")
    

# Production 環境設置
# 1. Environment: Production ===ICMP===> Type : Shipping
data = {
    "method" : "allow",
    "egresstype" : "environment",
    "egress" : "Production",
    "protocol": "ICMP",
    "ingresstype" : "type",
    "ingress" : "Shipping"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} Environment: Production ===ICMP===> Type : Shipping ✅")
else :
    print(f" {GREEN}Allow{RESET} Environment: Production ===ICMP===> Type : Shipping ❌")
# 2. Environment: Production ===ICMP===> function : Web
data = {
    "method" : "allow",
    "egresstype" : "environment",
    "egress" : "Production",
    "protocol": "ICMP",
    "ingresstype" : "function",
    "ingress" : "Web"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} Environment: Production ===ICMP===> function : Web ✅")
else :
    print(f" {GREEN}Allow{RESET} Environment: Production ===ICMP===> function : Web ❌")
# 3. function: Web ===TCP 3306===> Function : Database
data = {
    "method" : "allow",
    "egresstype" : "function",
    "egress" : "Web",
    "protocol": "TCP",
    "port": 3306,
    "ingresstype" : "function",
    "ingress" : "Database"
}
response = requests.post(url, json=data)
if response.status_code == 200:
    print(f" {GREEN}Allow{RESET} function: Web ===TCP 3306===> Function : Database ✅")
else :
    print(f" {GREEN}Allow{RESET} function: Web ===TCP 3306===> Function : Database ❌")