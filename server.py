"""
COMP.CS.100
Author: Oskari Heinonen

Basic networking functionality for chess
"""

import asyncio


class Server:
    """
    """

    def __init__(self, ip, port, app):
        """
        """

        self.__ip = ip
        self.__port = port
        self.__app = app
        # self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.__socket.bind((self.ip, self.port))
        # self.__socket.listen(1)

    async def handle_client(self, reader, writer):
        """An asynchronous method that is called for each client connection. 
        Reads data from the client using await reader.read(4),
        processes the data, and writes a response back to the client.
        """

        # Read data from the client
        data = await reader.read(4)

        # Decode the received bytes into a string
        move = list(map(int, data.decode()))

        # Get the client's address
        addr = writer.get_extra_info('peername')

        # Print the received message and client address
        print(f"Received '{data}' from {addr}")

        # Process the received data as needed
        # (This part would be where you handle the game logic)
        if data != '9999':
            self.__app.online_move_piece((move[0], move[1]),
                                       (move[2], move[3]))

        # Close the connection
        print("Closing the connection")
        writer.close()


    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client,
            host=self.__ip,
            port=self.__port
        )

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
        
