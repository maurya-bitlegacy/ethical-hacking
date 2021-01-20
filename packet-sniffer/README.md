# packet-sniffer

A python based packet sniffer based on the scapy library. 

packet-sniffer.py sniffs packets from the interface provided. arp-spoof.py does all the hard work of making packets of the target flow through this interface of our machine once we become the man in the middle.

packet-sniffer.py and arp-spoof.py need to be run in parallel. For more info on arp-spoof.py : https://github.com/maurya-bitlegacy/arp-spoofer. Do remember to enable IP forwarding using echo 1 > /proc/sys/net/ipv4/ip_forward on kali or else the target will lose internet access.

Some filters for the scapy sniff function: udp (capture udp packets), tcp, arp, port 21 (targetting ftp passwords), port 80 (capture data sent to websites and web servers). http is unfortunately not allowed in the filter field, so scapy_http needs to be installed for this. Recall that all the interesting stuff- URLs, usernames, passwords etc are sent over http.

This sniffer captures urls, usernames and passwords. So cool XD

A note on https: To bypass https, sslstrip needs to be set up which runs only on python2. Also, most websites use HSTS harcoding these days, so sslstrip is not likely to capture traffic on those websites. 
