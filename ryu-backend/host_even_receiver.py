import asyncio
import websockets
import json
import socket
import os 
import signal
import time 
# ================= WebSocket Server 接收主機事件 =================
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
    async for message in websocket:
        try:
            event = json.loads(message)
            print(f"[✅] 收到來自主機的事件：{event}")

            # TODO: 你可以在這裡加入 intent 白名單檢查邏輯
            log_event_to_file(event)  # ✅ 寫入 log.txt
            response = {"status": "received", "intent_check": "todo"}
            await websocket.send(json.dumps(response))
        except Exception as e:
            print(f"[❌] 接收錯誤：{e}")

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