import threading

def tarefa():
    print("Executando tarefa...")

t = threading.Thread(target=tarefa)
t.start()
t.join()

print("Finalizado")