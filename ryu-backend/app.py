from flask import Flask,jsonify,request
from dslmanager import transform_intent_to_dsl,reevaluate_dsl,load_rpg
from host_even_receiver import launch_ws_server
import threading
from db import get_db_connection
from dotenv import load_dotenv
import json
import re
import asyncio
import os 
app = Flask(__name__)

load_dotenv()

# 模擬讀取 intent.txt 和 epg.json 的路徑
INTENT_FILE = 'intent.txt'
RPG_FILE = os.getenv('RPG_FILE', 'rpg_case_1.json')


# 讀取 intent.txt
def read_intent_file():
    try:
        with open(INTENT_FILE, 'r') as file:
            intents = file.readlines()
        return [intent.strip() for intent in intents]  # 移除每行末尾的換行符
    except Exception as e:
        print(f"Error reading {INTENT_FILE}: {e}")
        return []

# 讀取 epg.json
def read_epg_json():
    try:
        with open(RPG_FILE, 'r') as file:
            epg_data = json.load(file)
        return epg_data
    except Exception as e:
        print(f"Error reading {RPG_FILE}: {e}")
        return []

# 讀取 label.json 檔案的函數
def load_labels(category):
    with open('label.json', 'r') as file:
        data = json.load(file)
    return data.get(category)

# 把資料插入到EPG之中
def insert_epg(ip , info):   
    # 🔽 寫入epg.json
    new_entry = {
        "ip": ip,
        "function": info.get("function", "Null"),
        "priority": info.get("priority", "Null"),
        "type": info.get("type", "Null"),
        "application": info.get("application", "Null"),
        "environment": info.get("environment", "Null")
    }
    try:
        with open(RPG_FILE, 'r') as file:
            epg_data = json.load(file)
    except FileNotFoundError:
        epg_data = []

    updated = False
    for entry in epg_data:
        if entry['ip'] == ip:
            entry.update(new_entry)
            updated = True
            break

    if not updated:
        epg_data.append(new_entry)

    with open(RPG_FILE, 'w') as file:
        json.dump(epg_data, file, indent=4)
    

# 取得特定標籤 ex : function,type,environment,application
@app.route('/datacenter/label/<category>', methods=['GET'])
def get_label(category):
    labels = load_labels(category)
    return jsonify(labels)
    
# 為 IP 去填上標籤，組成RPG
@app.route('/datacenter/submit_labels', methods=['POST'])
async def submit_labels():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # 提取 host 資料
    host_info = data.get("hostInfo", {})
    ipv4 = host_info.get('ipv4', 'N/A')[0]
    print(f"建立{ipv4} 的RPG")
    if ipv4 == 'N':
        return jsonify({"error": "No valid IP address provided"}), 400
    labels = data.get('labels', {})

    new_data = {
        "ip": ipv4,
        "function": labels.get("function", "Null"),
        "priority": labels.get("priority", "Null"),
        "type": labels.get("type", "Null"),
        "application": labels.get("application", "Null"),
        "environment" : labels.get("environment","Null"),
        "security" : labels.get("security","Null")
    }
    label_changed = False
    try:
        with open(RPG_FILE, 'r') as file:
            epg_data = json.load(file)
    except FileNotFoundError:
        # 如果檔案不存在，初始化為空列表
        epg_data = []
    ip_found = False
   
    diff_labels = {}
    index = 0
    
    for entry in epg_data:        
        if entry['ip'] == ipv4:            
            ip_found = True
            for key in new_data:
                old_val = entry.get(key)
                new_val = new_data[key]
                if old_val != new_val:
                    diff_labels[index] = {"before": old_val, "after": new_val}
                    index = index + 1
                    label_changed = True # 標籤有變更
                    break
            entry.update(new_data)  # 如果 IP 存在，更新該條目
            ip_found = True
            break
    if not ip_found:
        epg_data.append(new_data)
        label_changed = True # 標籤有變更
        
    # 將更新後的資料寫回 epg.json
    with open('epg_case_3.json', 'w') as file:        
        json.dump(epg_data, file, indent=4)
    
    # DSL 有改變，需重新評估
    if label_changed:
       print(f"🔁 {ipv4} Label has changed, triggering DSL reevaluation")
       print(f"🔁 {ipv4} diff_labels: {diff_labels}")
       await reevaluate_dsl(ipv4,diff_labels) 

    return jsonify({"status": "success", "message": "Labels received and processed."})

# 查詢特定RP中的RPG內容
@app.route('/datacenter/epg/<ip>', methods=['GET'])
def get_epg(ip):
    epg_values = load_rpg(ip)
    return jsonify(epg_values)

# 意圖增加
''' 
  { 
    "method" : "allow",
    "egress" : "Web",
    "egresstype" : "function",
    "port" : 3306,
    "protocol" : "TCP",
    "ingress" : "Database",
    "ingresstype" : "function"
   }
'''
@app.route('/datacenter/intent', methods=['POST'])
async def post_intent():
    data = request.get_json()
    
    method = data.get('method' , '')  # allow or deny
    egresstype = data.get('egresstype','') #value
    egress = data.get('egress','')  # function, type, environment, application .. etc 
    protocol = data.get('protocol','') # TCP、UDP、ICMP
    ingresstype = data.get('ingresstype','') #  value
    ingress = data.get('ingress','') #function, type, environment, application .. etc
    port = data.get('port','') # 3306,22,80..etc..  
    
    new_entry = f"{method} {egresstype}:{egress}, {protocol}:{port}, {ingresstype}:{ingress} \n"     
    print("插入的意圖為")
    print(new_entry)
    # 將意圖寫入 intent.txt
    with open('intent.txt', 'a') as intent_file:
        intent_file.write(new_entry)    

    await transform_intent_to_dsl(new_entry) # intent 轉換成DSL
    return "Intent deployed success.", 200

