from mininet.topo import Topo
from mininet.link import TCLink
from functools import partial
from mininet.net import Mininet
from mininet.log import setLogLevel, info

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
        self.addLink( recv1, leftSwitch, bw=800, delay='0.5ms')
        self.addLink( recv2, leftSwitch, bw=800, delay='0.5ms')
        self.addLink( recv3, leftSwitch, bw=800, delay='0.5ms')
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, send1, bw=800, delay='0.5ms')
        self.addLink( rightSwitch, send2, bw=800, delay='0.5ms')
        self.addLink( rightSwitch, send3, bw=800, delay='0.5ms')


def Test():
    topo = MyTopo()
    net = Mininet(topo = topo, link = partial(TCLink))
    net.start()
    s1, s2, s3, r1, r2, r3 = net.get('s1', 's2', 's3', 'r1', 'r2', 'r3')
    for i in range(4):
        print('exp started')
        s1.sendCmd("./stream_ser 10.0.0.4 8000 reno")
        s2.sendCmd("./stream_ser 10.0.0.5 8000 reno")
        s3.sendCmd("./stream_ser 10.0.0.6 8000 reno")
        r1.sendCmd("./stream_cli 10.0.0.4 8000 reno ex r1 log_files")
        r2.sendCmd("./stream_cli 10.0.0.5 8000 reno ex r2 log_files")
        r3.sendCmd("./stream_cli 10.0.0.6 8000 reno ex r3 log_files")
        r1.waitOutput()
        r2.waitOutput()
        r3.waitOutput()
        print('cl done')
        s1.waitOutput()
        s2.waitOutput()
        s3.waitOutput()
    net.stop()

Test()
