import socket

SERVER_IP = "192.168.1.147"
PORT = 5050

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sckt.bind((SERVER_IP, PORT))

sckt.listen()

connection, address = sckt.accept()

with connection:
    print(f"Connected by {address}")
    while True:
        data = connection.recv(1024)
        if not data:
            break
        connection.sendall(data)