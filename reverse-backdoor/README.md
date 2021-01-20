# backdoor
Allows full access to the target system.

2 ways of establishing a connection between hacker and target: The target listens on a specific port and accepts a connection from the hacker. Won't work most of the time because the target machine will throw a firewall warning for an open port.
TC
The other way is to run the backdoor on the target, and we listen on a port on the hacker machine. The target initiates a TCP connection with the hacker using the backdoor [reverse backdoor]. This connection is similar to opening a website on the target machine. Therefore, most firewalls will not detect this as something suspicious, especially if the port used on the hacker machine is a commonly used one, like port 80. Can use any port as long as it is not being used by any other process.

To open a listening port on hacker machine: nc -vv -l -p 4444. -vv: Show comprehensive info. -l: Listen. -p: port.

Serialization is needed because the server does not know where the data ends. It will just receive data to fill the buffer at once. With serialization, the data is well defined. The receiver knows if the message is incomplete. It can be used to send data structures(lists, dict etc). Using json is a common way of serialization.

It is beneficial to split the command into the list, so that the first string can be interpreted as the command, the other strings as arguments. check_output of subprocess runs the system command and returns the result but it wont change the working dir. Gotta implement it manually using os.chdir().

Using base64 encoding is necessary for downloading (writing) files other than simple text files (like images). Or elese UnicodeDecodeError will be thrown.

To avoid losing connection on doing illegal shit, like typing wrong commands, uploading non-existing files etc

