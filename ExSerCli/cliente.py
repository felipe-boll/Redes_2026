# Cliente
import socket

HOST = "192.168.246.27"
PORT = 2807

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:

        msg = input("Cliente: ")
        s.sendall(msg.encode())
        msg_recv = s.recv(1024).decode()
        print(f"servidor:", msg_recv)