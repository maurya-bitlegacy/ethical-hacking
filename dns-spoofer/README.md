# dns-spoof

Built similar to www.github.com/maurya-bitlegacy/netcut. We will convert packets into scapy packets to allow peeking into various layers and modify its fields.

The hacker comes in the middle of the target and the DNS server, modifying dns responses as spoof IPs and sending these spoof ip addresses as dns responses back to the target, hence redirecting the target to malicious web pages, fake login pages and even getting him to install fake updates!

The quickest way to get the IP of any website is to use ping -c 1 www.website.com where -c 1 means only 1 ping request. This ping generates a dns request, and hence generates a dns response too (quick way of generating these).

If the user accesses a certain website(s), say www.iitk.ac.in, (only then)we want to modify the dns response. To direct the target to our own apache2 page, enable apache2 first: service apache2 start

We modify dns responses on the fly by placing a custom response in the "an" field of the DNS layer of the packet. The ancount field of DNS layer also needs to be modified as the an field may contain multiple answers before and we are sending just one. After this, we need to take care of the len fields of the IP and UDP layers and the checksum fields whose job is to ensure that the packet has not been modified :p Easy- just remove these fields. Scapy will recalculate and place them back based on the modified packets XD
