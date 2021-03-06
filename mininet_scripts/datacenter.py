#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet()

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s2 = net.addSwitch('s2')
    s1 = net.addSwitch('s1')

    info( '*** Add hosts\n')
    h4 = net.addHost('h4')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    info( '*** Add links\n')
    net.addLink(s1, s4, bw=800, delay='1ms')
    net.addLink(s3, s2, bw=800, delay='1ms')
    net.addLink(s1, s3, bw=800, delay='1ms')
    net.addLink(s2, s4, bw=800, delay='1ms')
    net.addLink(s3, h1, bw=800, delay='1ms')
    net.addLink(s3, h2, bw=800, delay='1ms')
    net.addLink(s4, h3, bw=800, delay='1ms')
    net.addLink(s4, h4, bw=800, delay='1ms')

    info( '*** Starting network\n')
    net.start()



    info( '*** Post configure switches and hosts\n')

    s1, s2, r1, r2 = net.get('h1', 'h3', 'h2', 'h4')
    for i in range(4):
        print('started')
        s1.sendCmd("./app/pccserver recv 8000")
        s2.sendCmd("./app/pccserver recv 8000")
        r1.sendCmd("./app/pccclient send 10.0.0.1 8000 vivace 1 log_files")
        r2.sendCmd("./app/pccclient send 10.0.0.3 8000 vivace 2 log_files")
        r1.waitOutput()
        r2.waitOutput()
        print('cl done')
        s1.waitOutput()
        s2.waitOutput()
        print('sr done')

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

