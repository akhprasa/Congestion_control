from mininet.topo import Topo
from mininet.link import TCLink
from functools import partial
from mininet.net import Mininet
from threading import Thread
import random
import time
from mininet.log import setLogLevel, info

class HalfTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        recv1 = self.addHost('r1')
        recv2 = self.addHost('r2')
        recv3 = self.addHost('r3')
        recv4 = self.addHost('r4')

        send1 = self.addHost('s1')
        send2 = self.addHost('s2')
        send3 = self.addHost('s3')
        send4 = self.addHost('s4')

        leftSwitch = self.addSwitch('sw-1')
        rightSwitch = self.addSwitch('sw-2')

        # Add links
        self.addLink(recv1, leftSwitch, delay='200ms')
        self.addLink(recv2, leftSwitch, delay='200ms')
        self.addLink(recv3, leftSwitch, delay='200ms')
        self.addLink(recv4, leftSwitch, delay='200ms')
        self.addLink(leftSwitch, rightSwitch)
        self.addLink(rightSwitch, send1, delay='200ms')
        self.addLink(rightSwitch, send2, delay='200ms')
        self.addLink(rightSwitch, send3, delay='200ms')
        self.addLink(rightSwitch, send4, delay='200ms')

        # recv1 = self.addHost( 'r1' )
        # send1 = self.addHost( 's1' )
        # leftSwitch = self.addSwitch( 'sw-1' )
        #
        # self.addLink( recv1, leftSwitch, delay = "200ms" )
        # self.addLink( leftSwitch, send1, delay = "200ms")

def runTest(net, file_des):
    s1, s2, s3, s4, r1, r2, r3, r4 = net.get('s1', 's2', 's3', 's4', 'r1', 'r2', 'r3', 'r4')
    loss_thread = Thread(target = changeLoss, args = (net, ))
    loss_thread.start()
    for i in range(4):
        s1.sendCmd("./stream_ser 10.0.0.5 800" + str(i) + " " + 'hybla')
        s2.sendCmd("./stream_ser 10.0.0.6 800" + str(i) + " " + 'illinois')
        s3.sendCmd("./stream_ser 10.0.0.7 800" + str(i) + " " + 'cubic')
        s4.sendCmd("./app/pccserver recv 8000")
        r1.sendCmd("./stream_cli 10.0.0.5 800" + str(i) + " " + 'hybla' + " ex r1 " + file_des)
        r2.sendCmd("./stream_cli 10.0.0.6 800" + str(i) + " " + 'illinois' + " ex r1 " + file_des)
        r3.sendCmd("./stream_cli 10.0.0.7 800" + str(i) + " " + 'cubic' + " ex r1 " + file_des)
        r4.sendCmd("./app/pccclient send 10.0.0.8 8000 vivace 1 " + file_des)
        s1.waitOutput()
        r1.waitOutput()
        s2.waitOutput()
        r2.waitOutput()
        s3.waitOutput()
        r3.waitOutput()
        s4.waitOutput()
        r4.waitOutput()
    loss_thread.join()

def runTestPcc(net, file_des):
    s1, r1 = net.get('s1', 'r1')
    loss_thread = Thread(target = changeLoss, args = (net, ))
    loss_thread.start()
    for i in range(4):
        s1.sendCmd("./app/pccserver recv 8000")
        r1.sendCmd("./app/pccclient send 10.0.0.2 8000 vivace 1 " + file_des)
        s1.waitOutput()
        r1.waitOutput()
    loss_thread.join()

def Test():
    topo = HalfTopo()
    file_des = "log_files_sat"
    net = Mininet(topo = topo, link = partial(TCLink, bw=400))
    net.start()
    runTest(net, file_des)
    # runTest(net, file_des, "hybla")
    # runTest(net, file_des, "cubic")
    # runTest(net, file_des, "illinois")
    # runTestPcc(net, file_des)
    net.stop()

def changeLoss(net):
    s1, s2, s3, s4, sw1, sw2, r1, r2, r3, r4 = net.get('s1','s2', 's3','s4','sw-1',
                                                       'sw-2', 'r1', 'r2', 'r3', 'r4')
    for i in range(500):
        loss_1 = random.random()*2
        loss_2 = random.random()*2
        loss_3 = random.random()*2
        link = net.linksBetween(sw1, sw2)[0]
        link1 = net.linksBetween(s1, sw2)[0]
        link2 = net.linksBetween(r1, sw1)[0]
        link3 = net.linksBetween(s2, sw2)[0]
        link4 = net.linksBetween(r2, sw1)[0]
        link5 = net.linksBetween(s3, sw2)[0]
        link6 = net.linksBetween(r3, sw1)[0]
        link7 = net.linksBetween(s4, sw2)[0]
        link8 = net.linksBetween(r4, sw1)[0]
        link.loss = loss_3
        link1.loss = loss_1
        link2.loss = loss_2
        link3.loss = loss_1
        link4.loss = loss_2
        link5.loss = loss_1
        link6.loss = loss_2
        link7.loss = loss_1
        link8.loss = loss_2
        time.sleep(1)

if __name__ == "__main__":
    setLogLevel('info')
    Test()

#topos = {'topo' : (lambda: HalfTopo())}
