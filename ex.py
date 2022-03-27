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
        self.addLink( recv1, leftSwitch )
        self.addLink( recv2, leftSwitch )
        self.addLink( recv3, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, send1 )
        self.addLink( rightSwitch, send2 )
        self.addLink( rightSwitch, send3 )


def Test():
    topo = MyTopo()
    net = Mininet(topo = topo, link = partial(TCLink, delay='0.5ms', bw=400))
    net.start()
    s1, s2, s3, r1, r2, r3 = net.get('s1', 's2', 's3', 'r1', 'r2', 'r3')
    for i in range(10):
        s1.sendCmd("./stream_ser 10.0.0.4 800" + str(i) + " illinois")
        s2.sendCmd("./stream_ser 10.0.0.5 800" + str(i) + " illinois")
        s3.sendCmd("./stream_ser 10.0.0.6 800" + str(i) + " illinois")
        r1.sendCmd("./stream_cli 10.0.0.4 800" + str(i) + " illinois ex r1")
        r2.sendCmd("./stream_cli 10.0.0.5 800" + str(i) + " illinois ex r2")
        r3.sendCmd("./stream_cli 10.0.0.6 800" + str(i) + " illinois ex r3")
        s1.waitOutput()
        s2.waitOutput()
        s3.waitOutput()
        r1.waitOutput()
        r2.waitOutput()
        r3.waitOutput()
    net.stop()

if __name__ == "__main__":
    Test()

