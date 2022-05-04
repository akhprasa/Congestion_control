from mininet.topo import Topo
import logging
import os
from mininet.net import Mininet
from mininet.link import TCLink
from functools import partial
from mininet.log import setLogLevel, info

logging.basicConfig(filename='./fattree.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FatTree(Topo):
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
    HostList = []

    def __init__(self, k):
        " Create Fat Tree topo."
        self.pod = k
        self.iCoreLayerSwitch = (k / 2) ** 2
        self.iAggLayerSwitch = k * k / 2
        self.iEdgeLayerSwitch = k * k / 2
        self.density = k / 2
        self.iHost = self.iEdgeLayerSwitch * self.density

        self.bw_c2a = 400
        self.bw_a2e = 200
        self.bw_h2a = 100

        # Init Topo
        Topo.__init__(self)

        self.createTopo()
        logger.debug("Finished topology creation!")

        self.createLink(bw_c2a=self.bw_c2a,
                        bw_a2e=self.bw_a2e,
                        bw_h2a=self.bw_h2a)
        logger.debug("Finished adding links!")

    #    self.set_ovs_protocol_13()
    #    logger.debug("OF is set to version 1.3!")

    def createTopo(self):
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        self.createHost(self.iHost)

    """
    Create Switch and Host
    """

    def _addSwitch(self, number, level, switch_list):
        for x in range(1, number + 1):
            PREFIX = str(level) + "00"
            if x >= int(10):
                PREFIX = str(level) + "0"
            switch_list.append(self.addSwitch('s' + PREFIX + str(x)))

    def createCoreLayerSwitch(self, NUMBER):
        logger.debug("Create Core Layer")
        self._addSwitch(NUMBER, 1, self.CoreSwitchList)

    def createAggLayerSwitch(self, NUMBER):
        logger.debug("Create Agg Layer")
        self._addSwitch(NUMBER, 2, self.AggSwitchList)

    def createEdgeLayerSwitch(self, NUMBER):
        logger.debug("Create Edge Layer")
        self._addSwitch(NUMBER, 3, self.EdgeSwitchList)

    def createHost(self, NUMBER):
        logger.debug("Create Host")
        for x in range(1, NUMBER + 1):
            PREFIX = "h00"
            if x >= int(10):
                PREFIX = "h0"
            elif x >= int(100):
                PREFIX = "h"
            self.HostList.append(self.addHost(PREFIX + str(x)))

    """
    Add Link
    """

    def createLink(self, bw_c2a=0.2, bw_a2e=0.1, bw_h2a=0.5):
        logger.debug("Add link Core to Agg.")
        end = self.pod / 2
        for x in range(0, self.iAggLayerSwitch, end):
            for i in range(0, end):
                for j in range(0, end):
                    linkopts = dict(bw=bw_c2a)
                    self.addLink(
                        self.CoreSwitchList[i * end + j],
                        self.AggSwitchList[x + i],
                        **linkopts)

        logger.debug("Add link Agg to Edge.")
        for x in range(0, self.iAggLayerSwitch, end):
            for i in range(0, end):
                for j in range(0, end):
                    linkopts = dict(bw=bw_a2e)
                    self.addLink(
                        self.AggSwitchList[x + i], self.EdgeSwitchList[x + j],
                        **linkopts)

        logger.debug("Add link Edge to Host.")
        for x in range(0, self.iEdgeLayerSwitch):
            for i in range(0, self.density):
                linkopts = dict(bw=bw_h2a)
                self.addLink(
                    self.EdgeSwitchList[x],
                    self.HostList[self.density * x + i],
                    **linkopts)

def Test():
    topo = FatTree(4)
    net = Mininet(topo = topo, link = partial(TCLink, delay='2ms'))
    net.start()
    hst = topo.HostList
    s1, s2, s3, r1, r2, r3 = net.get(hst[0], hst[2], hst[4], hst[1], hst[3], hst[5])
    ip1 = s1.IP()
    ip2 = s2.IP()
    ip3 = s3.IP()
    print(r1.IP(), r2.IP(), r3.IP())
    for i in range(5):
        print("./app/pccclient send "+ip1+" 8000 vivace 1")
        print("./app/pccclient send "+ip2+" 8000 vivace 2")
        print("./app/pccclient send "+ip3+" 8000 vivace 3")
        s1.sendCmd("./app/pccserver recv 8000")
        s2.sendCmd("./app/pccserver recv 8000")
        #s3.sendCmd("./app/pccserver recv 8000")
        r1.sendCmd("./app/pccclient send "+ip1+" 8000 vivace 1")
        r2.sendCmd("./app/pccclient send "+ip2+" 8000 vivace 2")
        #r3.sendCmd("./app/pccclient send "+ip3+" 8000 vivace 3")
        r1.waitOutput()
        r2.waitOutput()
        #r3.waitOutput()
        print('cl exists')
        s1.waitOutput()
        s2.waitOutput()
        #s3.waitOutput()
        print('serv exits')
    net.stop()
if __name__ == '__main__':
    setLogLevel( 'info' )
    Test()
#topos = {'fattree': (lambda : FatTree(2))}
