import asyncio
import websockets
import json
import iptc
import subprocess

# 啟動時自動插入 iptables NFQUEUE 規則
def setup_nfqueue_rule():
    try:
        rule_check = subprocess.run(
            ["sudo", "iptables", "-C", "INPUT", "-p", "tcp", "--syn", "-j", "NFQUEUE", "--queue-num", "1"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        if rule_check.returncode != 0:
            print("[*] 插入 NFQUEUE 規則...")
            subprocess.run(
                ["sudo", "iptables", "-I", "INPUT", "-p", "tcp", "--syn", "-j", "NFQUEUE", "--queue-num", "1"],
                check=True
            )
            print("[+] NFQUEUE 規則已插入")
        else:
            print("[=] NFQUEUE 規則已存在，略過")
    except Exception as e:
        print(f"[!] 無法設定 NFQUEUE 規則：{e}")

# 處理接收到的 WebSocket 訊息
async def handle_message(websocket):
    async for message in websocket:
        try:
            # 解碼JSON訊息
            data = json.loads(message)
            
            if 'egress_ip' in data[0] and 'method' in data[0]:
                rule = {
                    'protocol': data[0]["protocol"],
                    'src' : data[0]['egress_ip'].split(",")[0],
                    'target' : 'ACCEPT' if data[0]["method"].lower() == "allow" else 'REJECT',
                }

                if data[0]["protocol"].lower() == "tcp":
                    rule['tcp'] = {'dport': str(data[0]["port"])}
                elif data[0]["protocol"].lower() == "udp":
                    rule['udp'] = {'dport': str(data[0]["port"])}

                print(f"Received message: {rule}")
                iptc.easy.insert_rule('filter', 'INPUT', rule)
                print(f"Rule to block traffic from {data[0]['egress_ip']} added successfully!")

                response_data = {"response": f"Policy deployed {data[0]['egress_ip']} successfully!"}
            else:
                response_data = {"response": "Invalid data format. Missing 'egreess ip ' or 'method'."}

            await websocket.send(json.dumps(response_data))

        except json.JSONDecodeError:
            print("Invalid JSON format")

# 啟動 WebSocket 伺服器
async def main():
    setup_nfqueue_rule()
    async with websockets.serve(handle_message, "0.0.0.0", 8766):
        print('start server: 0.0.0.0:8766')
        await asyncio.Future()

asyncio.run(main())
