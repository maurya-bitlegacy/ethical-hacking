# arp-spoofer
ARP spoofing to redirect the flow of packets in a network using scapy module of python

Input format: python arp-spoof.py --router router IP --client client IP
  
Use Ctrl+C to exit.
  
Use network-scanner.py to find the client if needed. Input format: python network-scanner.py -target <subnet>. For more info on network-scanner.py: https://github.com/maurya-bitlegacy/network-scanner

Poison the ARP tables of a client and the router to become the man in the middle!

Send an ARP reponse to a client computer, pretending to be the router (as source), and send an ARP response to the router, pretending to be the client computer (as source).

Exploits the vulnerability in the ARP protocol -- ARP responses get accepted and ARP tables get updated at the client and the router even if they didn't request a response. There is no verification at the target whatsoever!

To get the target IP as well as the fake source IP you wanna use, use the network-scanner.py using the subnet mask (eg python network-scanner.py --target 192.168.18.1/24) (shows all connected client IPs and their MACs)

If I send an ARP to a client (eg 192.168.18.50) from my computer(eg 192.168.18.30) but with source IP of the router (192.168.18.1), the client will associate my MAC address with the IP address of the router (192.168.18.1) in its ARP table. So every time this client wants to send a packet to the router's IP, it will send the packet to my MAC address instead, putting me in the middle of the connection.

To see ARP tables, use arp -a on windows.
Note: Need to send the spoof packets repeatedly in a loop to prevent the ARP tables getting reset to the correct addresses.
The client will lose it's internet connection on spoofing though. To prevent this, enable IP forwarding (kali) using echo 1 > /proc/sys/net/ipv4/ip_forward.
With this, our machine will forward all packets of the client to the router.

Bypassing https: Use sslstrip. sslstrip will downgrade https to http, and we get redirected to http versions of websites. sslstrip works on port 10000 only, so we need redirect any packet that comes to our computer on port 80 to this port. This redirection can be done using iptables. Command: iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

A note on https: To bypass https, sslstrip needs to be set up which runs only on python2. Also, most websites use HSTS harcoding these days, so sslstrip is not likely to capture traffic on those websites. 


