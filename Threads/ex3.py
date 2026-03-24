import threading
import time

WAITING_TIME = 0.1

# Semáforo
semaforo = threading.Semaphore(0) #Impedir que duas threads diferentes acessem o mesmo dado simultaneamente

def thread_0():
    for i in range(1, 11): #Roda o for do 1 até o 10
        semaforo.acquire() #Diminui o contador semaforo em 1 para nenhuma outra thread acessar
    
        print(f"[Thread 0] {i}", flush=True)
    
        semaforo.release() #Aumenta o contador semaforo em 1 para liberar a entrada da proxima
        time.sleep(WAITING_TIME)


def thread_1():
    for i in range(1, 11):
        semaforo.acquire()
        
        print(f"[Thread 1] {i}", flush=True)
    
        semaforo.release()
        time.sleep(WAITING_TIME)


# Instancia as threads
t0 = threading.Thread(target=thread_0)
t1 = threading.Thread(target=thread_1)

# Starta as threads
t0.start()
t1.start()

# Libera o semáforo
semaforo.release()

# Aguarda as threads finalizarem
print("[Main] Aguardando threads")
t0.join()
t1.join()

print("[Main] Finalizado")