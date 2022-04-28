from mininet.topo import Topo
from mininet.link import TCLink
from functools import partial
from mininet.net import Mininet

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        recv1 = self.addHost( 'r1' )
        recv2 = self.addHost( 'r2' )
        recv3 = self.addHost( 'r3' )
        send1 = self.addHost( 's1' )
        send2 = self.addHost( 's2' )
        send3 = self.addHost( 's3' )
        leftSwitch = self.addSwitch( 'sw-1' )
        rightSwitch = self.addSwitch( 'sw-2' )

        # Add links
        self.addLink( recv1, leftSwitch, delay='0.5ms')
        self.addLink( recv2, leftSwitch, delay='2ms')
        self.addLink( recv3, leftSwitch, delay='3.5ms')
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, send1, delay='0.5ms')
        self.addLink( rightSwitch, send2, delay='2ms')
        self.addLink( rightSwitch, send3, delay='3.5ms')


def Test():
    topo = MyTopo()
    net = Mininet(topo = topo, link = partial(TCLink, delay='2ms', bw=400))
    net.start()
    s1, s2, s3, r1, r2, r3 = net.get('s1', 's2', 's3', 'r1', 'r2', 'r3')
    for i in range(5):
        s1.sendCmd("./app/pccserver recv 8000")
        s2.sendCmd("./app/pccserver recv 8000")
        s3.sendCmd("./app/pccserver recv 8000")
        r1.sendCmd("./app/pccclient send 10.0.0.4 8000 vivace 1")
        r2.sendCmd("./app/pccclient send 10.0.0.5 8000 vivace 2")
        r3.sendCmd("./app/pccclient send 10.0.0.6 8000 vivace 3")
        s1.waitOutput()
        s2.waitOutput()
        s3.waitOutput()
        r1.waitOutput()
        r2.waitOutput()
        r3.waitOutput()
    net.stop()

Test()
