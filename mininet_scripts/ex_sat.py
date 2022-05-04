from mininet.topo import Topo
from mininet.link import TCLink
from functools import partial
from mininet.net import Mininet
from threading import Thread
import random
import time

class HalfTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        recv1 = self.addHost( 'r1' )
        send1 = self.addHost( 's1' )
        leftSwitch = self.addSwitch( 'sw-1' )

        self.addLink( recv1, leftSwitch, delay = "200ms" )
        self.addLink( leftSwitch, send1, delay = "200ms")

def runTest(net, file_des, cc):
    s1, r1 = net.get('s1', 'r1')
    loss_thread = Thread(target = changeLoss, args = (net, ))
    loss_thread.start()
    for i in range(4):
        s1.sendCmd("./stream_ser 10.0.0.2 800" + str(i) + " " + cc)
        r1.sendCmd("./stream_cli 10.0.0.2 800" + str(i) + " " + cc + " ex r1 " + file_des)
        s1.waitOutput()
        r1.waitOutput()
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
    runTest(net, file_des, "hybla")
    runTest(net, file_des, "cubic")
    runTest(net, file_des, "illinois")
    runTestPcc(net, file_des)
    net.stop()

def changeLoss(net):
    s1, sw1, r1 = net.get('s1', 'sw-1', 'r1')
    for i in range(500):
        loss_1 = random.random()*2
        loss_2 = random.random()*2
        link1 = net.linksBetween(s1, sw1)[0]
        link2 = net.linksBetween(r1, sw1)[0]
        link1.loss = loss_1
        link2.loss = loss_2
        time.sleep(1)

if __name__ == "__main__":
    Test()

#topos = {'topo' : (lambda: HalfTopo())}
