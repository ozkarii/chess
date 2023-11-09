"""
COMP.CS.100
Author: Oskari Heinonen

Basic networking functionality for chess
"""


import socket


class Server:
    """
    """

    def __init__(self, ip, port):
        """
        """

        self.__ip = ip
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def receive_move(self) -> str:
        """
        """

        # Bind the socket to a host and port
        self.__socket.bind((self.__ip, self.__port))

        while True:
            # Listen for incoming connections
            self.__socket.listen(1)

            # Accept a client connection
            conn, addr = self.__socket.accept()

            # Receive data from the client
            data = conn.recv(1024).decode()
            return data


class Client:
    """
    """

    def __init__(self, host_ip, port):
        """
        """
        
        self.__host = host_ip
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_move(self, move):
        """
        """
    
        self.__socket.connect((self.__host, self.__port))
        message = move
        self.__socket.sendall(message.encode())