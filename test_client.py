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
        
        self.__socket.connect((self.__host, self.__port))
        message = move
        self.__socket.sendall(message.encode())


def main():
    client = Client('localhost', 5000)
    move = input("Enter data: ")
    client.send_move(move)


if __name__ == "__main__":
    main()