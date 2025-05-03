import asyncio
import websockets
import json
import socket
import os 
import signal
import time 
# ================= WebSocket Server 接收主機事件 =================

# 讀取DSL
def load_dsl_rules(file_path="dsl.txt"):
    rules = []
    with open(file_path, "r") as f:
        for line in f:
            if not line.strip().startswith("allow"):
                continue
            try:
                # 解析語法：allow{TCP, A, B},{ 3306, (security:xxx),(type:xxx) }
                part1, part2 = line.strip().split("},{")
                proto, src, dst = part1.replace("allow{", "").split(",")
                port = part2.split(",")[0].strip()
                port = int(port) if port else None
                rules.append({
                    "protocol": proto.strip(),
                    "src_ip": src.strip(),
                    "dst_ip": dst.strip().rstrip(" }"),
                    "port": port
                })
            except Exception as e:
                print(f"[!] DSL 解析錯誤：{e}")
    return rules

# 檢查event 是否allow
def is_event_allowed(event, rules):
    if event["dst_port"] in [8765, 8766]:
        return True
    for rule in rules:
        if (
            rule["protocol"].upper() == event["protocol"].upper()
            and rule["src_ip"] == event["src_ip"]
            and rule["dst_ip"] == event["dst_ip"]
            and (rule["port"] is None or rule["port"] == event["dst_port"])
        ):
            return True
    return False

# 寫入到 log.txt
def log_event_to_file(event):
    print(event)
    with open("log.txt", "a") as f:
        f.write(json.dumps(event) + "\n")



# 🔍 檢查某個 TCP port 是否正在被使用
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# 🧼 嘗試釋放 port（僅限 Linux，利用 lsof + kill）
def free_port(port):
    print(f"[⚠️] Port {port} 已被佔用，嘗試釋放中...")
    try:
        # 取得佔用該 port 的 PID
        output = os.popen(f"lsof -i :{port} -sTCP:LISTEN -t").read()
        if output:
            pids = output.strip().split("\n")
            for pid in pids:
                os.kill(int(pid), signal.SIGTERM)
                print(f"[✔] 已終止 PID {pid} 使用的 port {port}")
        else:
            print(f"[❌] 找不到佔用 {port} 的進程")
    except Exception as e:
        print(f"[❌] 釋放 port 失敗：{e}")

async def handle_event(websocket):
    rules = load_dsl_rules()  # 每次連線前載入最新 dsl.txt
    
    async for message in websocket:
        try:
            event = json.loads(message)
            print(f"[✅] 收到來自主機的事件：{event}")

            # TODO: 你可以在這裡加入 intent 白名單檢查邏輯
            allowed = is_event_allowed(event, rules)
            if allowed:
                response = {"status": "received", "intent_check": "allowed"}
                print(f"[✅] 收到來自主機的事件，符合 DSL 規則：{event}")
            else:
                response = {
                    "status": "received",
                    "intent_check": "⚠ not allowed",
                    "action": "block_suggested",
                    "reason": "Intent not defined in DSL"
                }
                print(f"[❌] 收到來自主機的事件，但不在 DSL 規則中，建議阻擋：{event}")
                log_event_to_file(event)  # ✅ 寫入 log.txt
            await websocket.send(json.dumps(response))
        except websockets.exceptions.ConnectionClosedOK as e:
            print(f"[ℹ️] 主機連線已正常關閉：{e}")
        except Exception as e:
            print(f"[❌] WebSocket 錯誤：{e}")

async def start_websocket_server():
    print("[*] 啟動 WebSocket Server 監聽 0.0.0.0:8765")
    async with websockets.serve(handle_event, "0.0.0.0", 8765):
        await asyncio.Future()

def launch_ws_server():
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        if is_port_in_use(8765):
            free_port(8765)
            time.sleep(1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_server())
    
# =============================================================