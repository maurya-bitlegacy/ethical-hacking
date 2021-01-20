# keylogger
This is an implementation of 2 simple keyloggers in python. Prerequisite: python pynput library
1. LocalKeylogger is a local keylogger that stores the log of pressed keys locally
2. RemoteKeylogger sends the key sequences to an email after a certain interval of time [Uses threading]

todo: Create a working .exe using RemoteKeylogger

Keyloggers are malwares that track keys pressed by the victim and sends the key log to the attacker. The attacker can hence use the key log to know sensitive information like passwords, credit card information etc of the victim.

To detect keyloggers on your system without using any external tool, one simple way is to use netstat -b on Windows.  This shows all your applications connected to the internet and the details of their TCP connections. Loop up the application names displayed or their IP addresses to find out which one is the RAT.
Antimalwares today are expected to catch keyloggers automatically though. (Windows Defender good enough to do it?)

p.s Keyloggers can detect keystrokes on a virtual keyboard/on-screen keyboard too.
