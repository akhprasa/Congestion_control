from mininet.topo import Topo

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


topos = { 'mytopo': ( lambda: MyTopo() ) }
