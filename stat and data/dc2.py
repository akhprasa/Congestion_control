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
    s7 = net.addSwitch('s7', stp=True, failMode='standalone')
    s1 = net.addSwitch('s1', stp=True, failMode='standalone')
    s3 = net.addSwitch('s3', stp=True, failMode='standalone')
    s4 = net.addSwitch('s4', stp=True, failMode='standalone')
    s2 = net.addSwitch('s2', stp=True, failMode='standalone')
    s5 = net.addSwitch('s5', stp=True, failMode='standalone')
    s6 = net.addSwitch('s6', stp=True, failMode='standalone')

    info( '*** Add hosts\n')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, s2, bw=0.2)
    net.addLink(s1, s3, bw=0.2)
    net.addLink(s2, s4, bw=0.1)
    net.addLink(s2, s5, bw=0.1)
    net.addLink(s3, s6, bw=0.1)
    net.addLink(s3, s7, bw=0.1)
    net.addLink(s4, h1, bw=0.05)
    net.addLink(s4, h2, bw=0.05)
    net.addLink(s5, h3, bw=0.05)
    net.addLink(s5, h4, bw=0.05)
    net.addLink(s6, h5, bw=0.05)
    net.addLink(s6, h6, bw=0.05)
    net.addLink(s7, h7, bw=0.05)
    net.addLink(s7, h8, bw=0.05)

    net.start()
    info( '*** Starting network\n')
    # net.build()
    # info( '*** Starting controllers\n')
    # for controller in net.controllers:
    #     controller.start()

    #info( '*** Starting switches\n')
    # net.get('s7').start([])
    # net.get('s5').start([])
    # net.get('s3').start([])
    # net.get('s4').start([])
    # net.get('s2').start([])
    # net.get('s6').start([])
    # net.get('s1').start([])

    info( '*** Post configure switches and hosts\n')
    h1, h2, h3, h4, h5, h6, h7, h8 = net.get('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8')
    for i in range(5):
        h1.sendCmd("./app/pccserver recv 8000")
        h3.sendCmd("./app/pccserver recv 8000")
        h5.sendCmd("./app/pccserver recv 8000")
        h7.sendCmd("./app/pccserver recv 8000")
        h2.sendCmd("./app/pccclient send 10.0.0.1 8000 vivace 1")
        h4.sendCmd("./app/pccclient send 10.0.0.3 8000 vivace 2")
        h6.sendCmd("./app/pccclient send 10.0.0.5 8000 vivace 3")
        h8.sendCmd("./app/pccclient send 10.0.0.7 8000 vivace 4")
        h2.waitOutput()
        h4.waitOutput()
        h6.waitOutput()
        h8.waitOutput()
        print('done')
        h1.waitOutput()
        h3.waitOutput()
        h5.waitOutput()
        h7.waitOutput()
        print('done2')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

