import requests

# http status code of 200 means positive response
# Will get a ConnectionError for invalid domain
def request(url):
    try:
        return requests.get("http://"+url) # get simulates clicking on a link
    except Exception:
        pass # Do nothing

target_url = "iitk.ac.in"

with open("subdomains-wordlist.txt","r") as wordlist_file: # Discovering subdomains
    for line in wordlist_file:
        word = line.strip() # The words have \n appended in the file
        test_url = word + "." + target_url
        response = request(test_url) # Will contain None for "pass", ie nothing returned
        if response:
            print("[+] Discovered subdomain: "+test_url)

with open("files-and-dirs-wordlist.txt","r") as wordlist_file: # Discovering subdirectories
    for line in wordlist_file:
        word = line.strip() # The words have \n appended in the file
        test_url = target_url + "/" + word
        response = request(test_url) # Will contain None for "pass", ie nothing returned
        if response:
            print("[+] Discovered subdirectory: "+test_url)