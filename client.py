import socket

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.05)

    def Connect(self):
        try:
            self.client.connect((self.host, self.port))
        except:
            print('無法連線至server')
        
    def Receive(self):
        try:
            data = self.client.recv(1024)
            return data.decode('utf-8')
        except:
            return ''

    def Send(self, text):
        return self.client.send(text.encode())

    def Close(self):
        self.client.close()