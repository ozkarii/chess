import socket


class Client:
    """
    """

    def __init__(self, host_ip, port):
        """
        """
        
        self.__host = host_ip
        self.__port = port

        # TCP socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_move(self, move):
        """
        """
        
        try:
            self.__socket.connect((int(self.__host), int(self.__port)))
            message = move
            self.__socket.sendall(message.encode())
        except TypeError:
            print("invalid ip or port")
