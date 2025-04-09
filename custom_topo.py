from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

class CustomTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='192.168.173.101/24' , mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', ip='192.168.173.102/24' , mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', ip='192.168.173.103/24' , mac='00:00:00:00:00:03')
        self.addLink(h1, switch)
        self.addLink(h2, switch)
        self.addLink(h3, switch)

if __name__ == '__main__':
    topo = CustomTopo()
    net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633), link=TCLink)
    net.start()
    
    # 執行 websocket_server 程式（以背景程序方式）
    for host in [net.get('h1'), net.get('h2'), net.get('h3')]:
        host.cmd(f'python3 /home/sdntest/ryu/gateway/websocket_server.py > /tmp/{host}_server.log 2>&1 &')
        print(f"Started websocket_server on {host.name}")
    CLI(net)
    net.stop()
