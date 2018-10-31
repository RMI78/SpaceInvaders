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
        Send True and wait a message to determine the role
        """
        socket.send("True".encode())
        role = socket.recv(255).decode()
        return role

    def send(self, socket, object):
        """
        Send and recv data.
        Decode data and return
        """
        socket.send(object)
        data = socket.recv(255).decode()
        return data

    def decode_data(self, data):
        data = data.split(",")
        x, y = (int(i) for i in data[:2])
        shoot = int(data[2])
        xMouse, yMouse = (int(i) for i in data[-3:-1])
        angle = float(data[-1])

        return (x, y, shoot, xMouse, yMouse, angle)
