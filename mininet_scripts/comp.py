from mininet.topo import Topo
from mininet.link import TCLink
from functools import partial
from mininet.net import Mininet
from mininet.log import setLogLevel, info

class HalfTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        recv1 = self.addHost( 'r1' )
        recv2 = self.addHost( 'r2' )
        recv3 = self.addHost( 'r3' )
        send1 = self.addHost( 's1' )
        send2 = self.addHost( 's2' )
        send3 = self.addHost( 's3' )
        leftSwitch = self.addSwitch( 'sw-1' )
        rightSwitch = self.addSwitch( 'sw-2' )

        self.addLink( recv1, leftSwitch, delay = "0.5ms" )
        self.addLink( recv2, leftSwitch, delay = "0.5ms" )
        self.addLink( recv3, leftSwitch, delay = "0.5ms")
        self.addLink( leftSwitch, rightSwitch, delay = "0.5ms" )
        self.addLink( rightSwitch, send1, delay = "0.5ms")
        self.addLink( rightSwitch, send2, delay = "0.5ms" )
        self.addLink( rightSwitch, send3, delay = "0.5ms" )

class OneTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        recv1 = self.addHost( 'r1' )
        recv2 = self.addHost( 'r2' )
        recv3 = self.addHost( 'r3' )
        send1 = self.addHost( 's1' )
        send2 = self.addHost( 's2' )
        send3 = self.addHost( 's3' )
        leftSwitch = self.addSwitch( 'sw-1' )
        rightSwitch = self.addSwitch( 'sw-2' )

        self.addLink( recv1, leftSwitch, delay = "1ms" )
        self.addLink( recv2, leftSwitch, delay = "1ms" )
        self.addLink( recv3, leftSwitch, delay = "1ms")
        self.addLink( leftSwitch, rightSwitch, delay = "1ms" )
        self.addLink( rightSwitch, send1, delay = "1ms")
        self.addLink( rightSwitch, send2, delay = "1ms" )
        self.addLink( rightSwitch, send3, delay = "1ms" )

class TwoTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        recv1 = self.addHost( 'r1' )
        recv2 = self.addHost( 'r2' )
        recv3 = self.addHost( 'r3' )
        send1 = self.addHost( 's1' )
        send2 = self.addHost( 's2' )
        send3 = self.addHost( 's3' )
        leftSwitch = self.addSwitch( 'sw-1' )
        rightSwitch = self.addSwitch( 'sw-2' )

        self.addLink( recv1, leftSwitch, delay = "2ms" )
        self.addLink( recv2, leftSwitch, delay = "2ms" )
        self.addLink( recv3, leftSwitch, delay = "2ms")
        self.addLink( leftSwitch, rightSwitch, delay = "2ms" )
        self.addLink( rightSwitch, send1, delay = "2ms")
        self.addLink( rightSwitch, send2, delay = "2ms" )
        self.addLink( rightSwitch, send3, delay = "2ms" )

def runTest(net, file_des):
    s1, s2, s3, r1, r2, r3 = net.get('s1', 's2', 's3', 'r1', 'r2', 'r3')
    for i in range(4):
        print('started')
        s1.sendCmd("./stream_ser 10.0.0.4 800" + str(i) + " cubic")
        s2.sendCmd("./stream_ser 10.0.0.5 800" + str(i) + " reno")
        s3.sendCmd("./app/pccserver recv 8000")
        r1.sendCmd("./stream_cli 10.0.0.4 800" + str(i) + " cubic ex r1 " + file_des)
        r2.sendCmd("./stream_cli 10.0.0.5 800" + str(i) + " reno ex r1 " + file_des)
        r3.sendCmd("./app/pccclient send 10.0.0.6 8000 vivace 1 " + file_des)
        s1.waitOutput()
        s2.waitOutput()
        s3.waitOutput()
        r1.waitOutput()
        r2.waitOutput()
        r3.waitOutput()

def Test(topo, file_des, loss):
    net = Mininet(topo = topo, link = partial(TCLink, bw=400, loss=loss))
    net.start()
    runTest(net, file_des)
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    topo_list = [HalfTopo(), OneTopo(), TwoTopo()]
    folder_list_hal = ["log_files_0.5_0.5", "log_files_0.5_1", "log_files_0.5_2"]
    #Test(topo_list[1], "log_files_0.0_1", 0)
    for i in range(3):
        Test(topo_list[i], folder_list_hal[i], 0.5)