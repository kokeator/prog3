import math
import multiprocessing as mp
from typing import List
import time

def is_prime(n: int) -> bool:
    """Determina si un numero es primo, solo comprueba hasta la raiz cuadrada y los numeros impares"""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    limit = int(math.isqrt(n))
    for d in range(3, limit + 1, 2):
        if n % d == 0:
            return False
    return True

def worker(shared_counter, counter_lock, results_list, results_lock, limit, chunk_size):
    """
    Cada trabajador pide un bloque de 1000 números, lo procesa y guarda sus resultados.
    """
    while True:
        # 1. Pedir un bloque
        with counter_lock:
            start_range = shared_counter.value
            if start_range > limit:
                break
            shared_counter.value += chunk_size
        
        end_range = min(start_range + chunk_size - 1, limit)
        
        # 2. Procesar ese bloque localmente
        local_primes = []
        for n in range(start_range, end_range + 1):
            if is_prime(n):
                local_primes.append(n)
        
        # 3. Guardar los resultados del bloque
        if local_primes:
            with results_lock:
                results_list.extend(local_primes)

def find_primes_parallel(limit: int = 1000000, num_processes: int = 10):
    """Lanza los 10 procesos a la vez y esperan a que terminen, luego ordena la lista y retorna"""
    chunk_size = 1000 
    
    with mp.Manager() as manager:
        shared_counter = manager.Value('i', 1)
        counter_lock = manager.Lock()
        results_list = manager.list()
        results_lock = manager.Lock()
        
        processes = []
        for _ in range(num_processes):
            p = mp.Process(
                target=worker, 
                args=(shared_counter, counter_lock, results_list, results_lock, limit, chunk_size)
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        return sorted(list(results_list))

if __name__ == "__main__":
    LIMIT = 1_000_000
    N_PROCESOS = 10
    
    print(f"Calculando hasta {LIMIT} usando {N_PROCESOS} procesos...")
    
    start_time = time.time()
    primes = find_primes_parallel(limit=LIMIT, num_processes=N_PROCESOS)
    end_time = time.time()
    
    print(f"--- Finalizado en {end_time - start_time:.2f} segundos ---")
    print(f"Cantidad encontrada: {len(primes)}")
    print(f"Últimos 5 primos: {primes[-5:]}")