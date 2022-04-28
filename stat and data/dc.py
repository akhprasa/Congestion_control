#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from mininet.link import TCLink
from functools import partial
from subprocess import call
from mininet.topo import Topo


class MTP(Topo):

    def build( self):
        s7 = self.addSwitch('s7')
        s1 = self.addSwitch('s1')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s2 = self.addSwitch('s2')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')

        h5 = self.addHost('h5', cls=Host, ip='10.0.0.5')
        h6 = self.addHost('h6', cls=Host, ip='10.0.0.6')
        h4 = self.addHost('h4', cls=Host, ip='10.0.0.4')
        h7 = self.addHost('h7', cls=Host, ip='10.0.0.7')
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1')
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2')
        h8 = self.addHost('h8', cls=Host, ip='10.0.0.8')
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3')

        self.addLink(s3, s7)
        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(h1, s4)
        self.addLink(h2, s4)
        self.addLink(h3, s5)
        self.addLink(h4, s5)
        self.addLink(h5, s6)
        self.addLink(h6, s6)
        self.addLink(h7, s7)
        self.addLink(h8, s7)
        self.addLink(s4, s2)
        self.addLink(s2, s5)
        self.addLink(s2, s6)
        self.addLink(s2, s7)
        self.addLink(s3, s4)
        self.addLink(s3, s5)
        self.addLink(s3, s6)


def test():
    topo = MTP()
    net = Mininet(topo=topo, link=partial(TCLink, delay='2ms', bw=400))
    net.start()
    s1, s2, s3, r1, r2, r3 = net.get('h1', 'h3', 'h5', 'h2', 'h4', 'h6')
    for i in range(5):
        print(s1.IP(), s2.IP(), s3.IP())
        print(r1.IP(), r2.IP(), r3.IP())
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

