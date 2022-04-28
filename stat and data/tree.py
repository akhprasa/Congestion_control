from mininet.topo import Topo
import logging
import os
from mininet.net import Mininet
from mininet.link import TCLink
from functools import partial
from mininet.log import setLogLevel, info


class Tree(Topo):

    def build( self):

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')

        self.addLink(s1, s2)
        self.addLink(s1, s3)

        self.addLink(s2, s4)
        self.addLink(s2, s5)

        self.addLink(s3, s6)
        self.addLink(s3, s7)

        self.addLink(h1, s4)
        self.addLink(h2, s4)
        self.addLink(h3, s5)
        self.addLink(h4, s5)
        self.addLink(h5, s6)
        self.addLink(h6, s6)
        self.addLink(h7, s7)
        self.addLink(h8, s7)


def test():
    topo = Tree()
    net = Mininet(topo=topo, link=partial(TCLink, delay='2ms', bw=1000))
    net.start()
    s1, s2, s3, r1, r2, r3 = net.get('h1', 'h3', 'h5', 'h2', 'h4', 'h6')
    for i in range(5):
        print('started')
        s1.sendCmd("./app/pccserver recv 8000")
        s2.sendCmd("./app/pccserver recv 8000")
        s3.sendCmd("./app/pccserver recv 8000")
        r1.sendCmd("./app/pccclient send 10.0.0.1 8000 vivace 1")
        r2.sendCmd("./app/pccclient send 10.0.0.3 8000 vivace 2")
        r3.sendCmd("./app/pccclient send 10.0.0.5 8000 vivace 3")
        r1.waitOutput()
        r2.waitOutput()
        r3.waitOutput()
        print('cl done')
        s1.waitOutput()
        s2.waitOutput()
        s3.waitOutput()
        print('sr done')
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    test()

