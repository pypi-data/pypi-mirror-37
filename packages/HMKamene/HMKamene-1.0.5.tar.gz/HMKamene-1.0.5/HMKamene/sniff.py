from threading import Thread

from kamene.layers.l2 import ARP
from kamene.layers.ipsec import IPv6
from kamene.layers.dns import DNS, TCP, UDP
from kamene.utils import wrpcap
from kamene.all import sniff

class Sniffer:

    def __init__(self):
        self.sniffObj = self.SniffObj()
    
    def getPacketType(self, packet):
        if(IPv6 in packet):
            return("IPv6")
        elif(DNS in packet):
            return("DNS")
        elif(TCP in packet):
            return("TCP")
        elif(ARP in packet):
            return("ARP")
        elif(UDP in packet):
            return("UDP")
        else:
            return("New")

    def savePCAP(self, saveDst, output = False):
        for i in range(0, len(self.sniffObj.packets)):
            if(i == 0):
                wrpcap(saveDst, self.sniffObj.packets[i], append=False)
            else:
                wrpcap(saveDst, self.sniffObj.packets[i], append=True)
        if(output):
            print("Saved pcap file to: "+saveDst)


    def saveTXT(self, saveDst, output = False):
        textLines = []
        for i in range(0, len(self.sniffObj.packets)):
            textLines.append("#-------------"+str(i+1)+"--------------")
            textLines.append("<"+self.getPacketType(self.sniffObj.packets[i])+">")
            textLines.append(self.sniffObj.packets[i].command())
            textLines.append('\n\n\n\n')
        with open(saveDst, 'w') as filehandle:  
            filehandle.writelines("%s\n" % line for line in textLines)

        if(output):
            print("Saved text file to: "+saveDst)

    class SniffObj(Thread):
        def __init__(self):
            Thread.__init__(self)
            self.name = 'Sniff thread'

            self.count = 0
            self.store = 1
            self.opened_socket = None
            self.filter = None
            self.stopCallbackVar = None
            self.extendedMethod = callable()

            self.packets = []
        
        def run(self):
            sniff(count=self.count, store=self.store, prn=self.sniff_prn\
            , opened_socket=self.opened_socket, filter=self.filter, stop_callback=self.sniff_stop_check)

        def sniff_prn(self, packet):
            self.packets.append(packet)
            if(self.extendedMethod is not None):
                self.extendedMethod(packet)
        
        def sniff_stop_check(self):
            if(self.stopCallbackVar):
                return True
            else:
                return False

