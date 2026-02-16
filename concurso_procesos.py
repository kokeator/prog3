import multiprocessing as mp
import time
import random
import os

MOD = 1_000_000


def es_dorado(coord):
    return hash(coord) % MOD == 0


def paso_aleatorio(x, y):
    dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    return x + dx, y + dy


def lupa_proceso_concurso(origen, stop_event, q):
    # Semilla distinta en cada proceso (MUY IMPORTANTE)
    random.seed(os.getpid())

    x, y = origen
    n = 0

    while not stop_event.is_set():
        x, y = paso_aleatorio(x, y)
        n += 1

        if es_dorado((x, y)):
            if not stop_event.is_set():
                q.put((origen, (x, y), n))
                stop_event.set()
            return


def concurso_procesos(starts):
    stop = mp.Event()
    q = mp.Queue()
    procs = []

    t0 = time.perf_counter()

    for s in starts:
        p = mp.Process(target=lupa_proceso_concurso, args=(s, stop, q))
        p.start()
        procs.append(p)

    origen, coord, n = q.get()

    for p in procs:
        p.join()

    t1 = time.perf_counter()

    return {"start": origen, "coord": coord, "iter": n}, (t1 - t0)


if __name__ == "__main__":

    mp.set_start_method("spawn")

    print("Ejecutando...")

    starts = [(i * 1000, 0) for i in range(8)]

    ganador, tiempo = concurso_procesos(starts)

    print("ganador:", ganador)
    print("tiempo concurso (procesos):", tiempo)
