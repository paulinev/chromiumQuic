#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import Link
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.util import ensureRoot

from subprocess import Popen, PIPE
from time import sleep, time

import sys
import os
import math

ensureRoot()

class QuicTester(Topo):
    def __init__(self):
        
        # Initialise topology
        Topo.__init__(self)

        # Add hosts and switches
        client = self.addHost('client', ip='10.0.0.2', mac='00:00:00:00:00:02')
        server = self.addHost('server', ip='10.0.0.1', mac='00:00:00:00:00:01')

        # Add switch
        s1 = self.addSwitch('s1')

        # Add links
        self.addLink(client, s1)
        self.addLink(s1, server)

def set_all_IP(net, client, server):
    client.sendCmd('ifconfig client-eth0 10.0.0.2 netmask 255.255.255.0')
    client.waitOutput()
    server.sendCmd('ifconfig server-eth0 10.0.0.1 netmask 255.255.255.0')
    server.waitOutput()

def display_routes(net, client, server):
    print 'client route...'
    client.sendCmd('route -n')
    print client.waitOutput()
    print 'server route...'
    server.sendCmd('route -n')
    print server.waitOutput()

def run_quic(client, server):
    print "Running quic client..."
    client.sendCmd('/home/ubuntu/home/src_tarball/tarball/chromium/src/out/Debug/quic_client http://www.mit.edu/img/bckgrnd4.png  >/tmp/client-stdout 2>/tmp/client-stderr &')
    client.waitOutput()
    print "Running quic server..."
    server.sendCmd('/home/ubuntu/home/src_tarball/tarball/chromium/src/out/Debug/quic_server >/tmp/server-stdout 2>/tmp/server-stderr &')
    server.waitOutput()
    print "done."

def run_quic_topology():

    # kill old processes
    os.system( "killall -q controller" )
    os.system( "killall -q quic_client" )
    os.system( "killall -q quic_server" )

    topo = QuicTester()
    net = Mininet(topo=topo, host=Host, link=Link)
    net.start()

    client = net.getNodeByName('client')
    server = net.getNodeByName('server')

    set_all_IP(net, client, server)
    
    #Dump connections
    dumpNodeConnections(net.hosts)
    display_routes(net, client, server)

    run_quic(client, server)

    CLI(net)

    net.stop()

run_quic_topology()
