# 專案說明
專案的目標是POC零信任微分段結構，專案分成了ryu-dashboard(前端)、ryu-backend(後端)、ryu-project(Ryu SDN端)、gateway(各host端)
具體架構如下：
![alt text](image-1.png)

ryu-dashboard + ryu-backend = SDC(分段決策中心)
ryu-project (SDN Controller)

專案中還有一個custom_topo.py，會自動建立Mininet 連線以及其他初始設定

# branch 說明
本專案有兩個bracnh，一個有DB一個純粹使用json儲存資訊
主要是前者維護
* nginx 反向代理 :
[sdn](http://sdn.yuntech.poc.com/)

## NGINX  
使用nginx-proxy manager

做前後端反向代理之用途
```
  docker compose build
  docker compose up -d 
```
http://localhost:81 可以看到預設介面

![alt text](image.png)


Python 環境 : conda test_env

先執行ryu-project 專案，這樣SDN Controller 就會成功執行
```
 ryu-manager app.py
```
接著啟動ryu-backend，此為DataCenter的後端
```
  python app.py
```

最後啟動前端介面 ryu-dashboard
```
  npm start
```

執行mininet 腳本，這腳本會建立Mininet 連線並且設定好一些前置作業
```
  python custom_topo.py
```


## POST 測試

### 測試SDN 的policy

* ICMP

    epg.json
    ```json
        {
            "IP": "192.168.173.101",
            "function": "Service",
            "Priority": "User",
            "Type": "Shipping",
            "Security": "Normal"
        },
        {
            "IP": "192.168.173.103",
            "function": "Database",
            "Priority": "User",
            "Type": "Shipping",
            "Security": "Normal"
        }
    ```
  
  ```
   POST http://sdn.yuntech.poc.com/datacenter/intent
   {
        "method" : "deny",
        "egress" : "Service",
        "egresstype" : "function",
        "port" : "",
        "protocol" : "ICMP",
        "ingress" : "Database",
        "ingresstype" : "function"
    }
  ```


### 測試 iptables 的 policy 
