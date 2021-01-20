# network-scanner
A network scanner built on python

Uses scapy library in python

Uses ARP encapsulated in ethernet packets to broadcast and receive response from all hosts on the network to get their MAC addresses.

To use: python network-scanner.py --target "IP address of IP range"

eg: python network-scanner.py --target 192.168.18.1/24 where 192.168.18.1 is the gateway IP obtainable using ipconfig on Windows and using 192.168.18.1/24 sends 254 packets to all possible hosts in the subnet.
