from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.term import makeTerm  # 放在 import 區
import os
import time

class CustomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        # Host 設定
        h1 = self.addHost('h1', ip='192.168.173.101/24', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='192.168.173.102/24', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='192.168.173.103/24', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', ip='192.168.173.104/24', mac='00:00:00:00:00:04')

        # 不指定 port，Mininet 自行建立，後面我們會手動替換
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)

def fix_ofport(switch_name, iface_name, port_number):
    os.system(f"sudo ovs-vsctl set Interface {iface_name} ofport_request={port_number}")

if __name__ == '__main__':
    topo = CustomTopo()
    net = Mininet(topo=topo,
                  controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633),
                  switch=OVSSwitch,
                  link=TCLink,
                  autoSetMacs=True)


    net.start()

    # 等待 interface 建立完成
    time.sleep(1)

    # 固定指定 port
    fix_ofport('s1', 's1-eth1', 2)  # h1
    fix_ofport('s1', 's1-eth2', 3)  # h2
    fix_ofport('s1', 's1-eth3', 4)  # h3
    fix_ofport('s1', 's1-eth4', 5)  # h4

    print("\n✅ 已固定 Port 編號如下：")
    print("00:00:00:00:00:01 → port 2")
    print("00:00:00:00:00:02 → port 3")
    print("00:00:00:00:00:03 → port 4")
    print("00:00:00:00:00:04 → port 5")

    # 執行 websocket_server
    for host in [net.get('h1'), net.get('h2'), net.get('h3'),net.get('h4')]:
        host.cmd(f'python3 /home/sdntest/ryu/gateway/websocket_server.py > /tmp/{host}_server.log 2>&1 &')
        print(f"Started websocket_server on {host.name}")

    # h2 跟 h4 開啟3306連接
    #net.get('h2').cmd('nc -l -p 3306 > /tmp/h2_3306.log 2>&1 &')
    #net.get('h4').cmd('nc -l -p 3306 > /tmp/h4_3306.log 2>&1 &')
    #print("✅ h2、h4 已開啟模擬 3306 port 的 TCP 監聽服務")
    
    # ✅ 開啟 XTerm 終端視窗
    makeTerm(net.get('h1'), cmd="bash")
    makeTerm(net.get('h2'), cmd="bash")
    makeTerm(net.get('h3'), cmd="bash")
    makeTerm(net.get('h4'), cmd="bash")
    
    CLI(net)
    net.stop()