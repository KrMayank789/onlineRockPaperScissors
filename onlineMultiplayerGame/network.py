import socket
import pickle
#pickle serialize objects(convert the objects into byts for sending and then decompose it when recieved)

class Network:
    def __init__(self):
        self.client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = "192.168.43.108" #same as we used in the serevr file
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()


    def getP(self):
        return self.p


    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)









