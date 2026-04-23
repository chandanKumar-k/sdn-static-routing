from mininet.topo import Topo

class FirewallTopo(Topo):
    def build(self):
        # Hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Switches
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', protocols='OpenFlow13')

        # Links
        self.addLink(h1, s1)

        self.addLink(s1, s2)
        self.addLink(s2, h2)

        self.addLink(s1, s3)
        self.addLink(s3, h3)

topos = {'firewalltopo': (lambda: FirewallTopo())}