# 取得所有DSL，用於前端面板模擬
@app.route('/datacenter/dsl', methods=['GET'])
def get_all_dsl():
    function_labels = set()
    edges = []
    line_counter = 1
    with open('intent.txt', 'r') as intent_file:
        for line in intent_file:
            parts = line.strip().split(',')
            action_label = parts[0].strip().split(' ')
            action = action_label[0].lower()  # deny or allow
            source_label = action_label[1].strip().lower()
            
            protocol_port = parts[1].strip().lower()
            if ':' in protocol_port:
                protocol, port = protocol_port.split(':', 1)
            else:
                protocol, port = protocol_port, ''
            target_label = parts[2].strip().lower()
             # 收集節點
            function_labels.add(source_label)
            function_labels.add(target_label) 
            label = protocol.upper() +" " +  port
            edges.append({
                "id": f"e{line_counter}-2",
                "source": source_label,
                "target": target_label,
                "label": label,
                "action": action
            })
            line_counter += 1
    """
    with open('dsl.txt', 'r') as dsl_file:
        for line in dsl_file:          
            # 正則表達式：擷取 deny/allow, 協定類型, 端口號和標籤
            match = re.match(r"(deny|allow)\{([A-Za-z]+),\s*([\d\.]+(?:,\s*[\d\.]+)*)\s*\},\s*\{([^}]+)\}", line.strip())
            if match:   
                action = match.group(1)  # 'deny' 或 'allow'
                protocol = match.group(2)  # 協定類型，如 TCP, UDP, ICMP
                ip_addresses = match.group(3).split(',')  # 擷取所有 IP 地址
                
                labels_in_line = match.group(4).split(',')  # 擷取所有標籤
                # 去除多餘的括號和冒號，並取得標籤的值
                def extract_label(label):
                    # 使用正則去掉括號，並提取冒號後面的標籤名稱
                    match = re.match(r'\((\w+):([a-zA-Z0-9_]+)\)', label.strip())
                    if match:
                        return match.group(1).lower(), match.group(2).lower()  # 返回標籤值並轉為小寫
                    return label.strip().lower(), label.strip().lower()   # 如果沒有匹配，直接返回小寫標籤值
                source_label_type,source_label = extract_label(labels_in_line[1])               
                target_label_type,target_label = extract_label(labels_in_line[2])
                
                function_labels.add((source_label_type,source_label)) # 來源端 label 
                function_labels.add((target_label_type,target_label)) # 目的端label
                label = protocol + labels_in_line[0]
                                 
                edges.append({
                    "id": f"e{line_counter}-2",
                    "source": source_label,  # 使用 source_label 這裡直接使用標籤名
                    "target": target_label,  # 使用 target_label 這裡直接使用標籤名
                    "label": label,        
                    "action" : action
                })
                line_counter += 1
            

    node_data = []
    label_map = {} 
    seen = set()  # 用來記錄已經出現過的 (label_type, label_value, ip)
    for label_type, label_value in function_labels :
        key = (label_type, label_value)
        if key in seen:
            continue  # 如果重複就跳過，不要增加 idx
        seen.add(key)
        idx = len(node_data) + 1 # 動態根據目前有多少個 node_data 來編 idx
        node_data.append({
            "id": str(idx),
            "type": label_type,
            "label":label_value  # 按要求轉小寫
        })
        label_map[label_value] = str(idx)  # 建立標籤到 ID 的映射    
     # 使用標籤映射將 source 和 target 轉換為 ID
    for edge in edges:
        edge["source"] = label_map.get(edge["source"], edge["source"])  # 查找 source 標籤對應的 ID
        edge["target"] = label_map.get(edge["target"], edge["target"])  # 查找 target 標籤對應的 ID
        
    data = {
        "nodes" : node_data , 
        "edges" : edges
    }
    return  jsonify(data)
    """
    node_data = []
    label_map = {}
    seen = set()
    for label_value in function_labels:
        if label_value in seen:
            continue
        seen.add(label_value)
        idx = len(node_data) + 1
        # 自動判斷 type（根據冒號前的字）
        if ':' in label_value:
            label_type, label_real = label_value.split(':', 1)
        else:
            label_type, label_real = 'unknown', label_value

        node_data.append({
            "id": str(idx),
            "type": label_type,
            "label": label_real
        })
        label_map[label_value] = str(idx)

    # 把 source / target 轉成 ID
    for edge in edges:
        edge["source"] = label_map.get(edge["source"], edge["source"])
        edge["target"] = label_map.get(edge["target"], edge["target"])

    data = {
        "nodes": node_data,
        "edges": edges
    }
    return jsonify(data)
# 不確定有沒有用到 
# 神秘的URL
@app.route('/datacenter/dsl/ryu', methods=['GET'])
def get_dsl_ryu():
    result = []
    with open('dsl.txt', 'r') as dsl_file:
        lines = dsl_file.readlines()
    pattern = r"allow \{ (\w+), (\d+\.\d+\.\d+\.\d+), (\d+\.\d+\.\d+\.\d+) \}"
    for line in lines:
        # 使用正則表達式來提取需要的部分
        match = re.match(pattern, line.strip())
        if match:
            protocol = match.group(1)
            egress_ip = match.group(2)
            ingress_ip = match.group(3)
            
            # 建立 JSON 結構
            rule = {
                "allow": {
                    "protocol": protocol,
                    "egress_ip": egress_ip,
                    "ingress_ip": ingress_ip
                }
            }
            result.append(rule)
    return jsonify(result)
    
# ✅ 在 Flask 主程式之前就啟動 WebSocket Server（背景執行）
ws_thread = threading.Thread(target=launch_ws_server, daemon=True)
ws_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=False)
