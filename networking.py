import socket

class Networking:
    def __init__(self):
    	self.hote = "localhost"
    	self.port = 15555

    def connect(self):
        """
        Connect to server
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.hote, self.port))
        return s

    def sync(self, socket):
        """
        Send True and wait a True message
        """
        socket.send("True".encode())
        r = socket.recv(255)
        return r
        
    def send(self, socket, object):
        socket.send(object)
        data = socket.recv(4096)
        return data
