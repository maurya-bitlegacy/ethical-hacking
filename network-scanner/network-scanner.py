import scapy.all as scapy
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP or IP range.")
    # Arguments in the form of -t "IP"  or --target "IP". Use --help for help.
    options, arguments = parser.parse_args()
    return options # Contains the target IP

def scan(ip):
    #scapy.arping(ip) #Direct way of doing an arp ping
    arp_request=scapy.ARP(pdst=ip) # ARP request packet (Who has "ip"?)
    #arp_request.pdst=ip #Alternatively for above field
    #arp_request.show() # Show the details of this packet
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Ethernet packet for broadcast
    #broadcast.show()
    #scapy.ls(scapy.ARP()) # Lists all the fields we can set in ARP()
    #scapy.ls(scapy.Ether()) # Similarly for Ether()
    arp_request_broadcast = broadcast/arp_request # packet containing arp in an ethernet broadcase frame
    #arp_request_broadcast.show()

    answered_list, unanswered_list = scapy.srp(arp_request_broadcast,timeout=5, retry=3) # Returns 2 lists: One for answered packet, one for unanswered packet
    # send packet and receive response. timeout specifies how long to wait for unanswered packets in seconds
    # These lists are of the form (packet sent, packet response)
    # answered_list.summary() # Output: Request ==> Response
    #unanswered_list.summary() # Output: Request

    print("IP" + "\t\t\t\t\t" + "MAC Address\n-----------------------------------------------")
    for element in answered_list:
        #print(element[1].show()) # Print all info in the response packet
        print(element[1].psrc + "\t\t" + element[1].hwsrc) # Print just the target IPs and target MACs

options = get_arguments() # Fetch the target using command arguments
scan(options.target)
#scan("192.168.18.1/24") # Find the gateway using route -n in kali or ipconfig in windows.
# Can scanning the entire subnet. Sends 254 packets
