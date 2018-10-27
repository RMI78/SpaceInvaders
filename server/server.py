# coding: utf-8

import socket
from threading import Thread

class Waitsync(Thread):
    def __init__(self, client, id):
        Thread.__init__(self)
        self.client = client
        self.id = id

    def run(self):
        response = self.client.recv(255)
        if self.id:
            self.client.send("True".encode())
        else:
            self.client.send("False".encode())


class Waitpacket(Thread):
    def __init__(self, client1, client2):
        Thread.__init__(self)
        self.client1 = client1
        self.client2 = client2

    def send_packet(self, packet):
        """
        Send packet of client1 to client2
        """
        self.client2.send(packet)
        return True

    def wait_packet(self):
        """
        Wait packet of client1
        """
        packet = self.client1.recv(255)
        if packet != "":
            return packet

    def run(self):
        packet = self.wait_packet()
        print(packet)
        self.send_packet(packet)


if __name__ == "__main__":
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(('', 15555))

    socket.listen(5)
    client1, address = socket.accept()
    client2, address2 = socket.accept()

    waitsync1 = Waitsync(client1, True)
    waitsync2 = Waitsync(client2, False)

    waitsync1.start()
    waitsync2.start()

    waitsync1.join()
    waitsync2.join()

    while True:

        wait_packet1 = Waitpacket(client1, client2)
        wait_packet2 = Waitpacket(client2, client1)

        wait_packet1.start()
        wait_packet2.start()

        wait_packet1.join()
        wait_packet2.join()

    client1.close()
    client2.close()
    socket.close()
