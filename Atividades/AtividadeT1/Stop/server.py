import socket
import threading
from time import sleep

HOST = "0.0.0.0"
PORT = 9002

LETRA = ""

CEP = ["", ""]
NOME = ["", ""]

semaforo = threading.Semaphore(0)

semaforo.acquire()

semaforo_jogadas = {threading.Semaphore(0), threading.Semaphore(1)}
def rodar_stop(conn, addr, tid):
    global CEP
    global NOME

    with conn:
        conn.sendall(LETRA.encode())

        conn.sendall("CEP: ".encode())
        resposta = conn.recv(1024).decode("")
        CEP[tid] = resposta

        conn.sendall("Nome: ".encode())
        resposta = conn.recv(1024).decode("")
        NOME[tid] = resposta

        NOME[tid] = resposta

        pass

def iniciar_servidor():
    global LETRA

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Para não dar problema caso a porta ja esteja sendo usada
        server.bind((HOST, PORT))
        server.listen()

        #Aguardando jogador 1
        conn1, addr1 = server.accept()
        thread1 = threading.Thread(
            target=rodar_stop,
            args=(conn1, addr1),
            daemon=True
            )
        thread1.start()

        #Aguardando jogador 2
        conn2, addr2 = server.accept()
        thread2 = threading.Thread(
            target=rodar_stop,
            args=(conn2, addr2),
            daemon=True
            )
        thread2.start()

        LETRA = "T"

        semaforo.release
        semaforo.release

        for sem_i in semaforo_jogadas:
            sem_i.acquire()

        print(CEP)
        print(NOME)

        thread1.join()
        thread2.join()


if __name__ == "__main__":
    iniciar_servidor()