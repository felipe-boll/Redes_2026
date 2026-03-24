import socket

HOST = "0.0.0.0"
PORT = 2807

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)

    vitoria_j1 = 0
    vitoria_j2 = 0
    print("[server] Aguardando Jogador 1...")
    conn_1, addr1 = s.accept()
    conn_1.sendall("[server] OK, você é o Jogador 1".encode())

    print("[server] Aguardando Jogador 2...")
    conn_2, addr2 = s.accept()
    conn_2.sendall("[server] OK, você é o Jogador 2".encode())

    while vitoria_j1 < 3 or vitoria_j1 > -3 or vitoria_j2 < 3 or vitoria_j2 > -3:
        conn_1.sendall("Sua vez! Escolha (Pedra, Papel, Tesoura): ".encode())
        conn_2.sendall("Aguardando jogada do Jogador 1...".encode())
        escolha1 = conn_1.recv(1024).decode().strip()

            
        conn_2.sendall("Sua vez! Escolha (Pedra, Papel, Tesoura): ".encode())
        conn_1.sendall("Aguardando jogada do Jogador 2...".encode())
        escolha2 = conn_2.recv(1024).decode().strip()

        print(f"J1: {escolha1} vs J2: {escolha2}")

        if escolha1 == escolha2:
            msg = "Empate!"
        elif (escolha1 == "Pedra" and escolha2 == "Tesoura") or \
            (escolha1 == "Papel" and escolha2 == "Pedra") or \
            (escolha1 == "Tesoura" and escolha2 == "Papel"):
            msg = f"Jogador 1 ganhou! ({escolha1} vence {escolha2})"
            vitoria_j1 += 1
            vitoria_j2 -= 1
        else:
            msg = f"Jogador 2 ganhou! ({escolha2} vence {escolha1})"
            vitoria_j2 += 1
            vitoria_j1 -= 1

        resultado = f"\n[RESULTADO] {msg}\n"
        conn_1.sendall(resultado.encode())
        conn_2.sendall(resultado.encode())