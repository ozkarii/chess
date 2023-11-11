"""
COMP.CS.100
Author: Oskari Heinonen

Basic networking functionality for chess
"""

import asyncio


class Server:
    """
    """

    def __init__(self, ip, port):
        """
        """

        self.ip = ip
        self.port = port
        # self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.__socket.bind((self.ip, self.port))
        # self.__socket.listen(1)

    async def handle_client(self, reader, writer):
        """An asynchronous method that is called for each client connection. 
        Reads data from the client using await reader.read(1024),
        processes the data, and writes a response back to the client.
        """

        # Read data from the client
        data = await reader.read(1024)

        # Decode the received bytes into a string
        message = data.decode()

        # Get the client's address
        addr = writer.get_extra_info('peername')

        # Print the received message and client address
        print(f"Received {message!r} from {addr!r}")

        # Process the received data as needed
        # (This part would be where you handle the game logic)

        # Print the message that will be sent back to the client
        print("Sending: {!r}".format(message))

        # Write the data back to the client
        writer.write(data)

        # Wait until the outgoing buffer is flushed
        await writer.drain()

        # Close the connection
        print("Closing the connection")
        writer.close()


    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client,
            host=self.ip,
            port=self.port
        )

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
        

# class Client:
#     """
#     """

#     def __init__(self, host_ip, port):
#         """
#         """
        
#         self.__host = host_ip
#         self.__port = port

#         # TCP socket
#         self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     def send_move(self, move):
#         """
#         """
    
#         self.__socket.connect((self.__host, self.__port))
#         message = move
#         self.__socket.sendall(message.encode())