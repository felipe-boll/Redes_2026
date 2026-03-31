# Servidor
import socket

HOST = "0.0.0.0"
PORT = 2807

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen(1)
        conn, addr = s.accept()
        print("Cliente: ", addr)
        with conn:
            while True:
                data = conn.recv(1024)
                print("Cliente: " + data.decode())
                mensagem = input("Servidor: ")
                conn.sendall(mensagem.encode())

        print("Desconectado")