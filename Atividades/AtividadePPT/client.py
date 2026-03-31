import socket

HOST = "127.0.0.1"
PORT = 2807

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    print(s.recv(1024).decode())

    while True:
        data = s.recv(1024).decode()
        if not data:
            break
        print(data)
        if "Escolha" in data:
            msg = input(">> ")
            s.sendall(msg.encode())