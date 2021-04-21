# netcut

To run: python netcut.py

The scapy library in python cannot be used to intercept and drop packets. We can modify the original packet and send it, but cannot stop the original packet from the target to the router. Hence the router will received two requests. The router is very likely to recieve the original request first, so our modified request may not get processed by the router.

A better implementation is to place many packets in a queue, modify them, and send them after modification to the router. Going this way, the router will only receive one request. We can use the same method to modify responses as well. Again, this thing is not possible through scapy. We're going to use iptables instead - a program present in linux distros. iptables can be used to modify routing rules.

The FORWARD chain of iptables is the place where incoming packets to be forwarded are kept by default. We're going to keep the packets in NFQUEUE (Net Filter Queue). Can specify any queue number. Can also use the subprocess module to do this.
Command: iptables -I FORWARD -j NFQUEUE --queue-num 0

As the FORWARD chain stores the packets corresponding to IP forwarding, you need to become the man-in-the-middle first using ARP spoofing (arp-spoof.py). For more info on this, see www.github.com/maurya-bitlegacy/arp-spoof.

ps Packets coming to your own machine won't go into the FORWARD chain. Those go into the INPUT chain (Responses). Those going out of your machine go into the OUTPUT chain (Requests). So if you redirect the packets of the INPUT or OUTPUT chains to the queue by modifying the command before, you'd be cutting your own internet access :p

To handle this NFQUEUE, need to install: pip install netfilterqueue (Use python 3.6. Doesn't install with higher versions apparently)

If we don't forward the packets from the queue to the target, the target won't receive any packets and hence will be unable to browse. Use packet.accept() to forward packets to the target. Use packet.drop() to drop em.

In the end, don't forget to delete the IP table you created. (These things are already done using subprocess module, but still need to do it if program is terminated with something other than a keyboard interrupt).
