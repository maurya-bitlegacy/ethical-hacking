import requests
import re
import urllib.parse as urlparse

target_url = "https://iitk.ac.in/"
target_links = []

def extract_links_from(url):
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore")) #Use pythex for more info. Find URLs in the html
   # URLs are contained in href section of html code
   # Response.content contains the html of the webpage

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link) # Use to get full links for relative links like (/faq, /contact). Wont change full URLs

        if '#' in link:
            link = link.split('#')[0] #Links with # just open some section of the same webpage, so useless.

        if url in link and link not in target_links: # Used to filter out external URLs like facebook and linkedin etc and keep unique links only
            target_links.append(link)
            print(link)
            crawl(link) # Recurse to find all the links within

crawl(target_url)