import socket

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Connect(self):
        self.client.connect((self.host, self.port))

    def Send(self, text):
        try:
            self.client.send(text)
        except:
            print('請檢查是否連接到Server')

    def Close(self):
        self.client.close()